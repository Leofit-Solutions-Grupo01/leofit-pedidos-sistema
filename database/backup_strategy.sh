#!/bin/bash
# =============================================================================
# ESTRATEGIA DE BACKUP AUTOMATIZADO Y RECUPERACIÓN ANTE DESASTRES (PITR)
# SISTEMA DE GESTIÓN DE PEDIDOS LEOFIT SOLUTIONS
# =============================================================================

set -e

# Configuración de variables
BACKUP_DIR="/var/backups/leofit_db"
DATE=$(date +"%Y%m%d_%H%M%S")
DB_NAME="leofit_db"
DB_USER="postgres"
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR/daily"
mkdir -p "$BACKUP_DIR/wal_archives"

echo "=========================================================="
echo "🕒 [$(date)] Iniciando Backup Completo de Base de Datos..."
echo "=========================================================="

# 1. Volcado Lógico Completo con compresión gzip y formato custom (pg_dump)
BACKUP_FILE="$BACKUP_DIR/daily/leofit_backup_${DATE}.dump"
pg_dump -h localhost -U "$DB_USER" -F c -b -v -f "$BACKUP_FILE" "$DB_NAME"

# Generar checksum SHA-256 para validación de integridad
sha256sum "$BACKUP_FILE" > "${BACKUP_FILE}.sha256"

echo "✅ Backup completado exitosamente: $BACKUP_FILE"
echo "🔒 Checksum SHA-256 generado."

# 2. Política de Retención: Eliminar respaldos más antiguos a 30 días
echo "🧹 Purgando respaldos con más de ${RETENTION_DAYS} días de antigüedad..."
find "$BACKUP_DIR/daily" -type f -mtime +$RETENTION_DAYS -exec rm -f {} \;

# 3. Procedimiento de Restauración Rápida (Disaster Recovery):
# pg_restore -h localhost -U postgres -d leofit_db -v "$BACKUP_FILE"

echo "=========================================================="
echo "🎉 Rutina de Respaldo Finalizada Satisfactoriamente."
echo "=========================================================="
