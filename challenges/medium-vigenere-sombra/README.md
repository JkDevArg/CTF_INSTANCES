# La Sombra del Cifrado

| Campo       | Valor                |
|-------------|----------------------|
| Categoría   | Criptografía         |
| Dificultad  | Medium               |
| Docker      | Sí                   |
| Puerto      | 80                   |

## Descripción

Los archivos de un agente legendario fueron interceptados. Cifró sus mensajes con un método clásico usando una clave que era también su nombre. Encuentra la clave y descifra el diario.

## Archivos entregados

- `diario.txt` — texto cifrado con Vigenère

## Vulnerabilidad

Cifrado de Vigenère con clave corta (6 letras). Sujeto a análisis de frecuencias, Kasiski y/o ataque de texto conocido usando el prefijo `CTF{`.

## Solución esperada

1. Detectar longitud de clave con Índice de Coincidencia o prueba de Kasiski (~6)
2. Para cada posición de la clave, resolver un César por frecuencia de letras
3. Clave: `SOMBRA`
4. Descifrar el texto completo para extraer la flag

## Cómo ejecutar

```bash
FLAG="CTF{mi_flag_secreta}" docker compose up --build
```

Acceder en http://localhost:8080

## Nota sobre flags dinámicas

Whaley inyecta un FLAG único por instancia vía variable de entorno. El `build.py` lo embebe cifrado en el texto. Cada instancia genera un `diario.txt` diferente.
