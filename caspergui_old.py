#!/usr/bin/env python
# encoding: utf-8
"""
caspergui.py

Browser based Graphical User Interface (GUI) for control of CASPER hardware.
This script utilises the KATCP python libraries, the bottle web framework, 
and sqlite3:

    http://casper.berkeley.edu/wiki/KATCP
    http://bottle.paws.de/
    http://docs.python.org/library/sqlite3.html


The HTML/CSS is based on blueprint CSS web framework:
    http://www.blueprintcss.org/


Created by Danny Price on 2011-01-12.
Copyright (c) 2011 The University of Oxford. All rights reserved.
"""

# Imports for GUI 
from bottle import *
import sqlite3, struct, os, sys

# CASPER imports
import corr,time,numpy,re

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') # We don't want to send to X, rather to a imaging backend




# Change this to your root dir, where this file is located
DIRROOT = '/home/dan/Desktop/CASPERGUI'
port = 7147

def bin2dec(binary):
    return int(binary,2)

def dec2bin(decimal):
    HexBin ={"0":"0000", "1":"0001", "2":"0010", "3":"0011", "4":"0100", "5":"0101", "6":"0110", "7":"0111", "8":"1000", "9":"1001", "A":"1010", "B":"1011", "C":"1100", "D":"1101", "E":"1110", "F":"1111"}
    return "".join([HexBin[i] for i in '%X'%decimal]).lstrip('0')


def dec2hex(n):
    """return the hexadecimal string representation of integer n"""
    return "%X" % n
     
def hex2dec(s):
    """return the integer value of a hexadecimal string s"""
    return int(s, 16)

# Ping class
# Threaded version from wellho.net
from threading import Thread
class Pinger(Thread):
   def __init__ (self,ip):
      Thread.__init__(self)
      self.ip = ip
      self.status = -1
      self.lifeline = re.compile(r"(\d) received")
   def run(self):
      pingaling = os.popen("ping -q -c1 "+self.ip,"r")
      while 1:
        line = pingaling.readline()
        if not line: break
        igot = re.findall(self.lifeline,line)
        if igot:
           self.status = int(igot[0])

# ping def
def ping(hostlist):

    responses = []
    for host in hostlist:
       ip = str(host)
       current = Pinger(ip)
       responses.append(current)
       current.start()
    
    time.sleep(0.5)
    
    statuses = []
    for response in responses:
        statuses.append(response.status)
    return statuses


# Static files
@route('/files/:path#.+#')
def server_static(path):
    return static_file(path, root=DIRROOT+'/files')
    

# Force download of files
@route('/download/:filename')
def download(filename):
    return static_file(filename, root=DIRROOT+'/files', download=filename)

# Roach Status: list all
@route('/')
@route('/index.html')
@route('/status')
def list_hardware():
    # Retrieve hardware list from database
    # Establish database connection
    dbconnect = sqlite3.connect('casper.db')    
    db = dbconnect.cursor()
    db.execute("SELECT * FROM hardware")
    result = db.fetchall()
    db.close()
    
    hardware_list = []
    hostlist = [row[2] for row in result]
    pinglist = ping(hostlist)
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
         "status"       : pinglist[i]
        }
        
        hardware_list.append(hardware)
        i += 1
    
    output = template('overview', rows=hardware_list)
    return output

# Roach Status: overview of single piece of kit
@route('/status/:id')
def view_hardware(id):
    # Retrieve hardware list from database
    idno = int(id)
    sql = "SELECT * FROM hardware WHERE id=%i"%idno
    # Establish database connection
    dbconnect = sqlite3.connect('casper.db') 
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
     "type"         : result[9]
    }

    output = template('status', hardware=hardware)
    return output

# List registers (enhanced ?listdev)
@route('/:roach/listreg')
def read_regs(roach):
    
    fpga = corr.katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    registers = fpga.listdev()
    fpga.stop()

    # Sort out t he list of registers using regex matches
    pattern_snap = re.compile('snap_\w+_ctrl')
    pattern_sys = re.compile('sys_\w+')
    pattern_excl = re.compile("\w+(_bram|_addr)")

    snaplist, syslist, reglist = [], [], []

    # Filter registers one by one
    for register in registers:
        snap = pattern_snap.match(register)
        sys  = pattern_sys.match(register)
        excl = pattern_excl.match(register)
        
        if snap: snaplist.append(snap.group().rstrip('_ctrl'))
        elif sys: syslist.append(sys.group())
        elif not(excl): reglist.append(register)

    print "\nAvailable snap registers:"
    for item in snaplist: print "\t%s"%item
    print "\nAvailable system registers:"
    for item in syslist: print "\t%s"%item
    print "\nRegisters you might want to read/set:"
    for item in reglist: print "\t%s"%item

    output = template('listreg', reglist=[snaplist, syslist, reglist])
    
    return output
    
