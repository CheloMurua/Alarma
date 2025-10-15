import sys
import os

# ------------------------------
# 1. Activar tu virtualenv
# ------------------------------
activate_this = '/home/mchelom/.virtualenvs/mi_flask_env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# ------------------------------
# 2. Añadir el directorio de tu proyecto al sys.path
# ------------------------------
project_home = '/home/mchelom/mi_flask_app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ------------------------------
# 3. Variable de entorno Flask
# ------------------------------
os.environ['FLASK_ENV'] = 'production'

# ------------------------------
# 4. Importar la app como "application"
# ------------------------------
from app_flask import app as application

