import os
import re
import sys
from pathlib import Path

VERSIONS_DIR = Path(__file__).parent / 'migrations' / 'versions'

def slugify(text):
    text = text.lower().replace(' ', '_')
    text = re.sub(r'[^a-z0-9_]+', '', text)
    return text[:30]

def get_next_number():
    files = [f for f in os.listdir(VERSIONS_DIR) if f.endswith('.py')]
    nums = []
    for f in files:
        m = re.match(r'^(\d{4})-', f)
        if m:
            nums.append(int(m.group(1)))
    return f'{(max(nums) + 1) if nums else 1:04d}'

def get_latest_file():
    files = [f for f in os.listdir(VERSIONS_DIR) if f.endswith('.py')]
    if not files:
        print('Nenhum arquivo de migração encontrado.')
        sys.exit(1)
    files = sorted(files, key=lambda f: os.path.getmtime(VERSIONS_DIR / f), reverse=True)
    return files[0]

def main():
    if len(sys.argv) < 2:
        print('Uso: python rename_migration.py "descrição da migração"')
        sys.exit(1)
    desc = slugify(sys.argv[1])
    next_num = get_next_number()
    latest = get_latest_file()
    new_name = f'{next_num}-{desc}.py'
    src = VERSIONS_DIR / latest
    dst = VERSIONS_DIR / new_name
    os.rename(src, dst)
    print(f'Renomeado: {latest} -> {new_name}')

if __name__ == '__main__':
    main()
