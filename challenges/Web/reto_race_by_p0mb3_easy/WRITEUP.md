# Writeup — Banco HACKL4BS Vault

## Idea general

El reto está diseñado como una **race condition** en un portal de transferencias.  
La aplicación permite ejecutar transferencias de hasta `$100`, pero el backend procesa cada operación con un patrón vulnerable:

1. lee el saldo actual,
2. espera un tiempo aleatorio,
3. recién después descuenta el dinero y registra la transferencia.

Ese espacio entre la lectura y la escritura permite que varias peticiones concurrentes lean el mismo saldo antes de que se actualice, generando inconsistencias entre el saldo real de la cuenta y el total de transferencias aprobadas.

## Dónde está la vulnerabilidad

La lógica vulnerable está en `app/TransferService.php`, dentro de `executeTransfer()`.

El flujo es:

- validar que el monto esté entre `$1` y el límite permitido,
- buscar la cuenta activa,
- leer el saldo,
- esperar un delay aleatorio,
- actualizar el saldo,
- registrar la transferencia como aprobada.

Como no hay bloqueo transaccional entre la lectura y la escritura, varias solicitudes pueden trabajar sobre el mismo saldo inicial.

## Condición de desbloqueo

La conciliación se evalúa en `app/ReconciliationService.php`.

El reto se desbloquea cuando se cumplen estas dos condiciones:

- el desvío contable (`drift`) es mayor o igual a `UNLOCK_DRIFT = 1200`,
- la cantidad de transferencias aprobadas es mayor o igual a `MIN_APPROVED_TRANSFERS = 8`.

El `drift` se calcula así:

```text
drift = total_transferencias_aprobadas - debito_real
```

Si las transferencias concurrentes se pisan entre sí, el sistema aprueba más operaciones de las que realmente descuenta del saldo, creando ese desvío.

## Qué hace `solve.py`

El script automatiza el ataque de concurrencia:

- primero llama a `/reset.php` para restaurar el entorno,
- luego dispara **14 hilos simultáneos**,
- cada hilo envía una transferencia de `$100`,
- usa un `Barrier` para que todas las peticiones salgan al mismo tiempo,
- finalmente consulta `/` y `/estado.php` para verificar si se desbloqueó la alerta o salió la flag.

La clave está en estas constantes:

```python
WORKERS = 14
AMOUNT = 100
```

y en la sincronización:

```python
barrier = Barrier(WORKERS)
```

## Paso a paso del exploit

1. **Restablecer el entorno**  
   El script limpia el estado para partir desde el saldo inicial y sin movimientos previos.

2. **Lanzar muchas transferencias a la vez**  
   Se envían 14 solicitudes concurrentes de `$100`.

3. **Aprovechar la race condition**  
   Varias solicitudes leen el mismo saldo antes de que otra lo actualice.

4. **Superar el umbral de conciliación**  
   Cuando el desvío y la cantidad de transferencias superan los valores configurados, el sistema marca la cuenta como desbloqueada.

5. **Obtener la flag**  
   Al cargar la página principal, aparece la sección de **“Alerta de conciliación”** y se muestra el código oculto.

## Resultado esperado

Una vez explotado correctamente, la interfaz principal deja de mostrar el estado normal y pasa a mostrar el aviso de conciliación con el código revelado.  
Si el despliegue tiene configurada la variable `CTF_FLAG` o el archivo `private/flag.txt`, ahí aparece la flag final.

## Resumen corto

El reto se resuelve explotando una **race condition** en el endpoint de transferencias.  
`solve.py` dispara múltiples solicitudes simultáneas para forzar inconsistencias en el saldo y provocar que el sistema detecte un desvío contable suficiente para desbloquear la flag.

