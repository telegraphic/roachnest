#!/usr/bin/env python
# encoding: utf-8
"""
xport.py
========

Created by Danny Price, 03 October 2011.\n
Based on roach_monitor.py at:
https://casper.berkeley.edu/wiki/Roach_monitor_and_management_subsystem

This module allows for communication with the ROACH X-port. 
ROACH has an onboard, fully independent management subsystem that can be accessed through the Xport. 
The X-port system monitors voltages and temperatures and will shut down the board 
if these are out of specification. A log is kept of the shutdown cause, its value and time.

"""

# Python metadata
__author__    = "Danny Price"
__license__   = "GNU GPL"
__version__   = "1.0"

import socket,struct,os,sys,time

class xportError(Exception):
   """A simple class for X-port error handling"""
   def __init__(self, msg):
      self.msg = msg
      Exception.__init__(self, msg)
   def __str__(self):
      return repr(self.msg)

class Xport(object):
   """Actel Fusion X-port class, for communicating with M&C"""
   def __init__(self, ip, port):
      super(Xport, self)
      self.ip = ip
      self.port = port
      self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      self.is_connected = False
   
      self.serial = 0
      self.id     = 0
      
   def __repr__(self):
      return "X-PORT object, IP: %s, port: %i"%(self.ip, self.port)
   
   
   
   ################################
   ###    Basic connectivity    ###
   ################################
       
   def connect(self):
      """Connect to xport socket"""
      print "Connecting to x-port %s:%i..."%(self.ip, self.port),
      try: 
         self.socket.connect((self.ip,self.port))
      except:
         self.is_connected = False
         return "\nError: cannot connect to port:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
      print "OK."
      
      # Flush receiver buffer
      self.is_connected = True
      return self.is_connected
      
   def close(self):
     """Close xport socket connection"""
     try:
       self.socket.close()
     except:
       return "\nError: cannot connect to port:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
       
     self.is_connected = False
   
   def flush(self):
      """Flush receive buffer"""
      print "Flushing receive buffer ...",
      
      self.socket.setblocking(False)
      try: 
        raw=self.socket.recv(10)
      except: 
        print "\nError: receive buffer flush:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
        self.is_connected = False
        raise
      self.socket.setblocking(True)
   
   def write(self,addr,value):
       """Writes a 16bit value to the Fusion part through the Xport."""
       if(not self.is_connected):
         print "Warning: x-port not connected.\nAttempting to connect to x-port..."
         self.connect()
         
       request=struct.pack('<5B',0x02,addr&0xff,(addr&0xff00)>>8,value&0xff,(value&0xff00)>>8)
       self.socket.send(request)
       raw=self.socket.recv(10)
       
       if len(raw) != 1:
           self.socket.close()
           raise xportError("Write Error: Incorrect number of bits returned")
                
   def read(self,addr):
       """Reads a 16bit value from the Fusion part through the Xport."""
       
       if(not self.is_connected):
         print "Warning: x-port not connected.\nAttempting to connect to x-port..."
         self.connect()
         
       request=struct.pack('<3B',0x01,addr&0xff,(addr&0xff00)>>8)
       self.socket.send(request)
       raw=self.socket.recv(10)
       
       if len(raw) == 3:
           raw_unpacked=struct.unpack('<%iB'%len(raw),raw)
           #print 'Received: ',raw_unpacked
           value=(raw_unpacked[2]<<8) + raw_unpacked[1]
           #print 'Received value: ',value
           return value
       
       else:
           raw_unpacked=struct.unpack('<%iB'%len(raw),raw)
           self.socket.close()
           raise xportError("Read Error: Incorrect number of bits returned")
           
           
           
   ################################
   ###      Power & Reset       ###
   ################################
      
   def power_up(self):
       """Power up the ROACH (Wake on LAN)"""
       try:
          self.write(0x281,0xffff)
       except:
          return "\nError: power up failed\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
       return "Powered up successfully."
   
   def warm_rst(self):
       """Reset ROACH, but not Actel"""
       try:
          self.write(0x282,0x0)
       except:
          return "\nError: warm reset failed\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
       return "Warm reset successfully."
       
   def power_down(self):
       """Power down the ROACH"""
       try:
          self.write(0x282,0xffff)
       except:
          return "\nError: not powered down\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
       return "ROACH Powered down."
   
   def clear_crashlog(self):
       """Reset crash log counter"""
       try:
          self.write(0x283,0xffff)
       except:
          return "\nError: crash log not clearned\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
       return "Crash log cleared."

   def toggle_config_h(self):
        """todo: Toggle PPC EEPROM boot (config H)"""
        return "Not yet implemented"
        
   def toggle_power_on_reset(self):
        """todo: Toggle auto power-on after hard-reset."""
        return "Not yet implemented"
        
   def toggle_hard_threshold():
        return "Not yet implemented"
   
   
   ################################
   ###      Info Retrieval      ###
   ################################
   
   def get_serial(self):
     """Check and retrieve serial number. After first query the serial
        number is stored as class variable self.serial"""   
     if(self.serial == 0):
       try:    
         self.serial = '%c%c%c%c%c%c'%(chr(self.read(0xB8)),chr(self.read(0xB9)),chr(self.read(0xBA)),\
         chr(self.read(0xBB)),chr(self.read(0xBC)),chr(self.read(0xBD)))
         return self.serial
       except:
         return "\nError reading serial:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1]) 
     else:
       return self.serial
  
   def get_id(self):
     """Return board ID and revision"""
     if(self.id == 0):
       try:
         return 'ID: %i, revision %i.%i.%i'%(self.read(0),self.read(1),self.read(2),self.read(3))
       except:
         return "\nError reading board ID:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1]) 
       else:
         return self.id
  
   def get_board_time(self):
     """Check and retrieve board uptime. Returns board up time in seconds (int)."""
     try:
       return ((self.read(0x06)<<32)+(self.read(0x07)<<16)+(self.read(0x08)))
     except:
       return "\nError reading board uptime:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1]) 
   
   def get_power_state(self):
     """Check and retrive board power state. Returns power state as a string"""
     pwr_state_decode={4: 'Powered off', 3: 'Powered on', 2: 'Sequencing power up',\
                       1: 'Sequencing power up',0: 'Sequencing power up'}
     try:
       pwr_state_raw=self.read(0x280)
     except:
       return "\nError reading power state:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1]) 
     pwr_state=pwr_state_raw&7
     #shutdown_reason=(pwr_state_raw&0x300)>>8
     return 'Power state: %i (%s)'%(pwr_state,pwr_state_decode[pwr_state])
   
   def get_last_shutdown(self):
     """Check and retrieve reason for last shutdown. Returns reason as a string"""
     shutdown_reason_decode={0:'Cold start or hard reset', 1: 'Crash', 2:'watchdog overflow', 3: 'User shutdown'}
     try:
       pwr_state_raw=self.read(0x280)
     except:
       return "\nError reading power state:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1]) 
     #pwr_state=pwr_state_raw&7
     shutdown_reason=(pwr_state_raw&0x300)>>8
     return 'Reason for last shutdown: %i (%s)'%(shutdown_reason,shutdown_reason_decode[shutdown_reason])

   def get_power_good(self):
     """Check and retrieve power good status of voltage regulators. Returns a list of power good signals."""
     try:
       ps_powergds=self.read(0x288)
     except:
       return "\nError reading power good:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
     
     power_good = []
     
     power_good.append(('3v3aux', bool((ps_powergds&0x01)>>00)))
     power_good.append(('MGT_AVCCPLL', bool((ps_powergds&0x02)>>1)))
     power_good.append(('MGT_AVTTX', bool((ps_powergds&0x04)>>2)))
     power_good.append(('MGT_AVCC', bool((ps_powergds&0x08)>>3)))
     power_good.append(('ATX_PWR', bool((ps_powergds&0x10)>>4)))
     
     # Don't really know what the hell this line means, so I've commented it out.
     #print 'ADC values are averaged %i times.'%(2**(self.read(0x145)))
     
     return power_good

   def get_fan_speeds(self):
     """Check and retrieve fan speeds. Returns a list of fan speeds"""
     try:
      fan1 = self.read(0x300)*60
      fan2 = self.read(0x301)*60
      fan3 = self.read(0x302)*60
     except:
       return "\nError reading fan speeds:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1])
     return ("%i rpm"%fan1, "%i rpm"%fan2, "%i rpm"%fan3)
   
   def get_channels(self):
     """Retrieves the voltage and temperatures of the PPC, V5, PSU, and Actel chips. 
     
     Returns a list of format:
     (channel name, channel state, channel min operational value, channel max operational val)
     """
     channels={  7: '12V ATX (volts)', \
                10:'5V  ATX (volts)', \
                13:'3v3 ATX (volts)', \
                28:'2V5 PS  (volts)', \
                25:'1V8 PS  (volts)', \
                22:'1V5 PS  (volts)', \
                16:'1V  PS  (volts)', \
                0: '1v5aux  (volts)', \
                3: 'Virtex5 temp (deg C)', \
                9: 'PPC  temp (deg C)', \
                31:'Actl temp (deg C)'}
                
     valid_channels = channels.keys()
   
     channel_scale={0: 1600.0, \
                7: 250.0, \
                10: 500.0, \
                13: 1000.0, \
                16: 1600.0, \
                22: 1600.0, \
                25: 1600.0, \
                28: 1600.0, \
                3:  4.0, \
                9:  4.0, \
                31: 4.0, \
                11: 65.5, \
                17: 16.375, \
                23: 65.5, \
                26: 32.75, \
                29: 163.75, \
                11: 65.5, \
                14: 163.75}
                
     #the fusion measures temperature in Kelvin, with a positive 5 degree offset.
     channel_offset={ 0: 0,
                      7:0, \
                      17:0, \
                      23:0, \
                      26:0, \
                      29:0, \
                      14:0, \
                      11:0, \
                      10:0, \
                      13:0, \
                      16:0, \
                      22:0, \
                      25:0, \
                      28:0, \
                      3:-278, \
                      9:-278, \
                      31:-278}
     
     chan_state = []
     for chan in valid_channels:
         try:
           sample_addr=0x240+chan
           hard_thresh_min_addr=0x1c0+(chan*2)
           hard_thresh_max_addr=0x1c0+(chan*2)+1
         
           sample=self.read(sample_addr)/channel_scale[chan] + channel_offset[chan]
           hard_thresh_min=self.read(hard_thresh_min_addr)/channel_scale[chan] + channel_offset[chan]
           hard_thresh_max=self.read(hard_thresh_max_addr)/channel_scale[chan] + channel_offset[chan]
         except:
           return "\nError reading channel:\n\t%s\n\t%s"%(sys.exc_info()[0], sys.exc_info()[1]) 
         chan_state.append((channels[chan].rjust(15),sample,hard_thresh_min,hard_thresh_max))
     return chan_state
   
