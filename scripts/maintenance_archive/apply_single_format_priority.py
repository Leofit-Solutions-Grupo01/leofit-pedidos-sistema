import os
import shutil
import zipfile

pkg_dir = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3'
pdf_backup_dir = 'docs/fuentes_originales_y_backups/versiones_pdf'
extra_dir = 'docs/fuentes_originales_y_backups'
os.makedirs(pdf_backup_dir, exist_ok=True)

# 1. Bring back the clean 43-slide PPTX from extra_dir to pkg_dir as 03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx
src_pptx = os.path.join(extra_dir, 'GRUP01-Curso_Integrador_II_Software.pptx')
dst_pptx = os.path.join(pkg_dir, '03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx')
if os.path.exists(src_pptx):
    shutil.copy2(src_pptx, dst_pptx)
    print(f"Brought PPTX: {dst_pptx} ({os.path.getsize(dst_pptx)} bytes)")

# 2. Move all duplicate .pdf files from pkg_dir to pdf_backup_dir according to doc > ppt > pdf
pdfs_to_move = [
    '00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.pdf',
    '01_INFORME_FINAL_APF3_LEOFIT.pdf',
    '02_INFORME_ISO25010_SEMANAS_10_11_LEOFIT.pdf',
    '03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pdf'
]

for pdf in pdfs_to_move:
    src = os.path.join(pkg_dir, pdf)
    dst = os.path.join(pdf_backup_dir, pdf)
    if os.path.exists(src):
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(src, dst)
        print(f"Moved duplicate PDF {pdf} -> {pdf_backup_dir}")

# 3. Check what remains in pkg_dir (should be 5 distinct files: 3 docx, 1 pptx, 1 xlsx)
print("\nUnique files in delivery folder:")
current_files = []
for item in sorted(os.listdir(pkg_dir)):
    if item.endswith('.zip') or item.startswith('TEMP'):
        continue
    p = os.path.join(pkg_dir, item)
    print(f"  {item} ({os.path.getsize(p)} bytes)")
    current_files.append(item)

# 4. Rebuild the official ZIP package with ONLY these 5 non-duplicated files
zip_path = os.path.join(pkg_dir, 'PAQUETE_ENTREGA_APF3_GRUPO01_LEOFIT.zip')
temp_zip = os.path.join(pkg_dir, 'TEMP.zip')

print(f"\nBuilding consolidated ZIP: {zip_path}...")
with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for item in current_files:
        p = os.path.join(pkg_dir, item)
        zf.write(p, arcname=item)
        print(f"  Zipped: {item}")

if os.path.exists(zip_path):
    os.remove(zip_path)
os.rename(temp_zip, zip_path)
print(f"Final clean ZIP size: {os.path.getsize(zip_path)} bytes")

