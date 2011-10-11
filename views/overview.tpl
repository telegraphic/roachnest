%#status.tpl: CASPER GUI Template for status page

%include header title='Hardware Overview'



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
	<th>Status</th>
	<th>Actions</th>
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
	<td><form name="actions" action="/" method="GET">
	<select onchange="this.form.submit()" name="action">
	  <option value="#">---Actions---</option>
	  <option value="/status/{{row["id"]}}">Detailed status</option>
	  <option value="#">Wake on LAN</option>
	  <option value="#">Remote shutdown</option>
	  <option value="#">Program bitstream</option>
	  <option value="#">Connect via X-PORT</option>
	  <option value="#">Connect via serial</option>
	</select>
	</form>
	</td>
  </tr>
%end
</tbody>
</table>

%include footer
