import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

import speakcommand

def setup_osc(scripts):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=12346,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.UDPClient(args.ip, args.port)

    msg = osc_message_builder.OscMessageBuilder(address = "/scripts")
    for script in scripts:
        msg.add_arg(script)

    m = msg.build()
    client.send(m)

    return client

def receive_osc(scripts, is_train, client):
    cs = speakcommand.SpeakWCommand(scripts, is_train, client)

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
      type=int, default=12345, help="The port to listen on")
    args = parser.parse_args()
    _dispatcher = dispatcher.Dispatcher()
    #_dispatcher.map("/raw", cs.speak_w_command)
    _dispatcher.map("/predict", cs.speak_w_command)

    server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), _dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
