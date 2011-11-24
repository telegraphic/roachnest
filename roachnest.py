#!/usr/bin/env python
# encoding: utf-8
"""
caspergui.py
============

Created by Danny Price on 2011-01-12.\n
Copyright (c) 2011 The University of Oxford. All rights reserved.\n

Caspergui is a browser based Graphical User Interface (GUI) for control of CASPER hardware. This script needs lolkatcp.py to run, which houses all the katcp commands for data capture, plotting etc.

This is still under heavy development. Use at your own risk, and be aware that I've done no security checking (so don't run this on the world wide web).

"""

# Import dependencies
import os, sys, time, re, struct, sqlite3
from bottle import *
from lxml import etree

import numpy as np
import matplotlib
matplotlib.use('Agg') # We don't want to send to X, rather to a imaging backend
import matplotlib.pyplot as plt
import katcp

# CASPER GUI internal imports
import lib.config as config
import lib.katcp_wrapper as katcp_wrapper
from lib.katcp_helpers import *
import lib.ping as ping
import lib.xport as xport

# Globals
DIRROOT = config.dirroot  # Automatically set root dir to this script's location
DB_NAME = config.database # Name of the database file



# Static files
@route('/files/:path#.+#')
def server_static(path):
    """URL: *@route('/files/:path#.+#')*"""
    return static_file(path, root=DIRROOT+'/files')

# Force download of files
@route('/download/:filename')
def download(filename):
    """URL: *@route('/download/:filename')*"""
    return static_file(filename, root=DIRROOT+'/files', download=filename)

# Index page
@route('/')
@route('/index.html')
@route('/hardware')
def list_hardware():
    """URL: *@route('/hardware')* """
    # Retrieve hardware list from database
    # Establish database connection
    dbconnect = sqlite3.connect(DB_NAME)    
    db = dbconnect.cursor()
    db.execute("SELECT * FROM hardware")
    result = db.fetchall()
    db.close()
    
    hardware_list = []
    
    
    # Make a list of things to ping
    hostlist = [row[2] for row in result]
    xphostlist = [row[10] for row in result]
    
    pinglist = []
    for host in hostlist:
      pinglist.append(ping.Host(host))
    statuslist = ping.pingHosts(pinglist)
    
    pinglist = []
    for host in xphostlist:
      pinglist.append(ping.Host(host))
    xpstatuslist = ping.pingHosts(pinglist)
    
    i = 0
    for row in result:
        
        hardware = {
         "id"           : row[0],
         "hostname"     : row[1],
         "nickname"     : row[2],
         "MAC_address"  : row[3],
         "IP_address"   : row[4],
         "location"     : row[5],
         "notes"        : row[6],
         "serial"       : row[7],
         "firmware"     : row[8],
         "type"         : row[9],
         "XPORT_address": row[10],
         "status"       : statuslist[i].status,
         "XPORT_status" : xpstatuslist[i].status
        }
         
        hardware_list.append(hardware)
        i += 1
    flashmsgs = []
    
    # Turn all boards ON 
    if(request.GET.get('power','').strip() == "Power all ON"):
      for roach in hardware_list:
        if(roach["XPORT_status"] == 1):
          xp = xport.Xport(roach["XPORT_address"], 10001)
          flashmsgs.append("%s: %s"%(roach["nickname"], xp.power_up()))
          xp.close()
          
    # Turn all boards OFF       
    if(request.GET.get('power','').strip() == "Power all OFF"):
      for roach in hardware_list:
        if(roach["XPORT_status"] == 1):
          xp = xport.Xport(roach["XPORT_address"], 10001)
          flashmsgs.append("%s: %s"%(roach["nickname"], xp.power_down()))
          xp.close()
    
    output = template('hardware', rows=hardware_list, flashmsgs=flashmsgs)
    return output
    

