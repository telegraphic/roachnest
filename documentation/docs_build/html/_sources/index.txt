.. Stuff documentation master file, created by
   sphinx-quickstart on Tue Mar 29 17:24:58 2011.


ROACHNEST Documentation
=================================

Copyright & Licensing
---------------------

**ROACHNEST: A browser based user interface for monitor & control of CASPER hardware**

*Copyright (C) 2011  Danny Price*

**Everything I've written:** GNU General Public License (GPL)

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

**Everything else:** As per author's original licensing terms. 
Bottle.py and Flot are MIT licensed, Blueprint is a modified MIT license,
sqlite3 is public domain.

Introduction
-------------

Roachnest is a browser based Graphical User Interface (GUI) for control of CASPER hardware.
This script utilises the KATCP python libraries, the bottle web framework, and sqlite3:

   * http://casper.berkeley.edu/wiki/KATCP
   * http://bottle.paws.de/
   * http://docs.python.org/library/sqlite3.html

The HTML/CSS is based on blueprint CSS web framework, and plotting is done with HTML5/javascript flot:

   * http://www.blueprintcss.org/
   * http://code.google.com/p/flot/

**Warning:** I strongly suggest that this is available only through an internal network and 
is not made accessible via the WWW. Use at your own risk.

Screenshots
-----------
        
.. figure:: screenshot_index.png
    :scale: 30%
    :alt: Index page - screenshot
    :align: center
    
    Homepage: hardware management

.. figure:: screenshot_status.png
    :scale: 30%
    :alt: Status page - screenshot
    :align: center
    
    Detailed status and board control.
    
.. figure:: screenshot_plotsnap.png
    :scale: 30%
    :alt: Plot snap - screenshot
    :align: center
    
    Javascript plotting of snap BRAMs.

.. figure:: screenshot_listreg.png
    :scale: 30%
    :alt: List available registers - screenshot
    :align: center
    
    Reading and writing shared registers.

Getting Started
---------------

The first thing you'll need to do is to satisy the dependencies. You'll need:

  os, sys, time, re, struct, sqlite3_, bottle_, numpy_, katcp_, paste_, lxml_

.. _sqlite3: http://docs.python.org/library/sqlite3.html
.. _bottle: http://bottlepy.org/docs/dev/
.. _numpy: http://numpy.scipy.org/
.. _katcp: http://pypi.python.org/pypi/katcp/0.3.4
.. _paste: http://pythonpaste.org/
.. _lxml: http://lxml.de/

Note that paste_ and lxml_ are optional: paste improves webserver performance by using threading, and 
lxml is for parsing configuration files -- although these won't appear until a future release!

After downloading the files, you should edit *lib/config.py*, and check
that you're happy with the configuration. Note that you can change the page titles and the logo
in this file.

Next, assuming you've got the dependencies sorted, all you should need to do is run:

.. sourcecode:: python

    >> python roachnest.py  [options]

This would start up a webserver on localhost:8080. The options available are:

.. sourcecode:: python

    Options:
      -h, --help            show this help message and exit
      -p PORT, --port=PORT  Select KATCP port. Default is 7147
      -i HOSTIP, --hostip=HOSTIP
                            change host IP address to run server. Default is
                            localhost (127.0.0.1)
      -P HOSTPORT, --hostport=HOSTPORT
                            change host port for server. Default is 8080

Once the webserver is up and running, open a browser up and surf over to localhost:8080, or if you've changed
the IP address and port, type these in instead (eg. 192.168.126.6:8888). If you want the page to be viewable
over a network, you'll have to use the *--hostip* option and point this to the IP address of your ethernet card.

Module Listing
--------------

.. automodule:: roachnest
    :members:
    
.. automodule:: roachnest_helpers
    :members:

.. automodule:: ping
    :members:

.. automodule:: xport
    :members: