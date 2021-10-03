from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
app.config['JWT_SECRET_KEY']='clave-jwt'
app_context = app.app_context()
app_context.push()


cors = CORS(app)
jwt = JWTManager(app)
	
@app.route('/registro-historia', methods = ['POST'])
@jwt_required()
def post(self):
    
    response = requests.post("http://127.0.0.1:5002/historia", json = request.json, headers = request.headers)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return json.loads(response.text),response.status_code
		
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')