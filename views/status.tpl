%#status.tpl: CASPER GUI Template for status page
%include header title='%s: report'%roach["hostname"]

% # Setting up variables

%if(flashmsgs != 0 and flashmsgs != []):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

% from lib.ping import ping
% status = ping(roach["IP_address"])

<hr class="space" />

<div class="span-8 colborder">

<h3>Status report: <em>{{roach["hostname"]}}</em></h3>

<table>
<tbody>
    <tr><td>IP Address</td> <td>{{roach["IP_address"]}}</td></tr>
    <tr><td>XPORT Address</td> <td>{{roach["XPORT_address"]}}</td></tr>
    <tr><td>MAC Address</td> <td>{{roach["MAC_address"]}}</td></tr>
    <tr><td>Type</td>		<td>{{roach["type"]}}</td></tr>
    <tr><td>Serial</td> 	<td>{{roach["serial"]}}</td></tr>
    <tr><td>Firmware</td> 	<td>{{roach["firmware"]}}</td></tr>
    <tr><td>Location</td>  	<td>{{roach["location"]}}</td></tr>
    <tr><td>ZDOK0</td>  	<td>{{roach["ZDOK0"]}}</td></tr>
    <tr><td>ZDOK1</td>  	<td>{{roach["ZDOK1"]}}</td></tr>
</tbody>
</table>

<p><label>Notes:</label> {{roach["notes"]}}</p>


<h4>Xport information</h4>
%if(xinfo != 0):
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
%else:
<p><em>Xport is not connected.</em></p>
%end




<div class="back"><a href="/">&laquo; Return to overview</a></div>
   
</div>

<div class="span-9 colborder">
<h4>Operating temperature / voltages</h4>
%if(xinfo != 0):
%  chans = xinfo["channels"]
<table>
  %  for chan in chans:
  %    width = int( (float(chan[1])-float(chan[2])) / (float(chan[3])-float(chan[2])) * 100)
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
%else:
<p><em>Not available</em></p>
%end

<h4>Fan Speeds</h4>
%if(xinfo != 0):
% fans  = xinfo["fanspeeds"]
<table>
	<tr><td><label>Fan 1:</label> </td>
	<td>{{fans[0]}}</td></tr>
	<tr><td><label>Fan 2:</label> </td>
	<td>{{fans[1]}}</td></tr>
	<tr><td><label>Fan 3:</label> </td>
	<td>{{fans[2]}}</td></tr>
</table>
%else:
<p><em>Not available</em></p>
%end

</div>

<div class="span-5 last">

<h4>Actions</h4>
<ul class="ss_list">
	<li><span class="ss_sprite ss_disk_multiple"> &nbsp; </span>
	    %if(status):
	    <a href="/listbof/{{roach["id"]}}">Reprogram FPGA</a>
	    %else:
	    Reprogram FPGA
	    %end
	</li>
	<li>
	  <span class="ss_sprite ss_zoom"> &nbsp; </span>
	  %if(status):
	  <a href="/listreg/{{roach["id"]}}">List registers</a>
	  %else:
	  List registers
	  %end
	</li>
	%if(xinfo !=0):
	<li>
	  <span class="ss_sprite ss_control_play_blue"> &nbsp; </span>
	  %if(xinfo["powerstate"] == "Power state: 4 (Powered off)"):
	  <a href="/poweron/{{roach["id"]}}">Power ON</a>
	  %else:
	  <em>Power ON</em>
	  %end
	</li>
	<li>
	  <span class="ss_sprite ss_control_stop_blue"> &nbsp; </span>
	  %if(xinfo["powerstate"] == "Power state: 3 (Powered on)"):
	  <a href="/poweroff/{{roach["id"]}}">Power OFF</a>
	  %else:
	  <em>Power OFF</em>
	  %end	  
	</li>
  %end
</ul>

<h4>Manage entry</h4>

<script type="text/javascript">
  //quick anti-fumble delete test
$(function () {
  $("#delete").click(function () {
    var c = confirm("Are you sure you want to delete {{roach['hostname']}}");
    if(c==true) {
      window.location = "/delete/{{roach['id']}}"
    } else {
      return 0
    }
  });
});      
</script>
<ul class="ss_list">
  <li>
    <span class="ss_sprite ss_table_edit"> &nbsp; </span>  
    <a href="/edit/{{roach["id"]}}" title="Edit entry">Edit info</a>
  </li>
  <li>
    <span class="ss_sprite ss_table_delete"> &nbsp; </span> 
    <a id="delete" href="#">Delete</a>
  </li>
</ul>

<h4>Navigation</h4>
<ul class="ss_list">
	<li>
	  <span class="ss_sprite ss_arrow_refresh"> &nbsp; </span>
	  <a href="/status/{{roach["id"]}}">Refresh</a>
	</li>
	<li>
	  <span class="ss_sprite ss_arrow_left"> &nbsp; </span>
	  <a href="/">Return to overview</a>
	</li>
</ul>


</div>



<hr class="space" />



<hr class="space" />

%include footer
