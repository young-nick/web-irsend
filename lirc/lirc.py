from subprocess import call
import re
import shlex

class Lirc:
	"""
	Parses the lircd.conf file and can send remote commands through irsend.
	"""
	codes = {}
	
	def __init__(self, conf):
		# Parse the config file
		self.parse(conf)
		

	def devices(self):
		"""
		Return a dict of devices.
		"""
		return self.codes
	
	
	def parse(self,conf):
		"""
		Parse the lircd.conf config file and create a dictionary.
		"""
		remote_name = None
		code_section = False
		print "Opening %s" % conf
		conf = open(conf, "rb")
		
		for line in conf:
			# Convert tabs to spaces
			l = line.replace('\t',' ')
			#print l
			# Skip comments
			if re.match('^\s*#',line):
				continue
			
			split_l =  shlex.split(l)

			if split_l and split_l[0] == 'include':
				#print "Found an include for %s" % split_l[1]
				filename = split_l[1].strip()
				
				self.parse(split_l[1])


			# Look for a 'begin remote' line
			if l.strip()=='begin remote':
				# Got the start of a remote definition
				remote_name = None
				code_section = False
					
			elif not remote_name and l.strip().find('name')>-1:
				# Got the name of the remote
				remote_name = l.strip().split(' ')[-1]
				if remote_name not in self.codes:
					self.codes[remote_name] = {}
				
			elif remote_name and l.strip()=='end remote':
				# Got to the end of a remote definition
				remote_name = None
				
			elif remote_name and l.strip()=='begin codes':
				code_section = True

			elif remote_name and l.strip()=='end codes':
				code_section = False
				
			elif remote_name and code_section:
				# Got a code key/value pair... probably
				fields = l.strip().split(' ')
				self.codes[remote_name][fields[0]] = fields[-1]
 		conf.close()


			
	def send_once(self, device_id, message):
		"""
		Send single call to IR LED.
		"""

		#print "about to call 'irsend -d /dev/lircd1 SEND_ONCE %s %s'" % (device_id, message)
		call(['irsend', 'SEND_ONCE', device_id, message])

				
if __name__ == "__main__":
	lirc = Lirc('/etc/lirc/lircd.conf')
	
	
