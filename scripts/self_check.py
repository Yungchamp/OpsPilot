import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
errors = []

# Check Dockerfile
df = os.path.join(ROOT, 'Dockerfile')
if not os.path.exists(df):
    errors.append('Dockerfile missing')
else:
    with open(df) as f:
        txt = f.read()
    if 'FROM ubuntu:24.04' not in txt:
        errors.append('Dockerfile must use FROM ubuntu:24.04')
    if 'COPY . .' not in txt:
        errors.append('Dockerfile must use COPY . .')

# Check dockerignore
di = os.path.join(ROOT, '.dockerignore')
if not os.path.exists(di):
    errors.append('.dockerignore missing')
else:
    if '.git' in open(di).read():
        errors.append('.dockerignore must not exclude .git')

# Check for caches
for root, dirs, files in os.walk(ROOT):
    for d in dirs:
        if d in ('__pycache__', '.pytest_cache'):
            errors.append('Found cache dir: ' + os.path.join(root, d))
    for f in files:
        if f.endswith('.pyc'):
            errors.append('Found pyc file: ' + os.path.join(root, f))

# Check important dirs
for d in ('src', 'tests', 'data', 'docs', 'scripts'):
    if not os.path.exists(os.path.join(ROOT, d)):
        errors.append('Missing dir: ' + d)

if errors:
    print('SELF CHECK FAIL')
    for e in errors:
        print('- ' + e)
    sys.exit(2)

print('SELF CHECK OK')
