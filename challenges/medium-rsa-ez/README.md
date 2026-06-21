# RSA Lite

| Campo       | Valor                        |
|-------------|------------------------------|
| Categoría   | Criptografía                 |
| Dificultad  | Medium                       |
| Docker      | Sí                           |
| Puerto      | 80                           |

## Descripción

Un desarrollador cifró un mensaje corto con RSA y eligió `e = 3` por "eficiencia". El módulo es de 2048 bits. ¿Acaso el tamaño del módulo lo hace seguro?

## Archivos entregados

- `rsa_data.txt` — contiene `n`, `e = 3` y `c` (cifrado)

## Vulnerabilidad

**Small Public Exponent Attack (e = 3)**

Si el mensaje `m` es suficientemente corto (como una flag de ~40 bytes ≈ 320 bits), entonces:

```
m^3 < n  →  c = m^3  (la reducción modular nunca ocurre)
```

El atacante simplemente calcula la raíz cúbica entera de `c`.

## Solución

```python
from Crypto.Util.number import long_to_bytes

c = <valor de c>
m = round(c ** (1/3))          # aproximación flotante (puede fallar)

# Más robusto: búsqueda binaria para raíz cúbica exacta
# Ver solve.py
flag = long_to_bytes(m).decode()
print(flag)
```

Ver `solve.py` para la implementación completa.

## Cómo ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en `http://localhost:8080`, descargar `rsa_data.txt`.

## Flags dinámicas

Cada instancia generada por Whaley recibe un FLAG único vía variable de entorno.  
`build.py` genera un nuevo par `(n, c)` al arrancar el contenedor. El exponente `e = 3` es siempre fijo.
