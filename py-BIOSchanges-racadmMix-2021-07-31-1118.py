#!/usr/bin/env python
##################################################################################
###### Author: Tapan Kesarwani | version: 1.0.0 | Date Modified: 2021-07-30 ######
##################################################################################
import requests, json, sys, re, time, os, warnings, argparse
from datetime import datetime
warnings.filterwarnings("ignore")
parser=argparse.ArgumentParser(description="Python script using Redfish API to get all attributes or get current value for one specific attribute")
while True:
  args=vars(parser.parse_args())
  idrac_username="root"
  idrac_password="password"

  def nodeChoice():
    print("\n##### Select Node #####")
    print("[1] Controller\n" + "[2] Storage\n" + "[3] Compute\n" + "[4] Return to Previous Menu\n" + "[5] EXIT...\n")
    option = input("Select the desired option: ")
    if option == '1':
      return '1'
    elif option == '2':
      return '2'
    elif option == '3':
      return '3'
    elif option == '4':
      print("\nReturning to Previous Menu............\n")
      return '0'
    elif option == '5':
      print("\nExiting............\n")
      sys.exit(1)
    else:
      print("\nInvalid Choice, please chose again...!")
      return nodeChoice()

  def menuBootMode(node):
    print("===============================================================")
    print("Node Name\t\tNode IP \tBoot Mode \tStatus")
    print("===============================================================")
    nodedetail = ""
    nodenotok = ""
    ipnotok = ""
    for line in node.readlines():
      ip = line.strip()
      check_supported_idrac_version(ip)
      nodeBootMode = getBootMode(ip)
      if nodeBootMode == 'Bios':
        status = "OK"
      else:
        status = "NOT OK"
        ipnotok += str(line)
        nodenotok += get_DNSRacName(ip) + '  ' + '\t' + str(ip) + '\t' + nodeBootMode + '\t\t' + status + '\n'
      nodedetail += get_DNSRacName(ip) + '  ' + '\t' + str(ip) + '\t' + nodeBootMode + '\t\t' + status + '\n'
    print(nodedetail)
    ipnotok = ipnotok.rstrip()
    decn1 = input("Select \"NOT OK\" Nodes? (yes/no): ")
    if decn1 == "yes":
      print("\nNodes Pending Changes: \n")
      print("===============================================================")
      print("Node Name\t\tNode IP \tBoot Mode \tStatus")
      print("===============================================================")
      print(nodenotok)
      if (nodenotok == "" or nodenotok == "\n") :
        print("\nAll Nodes are \"OK\"\n\nReturning to Main Menu............\n")
      else:
        decn2 = input("\nContinue to change Boot Mode? (yes/no): ")
        print("")
        if decn2 == "yes":
          for ip1 in ipnotok.split('\n') :
            changeBootMode(ip1,"Bios")
            print("Boot Mode for %s set to \"Bios\"..." % ip1)
          print("")
          print('\033[91m' + "### Warning: The nodes are being rebooted for changes to take effect, please wait atleast 300 seconds before implementing any further changes on these nodes. ###\n" + '\033[0m')
        else:
          print("\nReturning to Main Menu............\n")
    else:
      print("\nReturning to Main Menu............\n")

  def menuPowerRecovery(node,value):
    print("======================================================================")
    print("Node Name\t\tNode IP \tAC Power Recovery \tStatus")
    print("======================================================================")
    nodedetail = ""
    nodenotok = ""
    ipnotok = ""
    for line in node.readlines():
      ip = line.strip()
      check_supported_idrac_version(ip)
      nodePowerRecovery = getPowerRecovery(ip)
      if nodePowerRecovery == value:
        status = "OK"
      else:
        status = "NOT OK"
        ipnotok += str(line)
        nodenotok += get_DNSRacName(ip) + '  ' + '\t' + str(ip) + '\t' + nodePowerRecovery + '\t\t\t' + status + '\n'
      nodedetail += get_DNSRacName(ip) + '  ' + '\t' + str(ip) + '\t' + nodePowerRecovery + '\t\t\t' + status + '\n'
    print(nodedetail)
    ipnotok = ipnotok.rstrip()
    decn1 = input("Select \"NOT OK\" Nodes? (yes/no): ")
    if decn1 == "yes":
      print("\nNodes Pending Changes: \n")
      print("======================================================================")
      print("Node Name\t\tNode IP \tAC Power Recovery \tStatus")
      print("======================================================================")
      print(nodenotok)
      if (nodenotok == "" or nodenotok == "\n") :
        print("\nAll Nodes are \"OK\"\n\nReturning to Main Menu............\n")
      else:
        decn2 = input("\nContinue to change AC Power Recovery? (yes/no): ")
        print("")
        if decn2 == "yes":
          for ip1 in ipnotok.split('\n') :
            changePowerRecovery(ip1,value)
            print("AC Power Recovery for %s set to \"%s\"..." % (ip1,value))
          print("")
          print('\033[91m' + "### Warning: The nodes are being rebooted for changes to take effect, please wait atleast 300 seconds before implementing any further changes on these nodes. ###\n" + '\033[0m')
        else:
          print("\nReturning to Main Menu............\n")
    else:
      print("\nReturning to Main Menu............\n")

  def menuSystemProfile(node,value):
    print("======================================================================")
    print("Node Name\t\tNode IP \tSystem Profile \t\tStatus")
    print("======================================================================")
    nodedetail = ""
    nodenotok = ""
    ipnotok = ""
    for line in node.readlines():
      ip = line.strip()
      check_supported_idrac_version(ip)
      nodeSystemProfile = getSystemProfile(ip)
      if nodeSystemProfile == value:
        status = "OK"
      else:
        status = "NOT OK"
        ipnotok += str(line)
        nodenotok += get_DNSRacName(ip) + '  ' + '\t' + str(ip) + '\t' + nodeSystemProfile + '  \t\t' + status + '\n'
      nodedetail += get_DNSRacName(ip) + '  ' + '\t' + str(ip) + '\t' + nodeSystemProfile + '  \t\t' + status + '\n'
    print(nodedetail)
    ipnotok = ipnotok.rstrip()
    decn1 = input("Select \"NOT OK\" Nodes? (yes/no): ")
    if decn1 == "yes":
      print("\nNodes Pending Changes: \n")
      print("======================================================================")
      print("Node Name\t\tNode IP \tSystem Profile \t\tStatus")
      print("======================================================================")
      print(nodenotok)
      if (nodenotok == "" or nodenotok == "\n") :
        print("\nAll Nodes are \"OK\"\n\nReturning to Main Menu............\n")
      else:
        decn2 = input("\nContinue to change System Profile? (yes/no): ")
        print("")
        if decn2 == "yes":
          for ip1 in ipnotok.split('\n') :
            changeSystemProfile(ip1,value)
            print("System Profile for %s set to \"%s\"..." % (ip1,value))
          print("")
          print('\033[91m' + "### Warning: The nodes are being rebooted for changes to take effect, please wait atleast 300 seconds before implementing any further changes on these nodes. ###\n" + '\033[0m')
        else:
          print("\nReturning to Main Menu............\n")
    else:
      print("\nReturning to Main Menu............\n")

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

  def getBootMode(idrac_ip):
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip,verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    return data[u'Attributes']["BootMode"]

  def changeBootMode(idrac_ip,bmode):
    os.system('. /root/TK/addtnlScripts/setBiosBootMode.sh {} {}' .format(str(idrac_ip),str(bmode)))

  def getPowerRecovery(idrac_ip):
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip,verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    for i in data['Attributes'].items():
      if i[0] == 'AcPwrRcvry':
        return i[1]

  def changePowerRecovery(idrac_ip,prec):
    os.system('. /root/TK/addtnlScripts/setAcPowerRecovery.sh {} {}' .format(str(idrac_ip),str(prec)))

  def getSystemProfile(idrac_ip):
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Bios' % idrac_ip,verify=False,auth=(idrac_username, idrac_password))
    data = response.json()
    for i in data['Attributes'].items():
      if i[0] == 'SysProfile':
        return i[1]

  def changeSystemProfile(idrac_ip,sprf):
    os.system('. /root/TK/addtnlScripts/setSystemProfile.sh {} {}' .format(str(idrac_ip),str(sprf)))

  if __name__ == "__main__":
    print("\n#######################################\n###### Node Hardware Settings... ######\n#######################################\n")
    print("[1] Boot Mode\n" + "[2] AC Power Recovery\n" + "[3] System Profile\n" + "[4] EXIT...\n")
    option = input("Select the desired option: ")
    ctrl = open("/root/TK/ipPlan/controller","r")
    strg = open("/root/TK/ipPlan/storage","r")
    comp = open("/root/TK/ipPlan/compute","r")
    if option == '1':
      ch = nodeChoice()
      if ch == '1':
        menuBootMode(ctrl)
      elif ch == '2':
        menuBootMode(strg)
      elif ch == '3':
        menuBootMode(comp)
    elif option == '2':
      ch = nodeChoice()
      if ch == '1':
        menuPowerRecovery(ctrl,"On")
      elif ch == '2':
        menuPowerRecovery(strg,"On")
      elif ch == '3':
        menuPowerRecovery(comp,"Last")
    elif option == '3':
      ch = nodeChoice()
      if ch == '1':
        menuSystemProfile(ctrl,"PerfOptimized")
      elif ch == '2':
        menuSystemProfile(strg,"PerfOptimized")
      elif ch == '3':
        menuSystemProfile(comp,"PerfOptimized")
    elif option == '4':
      print("\nExiting............\n")
      break
    else:
      print("\nInvalid Choice, running script again...\n")
