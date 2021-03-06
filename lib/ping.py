#/usr/bin/env python
 
"""
ping.py
=======

Ping multiple hosts/ip addresses in parallel, using threading

**Credits:** Modified from script by Jose Porrua:
http://www.joseporrua.com/2008/12/11/multi-threaded-ping-in-python
However, this script didn't work for me out of the box so I modified it to get it running.
"""

# Python metadata
__author__    = "Danny Price"
__license__   = "GNU GPL"
__version__   = "1.0"
 
import re, sys
import threading
from subprocess import Popen, PIPE 
 
# Globals
COUNT = 2
TIMEOUT = 1
 
class Host(object):
    """ Defines a host object. 
    
    Current attributes include: name, address and status.
    """
    def __init__ (self, ip):
        self.ip = ip
        self.status = 0
 
def pingHosts(hosts):
    """  Creates and starts pinging threads.
    
    Parameters
    ----------
    hosts: list []
      A list of host objects.
    """
    threads = []
    nloops = range(len(hosts))
 
    # Create Threads
    for i in nloops:
        t = threading.Thread(target=execute, args=[hosts[i]])
        threads.append(t)
 
    # Start Threads
    for i in nloops:
        threads[i].start()
 
    # Wait for them to finish
    for i in nloops:
        threads[i].join()
 
    # Display the results
    printResults(hosts)
    
    return hosts

def ping(hostname):
  """ Pings a single board
  
  Parameters
  ----------
  hostname: string
    hostname or IP address of hardware to ping
  """
  return pingHosts([ Host(hostname)])[0].status
 
def execute(host):
    """ Executes a ping command and sets the appropriate attribute.
    
    Parameters
    ----------
    host: ping.Host
      A host object.
    
    Notes
    -----
    This is significantly different to Jose Porrua's original script, which will not match
    ping requests on Mac OSX. TODO: Test this on Windows and modify if required.
    """
    
    # Ping differs slightly on Mac and Linux. So, we need a conditional to check.
    # Checking within this def will slow things down, but seems cleaner to me.
    status = 0
    
    if(sys.platform == 'darwin'):
      f = Popen(['ping','-c 1', '-W 1', host.ip], stdout=PIPE)
      output = f.communicate()[0]
      regex = re.compile("(\d) packets received")
      status = re.findall(regex, output)
        
    elif(sys.platform == 'linux2'):
      f = Popen(['ping','-c 1', '-w 1', host.ip], stdout=PIPE)
      output = f.communicate()[0]
      regex = re.compile("(\d) received") # This is different for Darwin!
      status = re.findall(regex, output)   
    
    else:
      f = Popen(['ping','-c 1', host.ip], stdout=PIPE) # This may be slow, but more likely to work
      output = f.communicate()[0]
      regex = re.compile("(\d) received") # This might not match correctly, but OK for default
    
    if status == []:
      status = 0
    else:
      status = int(status[0])   
    
    host.status = status
 
def printResults(hosts):
    """  Prints a results: address  status  hostname
    
    Parameters
    ----------
    hosts: list []
      A list of ping.Host objects
    """
    print
    for host in hosts:
        print "%s: %i" % (host.ip, host.status)

#####################
##   MAIN METHOD   ##
#####################
 
if __name__ == '__main__':
    hosts = []
 
    # A list of addresses. Ideally, these will come from a config file.
    addresses = ['localhost','google.com','rhinobeetle','junebug','tokolosh','grasshopper','fftt0','fftt1']
 
    # Create an object for each address
    for i in range(len(addresses)):
        hosts.append(Host(addresses[i]))
 
    # Ping them.
    pingHosts(hosts)