from flask import Flask, Blueprint, render_template, request, redirect, url_for
import openpyxl
import re

# Crear una aplicación Flask
app = Flask(__name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com|yahoo\.com|hotmail\.com)$')

# Crear un Blueprint para el perfil
profile_bp = Blueprint('profile', __name__)

def cargar_datos(username=None):
    # Cargar datos desde el archivo cuentas.xlsx
    wb = openpyxl.load_workbook('cuentas.xlsx')
    sheet = wb.active
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if username and username == row[0]:
            usuario = {
                'username': row[0],
                'password': row[1],
                'email': row[2],
                'phone': row[3]
            }
            return usuario
    return None

# Ruta para editar perfil
@app.route('/editar_perfil', methods=['POST'])
def editar_perfil():
    try:
        username = request.form.get('edit-username')
        email = request.form.get('edit-email')
        phone = request.form.get('edit-phone')

        # Validar dirección de correo electrónico
        if not EMAIL_REGEX.match(email):
            raise ValueError("Dirección de correo electrónico no válida")

        # Actualizar datos en el archivo Excel
        usuario = cargar_datos(username)
        if usuario:
            usuario['email'] = email
            usuario['phone'] = phone
            # Guardar cambios en el archivo Excel (debes implementar esto)

            # Mostrar mensaje de éxito
            return "Perfil actualizado correctamente"
        else:
            raise ValueError("Usuario no encontrado")
    except Exception as e:
        return str(e), 400  # Mostrar mensaje de error
if __name__ == '__main__':
    # Registrar el Blueprint para el perfil
    app.register_blueprint(profile_bp)
    app.run(debug=True)
