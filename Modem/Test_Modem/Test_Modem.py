"""This is the Test_Modem.py program that will test the Modem.py program using nose"""
import nose.tools as nt
import numpy as np
import time
import serial
import yaml
#pty does not work on windows
import pty
import os


class test_Modem(object):
	
	def setUp(self):
		pass
		
		
	def test_parse_config(self):
		with open("Test_KPC_9612_Plus_Config.yaml", 'r') as yamlfile:
			cfg = yaml.load(yamlfile)
		yamlfile.close()
		return cfg



	def test__init__(self):
		cfg = self.test_parse_config()
		#Virtual serial port
###############################################
		master, slave = pty.openpty()
		s_name = os.ttyname(master)
		self.ser = serial.Serial(s_name)
		self.ser.close()
		self.ser.open()
###############################################
		
		#Sets the test settings in the virtual serial port
###############################################
		count = len(cfg['Startup']['Terminal'])
		out = ''
		while count > 0:
			self.ser.write(cfg['Startup']['Terminal'][count - 1])
			self.ser.write('\r')
			count = count - 1
			time.sleep(1)
###############################################		

		#Displays the test settings
###############################################
		self.ser.write('DISPLAY' + '\r')
		time.sleep(5)
		while self.ser.inWaiting() > 0:
			out += self.ser.read(1)
		if out != '':
			print(">>" + out)
###############################################
		return self.ser
	
	def test_Reboot(self):
		self.ser = self.test__init__()
		cfg = self.test_parse_config()
		self.ser.write(cfg['Calabration']['RESTORE DEFAULT'])
		time.sleep(8)
		self.ser.write('*')
		time.sleep(1)
		self.ser.write(cfg['Startup']['MYCALL'])
		self.test__init__()


	def test_Switch_Port(self):
		self.ser = self.test__init__()
		cfg = self.test_parse_config()
		User = input("To select port, type 1 or 2")
		if User == 2:
			self.ser.write(cfg['PORT']['PORT_2'])
		if User == 1:
			self.ser.write(cfg['PORT']['PORT_1'])

		
	





