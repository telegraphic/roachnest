#!/usr/bin/env python
# encoding: utf-8
"""
katcp_helpers.py
------------

Created by Danny Price on 2011-01-12.\n
Copyright (c) 2011 The University of Oxford. All rights reserved.\n

Helper functions and classes for controlling roach boards by KATCP.

"""

import os, sys, sqlite3 
from lxml import etree

# Import values from configuration file
import config

# CASPER imports
import corr,time,numpy,re

# import numpy
import numpy as np

# import matplotlib - images are created with the Agg backend
import matplotlib
import matplotlib.pyplot as plt

def dbget(id):
    """ Retrieves a hardware record from the hardware database.
    
    TODO: give this function a better name"""
    # Retrieve hardware list from database
    idno = int(id)
    sql = "SELECT * FROM hardware WHERE id=%i"%idno
    # Establish database connection
    dbconnect = sqlite3.connect(config.database) 
    db = dbconnect.cursor()
    db.execute(sql)
    result = db.fetchone()
    db.close()

    
    hardware = {
     "id"           : result[0],
     "hostname"     : result[1],
     "nickname"     : result[2],
     "MAC_address"  : result[3],
     "IP_address"   : result[4],
     "location"     : result[5],
     "notes"        : result[6],
     "serial"       : result[7],
     "firmware"     : result[8],
     "type"         : result[9],
     "XPORT_address": result[10]
    }
    return hardware

def bin2dec(binary):
    """return the decimal string representation of *binary*"""
    return int(binary,2)

def dec2bin(decimal):
    """return the binary string representation of a *decimal*"""
    HexBin ={"0":"0000", "1":"0001", "2":"0010", "3":"0011", "4":"0100", "5":"0101", "6":"0110", "7":"0111", "8":"1000", "9":"1001", "A":"1010", "B":"1011", "C":"1100", "D":"1101", "E":"1110", "F":"1111"}
    return "".join([HexBin[i] for i in '%X'%decimal]).lstrip('0')


def dec2hex(n):
    """return the hexadecimal string representation of integer *n*"""
    return "%X" % n
     
def hex2dec(s):
    """return the integer value of a hexadecimal string *s*"""
    return int(s, 16)

def reset(fpga):
    """Resets the sync and all counters by sending reset signals to the FPGA.
    This assumes that the relevant control registers are called:
        
        * *cnt_rst*: counter reset
        * *sync_rst*: sync reset
        * *sync_en*: sync enable
        
    This def returns a flashmsg, which can be displayed on a page.
    """
    fpga.write_int('cnt_rst',1)
    fpga.write_int('sync_rst',1)
    time.sleep(0.1)
    fpga.write_int('cnt_rst',0)
    fpga.write_int('sync_rst',0)

    fpga.write_int('sync_en',1)
    time.sleep(1)
    fpga.write_int('sync_en',0)

    flashmsg = 'Counters reset & sync pulse sent.'

    return flashmsg

def snapper(fpga, snap_id, bytes=4096, fmt="uint32", byteswap=True):
    """Reads a snap block, and returns the unpacked values as an array.
    
      Parameters
      ----------
      
      fpga: katcp_wrapper.FpgaClient() 
        The fpgaClient object from katcp_wrapper
      snap_id: string
        name of the block to snap
      fmt: string (dtype)
        unpack format to use (numpy data formats, e.g. uint32, int8)
      bytes: int
        number of bytes to read (remember, 1 byte = 8 bits)
      byteswap: bool
        Defaults to true. The PowerPC has a different endianess to most architectures, and \
        KATCP does NOT do host-to-network bit swapping. So, the byte order generally needs 
        to be swapped.
     
    """
    # Snap is triggered when first control bit changes from low to high:
    fpga.write_int(snap_id+'_ctrl', 0)
    fpga.write_int(snap_id+'_ctrl', 1)
    
    # Read the data from the fpga
    packed = fpga.read(snap_id+'_bram',int(bytes))
    
    # unpack the data
    data = numpy.fromstring(packed, dtype=fmt)
    
    if byteswap:
        data = data.byteswap()
    
    return data

def writereg(fpga, name, value, base=10):
   """
   Writes a value to an FPGA register. 
   Very similar to fpga.write_int, but you can specify the base (e.g. base 2 for binary)
   """
   data = int(value, int(base))
   print name, value, base, data
   fpga.write_int(name,data)

def check_permissions(paths):
   """Check file permissions"""
   dict = {}
   status=""
   for p in paths:
       if not os.access(p, os.F_OK):
         dict[p]=status=status+"NOEXISTS"
       if(os.access(p,os.R_OK)):
         dict[p]=status=status+"READ,"
       if(os.access(p, os.W_OK)):
         dict[p]=status=status+"WRITE,"
       if (os.access(p, os.X_OK)):
         dict[p]=status=status+"EXECUTE"
       elif os.access(p, os.F_OK) and not (os.access(p,os.R_OK)) and not (os.access(p, os.W_OK)) and not (os.access(p, os.X_OK)):
         dict[p]=status=status="NOACCESS"
       status="" # Set blank before we enter the loop again
   return dict
