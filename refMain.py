import time
from prometheus_client import start_http_server, Gauge
import paho.mqtt.client as mqtt
import os
import config


class MqttConnection:
    def __init__(self):
        self.client = mqtt.Client("test-mqtt-connection", mqtt.MQTTv311)
        self.client.username_pw_set(config.mqttCreds["username"], config.mqttCreds["password"])
        self.client.connect(config.mqttCreds["hostname"], config.mqttCreds["port"])
        self.gauge = Gauge('mqtt_connection', 'check mqtt connection')
        self.start = time.time()
        self.disconnect = time.time()
        self.options()
        self.topic = config.mqttCreds["topic"]

    def options(self):
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("try to connect")
        client.subscribe(self.topic, 0)
        if rc == 0:
            print("connected")
            self.gauge.set(1)
            self.disconnect = time.time()
            self.start = time.time()
        else:
            self.gauge.set(0)
            time.sleep(10)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("I've subscribed with QoS: {}".format(
            granted_qos[0]))
        self.disconnect = time.time()
        self.start = time.time()

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.gauge.set(0)

    def on_message(self, client, userdata, msg):
        self.start = time.time()
        self.disconnect = time.time()

    def run(self, ):
        start_http_server(config.mqttCreds["exporter"])
        while True:
            if time.time() - self.start > 1 * 60:
                self.gauge.set(0)
                time.sleep(10)
            else:
                self.gauge.set(1)
            if time.time() - self.disconnect > 10 * 60:
                try:
                    os.system("sudo docker restart {}".format(config.mqttCreds["container"]))
                    print("docker container restart!")
                except:
                    print("cannot restart docker container!")
                time.sleep(10)


if __name__ == "__main__":
    mqttClient = MqttConnection()
    mqttClient.run()