# List bitstreams (?listbof)
@route('/:roach/listbof')
def read_regs(roach):
    
    fpga = corr.katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    boflist = fpga.listbof()
    fpga.stop()

    output = template('listbof', boflist=boflist, roach=roach, flashmsg=0)
    return output    

# Program FPGA (?progdev)
@route('/:roach/progdev/:bitstream')
def progdev(roach,bitstream):
    flashmsg = ["FAILURE: progdev failed for some reason.", "error"]
    
    fpga = corr.katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    if(fpga.is_connected()):
        fpga.progdev(bitstream)
        flashmsg = ["Programmed with %s"%bitstream, "success"] 
    boflist = fpga.listbof()
    fpga.stop()
    output = template('listbof', boflist=boflist, roach=roach, flashmsg=flashmsg)
    return output        

# ?read_int implementation for IO registers
@route('/:roach/readint/:regname')
def read_int(roach, regname):
    
    
    fpga = corr.katcp_wrapper.FpgaClient(roach, port, timeout=10)
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
@route('/:roach/snap/:snap_id/bytes/:bytes/fmt/:fmt')
def snap32(roach, snap_id, bytes, fmt):
    fpga = corr.katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    
    if(fpga.is_connected()):
        # grab the snap data and unpack
        fpga.write_int(snap_id+'_ctrl', 0)
        fpga.write_int(snap_id+'_ctrl', 1)
        packed = fpga.read(snap_id+'_bram',int(bytes))
        data = numpy.fromstring(packed, dtype=fmt)
        fpga.stop()
        
        # Generate a graph using matplotlib
        import matplotlib
        matplotlib.use('Agg') # We don't want to send to X, but to a backend
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(data)
        ax.set_title(snap_id)
        ax.set_xlim(0,len(data))
        fig.savefig('files/temp.png')
        
        output = template('plot_snap', snap_id=snap_id, fmt=fmt, bytes=bytes)
        return output     
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"


# Hardware management
# Create, Update & Delete
# Create new piece of kit
@route('/add', method='GET')
def hardware_add():
    
    try:
        if request.GET.get('save','').strip():
            hostname = request.GET.get('hostname', '').strip()
            nickname = request.GET.get('nickname', '').strip()
            MAC_address = request.GET.get('MAC_address', '').strip()
            IP_address = request.GET.get('IP_address', '').strip()
            location = request.GET.get('location', '').strip()
            notes = request.GET.get('notes', '').strip()
            serial = request.GET.get('serial', '').strip()
            firmware = request.GET.get('firmware', '').strip()
            atype = request.GET.get('type', '').strip()
            # Establish database connection
            dbconnect = sqlite3.connect('casper.db') 
            db = dbconnect.cursor()
            db.execute("INSERT INTO hardware (hostname,nickname,MAC_address,IP_address,location,notes,serial,firmware,type) VALUES (?,?,?,?,?,?,?,?,?)", (hostname,nickname,MAC_address,IP_address,location,notes,serial,firmware,atype))
        
            new_id = db.lastrowid
            dbconnect.commit()
            db.close()
            return '<p>Hardware with ID number %s updated successfully.</p>' %new_id
        else:
           return template('hardware_add.tpl') 
    except:
        return template('hardware_add.tpl')

# Edit piece of kit
@route('/edit/:id', method='GET')
def hardware_edit(id):
    try:
        if request.GET.get('save','').strip():

            hostname = request.GET.get('hostname', '').strip()
            nickname = request.GET.get('nickname', '').strip()
            MAC_address = request.GET.get('MAC_address', '').strip()
            IP_address = request.GET.get('IP_address', '').strip()
            location = request.GET.get('location', '').strip()
            notes = request.GET.get('notes', '').strip()
            serial = request.GET.get('serial', '').strip()
            firmware = request.GET.get('firmware', '').strip()
            atype = request.GET.get('type', '').strip()
            # Establish database connection
            dbconnect = sqlite3.connect('casper.db') 
            db = dbconnect.cursor()
            db.execute("UPDATE hardware SET hostname = ?, nickname = ?, MAC_address = ?, IP_address = ?,location = ?, notes = ?, serial = ?, firmware = ?, type= ? WHERE id LIKE ?", (hostname,nickname,MAC_address,IP_address,location,notes,serial,firmware,atype,id))

            dbconnect.commit()
            db.close()
            return '<p>Hardware with ID %s updated successfully.</p>' %id
        else:
            idno = int(id)
            sql = "SELECT * FROM hardware WHERE id=%i"%idno
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
             "type"         : result[9]
            }
                
            output = template('hardware_edit.tpl', hardware=hardware)
            return output
    except:
        return '<p>Error: record could not be loaded</p>'


