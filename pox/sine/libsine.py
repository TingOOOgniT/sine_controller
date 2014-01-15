#Jie Ding 
#This file for protocol handling 
#Refer to l3_learning.py

#import modules
from pox.core import core
import pox
log = core.getLogger()

from pox.sine import libmysql #DJ++ 20140114 
from pox.sine import * #DJ++ 20131225
from pox.lib.packet.packet_sine import sine #some constant defined in class sine
from pox.lib.packet.ipv4 import ipv4
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import str_to_bool, dpid_to_str
from pox.lib.recoco import Timer

import pox.openflow.libopenflow_01 as of

from pox.lib.revent import *
from collections import defaultdict

import time

#This part for constant definition
TIMEOUT = 10#globle timeout value


class sine_switch (EventMixin):
  def __init__ (self):
    # (dpid,IP) -> [(expire_time,buffer_id,in_port), ...]
    # These are buffers we've gotten at this datapath for this IP which
    # we can't deliver because we don't know where they go.
    self.lost_buffers = {}

    self.listenTo(core)

  def _send_lost_buffers (self, dpid, ipaddr, macaddr, port):
    """
    We may have "lost" buffers -- packets we got but didn't know
    where to send at the time.  We may know now.  Try and see.
    """
    if (dpid,ipaddr) in self.lost_buffers:
      # Yup!
      bucket = self.lost_buffers[(dpid,ipaddr)]
      del self.lost_buffers[(dpid,ipaddr)]
      log.debug("Sending %i buffered packets to %s from %s"
                % (len(bucket),ipaddr,dpid_to_str(dpid)))
      for _,buffer_id,in_port in bucket:
        po = of.ofp_packet_out(buffer_id=buffer_id,in_port=in_port)
        po.actions.append(of.ofp_action_dl_addr.set_dst(macaddr))
        po.actions.append(of.ofp_action_output(port = port))
        core.openflow.sendToDPID(dpid, po)

  #DJ++ START 20131209
  def _handle_SINEIn (self, event):
    #print "DJ---/pox/sine/libsine.py Entering _handle_SINEIn!" ,self
    print "DJ---/pox/sine/libsine.py Entering _handle_SINEIn!" ,event
    #print "DJ---/pox/sine/libsine.py Entering _handle_SINEIn!" ,core.openflow.connections
    
    #DJ++ START 20131218
    dpid = event.connection.dpid
    inport = event.port
    packet = event.parsed
    ofp = event.ofp

    connection = event.connection
    
    if not packet.parsed:
      log.warning("%i %i ignoring unparsed packet", dpid, inport)
      return

    type = packet.type
    length = packet.length
    flag = packet.flag
    print "DJ---/pox/sine/libsine.py _handle_SINEIn!TLF:", type, length, flag
    
    if type == sine.TYPE_SER_REG: # sercice registration/update
      nid = packet.nid
      sid = packet.sid
      print "DJ---/pox/sine/libsine.py _handle_SINEIn! ", repr(sid), repr(nid)
      #e = connection.ofnexus.raiseEventNoErrors(Collect_serInfo, connection, inport, event)
      #if e is None or e.halt != True:#false
        #connection.raiseEventNoErrors(Collect_serInfo, connection, inport, event)
      core.sine_event.raiseEventNoErrors(Collect_serInfo, connection, inport, event)

    elif type == sine.TYPE_CAP_REG:
      pass #TODO
    elif type == sine.TYPE_SER_REQ:
      pass #TODO
    elif type == sine.TYPE_SER_DAT:
      pass #TODO
    elif type == sine.TYPE_CON_MSG:
      pass #TODO
    else:
      log.error("SINE Packet Type Error! Type = %i", type)

    print "DJ---/pox/sine/libsine.py Leaving _handle_SINEIn!" ,event

    #DJ++ END 20131218 20131224
  #DJ++ END   20131209

  def _handle_GoingUpEvent (self, event):
    print "DJ---/pox/sine/libsine.py _handle_GoingUpEvent!"
    self.listenTo(core.openflow)#listen to SINEIn
    #self.listenTo(core.sine) #DJ++ 20131223
    log.debug("Up...")

  #def _handle_BarrierIn (self, event):
  #  print "DJ---l3_learning _handle_BarrierIn!"
  #DJ++ END   20131209

def launch ():
  print "DJ---/pox/sine/libsine.py launch!"
  core.registerNew(sine_switch)

