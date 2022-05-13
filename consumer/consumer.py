import pika
import time
import sys
import os

def callback(ch, method, properties, body):
    try:
        rabbit_data=[]
        if body != None:
            rabbit_data.append(body)
            if len(rabbit_data) > 0:    
                for i in rabbit_data:
                    time.sleep(10)
                    rabbit_data.remove(i)           
        else:
            ch.stop_consuming()
        ch.basic_ack(delivery_tag = method.delivery_tag,
                     multiple=False)

    except Exception as e:
        print (str(e))

def main():    
    try:
        rabbit_user = 'rabbituser'
        rabbit_pass = 'rabbitpass'
        rabbit_url = 'devrabbit.centralus.cloudapp.azure.com'
        vhost = 'scaletest'
        creds = pika.PlainCredentials(rabbit_user, rabbit_pass)
        
        params = pika.ConnectionParameters(host=rabbit_url,
                                           virtual_host=vhost, 
                                           credentials=creds,
                                           heartbeat=500,
                                           blocked_connection_timeout=300)

        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        channel.queue_declare(queue='docker-scale')

        # basic_qos will acknowdeging packet one by one 
        channel.basic_qos(prefetch_size=0,prefetch_count=1) 
        channel.basic_consume(queue='docker-scale', 
                              on_message_callback=callback,
                              auto_ack=False)
        
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as e:
        print(str(e))
     
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)