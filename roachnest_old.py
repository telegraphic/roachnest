###################################################
###  OLD FUNCTIONS - REQUIRE UPDATE / DELETION  ###
###################################################

# snap block plotter (64 bit)
@route('/snap64/:snap_id/bytes/:bytes')
def snap64(snap_id, bytes):
    """ URL: *@route('/snap64/:snap_id/bytes/:bytes')*"""
    
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
    """URL: *@route('/interleaved')*"""
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

# BRAM plotter (32 bit)
@route('/bram/:snap_id/bytes/:bytes/fmt/:fmt')
def bram(snap_id, bytes, fmt):
    """ URL: *@route('/bram/:snap_id/bytes/:bytes/fmt/:fmt')*"""
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



###############################
###   HARDWARE MANAGEMENT   ###
###############################

# Create, Update & Delete
# Create new piece of kit
@route('/add', method='GET')
def hardware_add():
    """URL: *@route('/add', method='GET')*"""
    
    try:
        if request.GET.get('save','').strip():
            hostname = request.GET.get('hostname', '').strip()
            nickname = request.GET.get('nickname', '').strip()
            MAC_address = request.GET.get('MAC_address', '').strip()
            IP_address = request.GET.get('IP_address', '').strip()
            XPORT_address = request.GET.get('XPORT_address', '').strip()
            location = request.GET.get('location', '').strip()
            notes = request.GET.get('notes', '').strip()
            serial = request.GET.get('serial', '').strip()
            firmware = request.GET.get('firmware', '').strip()
            atype = request.GET.get('type', '').strip()
            # Establish database connection
            dbconnect = sqlite3.connect(DB_NAME) 
            db = dbconnect.cursor()
            db.execute("INSERT INTO hardware (hostname,nickname,MAC_address,IP_address,location,notes,serial,firmware,type,XPORT_address) VALUES (?,?,?,?,?,?,?,?,?,?)", (hostname,nickname,MAC_address,IP_address,location,notes,serial,firmware,atype,XPORT_address))
        
            new_id = db.lastrowid
            dbconnect.commit()
            db.close()
            return '<p>Hardware with ID number %s updated successfully.</p>' %new_id
        else:
           return template('hardware_add.tpl') 
    except:
        return oops

# Edit piece of kit
@route('/edit/:id', method='GET')
def hardware_edit(id):
        """URL: *@route('/edit/:id', method='GET')*"""
        id = int(id)
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
            dbconnect = sqlite3.connect(DB_NAME) 
            db = dbconnect.cursor()
            db.execute("UPDATE hardware SET hostname = ?, nickname = ?, MAC_address = ?, IP_address = ?,location = ?, notes = ?, serial = ?, firmware = ?, type= ? WHERE id LIKE ?", (hostname,nickname,MAC_address,IP_address,location,notes,serial,firmware,atype,id))

            dbconnect.commit()
            db.close()
            return '<p>Hardware with ID %s updated successfully.</p>' %id
        else:
            roach = dbget(id)

            output = template('hardware_edit.tpl', hardware=hardware)
            return output


# Delete piece of kit
@route('/delete/:id')
def hardware_delete(id):
    """ URL: *@route('/delete/:id')*"""
    sql = "DELETE FROM hardware WHERE id=%s"%id
    # Establish database connection
    dbconnect = sqlite3.connect(DB_NAME) 
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
@route('/spectrometer')
def spectrometer():
    """URL: *@route('/spectrometer')*"""
    
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
    """ URL: *@route('/upload')* """
    output = template('upload')
    return output

@route('/upload/do', method='POST')
def upload():
    """ URL: *@route('/upload/do', method='POST')* """
    data = request.files.get('data')
    raw = data.file.read() # This is dangerous for big files
    filename = data.filename
    f = open(DIRROOT+'/config/'+filename,'wb')
    f.write(raw)
    f.close()
    return "You uploaded %s (%d bytes)." % (filename, len(raw))

@route('/config/:filename')
def config(filename):
    """ URL: *@route('/config/:filename')*"""
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

