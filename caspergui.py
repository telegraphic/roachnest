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
import lib.katcp_wrapper as katcp_wrapper
from lib.katcp_helpers import *
import lib.xport as xport

DIRROOT = os.getcwd() #automatically set root dir to this script's location

# Static files
@route('/files/:path#.+#')
def server_static(path):
    return static_file(path, root=DIRROOT+'/files')

# Force download of files
@route('/download/:filename')
def download(filename):
    return static_file(filename, root=DIRROOT+'/files', download=filename)

# Index page
@route('/')
@route('/index.html')
def index():
    pinglist = ping([roach])
    view = template('index', flashmsgs=0, ping=pinglist, roach=roach)
    return view    

# Power ON
@route('/poweron')
def power_on():
   ip, port = ('192.168.4.20', 10001)
   xp = xport.Xport(ip, port)
   xp.close()
   
   flashmsgs = []
   flashmsgs.append(xp)
   print xp.connect()
   flashmsgs.append(xp.connect())
   #flashmsg.append(xp.power_up())
   
   output = template('index', flashmsgs=flashmsgs, roach=roach)
   return output

# List registers (enhanced ?listdev)
@route('/listreg')
def listreg():
    """reads registers and then prints them"""
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
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
    pattern_excl   = re.compile("\w+(_ctrl|_addr|_rst|_en|_msb)")

    snaplist, snap64list, syslist, reglist = [], [], [], []

    # Filter registers one by one
    for register in registers:
        snap   = pattern_snap.match(register)
        snap64 = pattern_snap64.match(register)
        sys    = pattern_sys.match(register)
        excl   = pattern_excl.match(register)
        
        if snap: snaplist.append(snap.group().split('_bram')[0])
        elif snap64: snap64list.append(snap64.group().split('_bram_lsb')[0])
        elif sys: syslist.append(sys.group())
        elif not(excl): reglist.append(register)

    vals = []
    for item in reglist: 
        vals.append(fpga.read_int(item))

    data = {
         "snaplist"     : snaplist,
         "snap64list"   : snap64list,
         "syslist"      : syslist,
         "reglist"      : reglist,
         "vals"         : vals,
         "flashmsg"     : flashmsg
    }

    fpga.stop()
    output = template('listreg', data=data)
    
    return output
    
# List bitstreams (?listbof)
@route('/listbof')
def listbof():
    
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    boflist = fpga.listbof()
    boflist.sort()
    fpga.stop()
    
    '''
    boflist = os.listdir('dummy/boffiles')
    roach = 'bowie'
    '''
    output = template('listbof', boflist=boflist, roach=roach, flashmsg=0)
    return output    

# Program FPGA (?progdev)
@route('/progdev/:bitstream')
def progdev(bitstream):
    flashmsg = ["FAILURE: progdev failed for some reason.", "error"]
    
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    if(fpga.is_connected()):
        fpga.progdev(bitstream)
        flashmsg = ["Programmed with %s"%bitstream, "success"] 
    boflist = fpga.listbof()
    fpga.stop()
    output = template('listbof', boflist=boflist, roach=roach, flashmsg=flashmsg)
    return output        

# ?read_int implementation for IO registers
@route('/readint/:regname')
def read_int(regname):
    
    
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
    
# snap block plotter (64 bit)
@route('/snap64/:snap_id/bytes/:bytes')
def snap64(snap_id, bytes):
    
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(0.1)
    
    if(fpga.is_connected()):
        # grab the snap data and unpack
        fpga.write_int(snap_id+'_ctrl', 0)
        fpga.write_int(snap_id+'_ctrl', 1)
        
        packed_msb = fpga.read(snap_id+'_bram_msb',int(bytes))
        packed_lsb = fpga.read(snap_id+'_bram_lsb',int(bytes))
        
        fpga.stop()
        
        data_lsb =  np.fromstring(packed_lsb, dtype='uint32').byteswap()
        data_msb =  np.fromstring(packed_msb, dtype='uint32').byteswap()
        
        
        data = []

        #Step 3: Sew these back together
        for i in range(len(data_lsb)):
            data.append((data_msb[i] << 32) + data_lsb[i])

        flotdata = []
        for i in range(0,len(data)):
            flotdata.append([i,data[i]])
        
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
        
        output = template('plot_snap', data=flotdata, snap_id=snap_id, fmt='uint32*2', bytes=bytes, avg=0)
        return output     
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"



