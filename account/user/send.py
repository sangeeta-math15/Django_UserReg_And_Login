import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='send_mail')


def send_data_to_queue(data):
    """
        This method is used to send data to queue.
        :param data: It's accept data in dictionary format.
    """
    channel.basic_publish(exchange='', routing_key='send_mail', body=data)
    print('[x] Data sent to queue.')
    connection.close()