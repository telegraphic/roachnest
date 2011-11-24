%#status.tpl: CASPER GUI Template for status page
%include header title='%s: report'%roach["hostname"]

% # Setting up variables
% chans = xinfo["channels"]
% fans  = xinfo["fanspeeds"]

%if(flashmsgs != 0 and flashmsgs != []):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

<div class="span-7 colborder">
<table>
<thead>
	<tr><th>{{roach["hostname"]}}</th> <th>aka <em>"{{roach["nickname"]}}"</em></th></tr>
</thead>
<tbody>
    <tr><td>IP Address</td> <td>{{roach["IP_address"]}}</td></tr>
    <tr><td>MAC Address</td> <td>{{roach["MAC_address"]}}</td></tr>
    <tr><td>Type</td>		<td>{{roach["type"]}}</td></tr>
    <tr><td>Serial</td> 	<td>{{roach["serial"]}}</td></tr>
    <tr><td>Firmware</td> 	<td>{{roach["firmware"]}}</td></tr>
    <tr><td>Location</td>  	<td>{{roach["location"]}}</td></tr>
</tbody>
</table>

  <p><a href="/edit/{{roach["id"]}}" title="Edit entry"><span class="ss_sprite ss_table_edit"> &nbsp; </span> Edit info </a></p>

<br>
  
<h4>Xport information</h4>
<table>
  <tbody>
    <tr><td>Serial</td> <td>{{xinfo["serial"]}}     </td></tr>  
    <tr><td>ID</td> <td>{{xinfo["id"]}}         </td></tr>
    <tr><td>Uptime</td> <td>{{xinfo["boardtime"]}}  </td></tr>
    <tr><td>Power state</td> <td>{{xinfo["powerstate"]}} </td></tr>
    <tr><td>Last shutdown</td> <td>{{xinfo["shutdown"]}}   </td></tr>
    <tr><td>Power good?</td> <td>
      <ul>
      % for item in xinfo["powergood"]:
      <li>{{item[0]}} : {{item[1]}}</li> 
      %end
      </ul>
 </td></tr>
  </tbody>
</table>
   
</div>

<div class="span-8 colborder">
<h4>Operating temperature / voltages</h4>
<table>
  %for chan in chans:
  %  width = int( (float(chan[1])-float(chan[2])) / (float(chan[3])-float(chan[2])) * 100)
	<tr>
		<td><label>{{chan[0]}}</label></td>
		<td>{{str("%.1f")%chan[2]}}</td> 
		<td><div class="progress-container">
		    <div class="progress-text">{{str("%2.2f")%chan[1]}}</div>
		    <div class="bar" style="width: {{width}}px;"></div></div>
		    
		</td>
		<td>{{str("%.1f")%chan[3]}}</td>
	</tr>
	%end
</table>


</div>

<div class="span-7 last">

<h4>Fan Speeds</h4>
<table>
	<tr><td><label>Fan 1:</label> </td>
	<td>{{fans[0]}}</td></tr>
	<tr><td><label>Fan 2:</label> </td>
	<td>{{fans[1]}}</td></tr>
	<tr><td><label>Fan 3:</label> </td>
	<td>{{fans[2]}}</td></tr>
</table>

<h4>Actions</h4>
<ul>
	<li><a href="/listbof/{{roach["id"]}}">Reprogram FPGA</a></li>
	<li><a href="/listreg/{{roach["id"]}}">List registers</a></li>
	<li><a href="/poweron/{{roach["id"]}}">Power ON</a></li>
	<li><a href="/poweroff/{{roach["id"]}}">Power OFF</a></li>
	<li><a href="/status/{{roach["id"]}}">Refresh</a></li>
</ul>
</li>
</div>

<hr class="space">

<a href="/">&laquo; Return to overview</a>

%include footer