# Interleaver
@route('/interleaved')
def interleavr():

    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(0.1)
    bytes=4096*4
    

    if(fpga.is_connected()):
        # grab the snap data and unpack
        snap_id = 'snap32_even0'
        fpga.write_int(snap_id+'_ctrl', 0)
        fpga.write_int(snap_id+'_ctrl', 1)

        packed_msb = fpga.read(snap_id+'_bram',bytes)

        snap_id = 'snap32_odd0'
        fpga.write_int(snap_id+'_ctrl', 0)
        fpga.write_int(snap_id+'_ctrl', 1)

        packed2_msb = fpga.read(snap_id+'_bram',bytes)

        fpga.stop()

        data_msb =  np.fromstring(packed_msb, dtype='uint32').byteswap()
        data2_msb =  np.fromstring(packed2_msb, dtype='uint32').byteswap()
        
        data = []

        #Step 3: Sew these back together
        for i in range(len(data_msb)):
            data.append(10* np.log10(data_msb[i]))
            data.append(10* np.log10(data2_msb[i]))
            
        # Dump a timestamped pickle
        import cPickle as pkl
        from datetime import datetime
        now = str(datetime.now())
        filename = DIRROOT+"/pickles/%s.pkl"%now
        file = open(filename, "wb")
        pkl.dump(data,file)
        file.close()
        
        # Generate a graph using matplotlib
        import matplotlib
        matplotlib.use('Agg') # We don't want to send to X, but to a backend
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(data)
        ax.set_title("HIPSR spectrum: %s"%now)
        ax.set_xlim(0,len(data))
        fig.savefig('files/temp.png')

        output = template('plot_snap', snap_id=snap_id, fmt='uint32*2', bytes=bytes, avg=0)
        return output     
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"
 
# snap block plotter (32 bit)
@route('/snap/:snap_id/bytes/:bytes/fmt/:fmt')
def snap32(snap_id, bytes, fmt):
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(0.1)
    
    if(fpga.is_connected()):
        # grab the snap data and unpack
        fpga.write_int(snap_id+'_ctrl', 0)
        fpga.write_int(snap_id+'_ctrl', 1)
        
        packed = fpga.read(snap_id+'_bram',int(bytes))
        data =  np.fromstring(packed, dtype=fmt).byteswap()
        avg =  np.average(abs(data))
        fpga.stop()

        flotdata = []
        for i in range(0,len(data)):
            flotdata.append([i,data[i]])

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

        output = template('plot_snap', data=flotdata, snap_id=snap_id, fmt=fmt, bytes=bytes, avg=avg)
        return output     
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"

# BRAM plotter (32 bit)
@route('/bram/:snap_id/bytes/:bytes/fmt/:fmt')
def bram(snap_id, bytes, fmt):
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(0.1)

    if(fpga.is_connected()):
        # grab the snap data and unpack

        packed = fpga.read(snap_id,int(bytes))
        data =  np.fromstring(packed, dtype=fmt).byteswap()
        #import struct
        #data = struct.unpack('>%iL'%(int(bytes)/4), packed)
        
        acclen = fpga.read_int('acc_len')
        #data = data/acclen
        fpga.stop()

        # Generate a graph using matplotlib
        import matplotlib
        matplotlib.use('Agg') # We don't want to send to X, but to a backend
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(data)
        ax.set_title(snap_id)
        ax.set_xlim(-5,80)
        #ax.set_ylim(0,4.5e5)
        fig.savefig('files/temp.png')

        output = template('plot_snap', snap_id=snap_id, fmt=fmt, bytes=bytes, avg=0)
        return output     
    else:
        fpga.stop()
        return "<p> Something went wrong...</p>"

