# Copyright 2013 Jie Ding

'''
In this file, you can define your own sine class and sine event source for further deployment.
'''

# Import some POX stuff
from pox.core import core                     # Main POX object
#import pox.openflow.libopenflow_01 as of      # OpenFlow 1.0 library
#import pox.lib.packet as pkt                  # Packet parsing/construction
#from pox.lib.addresses import EthAddr, IPAddr # Address types
#import pox.lib.util as poxutil                # Various util functions
from pox.lib.revent import *              # Event library
#import pox.lib.recoco as recoco               # Multitasking library

# Create a logger for this component
log = core.getLogger()

#DJ++ 20131217


#DJ++ START 20131223
class Collect_serInfo(Event):
  def __init__(self, connection, inport, sinein_event):
    print "DJ---/pox/sine/__init__.py Event Colect_serInfo initiates!"
    Event.__init__(self)
    self.connection = connection
    self.dpid = connection.dpid
    self.inport = inport
    self.sine_packet = sinein_event.parsed
    self.connection = sinein_event.connection
    self.sid = self.sine_packet.sid
    self.nid = self.sine_packet.nid

class sine_event(EventMixin):

  _eventMixin_events = set([
    Collect_serInfo,
  ])

  def __init__ (self):
    print "DJ---/pox/sine/__init__.py Event class sine_event initiates!", self

  def method(self, arguments):
    pass
#DJ++ END 20131223


def _go_up (event):
  #print "DJ---/pox/sine/__init__.py _go_up!"
  log.info("Module sine is going up!")


def launch ():
  """
  The default launcher just logs its arguments
  """

  #log.warn("Foo: %s (%s)", foo, type(foo))
  #log.warn("Bar: %s (%s)", bar, type(bar))

  core.addListenerByName("UpEvent", _go_up)
  core.registerNew(sine_event) #DJ++ 20121223

