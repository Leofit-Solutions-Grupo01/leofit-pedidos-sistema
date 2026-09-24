#!/usr/bin/env bash
# =============================================================================
# ESTRATEGIA DE RESPALDO AUTOMATIZADO Y RECUPERACIÓN ANTE DESASTRES (PITR)
# SISTEMA DE GESTIÓN DE PEDIDOS - LEOFIT SOLUTIONS
# Firmas de integridad SHA-256 | Política de retención | Alertas por correo
# =============================================================================
# VERSION : 2.0.0
# USO     : ./backup_strategy.sh [full|incremental|verify|restore <archivo>]
# CRON    : 0 2 * * * /opt/leofit/database/backup_strategy.sh full >> /var/log/leofit_backup.log 2>&1
# =============================================================================

set -euo pipefail
IFS=$'\n\t'

# =============================================================================
# CONFIGURACIÓN — Ajustar para cada entorno
# =============================================================================
readonly DB_HOST="${DB_HOST:-localhost}"
readonly DB_PORT="${DB_PORT:-5432}"
readonly DB_NAME="${DB_NAME:-leofit_db}"
readonly DB_USER="${DB_USER:-postgres}"
readonly BACKUP_BASE="/var/backups/leofit_db"
readonly BACKUP_DAILY="${BACKUP_BASE}/daily"
readonly BACKUP_WAL="${BACKUP_BASE}/wal_archives"
readonly LOG_FILE="/var/log/leofit_backup.log"
readonly RETENTION_DAYS=30
readonly ALERT_EMAIL="${ALERT_EMAIL:-admin@leofit.pe}"
readonly DATE=$(date +"%Y%m%d_%H%M%S")
readonly HOSTNAME=$(hostname -s)