# Roach Status: overview of single piece of kit
@route('/status/:id')
def view_hardware(id):
    """ URL: *@route('/status/:id')*"""
    # Retrieve hardware list from database
    roach = dbget(id)

    flashmsgs = []
    
    # Get operating voltages etc from XPORT
    xp = xport.Xport(roach["XPORT_address"], 10001)

    xinfo = {
    "serial"     : xp.get_serial(),
    "id"         : xp.get_id(),
    "boardtime"  : xp.get_board_time(),
    "powerstate" : xp.get_power_state(),
    "shutdown"   : xp.get_last_shutdown(),
    "powergood"  : xp.get_power_good(),
    "channels"   : xp.get_channels(),
    "fanspeeds"  : xp.get_fan_speeds()
    }

    xp.close()

    output = template('status', roach=roach, flashmsgs=flashmsgs, xinfo=xinfo)
    return output

# Power ON
@route('/poweron/:id')
def power_on(id):
    """URL: *@route('/poweron/:id')* """
    # Retrieve hardware list from database
    roach = dbget(id)
    
    # Get operating voltages etc from XPORT
    xp = xport.Xport(roach["XPORT_address"], 10001)

    xinfo = {
    "serial"     : xp.get_serial(),
    "id"         : xp.get_id(),
    "boardtime"  : xp.get_board_time(),
    "powerstate" : xp.get_power_state(),
    "shutdown"   : xp.get_last_shutdown(),
    "powergood"  : xp.get_power_good(),
    "channels"   : xp.get_channels(),
    "fanspeeds"  : xp.get_fan_speeds()
    }

   
   
    flashmsgs = []
    flashmsgs.append(xp.power_up())
   
    xp.close()
   
    output = template('status', roach=roach, flashmsgs=flashmsgs, xinfo=xinfo)
    return output

# Power OFF
@route('/poweroff/:id')
def power_off(id):
    """URL: *@route('/poweroff/:id')* """
    # Retrieve hardware list from database
    roach = dbget(id)
    
    # Get operating voltages etc from XPORT
    xp = xport.Xport(roach["XPORT_address"], 10001)

    xinfo = {
    "serial"     : xp.get_serial(),
    "id"         : xp.get_id(),
    "boardtime"  : xp.get_board_time(),
    "powerstate" : xp.get_power_state(),
    "shutdown"   : xp.get_last_shutdown(),
    "powergood"  : xp.get_power_good(),
    "channels"   : xp.get_channels(),
    "fanspeeds"  : xp.get_fan_speeds()
    }
   
    flashmsgs = []
    flashmsgs.append(xp.power_down())

    xp.close()
   
    output = template('status', roach=roach, flashmsgs=flashmsgs, xinfo=xinfo)
    return output

