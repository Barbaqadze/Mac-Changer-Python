import subprocess
from optparse import OptionParser
import re
import sys

def get_arguments():
    parser = OptionParser()
    parser.add_option('-i' , '--interface' , dest='interface' , help='Interface to change its MAC address')
    parser.add_option('-m' , '--mac' , dest='new_mac' , help='New MAC address')
    (options , arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface , use --help for more info')
    elif not options.new_mac:
        parser.error('[-] Please specify an new mac, use --help for more info')
    return options


def change_mac(interface , new_mac):
    subprocess.run(['ifconfig' ,  interface , 'down'])
    subprocess.run(['ifconfig' ,  interface , 'hw' , 'ether' , new_mac])
    subprocess.run(['ifconfig' ,  interface , 'up'])


def get_current_mac(interface):
    search_ifconfig = subprocess.check_output(['ifconfig' , interface])
    search_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w' , str(search_ifconfig))
    

    if not search_mac:
        print('[-] Could not find MAC address')
        return False
    else :
        return search_mac.group(0)
    
    



options = get_arguments()
current_mac = get_current_mac(options.interface)
if current_mac == False:
    sys.exit()

change_mac(options.interface , options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print('[+] MAC address was successfully changed to ' + current_mac)
else :
    print('[-] MAC address is invalid')
