import app.CONFIG as CONFIG
from app import app
from app.utils import utils


if __name__ == "__main__":

    # cargar los modelos 
    print("Cargando modelos ")
    utils.load_models()
    print("Modelos cargados satisfactoriamente...")
    
    # correr el server
    app.run(host='0.0.0.0', debug=True)
