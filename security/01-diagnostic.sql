-- ═══════════════════════════════════════════════════════════
-- CançoNet — PASO 1: DIAGNÓSTICO (solo lectura, no cambia nada)
-- Pégalo en Supabase → SQL Editor y ejecútalo entero.
-- Guarda el resultado: hace falta para decidir las políticas del paso 2.
-- ═══════════════════════════════════════════════════════════

-- 1. ¿Qué tablas tienen RLS desactivado? (las que salen aquí son las expuestas)
select
  c.relname                as tabla,
  c.relrowsecurity         as rls_activado,
  c.relforcerowsecurity    as rls_forzado,
  count(p.polname)         as num_politicas
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
left join pg_policy p on p.polrelid = c.oid
where n.nspname = 'public' and c.relkind = 'r'
group by c.relname, c.relrowsecurity, c.relforcerowsecurity
order by c.relrowsecurity asc, num_politicas desc;

-- 2. ¿Qué políticas existen ya y qué condición aplican?
--    Fíjate en si usan auth.uid(): si la app iba como anon, nunca se cumplían.
select
  tablename  as tabla,
  policyname as politica,
  roles,
  cmd        as operacion,
  qual       as condicion_lectura,
  with_check as condicion_escritura
from pg_policies
where schemaname = 'public'
order by tablename, cmd;

-- 3. Vistas SECURITY DEFINER (los 33 warnings del advisor).
--    Estas vistas se saltan el RLS de quien consulta.
select
  c.relname as vista,
  case when 'security_invoker=true' = any(c.reloptions)
       then 'invoker (correcto)' else 'DEFINER (se salta RLS)' end as modo
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind = 'v'
order by 2, 1;

-- 4. Columnas de las tablas que la app escribe. Necesario para escribir
--    las políticas: hay que saber si existe user_id, email, nick...
select table_name as tabla, column_name as columna, data_type as tipo
from information_schema.columns
where table_schema = 'public'
  and table_name in ('profiles','scores','challenges','salas','sala_members',
                     'sala_scores','bustia','song_reports','game_sessions',
                     'game_rounds','user_events','copa_inscripcions','copa_partits')
order by table_name, ordinal_position;

-- 5. Permisos concedidos al rol anónimo (lo que puede hacer alguien sin login)
select table_name as tabla, privilege_type as permiso
from information_schema.role_table_grants
where table_schema = 'public' and grantee = 'anon'
order by table_name, privilege_type;
