# insane-crypto-rsa-lsb — RSACorp: LSB Oracle Attack

**Dificultad:** Insane  
**Categoria:** Criptografia  
**Tecnica:** RSA LSB Oracle Attack (busqueda binaria con propiedad multiplicativa)

---

## Descripcion del reto

Un servidor RSA ofrece descifrado de cualquier ciphertext, pero solo revela
el bit menos significativo (LSB) del plaintext descifrado — es decir, si el
resultado es par (0) o impar (1). La clave publica `(n, e)` y el ciphertext
`c` estan disponibles. El objetivo es recuperar el plaintext completo haciendo
solo `O(log n)` consultas al oraculo.

---

## Conceptos clave

### Propiedad multiplicativa de RSA

RSA es un criptosistema multiplicativamente homomorfico:

```
Enc(a) * Enc(b) mod n = Enc(a*b mod n)
```

En particular:

```
pow(2, e, n) * c mod n  =  Enc(2 * m mod n)
```

Es decir, podemos multiplicar el mensaje cifrado por 2 (en el espacio cifrado)
y el oraculo nos dira si `2m mod n` es par o impar.

### El ataque de busqueda binaria

Sea `m` el mensaje original (desconocido) con `0 <= m < n`.

En cada paso `i`, calculamos `c_i = pow(2, e, n)^i * c_orig mod n`:

- Si el oraculo devuelve `lsb = 0`: `2^i * m mod n` es **par**
  - Si `n` es impar (siempre en RSA), `2^i * m` es par → `m` esta en la mitad inferior del intervalo actual
- Si el oraculo devuelve `lsb = 1`: `2^i * m mod n` es **impar**
  - `m` esta en la mitad superior del intervalo actual

Manteniendo un intervalo `[lo, hi)` que se reduce a la mitad en cada paso,
despues de `log2(n)` iteraciones el intervalo tiene ancho 1 y `hi = m`.

**Numero de consultas:** exactamente `n.bit_length()` (512 para este reto).

### Por que es "insane"

- Requiere entender la homomorficidad de RSA (concepto avanzado)
- Implementar la busqueda binaria con aritmetica modular de enteros grandes
- Hacer 512 peticiones HTTP correctamente coordinadas
- Manejar la aritmetica de precision exacta (no usar floats)

---

## Estructura de archivos

```
insane-crypto-rsa-lsb/
  app/
    build.py       <- genera RSA 512 bits, cifra FLAG, guarda params.json + clave en /tmp
    server.py      <- Flask: pagina + POST /oracle que devuelve LSB
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
# Con el servicio corriendo en localhost:8080
python3 solve.py
```

El script:
1. Descarga `params.json` (n, e, c)
2. Calcula `f = Enc(2) = pow(2, e, n)`
3. En cada iteracion: multiplica c por f (en el espacio cifrado) y consulta el LSB
4. Actualiza el intervalo `[lo, hi]` con busqueda binaria
5. Despues de `n.bit_length()` iteraciones imprime el FLAG

**Tiempo estimado:** ~30-60 segundos dependiendo de la latencia de red.

---

## Recursos

- https://crypto.stackexchange.com/questions/11281/cryptanalysis-of-textbook-rsa
- https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Attacks_against_plain_RSA
- Boneh, D. (1999). "Twenty Years of Attacks on the RSA Cryptosystem"
- https://masterpessimist.github.io/rsa-lsb-oracle/
