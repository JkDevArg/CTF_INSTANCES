# medium-misc-git

**Categoria:** Misc  
**Dificultad:** Media  
**Puertos:** 80 (descarga web)

---

## Descripcion

Un repositorio git interno de "CorpCorp" fue filtrado. El equipo de seguridad
elimino las credenciales del codigo fuente en un commit posterior — pero en git,
lo que se elimina de un commit nunca desaparece del historial.

El jugador descarga el bundle, clona el repositorio y excava en el historial
para encontrar la flag que fue "borrada".

---

## Estructura del repositorio generado

| Commit | Mensaje | Contenido relevante |
|--------|---------|---------------------|
| 1 | `feat: initial commit` | README.md, config.py (limpio) |
| 2 | `fix: add backup configuration` | config.py con `BACKUP_KEY = "<FLAG>"` |
| 3 | `security: remove sensitive data from config` | config.py sin la clave |
| 4 | `feat: add application entry point` | app.py |

---

## Solucion paso a paso

### 1. Descargar el bundle

```bash
wget http://<host>/files/corp-repo.bundle
# o con curl:
curl -O http://<host>/files/corp-repo.bundle
```

### 2. Clonar desde el bundle

```bash
git clone corp-repo.bundle corp-repo
cd corp-repo
```

### 3. Ver el historial de commits

```bash
git log --oneline
```

Salida esperada (hashes variaran):

```
<hash4> feat: add application entry point
<hash3> security: remove sensitive data from config
<hash2> fix: add backup configuration   <- aqui esta la flag
<hash1> feat: initial commit
```

### 4. Ver el diff del commit sospechoso

```bash
git show <hash2>
# o usando el mensaje:
git log -p | grep -A2 BACKUP_KEY
```

### 5. Ver el archivo completo en ese commit

```bash
git show <hash2>:config.py
```

---

## Script automatizado

```bash
python3 solve.py
```

El script clona el bundle localmente y extrae la flag del historial con `git log -p`.

---

## Despliegue

```bash
docker-compose up --build
```

Al arrancar, `build.py` usa la FLAG inyectada por entorno para generar el
repositorio git con el historial completo y crear el bundle en `/app/dist/`.
Flask sirve el bundle en `http://<host>/files/corp-repo.bundle`.

---

## Conceptos cubiertos

- Git bundles (`git bundle create / clone`)
- Inspeccion de historial (`git log -p`, `git show`)
- Forense de repositorios: los datos "borrados" en commits anteriores
  permanecen en el grafo de objetos hasta que se hace `git gc` con filtros agresivos.