# Delete piece of kit
@route('/delete/:id')
def hardware_delete(id):
    sql = "DELETE FROM hardware WHERE id=%s"%id
    # Establish database connection
    dbconnect = sqlite3.connect('casper.db') 
    db = dbconnect.cursor()
    try:
        db.execute(sql)
        dbconnect.commit()
        db.close()
    except:
        # Establish database connection
        db.rollback()
        db.close()
    return '<p>Hardware with ID %s deleted successfully</p>'%id    




# D-PAD Spectrometer quick look
# Specifically designed for D-PAD fast transient backend
# Where the even and odd channels are 16.0_16.0 concatenated in 32bit BRAM
@route('/:roach/spectrometer')
def read_regs(roach):
    
    fpga = corr.katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    registers = fpga.listdev()
    flashmsgs = [] # We will be sending back some informative messages

    # ToDo: make this work with a for loop and not hard coded!
    if request.GET.get('update','').strip():
        fft_shift_old = int(request.GET.get('fft_shift_old','').strip(),2)
        fft_shift_new = int(request.GET.get('fft_shift_new','').strip(),2)
        gain_old = int(request.GET.get('gain_old','').strip(),16)
        gain_new = int(request.GET.get('gain_new','').strip(),16)
        acc_len_old = int(request.GET.get('acc_len_old','').strip())
        acc_len_new = int(request.GET.get('acc_len_new','').strip())
        
        
        reset_req = 0
        if(fft_shift_old != fft_shift_new): 
            fpga.write_int('fft_shift',fft_shift_new)
            reset_req = 1
            flashmsgs.append('fft_shift changed to %i'%fft_shift_new)
        if(acc_len_old != acc_len_new): 
            fpga.write_int('acc_len',acc_len_new)
            reset_req = 1
            flashmsgs.append('acc_len changed to %i'%acc_len_new)
        if(gain_old != gain_new): 
            fpga.write_int('gain',gain_new)
            flashmsgs.append('gain changed to %i'%gain_new)
            reset_req = 1
        if(reset_req):
            fpga.write_int('sync_rst',1)
            fpga.write_int('sync_en',1)
            time.sleep(0.5)
            fpga.write_int('sync_rst',0)
            fpga.write_int('sync_en',0)
            flashmsgs.append('Registers changed: sync pulse sent')

    if request.GET.get('reset','').strip():
        fpga.write_int('cnt_rst',1)
        time.sleep(0.1)
        fpga.write_int('cnt_rst',0)
        fpga.write_int('sync_rst',1)
        time.sleep(0.1)
        fpga.write_int('sync_rst',0)

        fpga.write_int('sync_en',1)
        time.sleep(1)
        fpga.write_int('sync_en',0)
        flashmsgs.append('Counters reset & sync pulse sent.')
    
    # Sort out the list of registers using regex matches
    pattern_snap = re.compile('snap_\w+_ctrl')
    pattern_sys = re.compile('sys_\w+')
    pattern_excl = re.compile("\w+(_bram|_addr)")

    snaplist, syslist, reglist = [], [], []

    
    reg = {
     "gain"        : dec2hex(fpga.read_int('gain')),
     "fft_shift"   : dec2bin(fpga.read_int('fft_shift')),
     "acc_len"     : fpga.read_int('acc_len'),
     "acc_cnt"     : fpga.read_int('acc_cnt'),
     "fft_of"     : fpga.read_int('fft_of'),
    }
    
    snap_id = 'snap_i'
    fmt = 'uint16'
    bytes = 2*256 # 16 bit=2 bytes, 256 channels
     
    if(fpga.is_connected()):
        # grab the snap data and unpack
        fpga.write_int(snap_id+'_ctrl', 0)
        fpga.write_int(snap_id+'_ctrl', 1)
        packed = fpga.read(snap_id+'_bram',int(bytes))
        data = numpy.fromstring(packed, dtype=fmt)
        fpga.stop()
        
        # Generate a graph using matplotlib
        fig = plt.figure(figsize=(7,5.25))
        ax = fig.add_subplot(111)
        freqs=numpy.arange(1000.0,1500.0,500.0/256)
        ax.plot(freqs,data)
        ax.set_title(snap_id)
        
        ax.set_xlim(1000,1500)
        ax.set_xlabel('Frequency (MHz)')
        ax.set_ylabel('Power (-)')
        fig.savefig('files/temp.png')
        
        output = template('spectrometer', snap_id=snap_id, fmt=fmt, bytes=bytes, reg=reg, flashmsgs=flashmsgs)
        return output     
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"


        
# Development mode
debug(True)
#run(reloader=True, host='180.149.250.248')
run(host='127.0.0.1', server=PasteServer, reloader=True)
