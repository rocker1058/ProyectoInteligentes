from flask import Flask
import app.CONFIG as CONFIG
import os


# crear los paths
if not os.path.exists(CONFIG.TEMP_FILES_PATH):
    os.makedirs(CONFIG.TEMP_FILES_PATH)


app = Flask(__name__)
app.secret_key = "hhfsdfhs00390dsafjsdafkh30940"
app.config['JSON_SORT_KEYS'] = False
# cors = CORS(app, resourcs={r"/*": {"origins": "*"}})

from app import views
