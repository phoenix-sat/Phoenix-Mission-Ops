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
		#Links to the TNC
##################################################
		self.ser = serial.Serial(
			port=cfg['Serial']['SERIAL_Port'],
			baudrate=cfg['Serial']['ABAUD'],
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
			)
		self.ser.close()
		self.ser.open()
#################################################

		#Sets the settings to the desired values
#################################################
		count = len(cfg['Startup']['Terminal'])
		out = ''
		while count > 0:
			self.ser.write(cfg['Startup']['Terminal'][count - 1])
			self.ser.write('\r')
			count = count - 1
#################################################		

		#Displays the current settings
#################################################
		self.ser.write('DISPLAY' + '\r')
		time.sleep(5)
		while self.ser.inWaiting() > 0:
			out += self.ser.read(1)
		if out != '':
			print(">>" + out)
#################################################

	
	def Reboot(self):
		cfg = self.parse_config()
		self.ser.write(cfg['Calabration']['RESTORE DEFAULT'])
		time.sleep(8)
		self.ser.write('*')
		time.sleep(1)
		self.ser.write(cfg['Startup']['MYCALL'])
		self.__init__()
		
		


if __name__ == "__main__":
	mymodem=Modem()
	#print(mymodem.cfg)
	#mymodem.__init__()
