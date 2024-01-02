import os, glob, yaml
from datetime import datetime
from flask import Flask, request, make_response, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from lib.queue import MQ
from lib.database import Database


with open("configuration.yaml", "r") as file:
    configuration = yaml.load(file, Loader=yaml.FullLoader)
    print(configuration)
    
app = Flask(__name__)

app.config['HOST'] = configuration.get('API_HOST')
app.config['PORT'] = configuration.get('API_PORT')

app.config['UPLOAD_FOLDER'] = configuration.get('FOLDER').get('UPLOAD')
app.config['TMP_FOLDER'] = configuration.get('FOLDER').get('TMP')
app.config['CONVERTED_FOLDER'] = configuration.get('FOLDER').get('CONVERTED')

app.config['RABBITMQ_URL'] = configuration.get('RABBITMQ_URL')
app.config['RABBITMQ_UPLOAD_QUEUE'] = configuration.get('RABBITMQ_UPLOAD_QUEUE')

app.config['MONGO_URL'] = configuration.get('MONGO_URL')
app.config['MONGO_USER'] = configuration.get('MONGO_USER')
app.config['MONGO_PASSWORD'] = configuration.get('MONGO_PASSWORD')
app.config['MONGO_DB'] = configuration.get('MONGO_DB')
app.config['MONGO_COLLECTION'] = configuration.get('MONGO_COLLECTION')


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        
        file = request.files['file']
        
        if file:
            current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
            filename = secure_filename(file.filename)
            filename = current_timestamp+'_'+filename
            file.save( os.path.join( app.config['UPLOAD_FOLDER'], filename ) )
            
            response = make_response( {'model_id':filename.split('.')[0]}, 200 )
            response.headers['Access-Control-Allow-Origin'] = '*'
            
            queue = MQ( 
                host=app.config['RABBITMQ_URL'], 
                queue=app.config['RABBITMQ_UPLOAD_QUEUE'] 
            )
            queue.send(filename)
            
            return response
            
        return make_response("Invalid POST request",status=400)
        
    return make_response("Invalid request type",status=400)


@app.route("/status", methods=['GET'])
def status():
    
    if request.method == 'GET':
        
        print(request)
        model_id = request.args.get('model_id')
        print(model_id)
        
        db = Database(
            url=app.config['MONGO_URL'],
            mongo_user=app.config['MONGO_USER'], 
            mongo_pass=app.config['MONGO_PASSWORD']
        )
        model_db = db.find_element(
            db_name=app.config['MONGO_DB'], 
            collection=app.config['MONGO_COLLECTION'],
            query={'model_id':model_id}
        )

        print(model_db)
        if model_db is None:
            response = make_response({}, 404)
        else:
            response = make_response(model_db, 200)
           
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return response
        
    return make_response("Invalid request type",status=400)


@app.route("/get_model", methods=['GET'])
def get_model():
    
    if request.method == 'GET':
        
        print(request)
        model_id = request.args.get('model_id')
        print(model_id)
        
        db = Database(
            url=app.config['MONGO_URL'],
            mongo_user=app.config['MONGO_USER'],
            mongo_pass=app.config['MONGO_PASSWORD']
        )
        model_db = db.find_element(
            db_name=app.config['MONGO_DB'],
            collection=app.config['MONGO_COLLECTION'],
            query={'model_id':model_id}
        )

        print(model_db)
        if model_db is None:
            response = make_response({}, 404)
        else:
            response = send_from_directory('.', model_db.get('link'), as_attachment=True)
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return response
        
    return make_response("Invalid request type",status=400)

if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=True)