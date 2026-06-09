# Trama Velada

Reto forense tipo CTF basado en una captura `traffic.pcap` protegida con TLS.

## Archivos

- `traffic.pcap`: captura principal.
- `keylog.txt`: secretos de sesión TLS para descifrar el tráfico.
- `solve.py`: script para extraer la flag.
- `WRITEUP.md`: explicación de la solución.

## Objetivo

Reconstruir el mensaje final oculto dentro del tráfico HTTPS. El flujo incluye:

1. una respuesta gzip con un JSON auxiliar,
2. una segunda respuesta con `Transfer-Encoding: chunked`,
3. una ofuscación final con `XOR + base64`.

## Uso

```bash
python3 solve.py
```

Requiere `tshark` instalado.

## Pistas

- Cargá `keylog.txt` al analizar la captura.
- No te quedes solo con la vista “de paquetes”; reconstruí el HTTP completo.
- Una respuesta entrega el seed y la otra el payload final.
