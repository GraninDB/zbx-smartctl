#!/usr/local/bin/python3

import subprocess

json_string = "{\n  \"data\":[\n    {\n"

disks = subprocess.getoutput("smartctl --scan").split("\n")
json_index = 1
for disk in disks:
	arr_disk = disk.split()
	
	if arr_disk[2] == "ata" or arr_disk[2] == "scsi":
		smart = "0"
		disk_type = "2"
		ser_number = ""
		model = ""

		diskinfo = subprocess.getoutput("smartctl -i " + arr_disk[0]).split("\n")
		for info in diskinfo:
			caption, value = info[:18].strip(), info[18:].strip()
			
			if model == "":
				if caption == "Device Model:" or caption == "Vendor:":
					model = value
			
			if caption == "Serial Number:":
				ser_number = value
			
			if smart == "0" and caption == "SMART support is:" and  value == "Enabled":
				smart = "1"

			if disk_type == "2" and caption == "Rotation Rate:":
				if "Solid State Device" in value:
					disk_type = "1"
				elif "rpm" in value:
					disk_type = "0"
					
		if json_index == 1:
			json_index += 1
		else:
			json_string += ",\n    {\n"
			
		json_string += "      \"{#DISKMODEL}\":\"" + model + "\",\n"
		json_string += "      \"{#DISKSN}\":\"" + ser_number + "\",\n"
		json_string += "      \"{#DISKNAME}\":\"" + arr_disk[0] + "\",\n"
		json_string += "      \"{#DISKCMD}\":\"" + arr_disk[0] + " " + arr_disk[1] + arr_disk[2] + "\",\n"
		json_string += "      \"{#SMART_ENABLED}\":\"" + smart + "\",\n"
		json_string += "      \"{#DISKTYPE}\":\"" + disk_type + "\"\n"

	json_string += "    }"
	
json_string +="\n  ]\n}"

print(json_string)
