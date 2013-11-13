import re
import getopt
import sys
import socket
import struct

ONKYO_KEYS_ARROW = ["UP","DOWN","LEFT","RIGHT"]
ONKYO_KEYS_HEX = ["0x%02x" % x for x in range(255)]
ONKYO_KEYS_NUMERIC = ["0","1","2","3","4","5","6","7","8","9"]
ONKYO_KEYS_ACTION = ["ENTER", "EXIT"]
ONKYO_KEYS_MEDIA_ACTION_BASIC = ["PLAY", "STOP","PAUSE", "FF", "REW"]
ONKYO_KEYS_TEST_KEY = ["TEST"]
ONKYO_KEYS_CHANNEL_SELECT = ["CHSEL"]
ONKYO_KEYS_TG = ["TG"]
ONKYO_KEYS_POWER_BASIC = ["POWER"]
ONKYO_KEYS_POWER_EXTENDED = ["PWRON", "PWROFF"]

ONKYO_COMMANDS = [
{'class': 'Amplifier','keys': [], 'cmd': 'PWR', 'string': 'Power'},
{'class': 'Amplifier','keys': [], 'cmd': 'AMT', 'string': 'Audo Mute'},
{'class': 'Amplifier','keys': [], 'cmd': 'SPA', 'string': 'Speaker A'},
{'class': 'Amplifier','keys': [], 'cmd': 'SPB', 'string': 'Speaker B'},
{'class': 'Amplifier','keys': [], 'cmd': 'MVL', 'string': 'Master Volume'},
{'class': 'Amplifier','keys': [], 'cmd': 'SLP', 'string': 'Sleep Set'},
{'class': 'Amplifier','keys': [], 'cmd': 'SLC', 'string': 'Speaker Level Calibration'},
{'class': 'Amplifier','keys': [], 'cmd': 'SWL', 'string': 'Subwoofer Level'},
{'class': 'Amplifier','keys': [], 'cmd': 'DIF', 'string': 'Display Information'},
{'class': 'Amplifier','keys': [], 'cmd': 'DIM', 'string': 'Dimmer Level'},
{'class': 'Amplifier','keys': [], 'cmd': 'OSD', 'string': 'Setup'},
{'class': 'Amplifier','keys': [], 'cmd': 'MEM', 'string': 'Memory Setup'},
{'class': 'Unit','keys': [], 'cmd': 'SLI', 'string': 'Input Select'},
{'class': 'Unit','keys': [], 'cmd': 'SLR', 'string': 'RECOUT Selector'},
{'class': 'Unit','keys': [], 'cmd': 'SLA', 'string': 'Audio Selector'},
{'class': 'Unit','keys': [], 'cmd': 'TGA', 'string': '12v Trigger A'},
{'class': 'Unit','keys': [], 'cmd': 'TGB', 'string': '12v Trigger B'},
{'class': 'Unit','keys': [], 'cmd': 'TGC', 'string': '12v Trigger C'},
{'class': 'Unit','keys': [], 'cmd': 'VOS', 'string': 'Video Output Select'},
{'class': 'Unit','keys': [], 'cmd': 'HDO', 'string': 'HDMI Output Select'},
{'class': 'Unit','keys': [], 'cmd': 'RES', 'string': 'Monitor Out Resolution'},
{'class': 'Surround','keys': [], 'cmd': 'LMD', 'string': 'Listening Mode'},
{'class': 'Surround','keys': [], 'cmd': 'LTN', 'string': 'Late Night'},
{'class': 'Surround','keys': [], 'cmd': 'RAS', 'string': 'Re-EQ'},
{'class': 'Tuner','keys': [], 'cmd': 'TUN', 'string': 'Tuning'},
{'class': 'Tuner','keys': [], 'cmd': 'PRS', 'string': 'Preset'},
{'class': 'Tuner','keys': [], 'cmd': 'RDS', 'string': 'RDS Information'},
{'class': 'Tuner','keys': [], 'cmd': 'PTS', 'string': 'PTY Scan'},
{'class': 'Tuner','keys': [], 'cmd': 'XCH', 'string': 'XM Channel'},
{'class': 'Tuner','keys': [], 'cmd': 'TPS', 'string': 'TP Scan'},
{'class': 'Tuner','keys': [], 'cmd': 'XCN', 'string': 'XM Channel Name'},
{'class': 'Tuner','keys': [], 'cmd': 'XAT', 'string': 'XM Artist'},
{'class': 'Tuner','keys': [], 'cmd': 'XTI', 'string': 'XM Title'},
{'class': 'Tuner','keys': [], 'cmd': 'XCT', 'string': 'XM Category'},
{'class': 'Tuner','keys': [], 'cmd': 'SCN', 'string': 'SIRIUS Channel Name'},
{'class': 'Tuner','keys': [], 'cmd': 'SAT', 'string': 'SIRIUS Artist'},
{'class': 'Tuner','keys': [], 'cmd': 'STI', 'string': 'SIRIUS Title'},
{'class': 'Tuner','keys': [], 'cmd': 'SCH', 'string': 'SIRIUS Channel'},
{'class': 'Tuner','keys': [], 'cmd': 'SCT', 'string': 'SIRIUS Category'},
{'class': 'Tuner','keys': [], 'cmd': 'SLK', 'string': 'SIRIUS Parentel Lock'},
{'class': 'Tuner','keys': [], 'cmd': 'HAT', 'string': 'HD Radio Artist'},
{'class': 'Tuner','keys': [], 'cmd': 'HCN', 'string': 'HD Radio Channel Name'},
{'class': 'Tuner','keys': [], 'cmd': 'HTI', 'string': 'HD Radio Title'},
{'class': 'Tuner','keys': [], 'cmd': 'HDS', 'string': 'HD Radio Detail'},
{'class': 'Tuner','keys': [], 'cmd': 'HPR', 'string': 'HD Radio Channel Program'},
{'class': 'Tuner','keys': [], 'cmd': 'HBL', 'string': 'HD Radio Blend Mode'},
{'class': 'Tuner','keys': [], 'cmd': 'HTS', 'string': 'HD Radio Tuner Status'},
{'class': 'Net Tuner','keys': [], 'cmd': 'NTC', 'string': 'Net Tune'},
{'class': 'CD Player','keys': [], 'cmd': 'CCD', 'string': 'CD Player'},
{'class': 'CD Player','keys': [], 'cmd': 'CT1', 'string': 'Tape 1'},
{'class': 'CD Player','keys': [], 'cmd': 'CT2', 'string': 'Tape 2'},
{'class': 'CD Player','keys': [], 'cmd': 'CEQ', 'string': 'Graphics Equalizer'},
{'class': 'CD Player','keys': [], 'cmd': 'CDT', 'string': 'DAT Recorder'},
{'class': 'RI System','keys': [], 'cmd': 'CDV', 'string': 'DVD Player'},
{'class': 'RI System','keys': [], 'cmd': 'CMD', 'string': 'MD Recorder'},
{'class': 'RI System','keys': [], 'cmd': 'CCR', 'string': 'CR-R Recorder'},

{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'ZPW', 'string': 'Zone 2 Power'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'ZMT', 'string': 'Zone 2 Mute'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'ZVL', 'string': 'Zone 2 Volume'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'SLZ', 'string': 'Zone 2 Selector'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'TUZ', 'string': 'Zone 2 Tuning'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'PRZ', 'string': 'Zone 2 Preset'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'NTZ', 'string': 'Zone 2 Net Tune'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'LMZ', 'string': 'Zone 2 Listening Mode'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'LTZ', 'string': 'Zone 2 Late Night'},
{'class': 'Zone 2 Amplifier','keys': [], 'cmd': 'RAZ', 'string': 'Zone 2 Re-EQ'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'PW3', 'string': 'Zone 3 Power'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'MT3', 'string': 'Zone 3 Mute'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'VL3', 'string': 'Zone 3 Volume'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'SL3', 'string': 'Zone 3 Selector'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'TU3', 'string': 'Zone 3 Tune'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'PR3', 'string': 'Zone 3 Preset'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'NT3', 'string': 'Zone 3 Net Tune'},
{'class': 'Zone 3 Amplifier','keys': [], 'cmd': 'CDS', 'string': 'Dock'}]



