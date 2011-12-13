#!/usr/bin/env python
# encoding: utf-8
"""
roachnest_helpers.py
--------------------

Created by Danny Price on 2011-01-12.\n
Copyright (c) 2011 The University of Oxford. All rights reserved.\n

Helper functions and classes for roachnest.

"""

import os, sys, sqlite3, ast
from lxml import etree

# Import values from configuration file
import config

# CASPER imports
import corr,time,numpy,re

# import numpy
import numpy as np

DB_NAME = os.path.join(config.dirroot, config.database)

#############################
##  Data type conversions  ##
#############################

def bin2dec(binary):
    """return the decimal string representation of *binary*
    
    Parameters
    ----------
    binary: binary string
      binary string to reinterpret as decimal
    """
    return int(binary,2)

def dec2bin(decimal):
    """return the binary string representation of a *decimal*
    Parameters
    ----------
    decimal: decimal string
      decimal string to reinterpret as binary
    """
    HexBin ={"0":"0000", "1":"0001", "2":"0010", "3":"0011", "4":"0100", "5":"0101", "6":"0110", "7":"0111", "8":"1000", "9":"1001", "A":"1010", "B":"1011", "C":"1100", "D":"1101", "E":"1110", "F":"1111"}
    return "".join([HexBin[i] for i in '%X'%decimal]).lstrip('0')

def dec2hex(n):
    """return the hexadecimal string representation of integer *n*
    
    Parameters
    ----------
    n: hexadecimal string
      hexadecimal string to reinterpret as decimal
    """
    return "%X" % n
     
def hex2dec(s):
    """return the integer value of a hexadecimal string *s*

    Parameters
    ----------
    s: decimal string
      decimal string to reinterpret as hexadecimal    
    """
    return int(s, 16)


##########################
##    KATCP helpers     ##
##########################

def writereg(fpga, name, value, base=10):
    """
    Writes a value to an FPGA register. 
    Very similar to fpga.write_int, but you can specify the base (e.g. base 2 for binary)

    Parameters
    ----------
    fpga: katcp_wrapper.FpgaClient object 
      fpga client object (which roach board to communitcate with)
    name: string
      register name
    value: integer
      value to write to register
    base: int
      base to write register. Default is 10 (decimal), but other bases may be used.
    """
    data = int(value, int(base))
    print name, value, base, data
    fpga.write_int(name,data)

def safe_eval(command):
    """
    A safer version of the eval() command, using ast.literal_eval
    TODO: make this more functional, at the moment it's pretty useless.
    
    Parameters
    ----------
    command: string
      command to evaluate (e.g. '2**10-1').
    """
    try:
      x = ast.literal_eval(command)
    except:
      x = "Error"
    return x


############################
##  Database management   ##
############################

def dbcreate():
  """ Creates a new database. 
  
  Notes
  -----
  This function should only be called once, for initial database setup.
  """
  try:
    # Create file if it doesnt exist
    msgs = []
    
    if not os.path.exists(DB_NAME):
      msgs.append("Database %s not found. Trying to create..."%DB_NAME)
      try:
        open(DB_NAME,'w').close()
        msgs.append("New database created successfully.")
      except:
        msgs.append("Error: database could not be created (check permissions!)")
      
    # Connect to database
    dbconnect = sqlite3.connect(DB_NAME)    
    db = dbconnect.cursor()
    
    # Create new table
    msgs.append("Creating table 'hardware'...")
    sql = """
          CREATE TABLE IF NOT EXISTS hardware (
          id INTEGER PRIMARY KEY,
          hostname TEXT NOT NULL,
          MAC_address TEXT,
          IP_address TEXT,
          location TEXT,
          notes TEXT,
          serial TEXT,
          firmware TEXT,
          type TEXT,
          XPORT_address TEXT,
          ZDOK0 TEXT,
          ZDOK1 TEXT
          );
          """
    
    try:      
      db.execute(sql)
      msgs.append("Table created successfully")
    except:
      msgs.append("Error: table could not be created.")
    return msgs
  except:
    msgs.append("Error: database could not be created.")
    return msgs

def dbgetall():
    """ Retrieves all records from the database.
    
    Notes
    -----
    Retrieves all records from the database. Returns a list of python dictionaries, with
    name: value pairs that correspond to database columns. Each python dictionary 
    contains the following entries:
    id, hostname, MAC_address, IP_address, location, notes, serial, firmware, type,
    XPORT_address, ZDOK0, ZDOK1, status, XPORT_status.
    """
    # Establish database connection
    dbconnect = sqlite3.connect(DB_NAME)    
    db = dbconnect.cursor()
    db.execute("SELECT * FROM hardware")
    result = db.fetchall()
    db.close()
    
    hardware_list = []
    
    # Create python dictionary for each piece of hardware
    for row in result:
        hardware = {
         "id"           : row[0],
         "hostname"     : row[1],
         "MAC_address"  : row[2],
         "IP_address"   : row[3],
         "location"     : row[4],
         "notes"        : row[5],
         "serial"       : row[6],
         "firmware"     : row[7],
         "type"         : row[8],
         "XPORT_address": row[9],
         "ZDOK0"        : row[10],
         "ZDOK1"        : row[11],
         "status"       : 0,
         "XPORT_status" : 0
        }
         
        hardware_list.append(hardware)
    
    return hardware_list


