# coding=utf-8
from pox.core import core
import pox.openflow.libopenflow_01 as of
import re
import sqlite3

log = core.getLogger()

class ShortesWidestPolicyController (object):
	def __init__ (self, connection, hosts, switches, links):
		self.connection = connection
		connection.addListeners(self)

	def SWDecision(sw,h):
		# 1) Dijkstra's algorithm: every links weight is 1
		# 2) List only inportent routes
		# 2.a) If there is only 1 minimum => return
		# 2.b) Multipule minimum => iterate over every minimum route
		#		maximum(minimum(bw)) => return
		
							
	def send_packet (self, buffer_id, raw_data, out_port, in_port):
		#Sends a packet out of the specified switch port.
		msg = of.ofp_packet_out()
		msg.in_port = in_port
		msg.data = raw_data
		# Add an action to send to the specified port
		action = of.ofp_action_output(port = out_port)
		msg.actions.append(action)
		# Send message to switch
		self.connection.send(msg)

	def _handle_PacketIn (self, event):
		# This is the parsed packet data.
		packet = event.parsed
		if not packet.parsed:
			log.warning("Ignoring incomplete packet")
			# The actual ofp_packet_in message.
			return packet_in = event.ofp
		
		self.send_packet(packet_in.buffer_id, packet_in.data, self.shortes_widest_magic[packet.dst], packet_in.in_port)


def createHost(i): return 'h%s' % (i+1)
def createSwitch(i): return 's%s' % (i+1)

def loadNetworkFromDB( conn ):
	c = conn.cursor()
	
	for sizes in c.execute("SELECT s FROM size WHERE name = 'switch'"):
		n = sizes[0]
	
	for sizes in c.execute("SELECT s FROM size WHERE name = 'host'"):
		k = sizes[0]
		
	switches = map(createSwitch, range(n))
	hosts = map(createHost, range(n*k))
	
	c.execute('''CREATE TABLE IF NOT EXISTS links (left_id text, right_id text, bw integer)''')

	for l in c.execute("SELECT left_id, right_id, bw  FROM links"):
		links.append(l)

	conn.commit()

	conn.close()
	return switches, hosts, links

def launch ():
	log.setLevel("DEBUG")	
	
	switches, hosts, links = loadNetworkFromDB( conn = sqlite3.connect('network.db') )
	
	def start_switch (event):
		log.debug("Controlling %s" % (event.connection,))
		ShortesWidestPolicyController(event.connection, switches=switches, hosts=hosts, links=links )

	core.openflow.addListenerByName("ConnectionUp", start_switch)
