import pika


class MQ:

    def __init__(self, host: str, queue: str):
        self.host = host
        self.queue = queue

    def send(self, filename: str):
        
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        channel.basic_publish(
            exchange='', 
            routing_key=self.queue, 
            body=filename
        )
        print(f" [x] Sent {filename} to {self.queue}")
        connection.close()

    
    def consume(self, function):
        
        connection = pika.BlockingConnection( 
            pika.ConnectionParameters(host=self.host)
        )
        channel = connection.channel()
        
        channel.queue_declare(queue=self.queue)
        
        channel.basic_consume(
            queue=self.queue, 
            on_message_callback=function, 
            auto_ack=True
        )
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()