def dbget(id):
    """ Retrieves a hardware record from the hardware database.
    
    Notes
    -----
    Queries database and returns a python dictionary with the following entries:
    id, hostname, MAC_address, IP_address, location, notes, serial, firmware, type,
    XPORT_address, ZDOK0, ZDOK1, status, XPORT_status.
    
    Parameters
    ----------
    id: integer
      primary key (ID number) of database entry
    """
    # Retrieve hardware list from database
    idno = int(id)
    sql = "SELECT * FROM hardware WHERE id=%i"%idno
    # Establish database connection
    dbconnect = sqlite3.connect(DB_NAME) 
    db = dbconnect.cursor()
    try:
      db.execute(sql)
      result = db.fetchone()
      db.close()
      
      hardware = {
       "id"           : result[0],
       "hostname"     : result[1],
       "MAC_address"  : result[2],
       "IP_address"   : result[3],
       "location"     : result[4],
       "notes"        : result[5],
       "serial"       : result[6],
       "firmware"     : result[7],
       "type"         : result[8],
       "XPORT_address": result[9],
       "ZDOK0"        : result[10],
       "ZDOK1"        : result[11],
       "status"       : 0,
       "XPORT_status" : 0
      }
    
    except:
      dbconnect.rollback()
      db.close()
      hardware = 0
    
    return hardware

def dbblank():
    """ Returns a blank hardware dictionary.
    
    Returns a BLANK python dictionary with the following entries:
    id, hostname, MAC_address, IP_address, location, notes, serial, firmware, type,
    XPORT_address, ZDOK0, ZDOK1, status, XPORT_status.
    """
    hardware = {
     "id"           : '',
     "hostname"     : '',
     "MAC_address"  : '',
     "IP_address"   : '',
     "location"     : '',
     "notes"        : '',
     "serial"       : '',
     "firmware"     : '',
     "type"         : '',
     "XPORT_address": '',
     "ZDOK0"        : '',
     "ZDOK1"        : '',
     "status"       : '',
     "XPORT_status" : ''
    }
    
    return hardware

def dbedit(id, hostname, MAC_address, IP_address, location, notes, serial, firmware, atype, XPORT_address, ZDOK0, ZDOK1):
    """ Edit an exisiting piece of hardware in the database
    
    Parameters
    ----------
    id: int
      Primary key (ID number) of record
    hostname: string
      Hostname of piece of hardware
    MAC_address: string
      MAC address of KATCP interface
    IP_address: string
      IP address of KATCP interface.      
    location: string
      Physical location of the hardware (eg Oxford DSP lab)
    notes: string
      Any relevant notes that you may have
    serial: string
      The serial number of the hardware.
    firmware:
      Firmware revision information
    atype: string
      What type of hardware is it? Options are generally ROACH, ROACH2, iBOB or BEE2
    XPORT_address: string
      IP address of XPORT interface.
    ZDOK0: string
      Notes about what is installed in ZDOK 0.
    ZDOK1: string
      Notes about what is installed in ZDOK 1.    
    """
    dbconnect = sqlite3.connect(config.database) 
    db = dbconnect.cursor()
    try:
      db.execute("UPDATE hardware SET hostname= ?, MAC_address= ?, IP_address= ?,location= ?, \
                  notes= ?, serial= ?, firmware= ?, type= ?, XPORT_address= ?, ZDOK0 = ?, ZDOK1 = ?\
                  WHERE id LIKE ?",\
                  (hostname,MAC_address,IP_address,location,notes,serial,firmware,atype,XPORT_address,ZDOK0,ZDOK1,id))
      dbconnect.commit()
      db.close()
      return "Hardware with ID %s updated successfully"%id
    except:
      dbconnect.rollback()
      db.close()
      return 'Error: could not edit hardware ID %s'%id       

  
def dbadd(hostname, MAC_address, IP_address, location, notes, serial, firmware, atype, XPORT_address, ZDOK0, ZDOK1):
    """ Add a new piece of hardware to the database
    
    Parameters
    ----------
    hostname: string
      Hostname of piece of hardware
    MAC_address: string
      MAC address of KATCP interface
    IP_address: string
      IP address of KATCP interface.      
    location: string
      Physical location of the hardware (eg Oxford DSP lab)
    notes: string
      Any relevant notes that you may have
    serial: string
      The serial number of the hardware.
    firmware:
      Firmware revision information
    atype: string
      What type of hardware is it? Options are generally ROACH, ROACH2, iBOB or BEE2
    XPORT_address: string
      IP address of XPORT interface.
    ZDOK0: string
      Notes about what is installed in ZDOK 0.
    ZDOK1: string
      Notes about what is installed in ZDOK 1. 
    """
    dbconnect = sqlite3.connect(config.database)
    db = dbconnect.cursor()  
    try:
      db.execute("INSERT INTO hardware (hostname,MAC_address,IP_address,location,notes,serial,firmware,type,XPORT_address,ZDOK0,ZDOK1) \
                  VALUES (?,?,?,?,?,?,?,?,?,?,?)",\
                  (hostname,MAC_address,IP_address,location,notes,serial,firmware,atype,XPORT_address,ZDOK0,ZDOK1))
      dbconnect.commit()
      db.close()
      return "New hardware added successfully"
      
    except:
      dbconnect.rollback()
      db.close()
      return 'Error: could not add hardware for some reason.'     

  
def dbdelete(id):
    """ Deletes a piece of hardware from the database.
    
    Parameters
    ----------
    id: int
      Primary key (ID number) of record    
    """
    dbconnect = sqlite3.connect(config.database) 
    db = dbconnect.cursor() 
    try:
      db.execute("DELETE FROM hardware WHERE id=%s"%id)
      dbconnect.commit()
      db.close()
      return 'Hardware with ID %s deleted successfully'%id   
    except:
      dbconnect.rollback()
      db.close()
      return 'Error: could not delete hardware with ID %s'%id 
  