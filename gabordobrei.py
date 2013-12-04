#!/usr/bin/python
# coding=utf-8

import sys
import os

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import lg, info
from mininet.node import Controller
from random import randint
from array import array
import re
import sqlite3


class ShortestWidestProxyController( Controller ):
	def start( self ):
		self.pox = '%s/pox/pox.py' % os.environ[ 'HOME' ]
		#self.cmd( self.pox, 'policy_routing.shortest_widest &' )
		self.cmd( self.pox, 'forwarding.l2_learning &' )
	def stop( self ):
		self.cmd( 'kill %' + self.pox )

controllers = { 'shortestwidest': ShortestWidestProxyController }


class generateTopoFromArrays(Topo):
	def __init__(self, hosts, switches, links, **opts):
		# Initialize topology and default options
		Topo.__init__(self, **opts)

		for s in switches:
			self.addSwitch(s)

		for h in hosts:
			self.addHost(h)
		
		for l in links:
			self.addLink(l[0], l[1])

def setupTopoLinks( topo, links ):
	for l in links:
		topo.setlinkInfo(l[0], l[1], l[2])


def createHost(i): return 'h%s' % (i+1)
def createSwitch(i): return 's%s' % (i+1)
def createRandomLink(h, switches): return (h, switches[randint(0, len(switches)-1)], (randint(1, 5)*10))

def createNetworkAndSaveToDB(n, conn):
	
	c = conn.cursor()
	c.execute('''DROP TABLE IF EXISTS size''')
	c.execute('''CREATE TABLE IF NOT EXISTS size (s integer, name text)''')
	c.execute("INSERT INTO size VALUES (?, 'switch')", [n])
	c.execute("INSERT INTO size VALUES (?, 'host')", [3*n])
	
	c.execute('''DROP TABLE IF EXISTS links''')
	c.execute('''CREATE TABLE IF NOT EXISTS links (left_id text, right_id text, bw integer)''')

	switches = map(createSwitch, range(n))
	hosts = map(createHost, range(n*3))
	links = []

	for i in switches:
		for j in range(i):
			links.append((switches[i], switches[j], 80+randint(0,4)*10))
	
	for h in hosts:
		links.append(createRandomLink(h, switches))
	
	for l in links:
		c.execute("INSERT INTO links VALUES (?, ?, ?)", [l[0], l[1], l[2]])

	conn.commit()

	conn.close()
	return switches, hosts, links

def simpleTest(n, k = 0):

	switches, hosts, links = createNetworkAndSaveToDB(n = n, conn = sqlite3.connect('network.db'))

	topo = generateTopoFromArrays(hosts = hosts, switches = switches, links = links)
	net = Mininet( topo=topo, controller=ShortestWidestProxyController, cleanup=True)

	net.start()
	#dumpNodeConnections(net.hosts)
	
	setupTopoLinks( topo, links )

	for l in links: print l[0], "<--", topo.linkInfo(l[0], l[1]) , "-->", l[1]
	#real_hosts = net.hosts
	#for h in real_hosts: print h.name, ": ", h.IP()
	#for sw in net.switches: print sw.name, ": ", sw.IP()
		
	net.pingAll()

	net.stop()

if __name__ == '__main__':
	lg.setLogLevel('info')
	simpleTest(int(sys.argv[1]))
