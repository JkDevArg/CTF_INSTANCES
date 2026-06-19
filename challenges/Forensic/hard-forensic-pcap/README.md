# NetCapture Corp — HTTP Traffic Analysis

| Campo       | Valor                                        |
|-------------|----------------------------------------------|
| Categoría   | Forensic                                     |
| Dificultad  | Hard                                         |
| Técnica     | Análisis de tráfico HTTP — extracción de datos ocultos |
| Docker      | Sí                                           |
| Puertos     | 80 (web)                                    |

## Descripción

Se capturó tráfico HTTP de la red interna de CorpSec durante un incidente de seguridad.
La flag fue filtrada accidentalmente en **dos transacciones HTTP distintas**:

- **Parte 1**: En un parámetro GET de una URL (`?token=`).
- **Parte 2**: En un campo JSON de una respuesta de API (`session_data`).

El jugador debe descargar el archivo `capture.log` y analizar el tráfico HTTP para encontrar y concatenar ambas partes.

## Técnica de solución

```bash
# Opción 1: grep directo
grep -oP 'token=\K[^\s&]+' capture.log
grep -oP '"session_data":\s*"\K[^"]+' capture.log

# Opción 2: python
python3 solve.py
```

## Cómo ejecutar

```bash
FLAG="CTF{test_flag}" docker compose up --build
```

Acceder al panel de descargas en `http://localhost:8080`.
Descargar `capture.log` y `README.txt`.
