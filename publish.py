import pika

rabbit_user = 'rabbituser'
rabbit_pass = 'rabbitpass'
rabbit_url = 'devrabbit.centralus.cloudapp.azure.com'
vhost = 'scaletest'
creds = pika.PlainCredentials(rabbit_user, rabbit_pass)


params = pika.ConnectionParameters(host=rabbit_url, 
                                   virtual_host=vhost,
                                   credentials=creds,
                                   heartbeat=500,
                                   blocked_connection_timeout=300
)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='docker-scale')

for i in range(100):
    channel.basic_publish('', 'docker-scale', "message body",
                          pika.BasicProperties(content_type='text/plain', 
                                               delivery_mode=1)
)
channel.close()
connection.close()