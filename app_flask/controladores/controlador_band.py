from flask import render_template, request, redirect, session
from app_flask.modelos.modelo_band import Band
from app_flask import app

@app.route('/dashboard', methods=['GET'])
def desplegar_band():
    if "id_usuario" not in session:
        return redirect('/')
    lista_band = Band.obtener_todos()
    return render_template('dashboard.html', lista_band = lista_band)

@app.route('/perfil/band/<int:id>', methods=['GET'])
def mostrar_perfil(id):
    if "id_usuario" not in session:
        return redirect('/')
    datos = {
        "id" : id,
        "id_usuario": session['id_usuario']
    }
    mis_bands = Band.obtener_todos_con_usuario(datos)
    return render_template('account.html', mis_bands = mis_bands)

@app.route('/formulario/band', methods=['GET'])
def desplegar_formulario_band():
    if "id_usuario" not in session:
        return redirect('/')
    return render_template('formulario_band.html')

@app.route('/crear/band', methods=['POST'])
def crear_band():
    if Band.validar_band(request.form) == False:
        return redirect('/formulario/band')
    nuevo_band = {
        **request.form,
        "id_usuario": session['id_usuario']
    }
    Band.crear_uno(nuevo_band)
    return redirect('/dashboard')

@app.route('/eliminar/band/<int:id>', methods=['POST'])
def eliminar_band(id):
    band = {
        "id": id
    }
    Band.elimina_uno(band)
    return redirect('/dashboard')

@app.route('/formulario/editar/band/<int:id>', methods=['GET'])
def despliega_formulario_editar_band(id):
    if "id_usuario" not in session:
        return redirect('/')
    datos = {
        "id" : id
    }
    band = Band.obtener_uno(datos)
    return render_template('formulario_editar_band.html', band = band)

@app.route('/editar/band/<int:id>', methods=['POST'])
def editar_band(id):
    if Band.validar_band(request.form) == False:
        return redirect(f'/formulario/editar/band/{id}')
    editar_band = {
        **request.form,
        "id" : id,
        "id_usuario" : session['id_usuario']
    }
    Band.actualizar_uno(editar_band)
    return redirect('/dashboard')
