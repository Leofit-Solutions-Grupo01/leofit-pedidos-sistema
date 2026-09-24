#!/usr/bin/env bash
# =============================================================================
# SCRIPT DE INSTALACIÓN Y CONFIGURACIÓN DE PGBOUNCER
# SISTEMA DE GESTIÓN DE PEDIDOS - LEOFIT SOLUTIONS
# =============================================================================
# USO     : sudo ./setup_pgbouncer.sh
# =============================================================================

set -euo pipefail

GREEN='\033[0;32m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'
log()     { echo -e "[$(date '+%H:%M:%S')] ${CYAN}INFO${NC}  $*"; }
success() { echo -e "[$(date '+%H:%M:%S')] ${GREEN}OK${NC}    $*"; }
error()   { echo -e "[$(date '+%H:%M:%S')] ${RED}ERROR${NC} $*" >&2; exit 1; }

# ── 1. Instalar PgBouncer ─────────────────────────────────────────────────────
log "Instalando PgBouncer..."
apt-get update -qq
apt-get install -y pgbouncer
success "PgBouncer instalado: $(pgbouncer --version)"

# ── 2. Crear roles en PostgreSQL ──────────────────────────────────────────────
log "Creando roles en PostgreSQL..."
psql -U postgres -d leofit_db << 'SQL'
-- Usuario de aplicación (permisos mínimos)
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='leofit_app') THEN
    CREATE ROLE leofit_app WITH LOGIN ENCRYPTED PASSWORD 'AppSecure2026!';
  END IF;
END $$;
GRANT CONNECT ON DATABASE leofit_db TO leofit_app;
GRANT USAGE ON SCHEMA public TO leofit_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO leofit_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO leofit_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO leofit_app;

-- Usuario de solo lectura (replica / reportes)
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='leofit_readonly') THEN
    CREATE ROLE leofit_readonly WITH LOGIN ENCRYPTED PASSWORD 'ReadOnly2026!';
  END IF;
END $$;
GRANT CONNECT ON DATABASE leofit_db TO leofit_readonly;
GRANT USAGE ON SCHEMA public TO leofit_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO leofit_readonly;

-- Usuario de autenticación PgBouncer (accede a pg_shadow)
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='pgbouncer_auth') THEN
    CREATE ROLE pgbouncer_auth WITH LOGIN ENCRYPTED PASSWORD 'BncAuth2026!';
  END IF;
END $$;

-- Función de autenticación segura (evita exponer pg_shadow directamente)
CREATE OR REPLACE FUNCTION pgbouncer.get_auth(p_usename TEXT)
RETURNS TABLE(usename TEXT, passwd TEXT) LANGUAGE SQL SECURITY DEFINER AS $$
  SELECT usename::TEXT, passwd::TEXT
  FROM pg_catalog.pg_shadow
  WHERE usename = p_usename;
$$;
GRANT EXECUTE ON FUNCTION pgbouncer.get_auth(TEXT) TO pgbouncer_auth;

-- Usuario de monitoreo
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='monitoring_user') THEN
    CREATE ROLE monitoring_user WITH LOGIN ENCRYPTED PASSWORD 'Monitor2026!';
  END IF;
END $$;
SQL
success "Roles creados en PostgreSQL."

# ── 3. Generar userlist.txt desde pg_shadow ───────────────────────────────────
log "Generando /etc/pgbouncer/userlist.txt desde pg_shadow..."
psql -U postgres -d leofit_db -tA \
  -c "SELECT '\"' || usename || '\" \"' || passwd || '\"'
      FROM pg_shadow
      WHERE usename IN ('leofit_app','leofit_readonly','pgbouncer_auth','pgbouncer','monitoring_user')" \
  > /etc/pgbouncer/userlist.txt
chmod 600 /etc/pgbouncer/userlist.txt
chown pgbouncer:pgbouncer /etc/pgbouncer/userlist.txt
success "userlist.txt generado con hashes reales."

# ── 4. Copiar configuración ───────────────────────────────────────────────────
log "Instalando pgbouncer.ini..."
cp "$(dirname "$0")/pgbouncer.ini" /etc/pgbouncer/pgbouncer.ini
chmod 640 /etc/pgbouncer/pgbouncer.ini
chown pgbouncer:pgbouncer /etc/pgbouncer/pgbouncer.ini
success "pgbouncer.ini instalado."

# ── 5. Crear directorios de log y pid ────────────────────────────────────────
mkdir -p /var/log/pgbouncer /var/run/pgbouncer
chown pgbouncer:pgbouncer /var/log/pgbouncer /var/run/pgbouncer
success "Directorios de log y pid creados."

# ── 6. Habilitar y arrancar el servicio ──────────────────────────────────────
log "Habilitando servicio PgBouncer..."
systemctl enable pgbouncer
systemctl restart pgbouncer
sleep 2
systemctl is-active --quiet pgbouncer && success "PgBouncer activo y escuchando en :6432" \
    || error "PgBouncer no pudo iniciar — revisar: journalctl -u pgbouncer -n 30"

# ── 7. Test de conexión a través de PgBouncer ─────────────────────────────────
log "Verificando conexión a través de PgBouncer..."
if psql -h 127.0.0.1 -p 6432 -U leofit_app -d leofit_db \
       -c "SELECT current_database(), current_user, version();" &>/dev/null; then
    success "✅ Conexión exitosa a leofit_db a través de PgBouncer :6432"
else
    error "No se pudo conectar. Verificar userlist.txt y pgbouncer.ini."
fi

# ── 8. Mostrar estadísticas de la consola PgBouncer ──────────────────────────
log "Estado de los pools:"
psql -h 127.0.0.1 -p 6432 -U pgbouncer pgbouncer \
     -c "SHOW POOLS;" 2>/dev/null || true

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ PgBouncer configurado correctamente para LEOFIT"
echo ""
echo "  Puerto cliente  : 127.0.0.1:6432"
echo "  Puerto PG real  : 127.0.0.1:5432"
echo "  Modo pooling    : transaction"
echo "  Consola admin   : psql -h 127.0.0.1 -p 6432 -U pgbouncer pgbouncer"
echo "  Comandos útiles : SHOW POOLS; SHOW STATS; SHOW CLIENTS; SHOW SERVERS;"
echo "═══════════════════════════════════════════════════════════"