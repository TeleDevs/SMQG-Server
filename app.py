import signal
import socket
import sys
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json

#DB credentials
user_mysql = sys.argv[1]
pass_mysql = sys.argv[2]
model = sys.argv[3]
create = sys.argv[4]

#DB access
engine = create_engine("mysql+mysqlconnector://" + user_mysql + ":" + pass_mysql + "@localhost:3306/" + model)
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

#DB tables
Gateway = Base.classes.Gateway
Sensor = Base.classes.Sensor
Reading = Base.classes.Reading

#MQTT definitions
client_name = socket.gethostname()
client = mqtt.Client(client_name)
broker = "localhost"
topic = sys.argv[5]

#mosquitto_pub -m '{"idGateway":1,"idSensor":1,"val":23,"datetime":"2021-03-14 13:07:08.104114"}' -t 'SMQG'
def on_message(client, userdata, message):
    message_rcv = str(message.payload.decode("utf-8"))
    print("message received ", message_rcv)
    # print("message topic=", message.topic)
    # print("message qos=", message.qos)
    # print("message retain flag=", message.retain)

    message_json = json.loads(message_rcv)
    reading = Reading()
    dump_json(reading, message_json)
    print(reading.idGateway)
    print(reading.idSensor)
    print(reading.val)
    print(reading.col)
    sessionSQL.add(reading)
    sessionSQL.commit()


def dump_json(reading, message_json):
    reading.idGateway = message_json["idGateway"]
    reading.idSensor = message_json["idSensor"]
    reading.val = message_json["val"]
    reading.col = message_json["datetime"]


def create_db():
    gateway = Gateway()
    gateway.idGateway = 1
    sensor = Sensor()
    sensor.idGateway = 1
    sensor.idSensor = 1
    sensor.type = "DHT11"
    sessionSQL.add(gateway)
    sessionSQL.add(sensor)
    sessionSQL.commit()
    sessionSQL.close()


def exit_handler(sig=None, frame=None):
    print("Exiting...")
    sessionSQL.close()
    client.loop_stop()
    sys.exit(0)


def start_client():
    client.connect(broker)
    client.subscribe("SMQG")
    client.on_message = on_message
    client.loop_forever()


#Run syntax:
#python3 app.py <mysql-user> <mysql-pass> <mysql-model> <create-stub-gateway&sensor> <mqtt-topic>
#Ex:
#python3 app.py guilherme password smqg False SMQG
if __name__ == '__main__':
    if create == 'True':
        create_db()
    sessionSQL = Session()
    signal.signal(signal.SIGINT, exit_handler)
    start_client()
