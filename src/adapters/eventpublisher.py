from src.config import Settings
from src.interfaces.abstractpublisher import AbstractPublisher
from confluent_kafka import Producer

class Eventpublisher(AbstractPublisher):
    config = {'bootstrap.servers': 'localhost:9092'}
    def __init__(self, topic:str = "patient"):
        self.producer = Producer(**self.config)
        self.topic = topic

    def delivery_report(self,err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to topic {} [{}]'.format(msg.topic(), msg.partition()))


    def publish(self, event_type,event_data):
        json_event_data = {
            "event_type": event_type,
            "data": dict(event_data)  # Convert the event object to a dictionary
        }

        self.producer.poll(0)
        self.producer.produce(self.topic, str(json_event_data).encode('utf-8'),callback=self.delivery_report)
        self.producer.flush()
