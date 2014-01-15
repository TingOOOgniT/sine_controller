#This defines MySQL operations

#DJ++ START 20140109 15:38 

import os

from pox.core import core
import MySQLdb
import _mysql_exceptions as DB_EXC
from collections import namedtuple

log = core.getLogger()

#define namedtuples for all four tables
#The designing of tables follows the SINE ER module
tab_cap = namedtuple("table_capability", ("nid", "dpid", "bandwidth"))#need more infomation
tab_ser = namedtuple("table_service", ("sid", "nid"))
tab_pinfo = namedtuple("table_portinformation", ("nid", "port", "ip", "mac"))
tab_topo = namedtuple("table_topology", ("nidsrc", "portsrc", "niddst", "portdst", "distance"))

class sinedb(object):
  '''
  A collection of operations SINE uses to operate MySQL
  '''

  def __init__(self, dbname = "SINE"):
    self.cxn = None
    self.cur = None
    self.dbname = dbname

  #done
  def connect(self): 
    #create connection
    try:
      self.cxn = MySQLdb.connect(db=self.dbname)
    except DB_EXC.OperationalError, e:
      log.exception("Connecting to MySQL failed!",e)

    #create cursor
    self.cur = self.cxn.cursor()
  
  def insert(self, table, *args):
    """
    If you want to insert an entry, you should give the name of the table 
    and give a complete entry, even the column allows "Null".
    Also, you can insert multiple entries.

    EXAMPLE:
    sinedb.insert(table = "table_capability", (nid, dpid, ''))
    Here the third column is for 'bandwidth' which allows "Null", but you still show give a "''".
    """

    if table == "table_capability":
      for entry in args:
        if len(entry) != 5:
          log.error("Inserting to table_capability error! length=",len(entry))
          return
        self.cur.execute(
          "INSERT INTO table_capability VALUES(%s, %s, %s, %s, %s)", entry)
        #TODO:should return something to make certern if operations have been done successfully!
    elif table == "table_service":
      for entry in args:
        if len(entry) != 3:
          log.error("Inserting to table_service error! length=",len(entry))
          return
      self.cur.executemany(
        "INSERT INTO table_service VALUES(%s, %s, %s)", args)
    elif table == "table_portinfo":
      for entry in args:
        if len(entry) != 5:
          log.error("Inserting to table_portinfo error! length=",len(entry))
          return
      self.cur.executemany(
        "INSERT INTO table_portinfo VALUES(%s, %s, %s, %s, %s)", args)
    elif table == "table_topology":
      for entry in args:
        if len(entry) != 5:
          log.error("Inserting to table_topology error! length=",len(entry))
          return
      self.cur.executemany(
        "INSERT INTO table_topology VALUES(%s, %s, %s, %s, %s)", args)

  def update(self, table, pk1, pk2 = None, **kw):
    """
    If you want to update one of the data in table, you should give the primary key and the data
    you want to update.

    Do like the example.
    EXAMPLE:
    sinedb.update(table = "table_service", pk = xxx, sid=xxx, nid=sss)
    pk is for primary key.
    You can give one or more parameter to update the entry in the table.
    """

    if not kw:
      log.warning("Nothing to update to table_capability!")
      return

    #table_capability
    #pk1:nid
    if table == "table_capability":
      for key, value in kw.iteritems():
        #Generally,nid should not be updated
        if key == "nid":
          self.cur.execute(
            "UPDATE table_capability SET nid=%s WHERE nid=%s" % (value, pk1))
          log.warning("Primary key nid is updated!")
        elif key == "dpid":
          self.cur.execute(
            "UPDATE table_capability SET dpid=%s WHERE nid=%s" % (value, pk1))
        elif key == "cpu":
          self.cur.execute(
            "UPDATE table_capability SET cpu=%s WHERE nid=%s" % (value, pk1))
        elif key == "memory":
          self.cur.execute(
            "UPDATE table_capability SET memory=%s WHERE nid=%s" % (value, pk1))
        elif key == "disk":
          self.cur.execute(
            "UPDATE table_capability SET disk=%s WHERE nid=%s" % (value, pk1))
        else:
          log.error("Data type error! Not in table_capability!")
          return
    #table_service 
    #pk1:sid
    #pk2:nid
    elif table == "table_service":
      for key, value in kw.iteritems():
        #Generally,sid and nid should not be updated
        if key == "sid":
          self.cur.execute(
            "UPDATE table_service SET sid=%s WHERE sid=%s AND nid=%s" % (value, pk1, pk2))
          log.warning("Primary key sid is updated!")
        elif key == "nid":
          self.cur.execute(
            "UPDATE table_service SET nid=%s WHERE sid=%s AND nid=%s" % (value, pk1, pk2))
          log.warning("Primary key nid is updated!")
        elif key == "sbd":
          self.cur.execute(
            "UPDATE table_service SET sbd=%s WHERE sid=%s AND nid=%s" % (value, pk1, pk2))
        else:
          log.error("Data type error! Not in table_service!")
          return
    #table_portinfo
    #pk1:nid
    #pk2:port
    elif table == "table_portinfo":
      for key, value in kw.iteritems():
        #Generally,sid and nid should not be updated
        if key == "nid":
          self.cur.execute(
            "UPDATE table_portinfo SET nid=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
          log.warning("Primary key nid is updated!")
        elif key == "port":
          self.cur.execute(
            "UPDATE table_portinfo SET port=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
          log.warning("Primary key port is updated!")
        elif key == "ip":
          self.cur.execute(
            "UPDATE table_portinfo SET ip=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
        elif key == "mac":
          self.cur.execute(
            "UPDATE table_portinfo SET mac=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
        elif key == "band-width":
          self.cur.execute(
            "UPDATE table_portinfo SET band-width=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
        else:
          log.error("Data type error! Not in table_portinfo!")
          return
    #table_topology
    #pk1:nidsrc
    #pk2:portsrc
    elif table == "table_topology":
      for key, value in kw.iteritems():
        #Generally,sid and nid should not be updated
        if key == "nidsrc":
          self.cur.execute(
            "UPDATE table_topology SET nidsrc=%s WHERE nidsrc=%s AND portsrc=%s" % (value, pk1, pk2))
          log.warning("Primary key nidsrc is updated!")
        elif key == "portsrc":
          self.cur.execute(
            "UPDATE table_topology SET portsrc=%s WHERE nidsrc=%s AND portsrc=%s" % (value, pk1, pk2))
        elif key == "niddst":
          self.cur.execute(
            "UPDATE table_topology SET niddst=%s WHERE nidsrc=%s AND portsrc=%s" % (value, pk1, pk2))
          log.warning("Primary key niddst is updated!")
        elif key == "portdst":
          self.cur.execute(
            "UPDATE table_topology SET portdst=%s WHERE nidsrc=%s AND portsrc=%s" % (value, pk1, pk2))
        elif key == "distance":
          self.cur.execute(
            "UPDATE table_topology SET distance=%s WHERE nidsrc=%s AND portsrc=%s" % (value, pk1, pk2))
        else:
          log.error("Data type error! Not in table_topology!")
          return
  

  def delete(self, table, pk1, pk2 = None):
    """
    If you want to delete an entry, you should give the name of the table 
    and give primary key(s).
  
    EXAMPLE:
    sinedb.delete(table = "table_capability", pk1=xxx)
    """

    if table == "table_capability":
      self.cur.execute('DELETE FROM table_capability WHERE nid=%s' % pk1)
        #TODO:should return something to make certern if operations have been done successfully!
    elif table == "table_service":
      self.cur.execute('DELETE FROM table_service WHERE sid=%s AND nid=%s' % (pk1, pk2))
    elif table == "table_portinfo":
      self.cur.execute('DELETE FROM table_portinfo WHERE nid=%s AND port=%s' % (pk1, pk2))
    elif table == "table_topology":
      self.cur.execute('DELETE FROM table_topology WHERE nidsrc=%s AND portsrc=%s' % (pk1, pk2))

    getRC = lambda self: self.cur.rowcount if hasattr(self.cur, 'rowcount') else -1
    return getRC(self)

  def pk_select(self, table, sid = None, nid = None, port = None):
    """
    select data from table
    """

    if table == "table_capability":
      if not nid:
        log.warning("No parameter when select from table_capability")
        return
      self.cur.execute('SELECT * FROM table_capability WHERE nid=%s' % nid)
      entries = self.cur.fetchchall()
      return entries
    elif table == "table_service":
      if sid and nid:
        self.cur.execute('SELECT * FROM table_service WHERE sid=%s AND nid=%s' % (sid, nid))
        entries = self.cur.fetchchall()
        return entries
      if sid:
        self.cur.execute('SELECT * FROM table_service WHERE sid=%s' % sid)
        entries = self.cur.fetchchall()
        return entries
      if nid:
        self.cur.execute('SELECT * FROM table_service WHERE nid=%s' % nid)
        entries = self.cur.fetchchall()
        return entries
      else:
        log.warning("No Proper Parameter when select from table_service!")
        return
    elif table == "table_portinfo":
      if port and nid:
        self.cur.execute('SELECT * FROM table_portinfo WHERE nid=%s AND port=%s' % (nid, port))
        entries = self.cur.fetchchall()
        return entries
      if nid:
        self.cur.execute('SELECT * FROM table_portinfo WHERE nid=%s' % nid)
        entries = self.cur.fetchchall()
        return entries
      if port:
        self.cur.execute('SELECT * FROM table_portinfo WHERE port=%s' % port)
        entries = self.cur.fetchchall()
        return entries
      else:
        log.warning("No Proper Parameter when select from table_portinfo!")
        return
    elif table == "table_topology":
      if port and nid:
        self.cur.execute('SELECT * FROM table_topology WHERE nidsrc=%s AND portsrc=%s' % (nid, port))
        entries = self.cur.fetchchall()
        return entries
      if nid:
        self.cur.execute('SELECT * FROM table_topology WHERE nidsrc=%s' % nid)
        entries = self.cur.fetchchall()
        return entries
      if port:
        self.cur.execute('SELECT * FROM table_topology WHERE portsrc=%s' % port)
        entries = self.cur.fetchchall()
        return entries
      else:
        log.warning("No Proper Parameter when select from table_topology!")
        return

  #remember to close MySQL when POX down
  def closedb(self):
    try:
      self.cxn.commit()
      self.cur.close()
      self.cxn.close()
    except:
      log.error("Close database failed!")

dbop = sinedb()
dbop.connect()

#DJ++ END 20140114 17:55
