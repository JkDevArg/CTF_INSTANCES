# La Flag Perdida

| Field      | Value                        |
|------------|------------------------------|
| Category   | Forensic                     |
| Difficulty | Intermediate                 |
| Docker     | Yes                          |
| Port       | 80 (host default: 8080)      |

## Description

Una imagen que esconde más de lo que muestra. El investigador dejó instrucciones, pero están dispersas. Sigue el rastro.

El archivo PNG contiene datos hexadecimales de un archivo ZIP embebidos fuera del contenido de imagen estándar. Al extraer el hex, convertirlo a binario y descomprimir con la contraseña `password123`, se obtiene `flag.txt` con la flag.

## Files

| File               | Description                                        |
|--------------------|----------------------------------------------------|
| `flag_perdida.png` | PNG con datos hex de un ZIP embebidos (8265 bytes) |
| `leer.txt`         | Instrucciones del investigador                     |
| `datos.txt`        | Datos auxiliares                                   |

## Vulnerability / Solution

1. Descargar `flag_perdida.png` y `leer.txt`.
2. Leer `leer.txt` para entender el proceso.
3. Extraer los datos hex del PNG (están fuera del contenido de imagen).
4. Convertir el hex a binario: `xxd -r -p datos.hex > archivo.zip` (o similar).
5. Descomprimir con contraseña: `unzip -P password123 archivo.zip`.
6. Leer `flag.txt` para obtener la flag.

## How to run

```bash
# Build and start
FLAG="H4L{...}" docker compose up --build -d

# Access
http://localhost:8080

# Stop
docker compose down
```
