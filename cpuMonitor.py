#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import sys
import re
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator
import os

def cb_exit(w, data):
	Gtk.main_quit()

def get_numberCores():
	numberCores=0
	for line in open("/proc/cpuinfo", 'r'):
    		if re.search("cpu cores", line):
			print line
			m = re.search(r'(\d)',line)
			numberCores = m.group()
			break
	print "Numero de cores = "+numberCores+"_\n"        	
	return int(numberCores)

def refreshData(ind_app):
	label=""
	for core in range(0,numberCores):
		label+= readcputemp(core)
		if core < numberCores -1:
			label+=" - "
	ind_app.set_label(label,"")
	return 1



def readcputemp(core):
# get CPU temp
	file_core = open('/sys/class/hwmon/hwmon0/device/temp'+str(core+1)+'_input','r')
	temp_core = file_core.read(2)+"º C"
	file_core.close()
	return temp_core


numberCores = get_numberCores()
ind_app = appindicator.Indicator.new ("cputemp-indicator","/usr/share/unity/icons/panel-shadow.png",appindicator.IndicatorCategory.HARDWARE)

ind_app.set_status (appindicator.IndicatorStatus.ACTIVE)

# create a menu
menu = Gtk.Menu()
menu_items = Gtk.MenuItem("Salir")
menu.append(menu_items)
menu_items.connect("activate", cb_exit, '')
menu_items.show()
ind_app.set_menu(menu)
GLib.timeout_add(500, refreshData, ind_app)
Gtk.main()
