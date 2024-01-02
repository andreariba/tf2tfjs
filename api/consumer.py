#!/usr/bin/env python
import pika, sys, os, yaml, subprocess
from datetime import datetime
from lib.queue import MQ
from lib.database import Database

with open("configuration.yaml", "r") as file:
    configuration = yaml.load(file, Loader=yaml.FullLoader)
    print(configuration)


def process(ch, method, properties, body) -> None:
    
    filename = body.decode('utf-8')
    filename_noext, ext = filename.split('.')
    if ext!="zip":
        print(f" [-] {body} invalid format. Only zip supported.")
        
    command_result = subprocess.run([
        "bash", 
        "convert.sh", 
        "-u", configuration.get('FOLDER').get('UPLOAD'), 
        "-t", configuration.get('FOLDER').get('TMP'), 
        "-c", configuration.get('FOLDER').get('CONVERTED'), 
        "-f", filename_noext
    ])
    print(command_result)
    current_timestamp = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

    if command_result.returncode!=0:
        processed_dict = {
            'model_id':filename_noext, 
            'timestamp':current_timestamp, 
            'status':1
        }
    else:
        processed_dict = {
            'model_id':filename_noext, 
            'timestamp':current_timestamp, 
            'status':0 , 
            'link':'converted/'+filename_noext+'.tar.gz'
        }
    
    db = Database(
        url=configuration.get('MONGO_URL'),
        mongo_user=configuration.get('MONGO_USER'), 
        mongo_pass=configuration.get('MONGO_PASSWORD')
    )
    db.add_element(
        db_name=configuration.get('MONGO_DB'), 
        collection=configuration.get('MONGO_COLLECTION'),
        element=processed_dict
    )
    print(f" [x] {body} processed")

    return


if __name__ == '__main__':
    try:
        queue = MQ( 
            host=configuration.get('RABBITMQ_URL'), 
            queue=configuration.get('RABBITMQ_UPLOAD_QUEUE')
        )
        queue.consume(function=process)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)