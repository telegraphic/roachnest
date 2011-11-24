%#status.tpl: CASPER GUI Template for status page

%include header title='Hardware Overview'

%if(flashmsgs != 0 and flashmsgs != []):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

<p>This page lists the status of CASPER hardware that is registered in CASPER GUI's database:</p>
<table>
<thead>
<tr>
	<th>ID</th>
	<th>hostname</th>
	<th>nickname</th>
	<th>MAC Address</th>
	<th>IP Address</th>
	<th>XPORT Address</th>
	<th>PPC Ping</th>
	<th>Xport Ping</th>
</tr>
</thead>
<tbody>
%for row in rows:
  <tr>
  	<td>{{row["id"]}}</td>
	<td><a href="/status/{{row["id"]}}">{{row["hostname"]}}</a></td>
	<td>{{row["nickname"]}}</td>
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


  </tr>
%end
</tbody>
</table>

<form name="power" action="/" method="GET">
<input type="submit" value="Power all ON" name="power" />
<input type="submit" value="Power all OFF" name="power" />
</form>

%include footer
