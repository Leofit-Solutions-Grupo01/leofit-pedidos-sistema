import os
import shutil
import zipfile

pkg_dir = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3'
extra_dir = 'docs/fuentes_originales_y_backups'
os.makedirs(extra_dir, exist_ok=True)

# 1. Move non-accepted formats (.md) and redundant manuals/drafts to extra_dir
files_to_move = [
    'HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.md',
    'GUIA_Y_GUION_DE_GRABACION_VIDEO_RUBRICA.md',
    'GUIA_Y_GUION_DE_GRABACION_VIDEO_RUBRICA.docx',
    'GUIA_Y_GUION_DE_GRABACION_VIDEO_RUBRICA.pdf',
    '05_MANUAL_CALIDAD_ISO_25000_TECNICO.docx',
    '06_MANUAL_CALIDAD_ISO_25000_EJECUTIVO.docx',
    'GRUP01-Curso_Integrador_II_Software.pptx',
    'GRUP01-Curso_Integrador_II_Software.pdf',
    '03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pptx'
]

for f in files_to_move:
    p = os.path.join(pkg_dir, f)
    if os.path.exists(p):
        dst = os.path.join(extra_dir, f)
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(p, dst)
        print(f"Moved {f} -> {extra_dir}")

# 2. Rename 03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pdf to a clear name
old_pres_pdf = os.path.join(pkg_dir, '03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pdf')
new_pres_pdf = os.path.join(pkg_dir, '03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pdf')
if os.path.exists(old_pres_pdf):
    if os.path.exists(new_pres_pdf):
        os.remove(new_pres_pdf)
    shutil.move(old_pres_pdf, new_pres_pdf)
    print(f"Renamed {old_pres_pdf} -> {new_pres_pdf}")

# 3. Rename HOJA_DE_ENTREGA to 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE
for ext in ['.pdf', '.docx']:
    old_h = os.path.join(pkg_dir, f'HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE{ext}')
    new_h = os.path.join(pkg_dir, f'00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE{ext}')
    if os.path.exists(old_h):
        if os.path.exists(new_h):
            os.remove(new_h)
        shutil.move(old_h, new_h)
        print(f"Renamed {old_h} -> {new_h}")

# 4. Check current files in pkg_dir
print("\nFiles in official delivery folder:")
for item in sorted(os.listdir(pkg_dir)):
    if item.endswith('.zip'):
        continue
    p = os.path.join(pkg_dir, item)
    print(f"  {item} ({os.path.getsize(p)} bytes)")

# 5. Build clean, non-repetitive ZIP
zip_path = os.path.join(pkg_dir, 'PAQUETE_ENTREGA_APF3_GRUPO01_LEOFIT.zip')
temp_zip = os.path.join(pkg_dir, 'TEMP.zip')

with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
    for item in sorted(os.listdir(pkg_dir)):
        if item.endswith('.zip') or item.startswith('TEMP'):
            continue
        p = os.path.join(pkg_dir, item)
        if os.path.isfile(p):
            zf.write(p, arcname=item)
            print(f"  Zipped: {item}")
    # Also add the PPTX presentation inside the zip so teacher has editable slides if needed
    pptx_in_extra = os.path.join(extra_dir, 'GRUP01-Curso_Integrador_II_Software.pptx')
    if os.path.exists(pptx_in_extra):
        zf.write(pptx_in_extra, arcname='03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx')
        print("  Zipped editable PPTX: 03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx")

if os.path.exists(zip_path):
    os.remove(zip_path)
os.rename(temp_zip, zip_path)
print(f"\nFinal pristine ZIP size: {os.path.getsize(zip_path)} bytes")

