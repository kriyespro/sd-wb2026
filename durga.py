#!/usr/bin/env python3
"""Dev server runner with cache clear."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def clear_cache():
    for pattern in ['__pycache__', '*.pyc', '.pytest_cache']:
        for path in BASE_DIR.rglob(pattern):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file():
                path.unlink(missing_ok=True)
    print('Cache cleared.')


def main():
    os.chdir(BASE_DIR)
    clear_cache()

    venv_python = BASE_DIR / 'venv' / 'bin' / 'python'
    python = str(venv_python) if venv_python.exists() else sys.executable

    if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
        subprocess.run([python, 'manage.py', 'migrate'], check=False)
        return

    if len(sys.argv) > 1 and sys.argv[1] == 'createsuperuser':
        subprocess.run([python, 'manage.py', 'createsuperuser'], check=False)
        return

    port = '8000'
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = sys.argv[1]

    print(f'Starting server at http://127.0.0.1:{port}')
    print(f'Admin at http://127.0.0.1:{port}/sd/')
    subprocess.run([python, 'manage.py', 'runserver', port], check=False)


if __name__ == '__main__':
    main()
