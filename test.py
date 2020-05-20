import os
APP_PATH = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_PATH = os.path.join(APP_PATH, 'templates')
TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, 'usuarios.html')

print(APP_PATH)

print(TEMPLATE_PATH)