# Colores para output (sólo si el terminal lo soporta)
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
[[ ! -t 1 ]] && RED='' && GREEN='' && YELLOW='' && CYAN='' && NC=''

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================
log()     { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${CYAN}INFO${NC}  $*" | tee -a "$LOG_FILE"; }
success() { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${GREEN}OK${NC}    $*" | tee -a "$LOG_FILE"; }
warn()    { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${YELLOW}WARN${NC}  $*" | tee -a "$LOG_FILE"; }
error()   { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${RED}ERROR${NC} $*" | tee -a "$LOG_FILE" >&2; }

send_alert() {
    local subject="$1" body="$2"
    if command -v mail &>/dev/null && [[ -n "$ALERT_EMAIL" ]]; then
        echo "$body" | mail -s "[LEOFIT-DB] $subject" "$ALERT_EMAIL" || true
    fi
}

ensure_dirs() {
    mkdir -p "$BACKUP_DAILY" "$BACKUP_WAL"
    chmod 700 "$BACKUP_BASE"
}

# =============================================================================
# FUNCIÓN: Generar firma SHA-256 y verificarla
# =============================================================================
generate_checksum() {
    local file="$1"
    local checksum_file="${file}.sha256"
    sha256sum "$file" > "$checksum_file"
    success "SHA-256 generado → $(cat "$checksum_file" | awk '{print $1}')"
    echo "$checksum_file"
}

verify_checksum() {
    local file="$1"
    local checksum_file="${file}.sha256"
    if [[ ! -f "$checksum_file" ]]; then
        error "Archivo de firma no encontrado: $checksum_file"
        return 1
    fi
    if sha256sum --check "$checksum_file" --status; then
        success "✅ Integridad verificada — SHA-256 válido: $file"
        return 0
    else
        error "❌ FALLO DE INTEGRIDAD — El archivo puede estar corrupto: $file"
        send_alert "ALERTA: Corrupción detectada" \
            "Servidor: $HOSTNAME\nArchivo: $file\nFecha: $(date)\nAcción: Verificar backup inmediatamente."
        return 1
    fi
}

# =============================================================================
# FUNCIÓN: Backup completo lógico (pg_dump formato custom)
# =============================================================================
cmd_full() {
    local backup_file="${BACKUP_DAILY}/leofit_full_${DATE}.dump"

    log "═══════════════════════════════════════════════════════"
    log "  Iniciando Backup COMPLETO — Base: ${DB_NAME}"
    log "  Servidor  : ${DB_HOST}:${DB_PORT}"
    log "  Destino   : ${backup_file}"
    log "═══════════════════════════════════════════════════════"

    # Verificar conectividad a la BD
    if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -q; then
        error "No se puede conectar a PostgreSQL en ${DB_HOST}:${DB_PORT}"
        send_alert "ERROR: PostgreSQL no disponible" \
            "Servidor: $HOSTNAME\nHora: $(date)\nNo se pudo iniciar el backup."
        exit 1
    fi

    # Ejecutar pg_dump en formato custom (compresión nativa, paralelizable)
    pg_dump \
        -h "$DB_HOST" \
        -p "$DB_PORT" \
        -U "$DB_USER" \
        --format=custom \
        --compress=9 \
        --blobs \
        --verbose \
        --file="$backup_file" \
        "$DB_NAME" 2>> "$LOG_FILE"

    local size
    size=$(du -sh "$backup_file" | cut -f1)
    success "Backup completado — Tamaño: ${size} — Archivo: ${backup_file}"

    # Generar y registrar firma SHA-256
    generate_checksum "$backup_file"

    # Exportar esquema separado (legible / auditable)
    local schema_file="${BACKUP_DAILY}/leofit_schema_${DATE}.sql"
    pg_dump \
        -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
        --schema-only --no-owner \
        --file="$schema_file" \
        "$DB_NAME" 2>> "$LOG_FILE"
    generate_checksum "$schema_file"
    success "Schema exportado → ${schema_file}"

    # Política de retención
    cmd_purge

    log "═══════════════════════════════════════════════════════"
    success "🎉 Backup completo finalizado satisfactoriamente."
    log "═══════════════════════════════════════════════════════"

    send_alert "Backup exitoso — ${DATE}" \
        "Servidor: $HOSTNAME\nBase: $DB_NAME\nArchivo: $backup_file\nTamaño: $size\nFecha: $(date)"
}

# =============================================================================
# FUNCIÓN: Backup incremental WAL (archivado de segmentos WAL)
# =============================================================================
cmd_incremental() {
    log "Iniciando archivado incremental de segmentos WAL..."

    # Forzar un nuevo segmento WAL para capturar transacciones recientes
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
         -c "SELECT pg_switch_wal();" >> "$LOG_FILE" 2>&1

    local wal_source="/var/lib/postgresql/16/main/pg_wal"
    if [[ -d "$wal_source" ]]; then
        local count=0
        for wal_file in "${wal_source}"/[0-9A-F]{24}; do
            [[ -f "$wal_file" ]] || continue
            local dest="${BACKUP_WAL}/$(basename "$wal_file")"
            if [[ ! -f "$dest" ]]; then
                cp "$wal_file" "$dest"
                generate_checksum "$dest" > /dev/null
                ((count++))
            fi
        done
        success "Archivados ${count} segmentos WAL → ${BACKUP_WAL}"
    else
        warn "Directorio pg_wal no accesible en este entorno. Configurar archive_command en postgresql.conf."
    fi
}

# =============================================================================
# FUNCIÓN: Verificar integridad de todos los backups existentes
# =============================================================================
cmd_verify() {
    log "Verificando integridad SHA-256 de todos los backups..."
    local ok=0 fail=0

    while IFS= read -r -d '' sha_file; do
        local original="${sha_file%.sha256}"
        if [[ -f "$original" ]]; then
            if sha256sum --check "$sha_file" --status 2>/dev/null; then
                success "✅ OK — $(basename "$original")"
                ((ok++))
            else
                error "❌ CORRUPTO — $(basename "$original")"
                ((fail++))
            fi
        else
            warn "Archivo original no encontrado: $original"
            ((fail++))
        fi
    done < <(find "$BACKUP_DAILY" -name "*.sha256" -print0)

    log "Verificación completa — OK: ${ok} | Fallidos: ${fail}"
    if (( fail > 0 )); then
        send_alert "ALERTA: ${fail} backup(s) corruptos" \
            "Servidor: $HOSTNAME\nFecha: $(date)\nVerificar directorio: $BACKUP_DAILY"
        exit 1
    fi
}

# =============================================================================
# FUNCIÓN: Restaurar desde un backup específico
# =============================================================================
cmd_restore() {
    local backup_file="${1:-}"
    if [[ -z "$backup_file" ]]; then
        error "Uso: $0 restore <ruta_al_archivo.dump>"
        exit 1
    fi
    if [[ ! -f "$backup_file" ]]; then
        error "Archivo no encontrado: $backup_file"
        exit 1
    fi

    log "Verificando integridad antes de restaurar..."
    verify_checksum "$backup_file"

    warn "⚠️  RESTAURACIÓN — Esto sobreescribirá la BD '${DB_NAME}'"
    warn "    Archivo: ${backup_file}"
    read -r -p "    ¿Confirmar restauración? [si/NO]: " confirm
    [[ "$confirm" != "si" ]] && { log "Restauración cancelada."; exit 0; }

    log "Iniciando restauración..."
    pg_restore \
        -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
        --dbname="$DB_NAME" \
        --verbose \
        --clean \
        --if-exists \
        "$backup_file" 2>> "$LOG_FILE"

    success "✅ Restauración completada desde: ${backup_file}"
}

# =============================================================================
# FUNCIÓN: Purga de respaldos antiguos (retención)
# =============================================================================
cmd_purge() {
    log "Aplicando política de retención: ${RETENTION_DAYS} días..."
    local purged=0
    while IFS= read -r -d '' old_file; do
        rm -f "$old_file" "${old_file}.sha256"
        ((purged++))
        warn "Eliminado por antigüedad: $(basename "$old_file")"
    done < <(find "$BACKUP_DAILY" -name "*.dump" -mtime "+${RETENTION_DAYS}" -print0)
    log "Purga completada — ${purged} archivo(s) eliminados."
}

# =============================================================================
# FUNCIÓN: Reporte de estado de backups
# =============================================================================
cmd_status() {
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo "  LEOFIT — Estado de Backups"
    echo "═══════════════════════════════════════════════════════"
    echo "  Directorio  : $BACKUP_DAILY"
    echo "  Retención   : $RETENTION_DAYS días"
    echo ""
    echo "  Últimos 5 backups:"
    ls -lht "$BACKUP_DAILY"/*.dump 2>/dev/null | head -5 || echo "  (sin backups)"
    echo ""
    local total
    total=$(du -sh "$BACKUP_BASE" 2>/dev/null | cut -f1 || echo "N/A")
    echo "  Espacio total usado: $total"
    echo "═══════════════════════════════════════════════════════"
}

# =============================================================================
# MAIN — Dispatcher de comandos
# =============================================================================
ensure_dirs

CMD="${1:-full}"
case "$CMD" in
    full)        cmd_full ;;
    incremental) cmd_incremental ;;
    verify)      cmd_verify ;;
    restore)     cmd_restore "${2:-}" ;;
    purge)       cmd_purge ;;
    status)      cmd_status ;;
    *)
        echo "Uso: $0 [full|incremental|verify|restore <archivo>|purge|status]"
        echo ""
        echo "  full          Backup completo lógico con firma SHA-256"
        echo "  incremental   Archivar segmentos WAL del período"
        echo "  verify        Verificar integridad SHA-256 de todos los backups"
        echo "  restore FILE  Restaurar desde un archivo .dump"
        echo "  purge         Eliminar backups con más de ${RETENTION_DAYS} días"
        echo "  status        Ver listado y espacio de backups"
        exit 1
        ;;
esac