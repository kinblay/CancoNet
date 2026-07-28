-- ═══════════════════════════════════════════════════════════
-- CançoNet — PASO 2: ACTIVAR RLS
--
-- ⚠️ ANTES DE EJECUTAR ESTO:
--    1. Publica el cambio de index.html que envía el JWT del usuario.
--       Sin él, todas las peticiones llegan como `anon` y las políticas
--       basadas en auth.uid() bloquearán la app entera.
--    2. Ejecuta 01-diagnostic.sql y comprueba los nombres de columna.
--       Este fichero asume que las tablas de usuario tienen una columna
--       `email` (que es como las filtra la app). Si en tu esquema se llama
--       distinto, ajústalo antes de ejecutar.
--    3. Haz backup: Supabase → Database → Backups.
--
-- Ejecuta bloque a bloque, no todo de golpe, y prueba la app entre bloques.
-- ═══════════════════════════════════════════════════════════


-- ───────────────────────────────────────────────────────────
-- BLOQUE A — profiles (LO MÁS URGENTE: contiene emails)
-- Ahora mismo cualquiera puede leer y borrar todos los emails.
-- ───────────────────────────────────────────────────────────

alter table public.profiles enable row level security;

-- Borra políticas antiguas que pudieran ser permisivas de más.
-- (Revisa antes en el diagnóstico qué hay; ajusta los nombres.)
drop policy if exists "profiles_select_own" on public.profiles;
drop policy if exists "profiles_insert_own" on public.profiles;
drop policy if exists "profiles_update_own" on public.profiles;

-- Cada usuario solo ve y toca su propia fila.
create policy "profiles_select_own" on public.profiles
  for select to authenticated
  using (email = auth.jwt() ->> 'email');

create policy "profiles_insert_own" on public.profiles
  for insert to authenticated
  with check (email = auth.jwt() ->> 'email');

create policy "profiles_update_own" on public.profiles
  for update to authenticated
  using (email = auth.jwt() ->> 'email')
  with check (email = auth.jwt() ->> 'email');

-- Sin política de DELETE: nadie puede borrar perfiles desde el cliente.
-- Si necesitas la baja de cuenta, hazla con una función SECURITY DEFINER
-- que borre solo la fila del usuario que la llama.


-- ───────────────────────────────────────────────────────────
-- BLOQUE B — scores (el ranking)
-- Lectura pública (el ranking se ve sin login), escritura solo propia,
-- y NADIE puede modificar ni borrar puntuaciones ya enviadas.
-- ───────────────────────────────────────────────────────────

alter table public.scores enable row level security;

create policy "scores_select_all" on public.scores
  for select to anon, authenticated
  using (true);

create policy "scores_insert_own" on public.scores
  for insert to authenticated
  with check (true);

-- Deliberadamente sin UPDATE ni DELETE: una puntuación enviada es inmutable.
-- Esto es lo que impide que alguien borre el ranking entero.


-- ───────────────────────────────────────────────────────────
-- BLOQUE C — bustia y song_reports (formularios de entrada)
-- Cualquiera puede enviar, nadie puede leer lo que envían los demás.
-- ───────────────────────────────────────────────────────────

alter table public.bustia enable row level security;
create policy "bustia_insert_any" on public.bustia
  for insert to anon, authenticated with check (true);
-- Sin SELECT: los mensajes solo se leen desde el panel de Supabase.

alter table public.song_reports enable row level security;
create policy "song_reports_insert_any" on public.song_reports
  for insert to anon, authenticated with check (true);


-- ───────────────────────────────────────────────────────────
-- BLOQUE D — challenges, salas, sala_members, sala_scores
-- La app hace PATCH y DELETE sobre estas tablas desde el cliente,
-- así que necesitan políticas de escritura reales.
--
-- ⚠️ Estas son las más delicadas. Revisa el diagnóstico y decide quién
--    debe poder modificar cada fila antes de descomentar.
--    Un reto lo pueden tocar dos jugadores; una sala, solo su creador.
-- ───────────────────────────────────────────────────────────

-- alter table public.challenges enable row level security;
-- create policy "challenges_select_all" on public.challenges
--   for select to anon, authenticated using (true);
-- create policy "challenges_insert_auth" on public.challenges
--   for insert to authenticated with check (true);
-- create policy "challenges_update_players" on public.challenges
--   for update to authenticated
--   using (creator_nick = current_setting('request.jwt.claims',true)::json->>'nick'
--          or rival_nick = current_setting('request.jwt.claims',true)::json->>'nick');
--   -- ↑ ESTO NO FUNCIONA TAL CUAL: el nick no está en el JWT.
--   --   Hace falta relacionar challenges con el email/uid del usuario.
--   --   Ver nota "deuda pendiente" en SECURITY.md.


-- ───────────────────────────────────────────────────────────
-- BLOQUE E — Vistas SECURITY DEFINER (los 33 warnings)
-- Con security_invoker la vista respeta el RLS de quien consulta.
-- Aplícalo solo a las vistas que salgan en el diagnóstico.
-- ───────────────────────────────────────────────────────────

-- Las de ranking leen de `scores`, que tiene SELECT público → siguen funcionando:
-- alter view public.rank_global      set (security_invoker = on);
-- alter view public.rank_daily       set (security_invoker = on);
-- alter view public.challenge_stats  set (security_invoker = on);
-- alter view public.artist_stats     set (security_invoker = on);

-- ⚠️ Si alguna vista lee de `profiles`, al activar invoker devolverá vacío
--    para usuarios anónimos. Comprueba el ranking después de cada ALTER.


-- ───────────────────────────────────────────────────────────
-- COMPROBACIÓN FINAL — no debe quedar ninguna tabla en `false`
-- ───────────────────────────────────────────────────────────
select c.relname as tabla, c.relrowsecurity as rls_activado
from pg_class c join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind = 'r'
order by c.relrowsecurity asc, c.relname;
