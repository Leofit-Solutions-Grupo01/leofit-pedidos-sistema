import os
import shutil

# --- 1. CLEAN AND ORGANIZE SCRIPTS DIRECTORY ---
scripts_dir = 'scripts'
gen_dir = os.path.join(scripts_dir, 'generators')
maint_dir = os.path.join(scripts_dir, 'maintenance_archive')

os.makedirs(gen_dir, exist_ok=True)
os.makedirs(maint_dir, exist_ok=True)

# Generators
generators = [
    'generate_05_erd_bd.py',
    'generate_15_rbac_flow.py',
    'generate_accessible_split_diagrams.py',
    'generate_apf2_complete_package.py',
    'generate_apf3_complete_package.py',
    'generate_apf3_figures.py',
    'generate_apf3_pptx.py',
    'generate_apf3_presentation.py',
    'generate_bpmn_tobe.py',
    'generate_c4_diagram.py',
    'generate_leofit_db_models_bw.py',
    'generate_risk_map.py',
    'generate_user_flow.py',
    'apf3_book_engine.py',
    'populate_iso25010_report.py',
    'enrich_iso25010_report.py'
]

for g in generators:
    src = os.path.join(scripts_dir, g)
    dst = os.path.join(gen_dir, g)
    if os.path.exists(src):
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(src, dst)
        print(f"Moved generator: {g} -> generators/")

# Maintenance & one-off fixes
maintenance = [
    'audit_all_slides_visuals.py',
    'beautify_presentation_styles.py',
    'cleanup_delivery_folder.py',
    'convert_apf3_subdocs.py',
    'convert_md_to_professional_docx.py',
    'deep_check_all_slides.py',
    'enforce_perfect_wcag_contrast.py',
    'enhance_all_titles_and_clarity.py',
    'find_and_remove_emojis.py',
    'fix_criterio4_superposiciones.py',
    'fix_criterio5_superposiciones.py',
    'fix_points_and_contrast_colors.py',
    'fix_slide24_table_and_s20_bullet.py',
    'fix_slide30_and_criterio5.py',
    'fix_slide6_bullets.py',
    'fix_visual_issues.py',
    'harmonize_iso_references.py',
    'inspect_presentation.py',
    'inspect_s12_details.py',
    'inspect_s20.py',
    'inspect_s24.py',
    'inspect_s26.py',
    'inspect_slide12.py',
    'inspect_slides_detail.py',
    'inspect_styles.py',
    'organize_utp_delivery.py',
    'apply_single_format_priority.py',
    'rebuild_zip.py',
    'remove_all_emojis.py',
    'reorder_and_update_presentation.py',
    'restore_indentation_and_clean_emojis.py',
    'sanitize_and_align_all_docs.py',
    'test_border.py',
    'test_imports.py',
    'update_slides_24_30.py'
]

for m in maintenance:
    src = os.path.join(scripts_dir, m)
    dst = os.path.join(maint_dir, m)
    if os.path.exists(src):
        if os.path.exists(dst):
            os.remove(dst)
        shutil.move(src, dst)
        print(f"Moved maintenance script: {m} -> maintenance_archive/")

# Delete rendered temporary images from scripts/
for f in os.listdir(scripts_dir):
    if f.endswith('_render.png'):
        p = os.path.join(scripts_dir, f)
        os.remove(p)
        print(f"Deleted temporary render: {f}")

# Delete __pycache__ if exists in scripts
pycache = os.path.join(scripts_dir, '__pycache__')
if os.path.exists(pycache):
    shutil.rmtree(pycache)
    print("Deleted __pycache__")

print("\nScripts directory cleaned and organized successfully.")