# List registers (enhanced ?listdev)
@route('/listreg/:id')
def listreg(id):
    """URL: *@route('/listreg')*"""
    # Retrieve hardware list from database
    roach = dbget(id)
    
    fpga = katcp_wrapper.FpgaClient(roach["IP_address"], port, timeout=10)
    time.sleep(0.1)
    registers = fpga.listdev()
        
    flashmsg = ""
    
    # Check if we need to update some registers
    if(request.GET.get('regname','').strip() and request.GET.get('regval','').strip()):
        regname = request.GET.get('regname','').strip()
        regtype = request.GET.get('regtype','').strip()
        if(regtype == 'eval'):
            regval = eval(request.GET.get('regval','').strip())
        else:
            regval = int(request.GET.get('regval','').strip(), int(regtype))
        
        
        fpga.write_int(regname, regval)
        flashmsg = "%s updated with value %i"%(regname,regval)
    
    # Check if reset is required
    if(request.GET.get('reset','').strip()):
        flashmsg = reset(fpga)
    
    # Check if there is a config to load
    if(request.GET.get('config','').strip()):
        filename = 'config/%s'%(request.GET.get('config','').strip())

        #etree.parse() opens and parses the data
        xmlData = etree.parse(filename)

        # Read the config file and load the register values
        config = xmlData.getroot()
        registers = config.findall('register')

        for reg in registers:
            #flashmsg.append("Writing value %s to register %s"%(reg.attrib['value'],reg.attrib['name']))
            writereg(fpga, reg.attrib['name'],reg.attrib['value'],reg.attrib['base'])


    # Sort out the list of registers using regex matches
    #registers = fpga.listdev()
    pattern_snap   = re.compile('[A-Za-z_0-9]+_bram$')
    pattern_snap64 = re.compile('[A-Za-z_0-9]+_bram_lsb$')
    pattern_sys    = re.compile('sys_\w+')
    pattern_outreg = re.compile('o_\w+')
    pattern_excl   = re.compile("\w+(_ctrl|_addr|_rst|_en|_msb)")

    snaplist, snap64list, syslist, reglist, outreglist = [], [], [], [], []

    # Filter registers one by one
    for register in registers:
        snap   = pattern_snap.match(register)
        snap64 = pattern_snap64.match(register)
        sys    = pattern_sys.match(register)
        outreg = pattern_outreg.match(register)
        excl   = pattern_excl.match(register)
        
        if snap: snaplist.append(snap.group().split('_bram')[0])
        elif snap64: snap64list.append(snap64.group().split('_bram_lsb')[0])
        elif sys: syslist.append(sys.group())
        elif outreg: outreglist.append(outreg.group())
        elif not(excl): reglist.append(register)

    vals = []
    for item in reglist: 
        vals.append(fpga.read_int(item))
    
    outregvals = []    
    for item in outreglist:
        outregvals.append(fpga.read_int(item))

    data = {
         "snaplist"     : snaplist,
         "snap64list"   : snap64list,
         "syslist"      : syslist,
         "reglist"      : reglist,
         "outreglist"   : outreglist,
         "vals"         : vals,
         "outregvals"   : outregvals,
         "flashmsg"     : flashmsg
    }

    fpga.stop()
    output = template('listreg', data=data, roach=roach)
    
    return output
    
# List bitstreams (?listbof)
@route('/listbof/:id')
def listbof(id):
    """URL: *@route('/listbof')*"""
    # Retrieve hardware list from database
    roach = dbget(id)
    fpga = katcp_wrapper.FpgaClient(roach["IP_address"], port, timeout=10)
    time.sleep(1)
    boflist = fpga.listbof()
    boflist.sort()
    fpga.stop()
    
    output = template('listbof', boflist=boflist, roach=roach, flashmsg=0)
    return output    

# Program FPGA (?progdev)
@route('/progdev/:id/:bitstream')
def progdev(id, bitstream):
    """URL: *@route('/progdev/:bitstream')*"""
    roach = dbget(id)
    flashmsg = ["FAILURE: progdev failed for some reason.", "error"]
    
    fpga = katcp_wrapper.FpgaClient(roach["IP_address"], port, timeout=10)
    time.sleep(1)
    if(fpga.is_connected()):
        fpga.progdev(bitstream)
        flashmsg = ["Programmed with %s"%(bitstream), "success"] 
    boflist = fpga.listbof()
    boflist.sort()
    fpga.stop()
    output = template('listbof', boflist=boflist, roach=roach, flashmsg=flashmsg)
    return output        

# ?read_int implementation for IO registers
@route('/readint/:regname')
def read_int(regname):
    """URL: *@route('/readint/:regname')*"""
    
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    regdata = fpga.read_int(regname)
    fpga.stop()
    
    
    regdata = {
        "name" : regname,
        "data" : regdata
    }
    
    output = template('read_int', register=regdata)
    return output    
    

