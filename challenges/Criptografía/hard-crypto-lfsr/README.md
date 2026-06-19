# hard-crypto-lfsr — StreamCorp: LFSR Stream Cipher

**Dificultad:** Hard  
**Categoria:** Criptografia  
**Tecnica:** Known-Plaintext Attack + Brute Force de estado LFSR

---

## Descripcion del reto

Un cifrador de flujo basado en un LFSR (Linear Feedback Shift Register) de 16 bits
fue utilizado para cifrar un mensaje que contiene el FLAG. El polinomio de
retroalimentacion y la estructura del LFSR son publicos. El estado inicial (semilla)
es desconocido, pero el espacio de busqueda tiene solo 65 536 posibilidades.

Ademas, se sabe que el mensaje comienza con el prefijo `HACKL4BS_CTF_`.

---

## Conceptos clave

### LFSR (Linear Feedback Shift Register)

Un LFSR es un registro de desplazamiento cuyo bit de entrada se calcula como
una funcion lineal (XOR) de algunos de sus bits anteriores. Genera una secuencia
pseudo-aleatoria determinista a partir de un estado inicial (semilla).

La implementacion usa la forma **Galois** con taps `0xB400`:

```
Polinomio: x^16 + x^14 + x^13 + x^11 + 1
```

En cada paso:
1. Se extrae el bit menos significativo (output bit)
2. Se desplaza el registro a la derecha
3. Si el bit de salida era 1, se XORea con los taps

El keystream se genera tomando 8 bits (1 byte) por cada 8 pasos del LFSR.

### El ataque

**Known-Plaintext Attack:** Como el prefijo `HACKL4BS_CTF_` es conocido,
podemos recuperar los primeros 13 bytes del keystream:

```
keystream[:13] = ciphertext[:13] XOR plaintext[:13]
```

Con el keystream inicial podemos verificar si una semilla candidata lo produce.
Como el espacio es solo 2^16 = 65 536, el brute force es instantaneo.

**Complejidad:** O(65 536) — menos de 1 segundo en cualquier maquina.

---

## Estructura de archivos

```
hard-crypto-lfsr/
  app/
    build.py       <- genera keystream LFSR, cifra el mensaje, guarda dist/stream.txt
    server.py      <- Flask: sirve dist/stream.txt
    entrypoint.sh
  Dockerfile
  docker-compose.yaml
  challenge.yaml
  README.md
  solve.py
```

---

## Ejecutar el reto

```bash
export FLAG="CTF{tu_flag_aqui}"
docker compose up --build
```

Acceder en: http://localhost:8080

---

## Ejecutar el solve

```bash
# Descargar stream.txt del reto y colocarlo en el directorio actual
python3 solve.py
```

El script:
1. Lee el ciphertext de `stream.txt`
2. Itera los 65 536 estados posibles del LFSR
3. Verifica contra el prefijo conocido `HACKL4BS_CTF_`
4. Al encontrar la semilla correcta, descifra el mensaje completo

---

## Recursos

- https://en.wikipedia.org/wiki/Linear-feedback_shift_register
- https://en.wikipedia.org/wiki/Known-plaintext_attack
- Golomb, S.W. (1967). "Shift Register Sequences"
