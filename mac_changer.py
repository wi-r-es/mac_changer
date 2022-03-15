#!/usr/bin/env python

import subprocess
import optparse
import re

def get_args():
    parser=optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options

    # interface = input("interface >") #to run on python 2.7 use raw_input() instead


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    ## not SECURE , user can use ; to execute other terminal commands
    # subprocess.call(f"ifconfig {interface} down", shell=True)
def check_mac(interface):
    pattern = re.compile(r"/([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})/gm")
    mac = subprocess.check_output(["ifconfig",interface])
    r = pattern.search(mac)
    if r:
        return r.group(0)
    else:
        print("[-] Could not read MAC address.")
#interfaceDefault = "wlp4s0"


options=get_args()
current_mac = check_mac(options.interface)
print("Current MAC --> " + str(current_mac))
change_mac(options.interface,options.mac)
current_mac = check_mac(options.interface)
if current_mac == options.mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
