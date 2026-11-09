import os

with open('full_repo_dump.txt', 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk('.'):
        if any(x in root for x in ['.git', 'node_modules', '.venv', '.github']):
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

print('Dump script finished generating full_repo_dump.txt')
