import csv
import os
import shutil
#Clear Cache and database
to_clear =["db.sqlite3","GroupAssignmentApp/__pycache__","GAP/__pycache__"]
for f in to_clear:
    if not os.path.exists(f):
        continue
    if os.path.isdir(f):
        shutil.rmtree(f)
    else:
        os.remove(f)
os.system('python manage.py makemigrations GroupAssignmentApp')
os.system('python manage.py makemigrations GroupAssignmentApp')
os.system('python manage.py migrate')
