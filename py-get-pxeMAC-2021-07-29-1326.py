#!/usr/bin/env python
##################################################################################
###### Author: Tapan Kesarwani | version: 1.0.0 | Date Modified: 2021-07-29 ######
##################################################################################
import requests, json, sys, re, time, os, warnings, argparse
from datetime import datetime
warnings.filterwarnings("ignore")
parser=argparse.ArgumentParser(description="Python script using Redfish API to get all attributes or get current value for one specific attribute")
while True:
  args=vars(parser.parse_args())
  idrac_username="root"
  idrac_password="password"
 
  def check_supported_idrac_version(idrac_ip):
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip,verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    if response.status_code == 401:
      print("\n- WARNING, status code %s returned. Incorrect iDRAC username/password or invalid privilege detected." % response.status_code)
    elif response.status_code != 200:
      print("\n- WARNING, iDRAC version installed does not support this feature using Redfish API")
    else:
      pass

  def get_DNSRacName(idrac_ip):
    response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/EthernetInterfaces/NIC.1' % idrac_ip,verify=False,auth=(idrac_username,idrac_password))
    data = response.json()
    return data[u'HostName']

  def get_pxeMAC(idrac_ip):
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/EthernetInterfaces/NIC.Integrated.1-1-1' % idrac_ip,verify=False,auth=(idrac_username,idrac_password))
    data = response.json()
    return data[u'MACAddress']

  if __name__ == "__main__":
    print("Get PXE MAC Address for Nodes...\n")
    print("[1] Controller\n" + "[2] Storage\n" + "[3] Compute\n" + "[4] EXIT...\n")
    option = input("Select the desired option: ")
    if option == '1':
      open('/root/TK/macPXE/mac-pxe-ctrl', 'w').close()
      mac = open("/root/TK/macPXE/mac-pxe-ctrl","w+")
      ctrl = open("/root/TK/ipPlan/controller","r")
      nodedetail = ""
      for line in ctrl.readlines():
        ip = line.strip()
        check_supported_idrac_version(ip)
        nodedetail += get_DNSRacName(ip) + '\t\t' + get_pxeMAC(ip) + '\t\t' + str(ip) + '\n'
      print(nodedetail)
      mac.write(nodedetail)
      ctrl.close()
      mac.close()
    elif option == '2':
      open('/root/TK/macPXE/mac-pxe-strg', 'w').close()
      mac = open("/root/TK/macPXE/mac-pxe-strg","w+")
      strg = open("/root/TK/ipPlan/storage","r")
      nodename = ""
      for line in strg.readlines():
        ip = line.strip()
        check_supported_idrac_version(ip)
        nodename += get_DNSRacName(ip) + '  ' + '\t\t' + get_pxeMAC(ip) + '\t\t' + str(ip) + '\n'
      print(nodename)
      mac.write(nodename)
      strg.close()
      mac.close()
    elif option == '3':
      open('/root/TK/macPXE/mac-pxe-comp', 'w').close()
      mac = open("/root/TK/macPXE/mac-pxe-comp","w+")
      comp = open("/root/TK/ipPlan/compute","r")
      nodename = ""
      for line in comp.readlines():
        ip = line.strip()
        check_supported_idrac_version(ip)
        nodename += get_DNSRacName(ip) + '  ' + '\t\t' + get_pxeMAC(ip) + '\t\t' + str(ip) + '\n'
      print(nodename)
      mac.write(nodename)
      comp.close()
      mac.close()
    elif option == '4':
      print("\nExiting............\n")
      break
    else:
      print("\nInvalid Choice, running script again\n")
