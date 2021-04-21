import signal
import socket
import sys
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json

# DB credentials
user_mysql = sys.argv[1]
pass_mysql = sys.argv[2]
model = sys.argv[3]

# DB access
engine = create_engine("mysql+mysqlconnector://" + user_mysql + ":" + pass_mysql + "@localhost:3306/" + model)
Session = sessionmaker(bind=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

# DB tables
Local = Base.classes.Local
Sensor = Base.classes.Sensor
Reading = Base.classes.Reading

# MQTT definitions
client_name = socket.gethostname()
client = mqtt.Client(client_name)
broker = sys.argv[4]
topic = sys.argv[5]


# mosquitto_pub -h mqtt.sj.ifsc.edu.br -m '{"idLocal":"local1","idSensor":"saca1","temperature":23,"humidity":25,"datetime":"2021-03-14 13:07"}' -t 'Empresa1'
def on_message(client, userdata, message):
    message_rcv = str(message.payload.decode("utf-8"))
    print("message received ", message_rcv)
    message_json = json.loads(message_rcv)
    reading = Reading()
    dump_json(reading, message_json)
    gateway = sessionSQL.query(Local).filter(Local.idLocal == reading.idLocal).first()
    if gateway is None:
        gateway = Local()
        gateway.idLocal = reading.idLocal
        sessionSQL.add(gateway)

    sensor = sessionSQL.query(Sensor)\
        .filter(Sensor.idSensor == reading.idSensor, Sensor.idLocal == reading.idLocal).first()
    if sensor is None:
        sensor = Sensor()
        sensor.idSensor = reading.idSensor
        sensor.idLocal = reading.idLocal
        sessionSQL.add(sensor)

    sessionSQL.add(reading)
    sessionSQL.commit()


def dump_json(reading, message_json):
    reading.idLocal = message_json["idLocal"]
    reading.idSensor = message_json["idSensor"]
    reading.temperature = message_json["temperature"]
    reading.humidity = message_json["humidity"]
    reading.col = message_json["datetime"]


def exit_handler(sig=None, frame=None):
    print("Exiting...")
    sessionSQL.close()
    client.loop_stop()
    sys.exit(0)


def start_client():
    client.connect(broker)
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()


# Run syntax:
# python3 app.py <mysql-user> <mysql-pass> <mysql-model> <mqtt-broker> <mqtt-topic>
# Ex:
# python3 app.py guilherme password smqg SMQG
if __name__ == '__main__':
    sessionSQL = Session()
    signal.signal(signal.SIGINT, exit_handler)
    start_client()
