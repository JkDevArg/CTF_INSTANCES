# hard-crypto-padding-oracle — CipherCorp: AES-CBC Padding Oracle

**Dificultad:** Hard  
**Categoria:** Criptografia  
**Tecnica:** Padding Oracle Attack (Vaudenay, 2002)

---

## Descripcion del reto

Un servicio de descifrado AES-CBC acepta ciphertexts arbitrarios y responde
si el padding PKCS#7 es valido o no. El FLAG fue cifrado con AES-CBC y el
ciphertext interceptado esta disponible para descargar. El objetivo es
recuperar el plaintext usando solo el oraculo de padding.

---

## Conceptos clave

### AES-CBC

En modo CBC (Cipher Block Chaining), el descifrado de un bloque funciona asi:

```
Plaintext_i = Decrypt(Ciphertext_i) XOR Ciphertext_{i-1}
```

El IV actua como el "bloque anterior" para el primer bloque.

### PKCS#7 Padding

El padding rellena el ultimo bloque hasta 16 bytes. Si faltan N bytes,
se agregan N bytes con valor N. Por ejemplo, si el mensaje termina con
3 bytes de relleno: `... 0x03 0x03 0x03`.

### El ataque

Dado que el oraculo revela si el padding es valido, podemos:

1. Modificar un byte del bloque anterior (el IV o cualquier bloque)
2. Probar los 256 valores posibles para ese byte
3. Cuando el padding es valido, sabemos que:
   `Decrypt(Ciphertext_i)[j] XOR crafted_byte = padding_value`
4. De ahi obtenemos el byte intermedio y luego el plaintext:
   `Plaintext[j] = intermediate[j] XOR original_prev_block[j]`

Se repite para cada byte de cada bloque, de derecha a izquierda,
ajustando el padding objetivo (0x01 para el ultimo byte, 0x02 para
los dos ultimos, etc.).

**Complejidad:** 256 * 16 * num_bloques peticiones al maximo (~4096 para 1 bloque).

---

## Estructura de archivos

```
hard-crypto-padding-oracle/
  app/
    build.py       <- cifra el FLAG, genera dist/intercepted.json, guarda KEY en /tmp
    server.py      <- Flask: sirve archivos + endpoint POST /oracle
    entrypoint.sh  <- mkdir dist && python3 build.py && python3 server.py
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
1. Descarga `intercepted.json` (IV + ciphertext)
2. Ejecuta el ataque de padding oracle bloque a bloque
3. Imprime el plaintext (FLAG)

---

## Recursos

- Vaudenay, S. (2002). "Security Flaws Induced by CBC Padding"
- https://robertheaton.com/2013/07/29/padding-oracle-attack/
- https://en.wikipedia.org/wiki/Padding_oracle_attack