def main():
   # Test of socket connection
   ip, port = ('192.168.4.20', 10001)
   xport = Xport(ip, port)
   print xport
   # Test functionality
   print xport.connect()
   
   # print('Starting board - POWER TURN ON!')
   # print xport.power_up()
   # print('Sleeping...')
   # time.sleep(5)
   
   # Note: I've never tested these...
   # print xport.warm_rst()
   # print xport.clear_crashlog()
   
   print xport.get_serial()
   print xport.get_id()
   print xport.get_board_time()
   print xport.get_power_state()
   print xport.get_last_shutdown()
   print xport.get_fan_speeds()
   print xport.get_power_good()
   chans =  xport.get_channels()
   
   print '\nCurrent values:'
   print '%s \t%s \t%s \t%s'%('Channel'.rjust(17),'Current'.rjust(10), 'Shutdown'.rjust(10), 'Shutdown'.rjust(10))
   print '%s \t%s \t%s \t%s'%('Name'.rjust(15),'value'.rjust(8), 'below'.rjust(8), 'above'.rjust(8))
   print '====================================================================='   
   for chan in chans:
     print '%s:\t %7.2f \t%7.2f \t%7.2f'%(chan[0].rjust(15),chan[1],chan[2],chan[3])
   
   # print('shutting down...')
   # print xport.power_down()
   
if __name__ == '__main__':
   main()