# Flot testing
@route('/flot')
def flot():
        snap_id = 'snap_block'
        fmt = 'uint8'
        bytes = 256
        
        data= []
        for i in range(0,1024):
            data.append([i,np.random.random_integers(100)-50])
        output = template('flot', data=data, fmt=fmt, bytes=bytes,snap_id=snap_id)
        return output     

# AJAX test thing.
@route('/is_ajax')
def is_ajax():
    if request.header.get('X-Requested-With') == 'XMLHttpRequest':
        time.sleep(2)
        return 'Your mum goes to college'
    else:
        return 'This is a normal request'

# D-PAD Spectrometer quick look
# Specifically designed for D-PAD fast transient backend
# Where the even and odd channels are 16.0_16.0 concatenated in 32bit BRAM
@route('/spectrometer')
def read_regs():
    
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    registers = fpga.listdev()
    flashmsgs = [] # We will be sending back some informative messages

    # ToDo: make this work with a for loop and not hard coded!
    if request.GET.get('update','').strip():
        fft_shift_old = request.GET.get('fft_shift_old','').strip()
        if(fft_shift_old==''):
            fft_shift_old = 0
        else:
            fft_shift_old = int(fft_shift_old,2)
        fft_shift_new = int(request.GET.get('fft_shift_new','').strip(),2)
        
        gain_old = request.GET.get('gain_old','').strip()
        if(gain_old==''):
            gain_old = 0
        else:
            gain_old = int(gain_old,16)
        gain_new = int(request.GET.get('gain_new','').strip(),16)
        
        acc_len_old = request.GET.get('acc_len_old','').strip()
        if(acc_len_old==''): 
            acc_len_old = 0
        else:
            acc_len_old = int(acc_len_old)
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
        data =  np.fromstring(packed, dtype=fmt).byteswap()
        fpga.stop()
        
        # Generate a graph using matplotlib
        fig = plt.figure(figsize=(7,5.25))
        ax = fig.add_subplot(111)
        freqs= np.arange(1000.0,1500.0,500.0/256)
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


@route('/upload')
def uploader():
    output = template('upload')
    return output

@route('/upload/do', method='POST')
def do_upload():
    data = request.files.get('data')
    raw = data.file.read() # This is dangerous for big files
    filename = data.filename
    f = open(DIRROOT+'/config/'+filename,'wb')
    f.write(raw)
    f.close()
    return "You uploaded %s (%d bytes)." % (filename, len(raw))

@route('/config/:filename')
def config(filename):
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)
    time.sleep(1)
    
    #etree.parse() opens and parses the data
    xmlData = etree.parse('config/%s'%filename) 

    config = xmlData.getroot()
    registers = config.findall('register')

    flashmsgs =[]

    for reg in registers:
        flashmsgs.append("Writing value %s to register %s"%(reg.attrib['value'],reg.attrib['name']))
        writereg(fpga, reg.attrib['name'],reg.attrib['value'],reg.attrib['base'])
    
    output = template('simpleflash', flashmsgs=flashmsgs)
    return output
        
if __name__ == '__main__':

    # Option parsing to allow command line arguments to be parsed
    from optparse import OptionParser
    p = OptionParser()
    p.set_usage('caspergui.py <ROACH_HOSTNAME_or_IP> [options]')
    p.set_description(__doc__)
    p.add_option("-k", "--katcpport", dest="port", type="int", default=7147,
                 help="Select KATCP port. Default is 7147")
    p.add_option("-i", "--hostip", dest="hostip", type="string", default="127.0.0.1",
                 help="change host IP address to run server. Default is localhost (127.0.0.1)")
    p.add_option("-p", "--hostport", dest="hostport", type="int", default=8080,
                 help="change host port for server. Default is 8080")

    (options, args) = p.parse_args(sys.argv[1:])

    if args==[]:
        print 'Error: no roach selected. Need help? Run with the -h flag to see all options.'
        exit()
    else:
        roach = args[0]
    
    port = options.port
    hostip = options.hostip
    hostport = options.hostport
    
    fpga = katcp_wrapper.FpgaClient(roach, port, timeout=10)

    # Development mode
    debug(True)
    
    #Start bottle server
    run(host=hostip, port=hostport, reloader=True)
