%#status.tpl: CASPER GUI Template for status page

%include header title='%s: report'%hardware["hostname"]

%if(flashmsgs != 0):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

<div class="span-7 colborder">
<table>
<thead>
	<tr><th>{{hardware["hostname"]}}</th> <th>aka <em>"{{hardware["nickname"]}}"</em></th></tr>
</thead>
<tbody>
    <tr><td>IP Address</td> <td>{{hardware["IP_address"]}}</td></tr>
    <tr><td>MAC Address</td> <td>{{hardware["MAC_address"]}}</td></tr>
    <tr><td>Type</td>		<td>{{hardware["type"]}}</td></tr>
    <tr><td>Serial</td> 		<td>{{hardware["serial"]}}</td></tr>
    <tr><td>Firmware</td> 	<td>{{hardware["firmware"]}}</td></tr>
    <tr><td>Location</td>  	<td>{{hardware["location"]}}</td></tr>
</tbody>
</table>
  <a href="/edit/{{hardware["id"]}}" title="Edit entry"><span class="ss_sprite ss_table_edit"> &nbsp; </span> Edit info </a> 
</div>

<div class="span-8 colborder">
<h4>Operating temperature / voltages</h4>
<table>
  %for chan in chans:
  %  width = int(float(chan[1]) / (float(chan[3])) * 100)
	<tr>
		<td><label>{{chan[0]}}</label></td>
		<td>{{str("%.1f")%chan[2]}}</td> 
		<td><div class="progress-container">
		    <div class="progress-text">{{str("%2.2f")%chan[1]}}</div>
		    <div style="width: {{width}}%"></div></div>
		</td>
		<td>{{str("%.1f")%chan[3]}}</td>
	</tr>
	%end
</table>
</div>

<div class="span-7 last">
<h4>KATCP</h4>
<label for="dummy6">?</label>
<input name="dummy6" id="dummy6" value="Enter command" type="text">


<h4>Actions</h4>
<ul>
	<li><a href="/{{hardware["nickname"]}}/listbof">Reprogram FPGA</a></li>
	<li><a href="/{{hardware["nickname"]}}/listreg">List registers</a></li>
	<li><a href="/{{hardware["nickname"]}}/spectrometer">Spectrometer GUI</a></li>
</ul>
</li>
</div>

<hr class="space">

<a href="/">&laquo; Return to overview</a>

%include footer
