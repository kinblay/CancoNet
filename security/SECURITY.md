# Seguridad — estado y plan

Alertas del Security Advisor de Supabase (26 jul 2026): **13 errores, 33 warnings**.
Proyecto `ikfouhxdtkptafglthmd`.

---

## El problema

La app es una PWA estática: no hay servidor propio, el navegador habla directamente
con PostgREST usando la *anon key*, que va escrita en `index.html`. Eso es normal y
esperado — la anon key es pública por diseño. **Lo único que protege los datos es RLS.**

Y RLS está desactivado.

El error crítico (`rls_disabled_in_public` sobre `public.profiles`) significa que
cualquiera que abra el HTML, copie la URL del proyecto y la anon key —treinta segundos
de trabajo— puede leer, modificar y **borrar** toda la tabla. `profiles` contiene los
emails de los usuarios registrados.

La variante `Policy Exists RLS Disabled` es aún más engañosa: las políticas están
escritas, parecen protección, pero **no se aplican** porque RLS nunca se activó.

## La causa de fondo

`index.html` implementaba login por OTP y guardaba el `access_token` en localStorage…
pero **nunca lo usaba**. La constante de cabeceras era fija:

```js
const SBH={...,'Authorization':'Bearer '+SB_KEY};   // siempre la anon key
```

Las 27 llamadas a la base de datos salían como rol `anon`. `auth.uid()` era `NULL`
en todas. Por eso activar RLS a ciegas habría dejado la app inservible: las políticas
basadas en el usuario nunca se cumplen si el usuario nunca se identifica.

Es muy probable que esa sea la historia de cómo se llegó aquí: alguien creó políticas,
vio que la app dejaba de funcionar, y desactivó RLS en vez de arreglar el token.

## Lo ya arreglado (en el código)

`Authorization` pasa a ser un *getter*: cada petición usa el JWT del usuario si hay
sesión válida, y cae a la anon key si no. Los 27 puntos de llamada quedan cubiertos
sin tocarlos, porque todos usan `SBH` o `{...SBH}`.

También estaba mal guardada la caducidad de sesión: se anotaba como 30 días cuando el
`access_token` de Supabase dura 1 hora. Ahora se usa el `expires_in` real y hay
renovación automática al arrancar y cada 10 minutos.

Este cambio **no altera el comportamiento actual** (con RLS desactivado todo pasa
igual), pero es el prerequisito para poder activarlo.

## Lo que falta (en Supabase — requiere tu acceso)

Por orden:

1. **Publica el cambio de `index.html`.** Sin esto, el paso 2 rompe la app.
2. Ejecuta `01-diagnostic.sql` y revisa el resultado.
3. Ejecuta `02-fix-rls.sql` **bloque a bloque**, probando la app entre bloques.
   Empieza por el bloque A (`profiles`), que es el crítico.

## Deuda pendiente

- **`challenges` y `salas` no tienen un dueño identificable.** Se relacionan por `nick`,
  que es texto libre y no está en el JWT. Mientras siga así no se pueden escribir
  políticas de UPDATE/DELETE correctas: o abres la escritura a todos (inseguro) o
  bloqueas a los jugadores legítimos. Hace falta añadir una columna `user_id uuid`
  ligada a `auth.users` y migrar las filas existentes.
- **La puntuación se calcula en el cliente.** Aunque RLS impida modificar puntuaciones
  ajenas, cualquiera puede enviar la suya propia con el valor que quiera. Blindarlo
  requiere validar en servidor (una función `SECURITY DEFINER` o un Edge Function).
  No es urgente para el lanzamiento, pero condiciona que el ranking sea creíble.
- **No hay rate limiting** en `bustia` ni `song_reports`: se pueden inundar.

## Nota sobre la anon key

No hace falta rotarla ni ocultarla: es pública por diseño y ocultarla no aportaría
nada. Lo que hay que arreglar es RLS. Si en algún momento se filtrase la
`service_role` key (esa sí es secreta, nunca debe aparecer en el HTML), habría que
rotarla de inmediato.
