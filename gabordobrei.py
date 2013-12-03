#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import sys
import os

class POXBridge( Controller ):
	"Custom Controller class to invoke POX forwarding.l2_learning"
	def start( self ):
		"Start POX learning switch"
		self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]
		self.cmd( self.pox, 'forwarding.l2_learning &' )
	def stop( self ):
		"Stop POX"
		self.cmd( 'kill %' + self.pox )

controllers = { 'poxbridge': POXBridge }

class SingleSwitchTopo(Topo):
	"Single switch connected to n hosts."
	def __init__(self, n=2, **opts):
		# Initialize topology and default options
		Topo.__init__(self, **opts)
		switch = self.addSwitch('s1')
		# Python's range(N) generates 0..N-1
		for h in range(n):
			host = self.addHost('h%s' % (h + 1))
			self.addLink(host, switch)


def simpleTest(size):
	"Create and test a simple network"
	topo = SingleSwitchTopo(n=size)
	net = Mininet(topo)
	net.start()
	""".
	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	print "Testing network connectivity"
	net.pingAll()
	"""



	net.stop()

if __name__ == '__main__':
	# Tell mininet to print useful information
	setLogLevel('info')
	simpleTest(int(sys.argv[1]))
