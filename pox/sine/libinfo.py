#libinfo.py by Jie Ding 
#This file for information collection and maintainance 
#Refer to l3_learning.py

#import modules
from pox.core import core
import pox
log = core.getLogger()

from pox.sine.libmysql import dbop
from pox.lib.packet.packet_sine import sine #some constant defined in class sine
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of

from pox.lib.revent import *
from collections import defaultdict

import time

#This part for constant definition
TIMEOUT = 10#globle timeout value

class info_collector (EventMixin):
  def __init__ (self):
    self.listenTo(core)

  #DJ++ START 20131209
  def _handle_Collect_serInfo (self, event):
    print "DJ---/pox/sine/libinfo.py Entering _handle_Collect_serInfo!", event
    sid = event.sid
    nid = event.nid
    #sbd need to be added
    
    print "DJ---/pox/sine/libinfo.py _handle_Collect_serInfo!", type(sid), repr(sid), type(nid), repr(nid)
    #search table_service if there has already been an entry about this nid and sid
    ret = dbop.pk_select("table_service", sid=sid, nid=nid)
    print "DJ---/pox/sine/libinfo.py Entering _handle_Collect_serInfo! ret = ", ret
    if not ret:
      entries = dbop.insert("table_service", (sid,nid,''))
  #DJ++ END 20140115

  #DJ++ START 20140116
  def _handle_Collect_capInfo (self, event):
    print "DJ---/pox/sine/libinfo.py Entering _handle_Collect_capInfo!", event
    nid = event.nid
    nbd = event.nbd
    flag = event.flag
    #ATTENTION!! TODO DJ 20140116
    dpid = event.dpid 
    #ATTENTION!! IF THIS IS AN HOST CAPABILITY REGISTRATION, DPID SHOULD NOT BE WRITEN INTO DATABAESE

    #NBD parameters
    cpu  = ''
    mem  = ''
    disk = ''
    link = ''
    ip   = ''
    mac  = ''
    port = ''
    
    #node registe for first time
    if flag & sine.FLAG_REG_REQ:
      while nbd:
        (tlv_t, tlv_l, tlv_v, nbd) = self.parse_tlv(nbd)
        if tlv_t == sine.TYPE_TLV_CPU:
          cpu = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_MEM:
          mem = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_DISK:
          disk = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_LINK:
          link = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_IP:
          ip = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_MAC:
          mac = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_PORT:
          port = tlv_v
          continue
        else:
          log.error("TLV Type error when handling capability registration message!")

      #search table_capability if there has already been an entry about this nid
      cap_ret = dbop.pk_select("table_capability", nid=nid)
      if not cap_ret:
        #no duplicate entry, insert into table_capability
        #here,there should be two conditions because of dpid, coz host do not have dpid
        entries = dbop.insert("table_capability", (nid, dpid, cpu, mem, disk))
      
      #insert into table_portinfo  
      if port == '':
        log.debug("Port is an empty string! Give up inserting into table_portinfo!")
        return
      #search table_portinfo if there has already been an entry about this nid and port
      port_ret = dbop.pk_select("table_portinfo", nid=nid, port=port)
      if not port_ret:
        entries = dbop.insert("table_portinfo", (nid, port, ip, mac, link))

    #node information update
    elif flag & sine.FLAG_UPD_REQ:
      #parse tlv
      while nbd:
        (tlv_t, tlv_l, tlv_v, nbd) = self.parse_tlv(nbd)
        if tlv_t == sine.TYPE_TLV_CPU:
          cpu = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_MEM:
          mem = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_DISK:
          disk = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_PORT:
          port = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_LINK:
          link = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_IP:
          ip = tlv_v
          continue
        elif tlv_t == sine.TYPE_TLV_MAC:
          mac = tlv_vi
          continue

      #update
      if cpu:
        ret = dbop.pk_select("table_capability", nid=nid)
        if ret:
          dbop.update("table_capability", pk1=nid, cpu=cpu)
        else:
          log.debug("table_capability update failure!")
      if mem:
        ret = dbop.pk_select("table_capability", nid=nid)
        if ret:
          dbop.update("table_capability", pk1=nid, memory=mem)
        else:
          log.debug("table_capability update failure!")
      if disk:
        ret = dbop.pk_select("table_capability", nid=nid)
        if ret:
          dbop.update("table_capability", pk1=nid, disk=disk)
        else:
          log.debug("table_capability update failure!")
      if port == '':
        log.debug("No port TLV. Give up updating IP/MAC/LINK!")
      else:
        if ip:
          ret = dbop.pk_select("table_portinfo", nid=nid, port=port)
          if ret:
            dbop.update("table_portinfo", pk1=nid, ip=ip)
          else:
            log.debug("table_portinfo update failure!")
        if mac:
          ret = dbop.pk_select("table_portinfo", nid=nid, port=port)
          if ret:
            dbop.update("table_portinfo", pk1=nid, mac=mac)
          else:
            log.debug("table_portinfo update failure!")
        if link:
          ret = dbop.pk_select("table_portinfo", nid=nid, port=port)
          if ret:
            dbop.update("table_portinfo", pk1=nid, link=link)
          else:
            log.debug("table_portinfo update failure!")
          


    print "DJ---/pox/sine/libinfo.py leaving  _handle_Collect_capInfo!"
  #DJ++ END 20140116

  def _handle_GoingUpEvent (self, event):
    print "DJ---/pox/sine/libsine.py _handle_GoingUpEvent!"
    #self.listenTo(core.openflow)#listen to SINEIn
    self.listenTo(core.sine_event) #DJ++ 20131223
    log.debug("Up...")


  #DJ++ START 20131209
  #def _handle_BarrierIn (self, event):
  #  print "DJ---l3_learning _handle_BarrierIn!"
  #DJ++ END   20131209

def launch ():
  print "DJ---/pox/sine/libsine.py launch!"
  core.registerNew(info_collector)

