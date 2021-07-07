import paho.mqtt.client as mqtt
import ssl
import psksupport as psk

def on_connect(client, user_data, flags, rc):
    print("result code : {0}".format(str(rc)))
    client.subscribe("sci-topic")    


def on_message(client, user_data, msg):
    #print("{}, {}".format(msg.topic, msg.payload))
    print("{}".format(msg.topic))


if __name__ == '__main__':

    print("Start !!")

    client = mqtt.Client(client_id="python_paho")

    client.on_connect = on_connect
    client.on_message = on_message

    context = psk.SSLPSKContext(ssl.PROTOCOL_TLS)

    context.set_ciphers('PSK')

    context.psk = (b'testuser', bytes("testuser", encoding="utf-8"))

    client.tls_set_context(context)

    host = "localhost"
    port = 10001
    keepalive = 60


    try:

        client.connect(host, port, keepalive)

        client.loop_forever()
    
    except KeyboardInterrupt:
   
        print("keyboard interrupted")

        client.disconnect()