ISCP_RECEIVER = 0x01

ISCP_SERIAL = 0x00
ISCP_ETHERNET = 0x01

ISCP_VERSION = 0x01

class ISCP:
	def __init__(self, transport=ISCP_SERIAL):
		self.transport = transport
		self.fd = None
		pass

	def connect(self, port):
		if self.transport == ISCP_SERIAL:
			pass
		elif self.transport == ISCP_ETHERNET:
			if len(port.split(":")) > 1:
				self.host = port.split(":")[0]
				self.port = port.split(":")[1]
			else:
				self.host = port
				self.port = 60128	
			self.fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.fd.connect((self.host, self.port))
		else:
			raise "unknown ISCP transport"

	def iscp_send(self,dat):
		if self.transport == ISCP_SERIAL:
			pass
		elif self.transport == ISCP_ETHERNET:
			t = struct.pack(">ccccIIBBBB",'I','S','C','P',0x10,len(dat),ISCP_VERSION,0,0,0)
                        self.fd.send(t+dat)

	def iscp_recv(self):
		buff = ""		

		sig = self.fd.recv(4)
		(hlen) = struct.unpack(">I",self.fd.recv(4))[0]
		(dlen) = struct.unpack(">I",self.fd.recv(4))[0]
		ver = ord(self.fd.recv(1))
		reserved = self.fd.recv(3)

		if (str(sig) == "ISCP") & (ver == 0x01):
			return self.fd.recv(dlen)

	def iscp_parse(self,line):
		m = re.match(r"!(\d)(...)([a-z|A-Z|0-9]*)", line)
		if m:
	                for c in ONKYO_COMMANDS:
	                        if c['cmd'] == m.groups()[1]:
	                                profile = c
					return (c,m.groups()[1],m.groups()[2])

		return 0

	def iscp_cmd(self, target,command, value=None):
	
		profile = None

		for m in ONKYO_COMMANDS:			
			if m['string'] == command:
				profile = m
	
		if profile:
			if value == None:
				tvalue = "QSTN"
			else:
				tvalue = value

			t =  "!%d%s%s\r\n" % (target,profile['cmd'],tvalue) 
			self.iscp_send(t)

			if value == None: #get results of query
				return self.iscp_recv()




