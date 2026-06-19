# Banco HACKL4BS Vault V3-C — Writeup

## Resumen

La versión final del reto ya no se resuelve con el endpoint antiguo de transferencias.
El flujo relevante es:

1. Preparar operaciones.
2. Confirmarlas.
3. Agruparlas en un lote operativo.
4. Marcar el lote listo para cierre.
5. Lanzar cierres concurrentes sobre el mismo lote.
6. Esperar la derivación a mesa de control.
7. Calcular la clave operativa.
8. Abrir el expediente.
9. Leer el código final.

---

## Reconocimiento inicial

El portal expone varias pantallas:

- `index.php`: dashboard principal.
- `preparar.php`: prepara una operación.
- `confirmar.php`: confirma la operación.
- `lote.php`: permite asociar operaciones al lote.
- `cerrar_lote.php`: ejecuta el cierre operativo.
- `mesa_control.php`: muestra los datos visibles de conciliación.
- `expediente.php`: entrega el código cuando la validación es correcta.

El endpoint viejo de transferencias ya no es útil para explotar el reto.

---

## Dónde está la vulnerabilidad

La condición de carrera real vive en el cierre del lote.

Cuando el lote está listo para cierre, varias requests concurrentes pueden entrar a `cerrar_lote.php` antes de que el estado final se estabilice.
Eso puede generar múltiples asientos de cierre para el mismo lote.

La revisión aparece cuando el desvío contable y la cantidad de asientos superan el umbral interno.

---

## Flujo usado por el solver

El solver automatiza este patrón:

1. Reinicia la ventana operativa usando el token del dashboard.
2. Prepara dos operaciones de 100.
3. Confirma ambas.
4. Las agrega al lote.
5. Marca el lote como listo para cierre.
6. Dispara muchas solicitudes simultáneas a `cerrar_lote.php`.
7. Espera a que la mesa de control se estabilice.
8. Calcula la clave operativa.
9. Prueba la apertura del expediente.

En la instancia local, la combinación más confiable fue usar muchos cierres paralelos con dos operaciones en el lote.

---

## Datos visibles en mesa de control

Cuando aparece la revisión, `mesa_control.php` muestra solo los ingredientes visibles para derivar la clave:

- referencia del lote
- total consolidado del lote
- cantidad de asientos de cierre
- sufijo visible del lote

La clave se calcula con esta fórmula:

```text
(batch_total + settlement_count + batch_numeric_suffix) % 97
```

Donde:

- `batch_total` es el total del lote
- `settlement_count` es la cantidad de asientos de cierre
- `batch_numeric_suffix` es el valor decimal de los últimos 4 hex del lote

---

## Apertura del expediente

`expediente.php` valida que la referencia del lote y la clave operativa sean correctas.

Si coinciden, muestra el código final dentro del bloque de auditoría.
Si no coinciden, devuelve un mensaje genérico sin filtrar información útil.

El solver no busca patrones amplios de texto: solo acepta el bloque real del expediente.

---

## Comportamiento del solver

El script `solve.py` hace lo siguiente:

- prepara operaciones
- dispara cierres concurrentes
- lee la mesa de control
- calcula la clave operativa
- prueba el expediente
- si no funciona a la primera, prueba los 97 valores posibles

Eso lo hace tolerante a pequeñas variaciones de timing entre ejecuciones.

---

## Comandos útiles

Levantar el reto:

```bash
docker compose up --build -d
```

Ejecutar el solver:

```bash
python3 solve.py
```

Modo más agresivo:

```bash
python3 solve.py --workers 60
```

Validar sintaxis del solver:

```bash
python3 -m py_compile solve.py
```

---

## Conclusión

El reto ya no depende de una única petición directa.
La solución requiere:

- descubrir el flujo bancario,
- entender que la carrera real está en el cierre del lote,
- derivar la clave operativa,
- y abrir el expediente con los datos correctos.

Ese es el camino que automatiza el solver.
