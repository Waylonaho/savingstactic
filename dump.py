python3 -c "
import os

with open('full_repo_dump.txt', 'w') as out:
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root or '.venv' in root:
            continue
        for file in files:
            if file.endswith(('.html', '.py', '.xml', '.yml', '.md')):
                path = os.path.join(root, file)
                out.write(f'\n=== FILE: {path} ===\n')
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        out.write(f.read())
                except Exception as e:
                    out.write(f'Error reading file: {e}\n')
print('Dump complete! Created full_repo_dump.txt')
"
