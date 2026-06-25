from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

# 1. Carga la llave privada (debe estar en el mismo repo en Render)
# Cambia "nombre-de-tu-archivo-json.json" por el nombre real de tu archivo de Firebase
cred = credentials.Certificate("firebase-key.json")

# 2. Inicializa Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kkkkl-8ff43-default-rtdb.firebaseio.com/'
})

app = Flask(__name__)

# URL de tu Gist (la que obtuvimos antes)
URL_GIST = "https://gist.githubusercontent.com/xgxbopor-sys/0b963773b319413b40dcb345d87c3202/raw/ef0a34789b789d2e72915a7f77339272a0ddfff2/gistfile1.txt"

@app.route('/verificar', methods=['GET'])
def verificar():
    # El usuario envía su llave así: tu-url-de-render.com/verificar?key=XXXXX
    key_recibida = request.args.get('key')
    
    # Buscamos en la sección "Keys" de tu base de datos
    ref = db.reference('Keys')
    keys_en_db = ref.get()
    
    # Verificamos si la llave existe y si su valor es "activa"
    if keys_en_db and key_recibida in keys_en_db:
        if keys_en_db[key_recibida] == "activa":
            # Si la llave es válida, entregamos la URL del script
            return jsonify({
                "status": "success", 
                "script_url": URL_GIST
            })
        else:
            return jsonify({"status": "error", "message": "Key expirada o inactiva"})
    
    # Si no es válida o no existe
    return jsonify({"status": "error", "message": "Key invalida"})

if __name__ == '__main__':
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)
