import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT_DIR = Path(".").resolve()
DOCS_DIR = ROOT_DIR / "docs"

LINK_REGEX = re.compile(r'!?\[([^\]]*)\]\(([^)]+)\)')

def should_skip(path: Path) -> bool:
    for part in path.parts:
        if part.startswith(".") and part != ".":
            return True
        if part in ("node_modules", "dist", "build", "coverage", ".venv", "venv"):
            return True
    return False

def validate_links():
    md_files = [p for p in DOCS_DIR.rglob("*.md") if not should_skip(p)]
    root_md = [p for p in ROOT_DIR.glob("*.md") if not should_skip(p)]
    all_files = md_files + root_md
    
    total_links = 0
    broken_links = []
    
    for file_path in all_files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
            
        lines = content.splitlines()
        for line_num, line in enumerate(lines, 1):
            matches = LINK_REGEX.findall(line)
            for text, url in matches:
                url = url.strip()
                # Split off anchor if present
                if "#" in url:
                    target_file, anchor = url.split("#", 1)
                else:
                    target_file, anchor = url, ""
                
                # Ignore web URLs, mailto, empty targets (anchors only)
                if not target_file:
                    continue
                if target_file.startswith(("http://", "https://", "mailto:", "javascript:")):
                    continue
                if target_file.startswith("data:"):
                    continue
                    
                total_links += 1
                clean_target = unquote(target_file)
                
                # Resolve relative path
                if clean_target.startswith("/"):
                    resolved = (ROOT_DIR / clean_target.lstrip("/")).resolve()
                else:
                    resolved = (file_path.parent / clean_target).resolve()
                    
                if not resolved.exists():
                    broken_links.append((str(file_path.relative_to(ROOT_DIR)), line_num, text, url, str(resolved)))

    print(f"Total relative links checked: {total_links}")
    if broken_links:
        print(f"Found {len(broken_links)} broken relative links:")
        for source, line, text, url, resolved in broken_links:
            print(f"  {source}:{line} -> '{url}'")
        return len(broken_links)
    else:
        print("[OK] All relative links resolve successfully. 0 broken links!")
        return 0

if __name__ == "__main__":
    sys.exit(validate_links())
