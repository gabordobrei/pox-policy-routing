# coding=utf-8
"""
3 darab T1-es, 5 darab T2-es és 7 darab T3-as router van a hálózatban, ill.
minden T3-as routerhez csatlakozik 3-3 hoszt, azaz 21 hoszt.

"""

from mininet.topo import Topo
from array import *

class BGPTopo( Topo ):
	"Simple topology example."

	def __init__( self ):
        	"Create custom topo."

		# Initialize topology
		Topo.__init__( self )

		# Add hosts and switches
		for i in range(1,6):
			self.addSwitch( 'sw_T1_%d' % i )
			
			for a in range(1,i):
				self.addLink( 'sw_T1_%d' % i, 'sw_T1_%d' % a )
			
			for j in range (0,2):
				self.addSwitch( 'sw_T2_%d' % (2*i-j) )
				self.addLink('sw_T2_%d' % (2*i-j), 'sw_T1_%d' % i)
				
				for k in range(0,4):
					self.addSwitch( 'sw_T3_%d' % (4*i - k) )
					self.addLink('sw_T3_%d' % (4*i - k), 'sw_T2_%d' % (2*i-j))
					
		for i in range(1,21):
			self.addHost( 'h_%d' % (2*i-1) )
			self.addHost( 'h_%d' % (2*i) )
			self.addLink('sw_T3_%d' % i, 'h_%d' % (2*i-1) )
			self.addLink('sw_T3_%d' % i, 'h_%d' % (2*i) )


topos = { 'bgp': ( lambda: BGPTopo() ) }