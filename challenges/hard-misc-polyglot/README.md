# hard-misc-polyglot

**Categoria:** Misc  
**Dificultad:** Hard  
**Puerto:** 80 (descarga de archivos)

## Descripcion

Reto de archivo poliglota (polyglot file). El archivo `artifact-7734.png` es simultaneamente un PNG valido y un ZIP valido.

- Los parsers PNG leen desde el inicio y se detienen en el chunk `IEND`, ignorando los bytes posteriores
- Los parsers ZIP buscan la firma `End of Central Directory` desde el **final** del archivo

Esto permite concatenar un PNG y un ZIP y obtener un archivo que ambos formatos aceptan como valido.

## Estructura del archivo

```
[PNG data: cabecera + chunks + IEND]
[ZIP data: local file headers + central directory + EOCD]
```

## Solucion

```bash
# Opcion 1: comando unzip directamente sobre el PNG
unzip artifact-7734.png

# Opcion 2: Python
python3 -c "import zipfile; print(zipfile.ZipFile('artifact-7734.png').read('flag.txt').decode())"

# Opcion 3: binwalk
binwalk -e artifact-7734.png
```

## Herramientas utiles

- `file artifact-7734.png` — identifica el tipo primario
- `binwalk artifact-7734.png` — detecta firmas embebidas
- `xxd artifact-7734.png | tail -20` — ver bytes finales (cabecera ZIP)
- `unzip -l artifact-7734.png` — listar contenido del ZIP

## Setup local

```bash
docker-compose up --build
# Descargar desde http://localhost/download/artifact-7734.png
python3 solve.py
```

## Archivos

- `app/build.py` — genera el archivo poliglota PNG+ZIP
- `app/server.py` — pagina informativa con enlace de descarga
- `solve.py` — solucion completa
