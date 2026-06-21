# Writeup — postal

## Idea

La flag no está en los píxeles sino en los metadatos PNG, dentro del campo `Comment`.

## Resolución esperada

```bash
exiftool player/postal.png
```

Se observa una entrada similar a:

```text
Comment: SDRMe01FVEFEQVRBX05PX0VTX0JBU1VSQX0=
```

Luego:

```bash
echo 'SDRMe01FVEFEQVRBX05PX0VTX0JBU1VSQX0=' | base64 -d
```

Resultado:

```text
H4L{METADATA_NO_ES_BASURA}
```

## Aprendizaje

- Mirar metadata
- Buscar strings y comentarios embebidos
- Reconocer base64