# snap block plotter (32 bit)
@route('/snap/:id/:snap_id/bytes/:bytes/fmt/:fmt/op/:op')
def snap32(id, snap_id, bytes, fmt, op):
    """ URL: *@route('/snap/:snap_id/bytes/:bytes/fmt/:fmt')*"""
    roach = dbget(id)
    fpga = katcp_wrapper.FpgaClient(roach["IP_address"], port, timeout=10)
    time.sleep(0.1)
    
    if(fpga.is_connected()):
        # grab the snap data and unpack
        fpga.write_int(snap_id+'_ctrl', 0)
        fpga.write_int(snap_id+'_ctrl', 1)
        
        # Unpack data in correct format (signed, unsigned or complex signed)
        packed = fpga.read(snap_id+'_bram',int(bytes))
        if(fmt == 'comp8'):
            data =  np.fromstring(packed, dtype='int8').byteswap()
            data =  data.reshape([int(bytes)/2, 2])
            data =  data[:,0] + 1j * data[:,1]
        elif(fmt == 'comp16'):
            data =  np.fromstring(packed, dtype='int16').byteswap()
            data =  data.reshape([int(bytes)/4, 2])
            data =  data[:,0] + 1j * data[:,1]
        else:
            data =  np.fromstring(packed, dtype=fmt).byteswap()
            
        fpga.stop()

        # Generate a graph using matplotlib
        #import matplotlib
        #matplotlib.use('Agg') # We don't want to send to X, but to a backend
        #import matplotlib.pyplot as plt
        #fig = plt.figure()
        #ax = fig.add_subplot(111)
        #ax.plot(data)
        #ax.set_title(snap_id)
        #ax.set_xlim(0,len(data))
        #fig.savefig('files/temp.png')
        
        # Generate data for Flot (javascript plotting library)
        # Need to reduce data down to 1024 points
        
        
        # xvals = 200.0/1024 * np.cumsum(np.ones(1024)) + 100
        
        if(len(data) > 1024):
            xvals = len(data)/1024 * np.cumsum(np.ones(1024))
            yvals = np.sum(data.reshape([1024, len(data)/1024]), axis=1)
        else:
            xvals = np.cumsum(np.ones(len(data)))
            yvals = data

       
        # Apply numpy operations - passed on 'op' variable
        if(op == 'real'):
            yvals = np.real(yvals)
        elif(op == 'imag'):
            yvals = np.imag(yvals)
        elif(op == 'powfftdb'):
            yvals = 10 * np.log10(np.abs(np.fft.fft(yvals)))
        elif(op == 'powfftlin'):
            yvals = np.abs(np.fft.fft(yvals))
        elif(op == 'bits'):
            yvals = np.log2(np.abs(yvals)+1)
        elif(op == 'decibels'):
            yvals = 10 * np.log10(yvals)
        else:
            yvals = yvals        

        data = np.ones([len(yvals),2])
        data[:,0] = xvals
        data[:,1] = yvals                


        output = template('plot_snap', roach=roach, snap_id=snap_id, data=data, fmt=fmt, bytes=bytes, op=op)
        return output     
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"

##########################
##  BEGINNING OF MAIN  ###
##########################
        
if __name__ == '__main__':

    # Option parsing to allow command line arguments to be parsed
    from optparse import OptionParser
    p = OptionParser()
    p.set_usage('caspergui.py [options]')
    p.set_description(__doc__)
    p.add_option("-k", "--katcpport", dest="port", type="int", default=7147,
                 help="Select KATCP port. Default is 7147")
    p.add_option("-i", "--hostip", dest="hostip", type="string", default="127.0.0.1",
                 help="change host IP address to run server. Default is localhost (127.0.0.1)")
    p.add_option("-p", "--hostport", dest="hostport", type="int", default=8080,
                 help="change host port for server. Default is 8080")

    (options, args) = p.parse_args(sys.argv[1:])

   
    port = options.port
    hostip = options.hostip
    hostport = options.hostport

    # Development mode
    debug(True)
    
    #Start bottle server
    run(host=hostip, port=hostport, reloader=True)
