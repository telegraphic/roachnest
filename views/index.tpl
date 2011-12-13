%#status.tpl: CASPER GUI Template for status page
% import lib.config as config

%include header title='Hardware Overview'

%if(flashmsgs != 0 and flashmsgs != []):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

%if(not rows==[]):
<p>This page lists the status of CASPER hardware that is registered in roachnest's database:</p>
<table>
<thead>
<tr>
	<th>ID</th>
	<th>hostname</th>
	<th>MAC Address</th>
	<th>IP Address</th>
	<th>XPORT Address</th>
	<th>PPC Ping</th>
	<th>Xport Ping</th>
	<th>Actions</th>
</tr>
</thead>
<tbody>
%for row in rows:
  <tr>
  	<td>{{row["id"]}}</td>
	<td><a href="/status/{{row["id"]}}">{{row["hostname"]}}</a></td>
	<td>{{row["MAC_address"]}}</td>
	<td>{{row["IP_address"]}}</td>
	<td>{{row["XPORT_address"]}}</td>

	<td>
	%if(row["status"] == 1):
	  <span class="ss_sprite ss_accept "> &nbsp; </span>
	%else:
	  <span class="ss_sprite ss_cancel"> &nbsp; </span>
	%end	
	</td>

	<td>
	%if(row["XPORT_status"] == 1):
	  <span class="ss_sprite ss_accept "> &nbsp; </span>
	%else:
	  <span class="ss_sprite ss_cancel"> &nbsp; </span>
	%end	
	</td> 
  <td>
    <form action="../">
<select onchange="window.open(this.options[this.selectedIndex].value,'_top')">
    <option value="">Select...</option>
    <option value="/status/{{row['id']}}">Status</option>
    <option value="/listbof/{{row['id']}}">Reprogram FPGA</option>
    <option value="/listreg/{{row['id']}}">List Registers</option>
    <option value="/poweron/{{row['id']}}">Power ON</option>
    <option value="/poweroff/{{row['id']}}">Power OFF</option>
</select>
</form>
</td>

  </tr>
%end
</tbody>
</table>

<div class="db_nav">
  <a href="/add">
    <span class="ss_sprite ss_database_add"> &nbsp; </span>  Add new hardware
  </a>
</div>

<form name="power" action="/" method="GET">  
<input type="submit" value="Power all ON" name="power" />
<input type="submit" value="Power all OFF" name="power" />
</form>

%else:
<h2> Welcome to roachnest</h2>

<p> Roachnest can't find any entries in its database, <em>{{config.database}}</em>.

<h3>Getting started</h3>
<p> If you've only just started, you need to create a database and add some hardware. 
    <a href="/dbcreate">click here to get started</a>.</p>

<h3> Help, I've got an error! </h3>
<p> Some possible reasons you're seeing this are:
  
<ul>
  <li><strong>Your config is incorrect.</strong> Have a look in <em>lib/config.py</em>, and check 
    there's nothing fishy going on.</li>
  <li><strong>Your database is dead / non-existent.</strong> Your database should be located in the
  root directory, and with the name {{config.database}}, which is set in <em>lib/config.py</em></li>
</ul>

%end

%include footer
