%#hardware_add.tpl: CASPER GUI: edit hardware
%include header title='Edit Hardware'

%if(flashmsgs != 0 and flashmsgs != []):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

<form action="/add" method="GET">
<fieldset>
	<legend>Add Hardware</legend>
<table>
<tr>
	<td><label for="hostname">Hostname</label></td>
	<td><input type="text" size="100" maxlength="100" name="hostname" value="{{roach["hostname"]}}" /></td>
	</tr>
<tr>
	<td><label for="MAC_address">MAC Address</label></td>
	<td><input type="text" size="100" maxlength="100" name="MAC_address" value="{{roach["MAC_address"]}}" /></td>
</tr>
<tr>
	<td><label for="IP_address">IP Address</label></td>
	<td><input type="text" size="100" maxlength="100" name="IP_address" value="{{roach["IP_address"]}}" /></td>
</tr>
<tr>
	<td><label for="location">Location</label></td>
	<td><input type="text" size="100" maxlength="100" name="location" value="{{roach["location"]}}" /></td>
</tr>
<tr>
	<td><label for="notes">Notes</label></td>
	<td><input type="text" size="100" maxlength="100" name="notes" value="{{roach["notes"]}}" /></td>
</tr>
<tr>
	<td><label for ="serial">Serial</label></td>
	<td><input type="text" size="100" maxlength="100" name="serial" value="{{roach["serial"]}}" /></td>
</tr>
<tr>
	<td><label for="firmware">Firmware</label></td>
	<td><input type="text" size="100" maxlength="100" name="firmware" value="{{roach["firmware"]}}" /></td>
</tr>
<tr>
	<td><label for="type">Type</label></td>
	<td><select name="type">
	    <option value="">Please select:</option>
	    %if (roach["type"] == 'ROACH'):
	    <option value="ROACH" SELECTED>ROACH</option>
	    %else:
	    <option value="ROACH">ROACH</option>
	    %end
	    
	    %if (roach["type"] == 'iBOB'):
	    <option value="iBOB" SELECTED>iBOB</option>
	    %else:
	    <option value="iBOB">iBOB</option>
	    %end
	    
	    %if (roach["type"] == 'ROACH II'):
	    <option value="ROACH II" SELECTED>ROACH II</option>
	    %else:
	    <option vlaue="ROACH II">ROACH II</option>
	    %end
	    </select></td>
</tr>
<tr>
	<td><label for="XPORT_address">XPORT Address</label></td>
	<td><input type="text" size="100" maxlength="100" name="XPORT_address" value="{{roach["XPORT_address"]}}" /></td>
</tr>
<tr>
	<td><label for="ZDOK0">ZDOK 0</label></td>
	<td><input type="text" size="100" maxlength="100" name="ZDOK0" value="{{roach["ZDOK0"]}}" /></td>
</tr>
<tr>
	<td><label for="ZDOK1">ZDOK 1</label></td>
	<td><input type="text" size="100" maxlength="100" name="ZDOK1" value="{{roach["ZDOK1"]}}" /></td>
</tr>

</table>
<input type="submit" name="save" value="save" method="GET">
</fieldset>
</form>

%include footer
