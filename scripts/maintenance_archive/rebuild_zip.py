import zipfile
import os

pkg_dir = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3'
zip_filename = os.path.join(pkg_dir, 'PAQUETE_ENTREGA_APF3_GRUPO01_LEOFIT.zip')
temp_zip = os.path.join(pkg_dir, 'TEMP_PAQUETE.zip')

EXCLUDE_PATTERNS = ['_BACKUP', '_REORDERED', 'rendered.png', 'TEMP_', '.zip']

print(f"Re-packaging pristine ZIP: {zip_filename}...")
with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for item in sorted(os.listdir(pkg_dir)):
        if any(pat in item for pat in EXCLUDE_PATTERNS):
            continue
        item_path = os.path.join(pkg_dir, item)
        if os.path.isfile(item_path):
            zf.write(item_path, arcname=item)
            print(f"  Added: {item} ({os.path.getsize(item_path)} bytes)")

if os.path.exists(zip_filename):
    os.remove(zip_filename)
os.rename(temp_zip, zip_filename)
print(f"Pristine ZIP package updated successfully! Final size: {os.path.getsize(zip_filename)} bytes")
