"""This is the Test_Modem.py program that will test the Modem.py program using nose"""
import nose.tools as nt
import numpy as np
import time
import serial
import yaml
#pty does not work on windows
import pty
import os
import mock

class test_Modem(object):
	
	def setUp(self):
		self.User_Port = 1 
		
		
	def test_parse_config(self):
		with open("Test_KPC_9612_Plus_Config.yaml", 'r') as yamlfile:
			cfg = yaml.load(yamlfile)
		yamlfile.close()
		return cfg



	def test__init__(self):
		cfg = self.test_parse_config()
		self.ser = self.test_Setup_Modem()
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
	
	def test_Reboot(self):
		self.ser = self.test_Setup_Modem()
		cfg = self.test_parse_config()
		self.ser.write(cfg['Calabration']['RESTORE DEFAULT'])
		time.sleep(8)
		self.ser.write('*')
		time.sleep(1)
		self.ser.write(cfg['Startup']['MYCALL'])
		self.test__init__()


	def test_Switch_Port(self):
		out = ''
		self.ser = self.test_Setup_Modem()
		cfg = self.test_parse_config()
		User = self.User_Port
		if User == 2:
			self.ser.write(cfg['PORT']['PORT_2'])
			self.ser.write('\r')
			#self.ser.flush()
			'''time.sleep(1)
			while self.ser.inWaiting() > 0:
				out += self.ser.read(1)'''
		if User == 1:
			self.ser.write(cfg['PORT']['PORT_1'])
			self.ser.write('\r')
			#self.ser.flush()
			'''time.sleep(1)
			while self.ser.inWaiting() > 0:
				out += self.ser.read(1)'''
		'''self.ser.write('PORT' + '\r')
		out = '''''
		time.sleep(1)
		while self.ser.inWaiting() > 5:
			print(self.ser.inWaiting())
			out += self.ser.read(1)
		if out != '':
			print(out)

	def test_get_Modem_State(self):
		out = ''
		self.ser = self.test_Setup_Modem()
		self.ser.write('DISPLAY' + '\r')
		time.sleep(5)
		while self.ser.inWaiting() > 5:
			out += self.ser.read(1)
		if out != '':
			print(out)


	def test_Setup_Modem(self):
		cfg = self.test_parse_config()
		master, slave = pty.openpty()
		s_name = os.ttyname(master)
		self.ser = serial.Serial(s_name)
		'''self.ser = serial.Serial(
			port=cfg['Serial']['SERIAL_Port'],
			baudrate=cfg['Serial']['ABAUD'],
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
			)'''
		return self.ser
		
	





