#!/usr/bin/env python
# encoding: utf-8
"""
roachnest.py
============

Created by Danny Price on 2011-01-12.\n
Copyright (c) 2011 The University of Oxford. All rights reserved.\n

Roachnest is a browser based Graphical User Interface (GUI) for control of CASPER hardware.
It facilitates basic monitor and control tasks, such as turning boards on and off via the XPORT, 
reprogramming the FPGA, reading and writing registers, and plotting the contents of shared BRAMS 
(snap blocks).

Roachnest also provides basic hardware management through a small sqlite database. Users can add
notes, specify IP addresses, hostnames, and other basic information necessary to keep track of
hardware specifics.

**License:** GNU GPL: http://www.gnu.org/copyleft/gpl.html

**Warning:** I strongly suggest that this is available only through an internal network and 
is not made accessible via the WWW. Use at your own risk.

"""

# Python metadata
__author__    = "Danny Price"
__license__   = "GNU GPL"
__version__   = "1.0"

# Import dependencies
import os, sys, time, re, struct, sqlite3
from bottle import *
from lxml import etree

import numpy as np
import katcp

# CASPER GUI internal imports
import lib.config as config
import lib.katcp_wrapper as katcp_wrapper
from   lib.roachnest_helpers import *
import lib.ping as ping
import lib.xport as xport

# Globals
DIRROOT = config.dirroot  # Automatically set root dir to this script's location
DB_NAME = config.database # Name of the database file

# Static files
@route('/files/:path#.+#')
def server_static(path):
    """URL: */files/:path#.+#*
    
    Returns static files (eg images, css, scripts, favicons).
    """
    return static_file(path, root=DIRROOT+'/files')

# Force download of files
@route('/download/:filename')
def download(filename):
    """URL: */download/:filename*
    
    Forces download of static files.
    """
    return static_file(filename, root=DIRROOT+'/files', download=filename)

# Index page
@route('/')
@route('/index.html')
@route('/hardware')
def list_hardware():
    """URL: */* 
    
    Index page. Lists all boards in the hardware database.
    """
    # Retrieve hardware list from database
    # Establish database connection
    dbconnect = sqlite3.connect(DB_NAME)    
    db = dbconnect.cursor()
    flashmsgs = []
    
    try:
      hardware_list = dbgetall()
      
      # Make a list of things to ping
      hostlist   = [ping.Host(h["IP_address"]) for h in hardware_list]
      xphostlist = [ping.Host(h["XPORT_address"]) for h in hardware_list]
      
      # Ping the fkrs
      statuslist   = ping.pingHosts(hostlist)
      xpstatuslist = ping.pingHosts(xphostlist)
      
      i = 0
      for roach in hardware_list:
          roach["status"]       = statuslist[i].status
          roach["XPORT_status"] = xpstatuslist[i].status
          i += 1
          
      # Turn all boards ON 
      if(request.GET.get('power','').strip() == "Power all ON"):
        for roach in hardware_list:
          if(roach["XPORT_status"] == 1):
            xp = xport.Xport(roach["XPORT_address"], 10001)
            flashmsgs.append("%s: %s"%(roach["hostname"], xp.power_up()))
            xp.close()
            
      # Turn all boards OFF       
      if(request.GET.get('power','').strip() == "Power all OFF"):
        for roach in hardware_list:
          if(roach["XPORT_status"] == 1):
            xp = xport.Xport(roach["XPORT_address"], 10001)
            flashmsgs.append("%s: %s"%(roach["hostname"], xp.power_down()))
            xp.close()
      
      
      output = template('index', rows=hardware_list, flashmsgs=flashmsgs)
      
      return output
    except:
      output = template('index', rows=[], flashmsgs=flashmsgs)
      return output
    

@route('/status/:id')
def view_hardware(id):
    """ URL: */status/:id*
    
    Provides overview of a single piece of kit.
    """
    # Retrieve hardware list from database
    roach = dbget(id)
    flashmsgs = []

    # Check if XPORT is responding or not
    xping = ping.Host(roach["XPORT_address"])
    xstatus = ping.pingHosts([xping])[0].status

    if(xstatus == 1):
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
    else:
      flashmsgs.append("Warning: Xport is not responding to pings. Detailed status not available.")
      xinfo = 0

    output = template('status', roach=roach, flashmsgs=flashmsgs, xinfo=xinfo)
    return output

# Power ON
@route('/poweron/:id')
def power_on(id):
    """URL: */poweron/:id* 
    
    Powers up a ROACH board using XPORT.
    """
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
    """URL: */poweroff/:id* 
    
    Powers off a ROACH board using XPORT.
    """
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
    """URL: */listreg*
    
    Lists registers and applies basic sorting regex. Uses KATCP ?listdev command.
    """
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
            # Evaluate safely, at Griffin's request
            regval = safe_eval(request.GET.get('regval','').strip())
        else:
            regval = int(request.GET.get('regval','').strip(), int(regtype))
        
        if(regval != 'Error'):
          fpga.write_int(regname, regval)
          flashmsg = "%s updated with value %i"%(regname,regval)
        else:
          flashmsg = "Error: I'm sorry, Dave, I can't let you do that..."
    
    # Check if there is a config to load
    if(request.GET.get('config','').strip()):
        filename = 'config/%s'%(request.GET.get('config','').strip())

        #etree.parse() opens and parses the data
        xmlData = etree.parse(filename)

        # Read the config file and load the register values
        config = xmlData.getroot()
        registers = config.findall('register')

        for reg in registers:
            writereg(fpga, reg.attrib['name'],reg.attrib['value'],reg.attrib['base'])


    # Sort out the list of registers using regex matches
    #registers = fpga.listdev()
    pattern_snap   = re.compile('[A-Za-z_0-9]+_bram$')
    pattern_snap64 = re.compile('[A-Za-z_0-9]+_bram_lsb$')
    pattern_sys    = re.compile('sys_\w+')
    pattern_outreg = re.compile('o_\w+')
    pattern_excl   = re.compile("\w+(_ctrl|_addr|_rst|_msb)")

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
    """URL: */listbof*
    
    Lists all bitstreams. Uses KATCP ?listbof command.
    """
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
    """URL: */progdev/:bitstream*
    
    Executes KATCP ?progdev command to program FPGA.
    """
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