def usage():

	currentclass = ""
	for v in ONKYO_COMMANDS:
		if v['class'] != currentclass:
			currentclass = v['class']
			print "%s:" % currentclass
		print "\t\"%s\"" % v['string']


if __name__ == "__main__":

    
	try:
		opts, args = getopt.getopt(sys.argv[1:], "lt:h:c:v:p:", ["help", "output="])
	except getopt.GetoptError, err:
		print str(err) 
		usage()
		sys.exit(2)
    
	output = None
	verbose = False
	host = "192.168.1.121"
	port = "/dev/ttyUSB0"
	transport = ISCP_ETHERNET
	command = "Power"
	value = ""
	dousage = 1

	for o, a in opts:
		dousage = 0 				#ok.. we wont spam because your using an option
		if o == "-v":				#value
			value = a
		elif o == "-h":				#host
			host = a
		elif o in ("-l", "--list"):		#list commands
			for i in ONKYO_COMMANDS:
				print "\"%s\"" % i['string']

			sys.exit()
		elif o in ("-c", "--command"):		#command
			command  = a
		elif o in ("-p", "--serial-port"):	#port
			port  = a
		elif o in ("-t", "--transport"):	#transport
			if a in ["ISCP_ETHERNET","ISCP_SERIAL"]:
				if a == "ISCP_ETHERNET":
					transport = 1
				elif a == "ISCP_SERIAL":
					transport = 0
		else:
			usage()
			sys.exit()


	if(dousage):
		usage()


	N = ISCP(transport)
	N.connect(host)
	if value != "":
		N.iscp_cmd(ISCP_RECEIVER,command,value)
		print "done."
	else:
		r = N.iscp_parse(N.iscp_cmd(ISCP_RECEIVER,command))
		print "%s is currently \"%s\"" % (r[0]['string'],r[2])
