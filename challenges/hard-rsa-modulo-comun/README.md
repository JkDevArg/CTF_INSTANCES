# Doble Cifrado

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoría   | Criptografía                 |
| Dificultad  | Hard                         |
| Docker      | Sí                           |
| Puerto      | 80                           |

## Descripción

El mismo mensaje fue cifrado dos veces con RSA usando el mismo módulo `n` pero con exponentes públicos distintos (`e1 = 3`, `e2 = 65537`). Ambos cifrados fueron interceptados. Recupera el mensaje original.

## Archivos entregados

- `intercepted.txt` — contiene `n`, `e1`, `c1`, `e2`, `c2`

## Vulnerabilidad

**Common Modulus Attack**

Si `gcd(e1, e2) = 1` (coprimos), el Algoritmo de Euclides Extendido encuentra `a`, `b` tales que:

```
a·e1 + b·e2 = 1
```

Por las propiedades de RSA:

```
c1^a · c2^b ≡ m^(a·e1) · m^(b·e2) ≡ m^(a·e1 + b·e2) ≡ m^1 ≡ m  (mod n)
```

Si `a` o `b` son negativos, se usa el inverso modular de `c1` o `c2`.

## Solución

```python
g, a, b = extended_gcd(e1, e2)   # a·e1 + b·e2 = 1
base1 = modinv(c1, n) if a < 0 else c1
base2 = modinv(c2, n) if b < 0 else c2
m = (pow(base1, abs(a), n) * pow(base2, abs(b), n)) % n
flag = long_to_bytes(m).decode()
```

Ver `solve.py` para la implementación completa.

## Cómo ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`, descargar `intercepted.txt`.

## Flags dinámicas

`build.py` genera un nuevo módulo `n` y calcula `c1`, `c2` a partir del FLAG inyectado por Whaley. Los exponentes `e1 = 3` y `e2 = 65537` son siempre fijos.