# snap block plotter (32 bit)
@route('/snap/:id/:snap_id/bytes/:bytes/fmt/:fmt/op/:op')
def snap32(id, snap_id, bytes, fmt, op):
    """ URL: */snap/:snap_id/bytes/:bytes/fmt/:fmt*
    
    Plots data from a snap register. Can be read in a variety of different formats.
    Uses /ajax_snap to retrieve data (/ajax_snap docs).
    """
    roach = dbget(id)
    output = template('plot_snap', roach=roach, snap_id=snap_id, fmt=fmt, bytes=bytes, op=op)
    return output     

############################
##  Database management   ##
############################

# Create new database
@route('/dbcreate')
def create_db():
  """URL: */dbcreate*
  
  Creates a new database.
  """
  
  # Create database
  flashmsgs = dbcreate()
  
  # Create a new (blank) roach record
  roach = dbblank() 
  
  output = template('hardware_add', roach=roach, flashmsgs=flashmsgs)
  return output 
  

# Edit piece of kit
@route('/edit/:id', method='GET')
def hardware_edit(id):
  """URL: */edit/:id*
  
  Edits a piece of kit in the database.
  """
  id = int(id)
  flashmsgs = []
  roach = dbget(id)
  
  if request.GET.get('save','').strip():
      # get hardware details from GET request
      hostname = request.GET.get('hostname', '').strip()
      MAC_address = request.GET.get('MAC_address', '').strip()
      IP_address = request.GET.get('IP_address', '').strip()
      XPORT_address = request.GET.get('XPORT_address', '').strip()
      ZDOK0 = request.GET.get('ZDOK0', '').strip()
      ZDOK1 = request.GET.get('ZDOK1', '').strip()
      location = request.GET.get('location', '').strip()
      notes = request.GET.get('notes', '').strip()
      serial = request.GET.get('serial', '').strip()
      firmware = request.GET.get('firmware', '').strip()
      atype = request.GET.get('type', '').strip() # Type is a restricted word so using atype
      
      flashmsgs.append(
        dbedit(id, hostname, MAC_address, IP_address, location, notes, serial, firmware, atype, XPORT_address, ZDOK0, ZDOK1)
        )
      output = template('hardware_edit', roach=roach, flashmsgs=flashmsgs)
  else:
      output = template('hardware_edit', roach=roach, flashmsgs=flashmsgs)
  
  return output

# Add new piece of kit
@route('/add')
def hardware_add():
  """URL: */add*
  
  Add a new piece of kit to the database.
  """
  flashmsgs = []
  # Create a new (blank) roach record
  roach = dbblank()

  if request.GET.get('save','').strip():
      # get hardware details from GET request
      hostname = request.GET.get('hostname', '').strip()
      MAC_address = request.GET.get('MAC_address', '').strip()
      IP_address = request.GET.get('IP_address', '').strip()
      XPORT_address = request.GET.get('XPORT_address', '').strip()
      ZDOK0 = request.GET.get('ZDOK0', '').strip()
      ZDOK1 = request.GET.get('ZDOK1', '').strip()
      location = request.GET.get('location', '').strip()
      notes = request.GET.get('notes', '').strip()
      serial = request.GET.get('serial', '').strip()
      firmware = request.GET.get('firmware', '').strip()
      atype = request.GET.get('type', '').strip() # Type is a restricted word so using atype
      
      flashmsgs.append(
        dbadd(hostname, MAC_address, IP_address, location, notes, serial, firmware, atype, XPORT_address, ZDOK0, ZDOK1)
        )
      output = template('hardware_add', roach=roach, flashmsgs=flashmsgs)
      redirect("/")
  else:
      output = template('hardware_add', roach=roach, flashmsgs=flashmsgs)
      return output

# Delete piece of kit
@route('/delete/:id')
def hardware_edit(id):
  """URL: */delete/:id*
  
  Delete a piece of kit from the database.
  """
  flashmsgs = []
  flashmsgs.append(
    dbdelete(id)
    )
    
  output = template('simpleflash', flashmsgs=flashmsgs)
  return output
  

############################
##  AJAX request handlers ##
############################

@route('/ajax_snap/:id/:snap_id/bytes/:bytes/fmt/:fmt/op/:op')
def snap32(id, snap_id, bytes, fmt, op):
    """ URL: *ajax_snap/:snap_id/bytes/:bytes/fmt/:fmt*
    
    AJAX request handler for /snap plotting page. Returns JSON data for
    the Flot javascript plotting library to plot.
    """
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

        # Generate data for Flot (javascript plotting library)
        # Need to reduce data down to 1024 points      
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

        # Convert numpy array into a python dictionary
        # Bottle will pass this as a JSON array to the requester
        output = {'data' : [list(pair) for pair in data] }
        return output
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"


#########################
##  BEGINNING OF MAIN  ##
#########################
        
if __name__ == '__main__':

    # Option parsing to allow command line arguments to be parsed
    from optparse import OptionParser
    p = OptionParser()
    p.set_usage('roachnest.py [options]')
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
    
    # Start bottle server
    # See: http://bottlepy.org/docs/dev/tutorial_app.html#server-setup
    run(host=hostip, port=hostport, reloader=True, server=PasteServer)