# Copyright 2013 Jie Ding

#this file define the SINE protocol, including message format and packet extraction

import struct
import time
from packet_utils       import *

from packet_base import packet_base


#DJ+++ 20131202
class sine(packet_base):
    "SINE packet struct"
    MIN_LEN = 4 #length of (type,length,flag)
    NID_LEN = 16
    SID_LEN = 20

    TYPE_SER_REG = 1  #sercice registration/update
    TYPE_CAP_REG = 2  #capability registration/update
    TYPE_SER_REQ = 3  #service request
    TYPE_SER_DAT = 4  #service data
    TYPE_CON_MSG = 5  #control message

    TYPE_TLV_CPU  = 1
    TYPE_TLV_MEM  = 2
    TYPE_TLV_DISK = 3
    TYPE_TLV_LINK = 4
    TYPE_TLV_IP   = 5
    TYPE_TLV_MAC  = 6
    TYPE_TLV_PORT = 7

    #min length dictionary of all the message types
    MIN_LEN_DICT = {
      TYPE_SER_REG:40,  
      TYPE_CAP_REG:20,  
      TYPE_SER_REQ:40,  
      TYPE_SER_DAT:56,
      TYPE_CON_MSG:20
    }

    FLAG_REG_REQ = 0x00  #refer to 973 scheme version 1.0
    FLAG_REG_ACK = 0x40
    FLAG_UPD_REQ = 0x80
    FLAG_UPD_ACK = 0xC0

    def __init__(self, raw=None, prev=None, **kw):
        print "DJ---/pox/lib.packet_sine.py class sine __init__!"
        packet_base.__init__(self)

        self.prev = prev

        #header information
        self.type   = 0
        self.length = 0 #including header
        self.flag   = 0

        #all information to be used in SINE
        self.sid    = None
        self.srcnid = None
        self.dstnid = None
        self.sbd    = None 
        self.nbd    = None
        self.nid = None
        self.swnid = None
        self.port = None # the port of the nearby router connected with server
        self.ip = None
        self.mac = None

        self.next   = b''

        if raw is not None:
            self.parse(raw)

    def parse_tlv(self, tlv):
        (tlv_t, tlv_l) = struct.unpack('!BB', tlv)
        #get value
        tlv_v = tlv[2:tlv_l]
        next = tlv[tlv_l:]
        return (tlv_t, tlv_l, tlv_v, next)

#DJ++ 20121203
    def parse(self, raw):
        assert isinstance(raw, bytes)
        #self.raw = raw 20140116 by dj
        dlen = len(raw)
        if dlen < sine.MIN_LEN:
            self.msg('warning SINE packet data too short to parse header: data len %u' % (dlen,))
            return
        print "DJ---/pox/lib/packet/packet_sine.py received ",dlen,"bytes"

        (self.type,self.length,self.flag) \
             = struct.unpack('!BHB', raw[:sine.MIN_LEN])

        # At this point, sine is parsed
        # each type of sine packets should then be parsed respectively
        self.parsed = True
        self.next = raw[self.MIN_LEN:dlen]

        if self.type == sine.TYPE_SER_REG: # sercice registration/update
            #DJ++ 20131218
            #due to the length of SID and NID, we get data in the format of string
            (self.sid, self.nid) = struct.unpack('!20s16s',self.next)
            print "DJ---/pox/lib/packet/packet_sine.py parse sine ", \
                self.type, self.length, self.flag, self.sid, self.nid

        elif self.type == sine.TYPE_CAP_REG:
            self.nid = struct.unpack('!16s',self.next)
            self.nbd = raw[self.MIN_LEN+NID_LEN:dlen]
                
        elif self.type == sine.TYPE_SER_REQ:
            pass #TODO
        elif self.type == sine.TYPE_SER_DAT:
            pass #TODO
        elif self.type == sine.TYPE_CON_MSG:
            pass #TODO
        else:
            self.msg('warning SINE packet type error')


    def hdr(self):

        buf = struct.pack('!BHB', self.type,self.length,self.flag)

        if self.type == sine.TYPE_SER_REG:
            buf = buf + self.sid + self.nid
        elif self.type == sine.TYPE_CAP_REG:
            pass #TODO
        elif self.type == sine.TYPE_SER_REG:
            pass #TODO
        elif self.type == sine.TYPE_SER_DAT:
            pass #TODO
        elif self.type == sine.TYPE_CON_MSG:
            pass #TODO
        else:
            self.msg('warning SINE packet type error')
        return buf
