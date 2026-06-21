# easy-osint-exif — MediaCorp EXIF Metadata

**Dificultad**: Fácil  
**Categoría**: OSINT  
**Puerto**: 80

## Descripción
Una imagen PNG del servidor de medios de HACKL4BS Corp contiene información oculta en sus metadatos EXIF/PNG. Analiza los metadatos completos de la imagen para encontrar la flag.

## Cómo iniciar
```bash
docker-compose up -d
```
Accede en: http://localhost:8080

## Solución
```bash
# Con exiftool
exiftool summit_2024.png | grep Comment

# Con Python
python3 solve.py
```

## Concepto
Los archivos de imagen almacenan metadatos (EXIF, PNG text chunks, etc.) que pueden contener información sensible filtrada accidentalmente.
