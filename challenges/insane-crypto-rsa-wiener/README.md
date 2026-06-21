# insane-crypto-rsa-wiener — RSACorp: Wiener's Attack

**Dificultad:** Insane  
**Categoria:** Criptografia  
**Tecnica:** Wiener's Attack mediante Fracciones Continuas

---

## Descripcion del reto

Un mensaje fue cifrado con RSA usando un exponente privado `d` inusualmente
pequeno, elegido por razones de "eficiencia computacional". La clave publica
`(n, e)` y el ciphertext `c` estan disponibles. El objetivo es recuperar `d`
sin factorizar `n`, aplicando el teorema de Wiener.

---

## Conceptos clave

### RSA estandar

```
Generacion: p, q primos grandes; n = p*q; phi = (p-1)*(q-1)
            e*d ≡ 1 (mod phi)
Cifrado:    c = m^e mod n
Descifrado: m = c^d mod n
```

### Teorema de Wiener (1990)

**Si `d < n^0.25 / 3`, entonces `d` puede recuperarse de forma eficiente
usando la expansion en fracciones continuas de `e/n`.**

La idea clave es que si `e*d ≡ 1 (mod phi)`, entonces existe un entero `k`
tal que:

```
e*d = k*phi + 1
e/n ≈ k/d    (porque phi ≈ n)
```

Los convergentes de la fraccion continua de `e/n` son aproximaciones
racionales muy buenas. Uno de ellos es exactamente `k/d`.

### Algoritmo del ataque

1. Calcular los coeficientes de la fraccion continua de `e/n`:
   ```
   e/n = a0 + 1/(a1 + 1/(a2 + ...))
   ```

2. Calcular los convergentes `k_i/d_i` de esa fraccion continua.

3. Para cada convergente `(k, d)`:
   - Si `k == 0`, saltar
   - Calcular `phi_candidate = (e*d - 1) / k` (debe ser entero)
   - Verificar si `n - phi_candidate + 1` tiene raices enteras:
     `discriminante = (n - phi + 1)^2 - 4n >= 0` y es un cuadrado perfecto
   - Si las raices `p, q` satisfacen `p*q == n`, entonces `d` es correcto

4. Descifrar: `m = c^d mod n`

**Complejidad:** O(log n) — solo necesita recorrer los convergentes.

---

## Estructura de archivos

```
insane-crypto-rsa-wiener/
  app/
    build.py       <- genera RSA con d pequeno, cifra FLAG, guarda dist/wiener.txt
    server.py      <- Flask: sirve dist/wiener.txt con explicacion del reto
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
# Descargar wiener.txt del reto y colocarlo en el directorio actual
python3 solve.py
```

El script implementa el ataque completo de Wiener:
1. Parsea `n`, `e`, `c` de `wiener.txt`
2. Calcula la expansion en fracciones continuas de `e/n`
3. Itera los convergentes buscando el `d` correcto
4. Descifra el FLAG con `c^d mod n`

---

## Recursos

- Wiener, M. (1990). "Cryptanalysis of Short RSA Secret Exponents"
- https://en.wikipedia.org/wiki/Wiener%27s_attack
- https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf
- Boneh, D. & Durfee, G. (1999). "Cryptanalysis of RSA with private key d less than n^0.292"
