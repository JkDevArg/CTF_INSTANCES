# Módulo de Forense — Lab 02

## Cómo usar

1. **Descargar imagen de práctica** (MemLabs o similar):
   ```bash
   # Opción A: MemLabs challenge images (gratuitas)
   wget https://mega.nz/...  # ver README de MemLabs en GitHub

   # Opción B: Crear imagen de prueba con LiME en VM local
   # Opción C: Usar imagen de ejemplo incluida (simulada)
   ```

2. **Copiar imagen a esta carpeta:**
   ```bash
   cp ~/Downloads/memory.raw ./incident.raw
   ```

3. **Abrir Volatility3 Jupyter Notebook:**
   - Navega a http://localhost:8888
   - Token: `lab2024`
   - Abre `notebook.ipynb`

## Comandos Volatility3 clave

```bash
# Desde el contenedor lab02-volatility
docker exec -it lab02-volatility bash

vol -f /memory/incident.raw windows.info
vol -f /memory/incident.raw windows.pslist
vol -f /memory/incident.raw windows.pstree
vol -f /memory/incident.raw windows.malfind
vol -f /memory/incident.raw windows.cmdline
vol -f /memory/incident.raw windows.netscan
```

## Flag del módulo forense
La Flag #1 está codificada en los artefactos de la imagen de memoria.
Usa `windows.strings` y `windows.malfind` para encontrarla.
