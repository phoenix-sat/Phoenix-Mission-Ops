#Created by Nick Altman KI7NUU
#Student at Arizona State University
#Creation date 7-24-17
#Member of the Phoenix Cubesat Team
#The purpose of this program is to interface with what ever modem is connected
#to the ground station. For right now I am going to put the Kaltronics 9612 plus
#in here. In the future, that will be split off into its own child class
import time
import serial
import yaml

class Modem(object):
	#parse_config method creates the dictonary of primary settings needed to be set. right now there are only 8 but more will be added
	def parse_config(self):
		with open("KPC_9612_Plus_Config.yaml", 'r') as yamlfile:
			cfg = yaml.load(yamlfile)
		yamlfile.close()
		return cfg


	#init sets up a link with the tnc and reads the dictionary and sets the settings to their approprate values
	def __init__(self):
		cfg = self.parse_config()
		self.ser = self.Setup_Modem()
		#connects to the KPC 9612 Plus
		self.ser.close()
		self.ser.open()
		#Sets the settings to the desired values
		count = len(cfg['Startup']['Terminal'])
		out = ''
		while count > 0:
			self.ser.write(cfg['Startup']['Terminal'][count - 1])
			self.ser.write('\r')
			count = count - 1		

	#adding this in just in case we want to start fresh when activiating the TNC
	'''def Reboot(self):
		self.ser = self.Setup_Modem()
		cfg = self.parse_config()
		self.ser.write(cfg['Calabration']['RESTORE DEFAULT'])
		time.sleep(8)
		self.ser.write('*')
		time.sleep(1)
		self.ser.write(cfg['Startup']['MYCALL'])
		self.__init__()'''
		
	#This will switch the ports we are listening and transmitting to.
	#I do not have to worry about changeing the HBAUD here because that can be changed in the config
	#All this will really do is switch from port 1 to port 2 to listen and transmit	
	def Switch_Port(self):
		out = ''
		cfg = self.parse_config()
		User = input("To select port, type 1 or 2: ")
		if User == 2:
			self.ser.write(cfg['PORT']['PORT_2'])
			self.ser.write('\r')
			#self.ser.flushInput()
			'''time.sleep(1)
			while self.ser.inWaiting() > 0:
				out += self.ser.read(1)'''
		if User == 1:
			self.ser.write(cfg['PORT']['PORT_1'])
			self.ser.write('\r')
			#self.ser.flushInput()
			'''time.sleep(1)
			while self.ser.inWaiting() > 0:
				out += self.ser.read(1)'''
		'''self.ser.write('PORT' + '\r')
		out = '''''
		time.sleep(1)
		while self.ser.inWaiting() > 5:
			#print(self.ser.inWaiting())
			out += self.ser.read(1)
		if out != '':
			print(out)


	#sets up the connection with the TNC without making a link
	def Setup_Modem(self):
		cfg = self.parse_config()
		self.ser = serial.Serial(
			port=cfg['Serial']['SERIAL_Port'],
			baudrate=cfg['Serial']['ABAUD'],
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
			)
		return self.ser

	#Displays the current settings of the TNC
	def get_Modem_State(self):
		out = ''
		self.ser = self.Setup_Modem()
		self.ser.write('DISPLAY' + '\r')
		time.sleep(5)
		while self.ser.inWaiting() > 5:
			out += self.ser.read(1)
		if out != '':
			print("\nThe current settings:\n" + out)

	def Check_Consistency(self):
		pass

if __name__ == "__main__":
	mymodem=Modem()
	mymodem.Switch_Port()
	mymodem.get_Modem_State()
	#print(mymodem.cfg)
	#mymodem.__init__()




















