#!/usr/bin/env python
##################################################################################
###### Author: Tapan Kesarwani | version: 1.0.3 | Date Modified: 2021-07-29 ######
##################################################################################
while True:
  ctrl = open('/root/TK/macPXE/mac-pxe-ctrl','r')
  strg = open('/root/TK/macPXE/mac-pxe-strg','r')
  comp = open('/root/TK/macPXE/mac-pxe-comp','r')
  print("Create json file for:\n")
  print("[1] Controller\n" + "[2] Storage\n" + "[3] Compute\n" + "[4] EXIT...\n")
  option = input("Select the desired option: ")
  if option == '1':
    open('/root/TK/jsonFiles/instack-ctrl.json', 'w').close()
    json = open("/root/TK/jsonFiles/instack-ctrl.json","w+")
    tempctrl = '{ \n' + '  "nodes":['
    x=0
    for line in ctrl.readlines():
      for word in line.split():
        nodename,nodemac,nodeip=line.split()
      tempctrl += '\n    {\n' + '        "name":"' + nodename + '",\n'
      tempctrl +='        "mac":["' + nodemac + '"],\n' + '        "cpu":"32",\n' + '        "memory":"131072",\n' + '        "disk":"500",\n'
      tempctrl += '        "arch":"x86_64",\n' + '        "pm_type":"ipmi",\n' + '        "pm_user":"root",\n'
      tempctrl += '        "pm_password":"m4venir2!",\n' + '        "pm_addr":"' + nodeip + '",\n'
      tempctrl += '        "capabilities":"node:controller-' + str(x) + ',profile:control,boot_option:local"\n' + '    },'
      x+=1
    tempctrl = tempctrl[:tempctrl.rfind('\n')]
    tempctrl += '\n    }\n' + '  ] \n' + '}\n'
    json.write(tempctrl)
    json.close()
    print("\njson file created successfully for controller nodes...\n")
  elif option == '2':
    open('/root/TK/jsonFiles/instack-strg.json', 'w').close()
    json = open("/root/TK/jsonFiles/instack-strg.json","w+")
    tempstrg = '{ \n' + '  "nodes":['
    x=0
    for line in strg.readlines():
      for word in line.split():
        nodename,nodemac,nodeip=line.split()
      tempstrg += '\n    {\n' + '        "name":"' + nodename + '",\n'
      tempstrg +='        "mac":["' + nodemac + '"],\n' + '        "cpu":"96",\n' + '        "memory":"256000",\n' + '        "disk":"500",\n'
      tempstrg += '        "arch":"x86_64",\n' + '        "pm_type":"ipmi",\n' + '        "pm_user":"root",\n'
      tempstrg += '        "pm_password":"m4venir2!",\n' + '        "pm_addr":"' + nodeip + '",\n'
      tempstrg += '        "capabilities":"node:storage-' + str(x) + ',profile:ceph-storage,boot_option:local"\n' + '    },'
      x+=1
    tempstrg = tempstrg[:tempstrg.rfind('\n')]
    tempstrg += '\n    }\n' + '  ] \n' + '}\n'
    json.write(tempstrg)
    json.close()
    print("\njson file created successfully for storage nodes...\n")
  elif option == '3':
    open('/root/TK/jsonFiles/instack-comp.json', 'w').close()
    json = open("/root/TK/jsonFiles/instack-comp.json","w+")
    tempcomp = '{ \n' + '  "nodes":['
    x=0
    for line in comp.readlines():
      for word in line.split():
        nodename,nodemac,nodeip=line.split()
      tempcomp += '\n    {\n' + '        "name":"' + nodename + '",\n'
      tempcomp +='        "mac":["' + nodemac + '"],\n' + '        "cpu":"104",\n' + '        "memory":"512000",\n' + '        "disk":"500",\n'
      tempcomp += '        "arch":"x86_64",\n' + '        "pm_type":"ipmi",\n' + '        "pm_user":"root",\n'
      tempcomp += '        "pm_password":"m4venir2!",\n' + '        "pm_addr":"' + nodeip + '",\n'
      tempcomp += '        "capabilities":"node:computeDell6230-' + str(x) + ',profile:baremetal,boot_option:local"\n' + '    },'
      x+=1
    tempcomp = tempcomp[:tempcomp.rfind('\n')]
    tempcomp += '\n    }\n' + '  ] \n' + '}\n'
    json.write(tempcomp)
    json.close()
    print("\njson file created successfully for compute nodes...\n")
  elif option == '4':
    print("\nExiting............\n")
    break
  else:
    print("\nInvalid Choice, running script again\n")
  ctrl.close()
  strg.close()
  comp.close()
