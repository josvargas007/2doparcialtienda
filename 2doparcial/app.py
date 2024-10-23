from flask import Flask, render_template, request, session, redirect, url_for
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Ruta para mostrar todos los productos
@app.route('/')
def index():
    if 'productos' not in session:
        session['productos'] = []
    return render_template('index.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET','POST'])
def agregar_producto():
    if request.method == 'POST':
        producto = {
            'id': str(uuid.uuid4().int),
            'nombre': request.form["nombre"],
            'cantidad': int(request.form["cantidad"]),
            'precio': float(request.form["precio"]),
            'fecha_vencimiento': request.form["fecha_vencimiento"],
            'categoria': request.form["categoria"]
        }
        
        if 'productos' in session and producto:
            session['productos'].append(producto)
            session.modified = True
            return redirect(url_for("index"))
        else:
            # Puedes agregar un mensaje de error o redireccionar a otra página
            return "No se pudo agregar el producto"
    else:
        return render_template('agregar.html')


# Ruta para eliminar un producto
@app.route('/eliminar/<id>')
def eliminar_producto(id):
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    return redirect(url_for('index'))

# Ruta para actualizar un producto
@app.route('/actualizar/<id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    producto = next((p for p in session['productos'] if p['id'] == id), None)
    if producto is None:
        return "Producto no encontrado", 404
    
    if request.method == 'POST':
        try:
            producto['nombre'] = request.form.get('nombre')
            producto['cantidad'] = int(request.form.get('cantidad'))
            producto['precio'] = float(request.form.get('precio'))
            producto['fecha_vencimiento'] = datetime.strptime(request.form.get('fecha_vencimiento'), '%Y-%m-%d').date()
            producto['categoria'] = request.form.get('categoria')
            session.modified = True
            return redirect(url_for('index'))
        except ValueError:
            return "Error al convertir valores numéricos", 400
    return render_template('actualizar.html', producto=producto)



# Ruta para mostrar el formulario de agregar producto
@app.route('/agregar_form')
def agregar_form():
    return render_template('agregar.html')

# Ruta para mostrar el formulario de actualizar producto
@app.route('/actualizar_form/<id>',methods=['POST'])
def actualizar_form(id):
    producto = next((p for p in session['productos'] if p['id'] == id), None)
    return render_template('actualizar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
