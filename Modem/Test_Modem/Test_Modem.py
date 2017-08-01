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
		self.ser = serial.Serial(port = "COM3")
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
	
	def test_Reboot(self):
		cfg = self.test_parse_config()
		self.ser.write(cfg['Calabration']['RESTORE DEFAULT'])
		time.sleep(8)
		self.ser.write('*')
		time.sleep(1)
		self.ser.write(cfg['Startup']['MYCALL'])
		self.test__init__()

		#Takes the known settings and confirms that the settings will match
###############################################
class test_Port:
	pass
	
	




"""if __name__ == "__main__":
	mymodem=test_Modem()
	mymodem.setUp()
	#print(mymodem.cfg)
	#mymodem.__init__()"""
"""BKONDEL  ON
BLT      
1 EVERY 00:00:00/EVERY 00:00:00
2 EVERY 00:00:00/EVERY 00:00:00
3 EVERY 00:00:00/EVERY 00:00:00
4 EVERY 00:00:00/EVERY 00:00:00
BP96     OFF
BREAK    OFF
BTEXT    
BUDLIST  OFF NONE
A/1 Link state is: DISCONNECTED
CANLINE  $18 (CTRL-X)
CANPAC   $19 (CTRL-Y)
CD       INTERNAL/INTERNAL
CHECK    0/0
CMDTIME  1 (1 sec)
CMSG     OFF/OFF
COMMAND  $03 (CTRL-C)
CONLIST  OFF NONE
CONMODE  CONVERS
CONOK    ON/ON
CONPERM  OFF
CPACTIME OFF
CR       ON
CRSUP    OFF
CSTAMP   OFF
CTEXT    
CWID     EVERY 0/EVERY 0
CWIDTEXT DE KI7NUU
DAYTIME  01/01/2001 00:09:06
DAYTWEAK 8
DAYSTR   mm/dd/yyyy hh:mm:ss
DAMA     OFF/OFF
DAMACHCK 18/18 (180/180 sec)
DBLDISC  OFF
DELETE   $08 (CTRL-H)
DIGIPEAT ON/ON
DWAIT    0/0
ECHO     ON
EQUALIZE 115
ESCAPE   OFF
FLOW     ON
FILTER   OFF
FRACK    4/4 (4/4 sec)
FULLDUP  OFF/OFF
GPSHEAD  
1 $GPGGA
2 
3 
4 
GPSINIT  
GPSTIME  VALID RMC
HBAUD    1200/9600
HEADERLN ON
HID      ON/ON
HTEXT    
INTFACE  TERMINAL
KNTIMER  15
KNXCON   OFF
LCOK     ON
LFADD    OFF
LFSUP    OFF
LLIST    OFF NONE
LT       
1 
2 
3 
4 
LTP      
1 GPS/GPS
2 GPS/GPS
3 GPS/GPS
4 GPS/GPS
LTRACK   0
MONITOR  ON/ON
MALL     ON/ON
MAXFRAME 4/4
MAXUSERS 10/10
MBEACON  ON/ON
MCON     OFF/OFF
MCOM     ON/ON
MHEADER  ON/ON
MRESP    ON/ON
MRPT     ON/ON
MSTAMP   OFF
MXMIT    ON/ON
MYCALL   KI7NUU/KI7NUU
MYALIAS  disabled/disabled
MYDGPS   disabled
MYDROP   0/1
MYGATE   KI7NUU-3
MYNODE   KI7NUU-7
MYPBBS   KI7NUU-1
MYPAGE   disabled
MYREMOTE disabled
NDWILD   OFF
NEWMODE  ON
NETCALL  disabled
NETALIAS /
NETBUFFS 32
NETCIRCS 5
NETDESTS 25
NETLINKS 10
NETROUTE 5
NETUSERS 5/5
NOMODE   OFF
NTEXT    
NUMNODES 0
ONERADIO OFF
PACLEN   128/128
PACTIME  AFTER 10
PAGECWID ON
PAGEDIR  0
PAGELOG  0
PAGEMON  OFF
PAGEPRIV OFF
PAGEPSWD 
PAGETEXT 
PAGEXINV OFF
PASS     $16 (CTRL-V)
PASSALL  OFF/OFF
PBBS     480
PBFORWRD NONE  PORT1  EVERY 0 (disabled)
PBHEADER ON
PBHOLD   ON
PBKILLFW ON
PBLIST   OFF NONE
PBLO     NEW VARIABLE
PBMAIL   OFF
PBPERSON OFF
PBREVERS OFF
PBSIZE   0
PBUSERS  1
PERSIST  63/63 (25%/25%)
PID      OFF/OFF
PMODE    CMD
PORT     1
PTEXT    
RANGE    0:255/0:255/0:255/0:255/0:255
REDISPLA $12 (CTRL-R)
RELINK   OFF/OFF
RETRY    10/10
RING     ON
RNRTIME  0
RTEXT    
SCREENL  0
SENDPAC  $0D (CTRL-M)
SLOTTIME 10/10 (100/100 msec)
START    $11 (CTRL-Q)
STOP     $13 (CTRL-S)
STREAMSW $7C (|)
STREAMCA OFF
STREAMEV OFF
SUPLIST  OFF NONE
SWP      17,17,108
TELEMTRY 0/0
TRACE    OFF/OFF
TRFLOW   OFF
TRIES    10
TXDELAY  30/30 (300/300 msec)
TXFLOW   OFF
UNPROTO  CQ/CQ
UIDIGI   OFF NONE/OFF NONE
UIDUPE   0/0
UIDWAIT  OFF/OFF
UIFLOOD  disabled,30,NOID/disabled,30,NOID
UIGATE   OFF/OFF
UITRACE  disabled,30/disabled,30
USERS    1/1
XFLOW    ON
XKCHKSUM OFF
XKPOLLED OFF
XMITLVL  100/64
XMITOK   ON/ON
XOFF     $13 (CTRL-S)
XON      $11 (CTRL-Q)
cmd:"""
