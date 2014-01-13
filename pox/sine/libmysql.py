#This defines MySQL operations

#DJ++ START 20140109 15:38 

import os

import MySQLdb
import _mysql_exceptions as DB_EXC

log = core.getLogger()

#define namedtuples for all four tables
#The designing of tables follows the SINE ER module
tab_cap = namedtuple("table_capability", ("nid", "dpid", "bandwidth"))#need more infomation
tab_ser = namedtuple("table_service", ("sid", "nid"))
tab_ninfo = namedtuple("table_nodeinformation", ("nid", "port", "ip", "mac"))
tab_topo = namedtuple("table_topology", ("nidsrc", "portsrc", "niddst", "portdst", "distance"))

class sinedb(object):
  '''
  A collection of operations SINE uses to operate MySQL
  '''

  def __init__(self, dbname = "SINE"):
    self.cnx = None
    self.cur = None
    self.dbname = dbname

  #done
  def connect(self): 
    #create connection
    try:
      self.cxn = MySQLdb.connect(db=self.dbName)
    except DB_EXC.OperationalError, e:
      log.exception("Connecting to MySQL failed!",e)

    #create cursor
    self.cur = self.cnx.cursor()
  
  def insert(self, table, *args):
  '''
  If you want to insert an entry, you should give the name of the table 
  and give a complete entry, even the column allows "Null".
  Also, you can insert multiple entries.

  EXAMPLE:
  sinedb.insert(table = "table_capability", (nid, dpid, ''))
  Here the third column is for 'bandwidth' which allows "Null", but you still show give a "''".
  '''
    if table == "table_capability":
      for entry in args:
        if len(entry) != 3:
          log.error("Inserting to table_capability error! length=",len(entry))
          return
        self.cur.execute(
          "INSERT INTO table_capability VALUES(%s, %s, %s)", entry)
        #TODO:should return something to make certern if operations have been done successfully!
    elif table == "table_service":
      for entry in args:
        if len(entry) != 3:
          log.error("Inserting to table_service error! length=",len(entry))
          return
      self.cur.executemany(
        "INSERT INTO table_service VALUES(%s, %s, %s)", args)
    elif table == "table_nodeinfo":
      for entry in args:
        if len(entry) != 4:
          log.error("Inserting to table_nodeinfo error! length=",len(entry))
          return
      self.cur.executemany(
        "INSERT INTO table_nodeinfo VALUES(%s, %s, %s, %s)", args)
    elif table == "table_topology":
      for entry in args:
        if len(entry) != 5:
          log.error("Inserting to table_topology error! length=",len(entry))
          return
      self.cur.executemany(
        "INSERT INTO table_topology VALUES(%s, %s, %s, %s, %s)", args)

  def update(self, table, pk1, pk2 = None, **kw):
  '''
  If you want to update one of the data in table, you should give the primary key and the data
  you want to update.

  Do like the example.
  EXAMPLE:
  sinedb.update(table = "table_service", pk = xxx, sid=xxx, nid=sss)
  pk is for primary key.
  You can give one or more parameter to update the entry in the table.
  '''
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
        elif key == "band-width":
          self.cur.execute(
            "UPDATE table_capability SET band-width=%s WHERE nid=%s" % (value, pk1))
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
    #table_nodeinfo
    #pk1:nid
    #pk2:port
    elif table == "table_nodeinfo":
      for key, value in kw.iteritems():
        #Generally,sid and nid should not be updated
        if key == "nid":
          self.cur.execute(
            "UPDATE table_nodeinfo SET nid=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
          log.warning("Primary key nid is updated!")
        elif key == "port":
          self.cur.execute(
            "UPDATE table_nodeinfo SET port=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
          log.warning("Primary key port is updated!")
        elif key == "ip":
          self.cur.execute(
            "UPDATE table_nodeinfo SET ip=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
        elif key == "mac":
          self.cur.execute(
            "UPDATE table_nodeinfo SET mac=%s WHERE nid=%s AND port=%s" % (value, pk1, pk2))
        else:
          log.error("Data type error! Not in table_nodeinfo!")
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
  

  def delete(cur):
    rm = rrange(1,5)
    cur.execute('DELETE FROM users WHERE prid=%d' % rm)
    return rm, getRC(cur)

  def dbDump(cur):
    cur.execute('SELECT * FROM users')
    print '\n%s%s%s' % ('LOGIN'.ljust(COLSIZ),
      'USERID'.ljust(COLSIZ), 'PROJ#'.ljust(COLSIZ))
    for data in cur.fetchall():
      print '%s%s%s' % tuple([str(s).title().ljust(COLSIZ) \
        for s in data])

  #remember to close MySQL when POX down
  def closedb(self):
    pass
    #TODO

  #getRC = lambda cur: cur.rowcount if hasattr(cur, 'rowcount') else -1

#DJ++ END 20140113 15:38 