# La Caja Negra

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoría   | Criptografía                 |
| Dificultad  | Hard                         |
| Docker      | Sí                           |
| Puerto      | 80                           |

## Descripción

Un servicio de cifrado acepta tu input y devuelve el resultado cifrado con AES. Antes de cifrar, siempre concatena un secreto al final del input. La clave es fija durante toda la vida del contenedor. El modo es determinista. Extrae el secreto byte a byte.

## API

```
POST /encrypt
Content-Type: application/json

{ "data": "<hex string>" }

→ { "ciphertext": "<hex string>" }
```

El oráculo cifra: `AES-ECB(pad(user_input + FLAG, 16))` con clave fija.

## Vulnerabilidad

**AES-ECB Byte-at-a-time Decryption**

AES-ECB es determinista: el mismo bloque de 16 bytes siempre produce el mismo ciphertext. No hay IV ni estado.

El atacante controla `user_input` y puede alinear los bytes de `FLAG` de forma que queden en posiciones conocidas de cada bloque. Luego, probando los 256 valores posibles para cada byte, puede recuperar el FLAG completo.

## Ataque (resumen)

```
Para byte i del FLAG:
  1. Enviar 'A' * (15 - i%16) → el byte FLAG[i] cae al final del bloque i//16
  2. Capturar ese bloque objetivo
  3. Bruteforce: probar oracle('A'*(15-i%16 si i<15, o known_bytes) + chr(b))
     hasta que el primer bloque del ciphertext coincida
  4. FLAG[i] = b encontrado
```

Complejidad: `O(256 × len(FLAG))` llamadas al oráculo — trivial.

## Cómo detectar ECB

```python
ct = oracle(b'A' * 32)
assert ct[0:16] == ct[16:32]  # bloques idénticos → ECB confirmado
```

## Cómo ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`. El script `solve.py` automatiza el ataque completo.

## Flags dinámicas

El FLAG viene del entorno inyectado por Whaley. La clave AES se genera aleatoriamente al arrancar el contenedor (`secrets.token_bytes(16)`), es única por instancia y nunca se expone.
