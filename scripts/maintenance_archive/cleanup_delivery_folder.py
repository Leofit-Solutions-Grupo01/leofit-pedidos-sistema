import os
import shutil

pkg_dir = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3'
backup_dir = 'docs/backup_slides'
os.makedirs(backup_dir, exist_ok=True)

# 1. Move backup pptx files out of the official delivery folder
for f in ['GRUP01-Curso_Integrador_II_Software_ORIGINAL_BACKUP.pptx', 'GRUP01-Curso_Integrador_II_Software_REORDERED.pptx']:
    src = os.path.join(pkg_dir, f)
    dst = os.path.join(backup_dir, f)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {f} to {backup_dir}")

# 2. Delete temporary rendered pngs
for f in ['slide_24_rendered.png', 'slide_30_rendered.png']:
    p = os.path.join(pkg_dir, f)
    if os.path.exists(p):
        os.remove(p)
        print(f"Removed temporary {f}")

# 3. Synchronize 03_PRESENTACION_SUSTENTACION with the official 43-slide presentation
# so that both naming conventions have the exact latest 43-slide presentation
src_pptx = os.path.join(pkg_dir, 'GRUP01-Curso_Integrador_II_Software.pptx')
src_pdf = os.path.join(pkg_dir, 'GRUP01-Curso_Integrador_II_Software.pdf')

dst_pptx = os.path.join(pkg_dir, '03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pptx')
dst_pdf = os.path.join(pkg_dir, '03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pdf')

if os.path.exists(src_pptx):
    shutil.copy2(src_pptx, dst_pptx)
    print("Updated 03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pptx to match GRUP01 presentation.")

if os.path.exists(src_pdf):
    shutil.copy2(src_pdf, dst_pdf)
    print("Updated 03_PRESENTACION_SUSTENTACION_APF3_LEOFIT.pdf to match GRUP01 presentation.")

print("\nCleanup completed.")

