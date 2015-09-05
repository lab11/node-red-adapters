import os
import subprocess
import paho.mqtt.client as mqtt
from time import sleep
from sys import argv, exit
import json

nmap_mac_cmd = ["sudo", "nmap", "-sP", "-n", "192.168.1.0/24"]

connected = False

def main():
    global connected
    config = get_cmd_line_config()
    client = mqtt.Client(protocol=mqtt.MQTTv31)
    client.on_connect = on_connect
    client.on_publish = on_publish
    print("Connecting"),
    client.connect(config["broker_addr"])
    while(connected == False):
        print("."),
        client.loop()
        sleep(0.1)
    print("Starting scanner")
    client.loop_start()
    try:
        while True:
            #client.loop()
            addresses = get_mac_addresses()
            quoted_addresses = [("\"" + a + "\"") for a in addresses]
            addr_str = "[" + ", ".join(quoted_addresses) + "]"
            msg = "{\"mac_addrs\": " + addr_str + "}"
            client.publish(config["topic"], msg)
            if config["verbose"]:
                print("Published msg {} on topic {} to broker at {}".format(msg, config["topic"], config["broker_addr"]))
            sleep(2)
    except KeyboardInterrupt:
        client.disconnect()
        exit()

def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        connected = True
        print("\nConnected")
    else:
        print("Did not connect")
        print(str(rc))

def on_publish(client, userdata, mid):
    print("PUBLISH SUCCESS:"),

def get_cmd_line_config():
    program_file = argv.pop(0) # don't need
    config = {}
    verbose = False
    while len(argv) > 0:
        arg = argv.pop(0)
        if arg == '--topic' or arg == '-t':
            config["topic"] = argv.pop(0)
        elif arg == '--broker' or arg == '-b':
            config["broker_addr"] = argv.pop(0)
        elif arg == '--verbose' or arg == '-v':
            verbose = True
        else:
            print("Unknown argument: {0}".format(arg))
    if len(config) != 2:
        print("Usage: python <program.py> [-v] -t <mqtt topic> -b <broker_addr>")
        exit()
    config["verbose"] = verbose
    return config

def get_mac_addresses():
    output = subprocess.Popen(nmap_mac_cmd, stdout=subprocess.PIPE)
    stdout = output.communicate()[0]
    records = grep(stdout, "MAC Address")
    addresses = [str(r[2]) for r in records]
    return addresses

#return lines containing certain search string
def grep(stdout, s):
    result = []
    stdout = stdout.decode("utf-8")
    lines = stdout.split('\n')
    for line in lines:
        if s in line:
            #print line
            fields = line.split()
            result.append(fields)
    return result

def debug():
   print(get_mac_addresses())

if __name__=="__main__":
   main()
