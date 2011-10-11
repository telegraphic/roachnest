.. Stuff documentation master file, created by
   sphinx-quickstart on Tue Mar 29 17:24:58 2011.


CASPERGUI Documentation
=================================

Copyright & Licensing
---------------------

**CASPERGUI: A browser based user interface for monitor & control of CASPER hardware**

*Copyright (C) 2011  Danny Price*

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

.. toctree::


Introduction
-------------

Caspergui is a browser based Graphical User Interface (GUI) for control of CASPER hardware.
This script utilises the KATCP python libraries, the bottle web framework, 
and sqlite3:

   * http://casper.berkeley.edu/wiki/KATCP
   * http://bottle.paws.de/
   * http://docs.python.org/library/sqlite3.html

The HTML/CSS is based on blueprint CSS web framework, and plotting is done with HTML5/javascript flot:

   * http://www.blueprintcss.org/
   * http://code.google.com/p/flot/

This is still under heavy development, with features being added / removed sporadically. Use at your own risk, and be aware that I've done no security checking (so don't run this on the world wide web).

Usage
-----

Assuming you've got the dependencies sorted, all you should need to do is run:

.. sourcecode:: python

    >> python caspergui.py <ROACH_NAME or IP> [options]

for example, I've got an entry in my /etc/hosts file for 'junebug', whose IP address is 192.168.126.3. I would
run:

.. sourcecode:: python

    >> python caspergui.py junebug

This would start up a webserver on localhost:8080, and junebug is set as the roach to send and receive queries from. The options available are:

.. sourcecode:: python

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  Select KATCP port. Default is 7147
      -i HOSTIP, --hostip=HOSTIP
                            change host IP address to run server. Default is
                            localhost (127.0.0.1)
      -P HOSTPORT, --hostport=HOSTPORT
                            change host port for server. Default is 8080


        
.. figure:: picture.jpg
    :scale: 50%
    :alt: alternate text
    :align: center
    
    apparently this will show up as a caption


Module Listing
--------------

.. automodule:: caspergui
    :members:

.. automodule:: xport
    :members:
    
.. automodule:: katcp_helpers
    :members: