import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

from Config import config
import time

osc_type = input("raw osc(r), face osc(f) or no osc(n)")
command_list = ["normal", "smile", "surprised", "right", "left"]

'''
OSC
'''
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=12345,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.UDPClient(args.ip, args.port)

def send(predict=0):
    if osc_type == "n":
        print("predict + no osc", predict)
        return
    elif osc_type == "r":
        print("predict + send predict osc", predict)
        msg = osc_message_builder.OscMessageBuilder(address="/predict")
        if predict is None:
            return
        msg.add_arg(int(predict))
        msg = msg.build()
        client.send(msg)
    elif osc_type == "f":
        print(predict, command_list[predict])
        time.sleep(0)
        if command_list[predict] is None:
            return

        msg = {}
        builded_msg = {}
        addresses = {"/predict": predict, "/raw": command_list[predict]}
        #print(addresses)
        for a in addresses.items():
            msg[a[0]] = osc_message_builder.OscMessageBuilder(address=a[0])
            #print(a[1])
            msg[a[0]].add_arg(str(a[1]))
            builded_msg[a[0]] = msg[a[0]].build()
            client.send(builded_msg[a[0]])
