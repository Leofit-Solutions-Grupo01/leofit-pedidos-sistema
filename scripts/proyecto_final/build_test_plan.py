# -*- coding: utf-8 -*-
"""
@file build_test_plan.py
@description Wrapper de conveniencia para invocar scripts/build_infographic_test_plan.py
             y compilar el Plan de Pruebas ISO/IEC/IEEE 29119-3/4 en DOCX, PDF (3 págs A4) y HTML.
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
TARGET_SCRIPT = os.path.join(BASE_DIR, "scripts", "build_infographic_test_plan.py")

if __name__ == "__main__":
    ret = subprocess.call([sys.executable, TARGET_SCRIPT])
    sys.exit(ret)

