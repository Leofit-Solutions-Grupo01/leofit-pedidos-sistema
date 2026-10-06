# -*- coding: utf-8 -*-
import os
import re

directory = 'frontend/src'

def replace_classes(content):
    content = re.sub(r'bg-slate-50', r'bg-slate-950', content)
    content = content.replace('min-h-screen bg-[#0F223D]', 'min-h-screen bg-slate-950')
    content = re.sub(r'(?<!/)bg-white', r'bg-slate-900', content)
    
    content = re.sub(r'text-slate-9[05]0', r'text-white', content)
    content = re.sub(r'text-slate-[78]00', r'text-slate-100', content)
    content = re.sub(r'text-slate-[45]00', r'text-slate-300', content)
    
    content = re.sub(r'border-slate-[23]00', r'border-slate-700', content)
    
    content = re.sub(r'bg-\[\#0F223D\]', r'bg-cyan-500', content)
    content = re.sub(r'bg-\[\#E63946\]', r'bg-cyan-500', content)
    
    content = re.sub(r'amber-[45]00', r'orange-500', content)
    
    content = re.sub(r'emerald-600', r'lime-500', content)
    
    content = re.sub(r'bg-red-100', r'bg-red-950/50', content)
    content = re.sub(r'border-red-300', r'border-red-900', content)
    content = re.sub(r'text-red-700', r'text-red-400', content)
    content = re.sub(r'text-red-950', r'text-red-200', content)

    content = content.replace('bg-cyan-500 text-white', 'bg-cyan-500 text-slate-950')
    content = content.replace('bg-cyan-500 hover:bg-[#1E293B] text-white', 'bg-cyan-500 hover:bg-cyan-400 text-slate-950')
    content = content.replace('bg-cyan-500 hover:bg-[#C62828] active:scale-[0.98] text-white', 'bg-cyan-500 hover:bg-cyan-400 active:scale-[0.98] text-slate-950')
    
    return content

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            new_content = replace_classes(original_content)
            
            if original_content != new_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated {path}')
