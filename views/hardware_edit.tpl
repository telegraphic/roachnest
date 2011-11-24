%#hardware_add.tpl: CASPER GUI: add new hardware
%include header title='Add New Hardware'

<form action="/edit/{{hardware["id"]}}" method="GET">
<fieldset>
	<legend>Add Hardware</legend>
<table>
<tr>
	<td><label for="hostname">Hostname</label></td>
	<td><input type="text" size="100" maxlength="100" name="hostname" value="{{hardware["hostname"]}}" /></td>
	</tr>
<tr>
	<td><label for="nickname">Nickname</label></td>
	<td><input type="text" size="100" maxlength="100" name="nickname" value="{{hardware["nickname"]}}" /></td>
</tr>
<tr>
	<td><label for="MAC_address">MAC Address</label></td>
	<td><input type="text" size="100" maxlength="100" name="MAC_address" value="{{hardware["MAC_address"]}}" /></td>
</tr>
<tr>
	<td><label for="IP_address">IP Address</label></td>
	<td><input type="text" size="100" maxlength="100" name="IP_address" value="{{hardware["IP_address"]}}" /></td>
</tr>
<tr>
	<td><label for="location">Location</label></td>
	<td><input type="text" size="100" maxlength="100" name="location" value="{{hardware["location"]}}" /></td>
</tr>
<tr>
	<td><label for="notes">Notes</label></td>
	<td><input type="text" size="100" maxlength="100" name="notes" value="{{hardware["notes"]}}" /></td>
</tr>
<tr>
	<td><label for ="serial">Serial</label></td>
	<td><input type="text" size="100" maxlength="100" name="serial" value="{{hardware["serial"]}}" /></td>
</tr>
<tr>
	<td><label for="firmware">Firmware</label></td>
	<td><input type="text" size="100" maxlength="100" name="firmware" value="{{hardware["firmware"]}}" /></td>
</tr>
<tr>
	<td><label for="type">Type</label></td>
	<td><select name="type">
	    %if (hardware["type"] == 'ROACH'):
	    <option value="ROACH" SELECTED>ROACH</option>
	    %else:
	    <option value="ROACH">ROACH</option>
	    %end
	    
	    %if (hardware["type"] == 'iBOB'):
	    <option value="iBOB" SELECTED>iBOB</option>
	    %else:
	    <option value="iBOB">iBOB</option>
	    %end
	    
	    %if (hardware["type"] == 'ROACH II'):
	    <option vlaue="ROACH II" SELECTED>ROACH II</option>
	    %else:
	    <option vlaue="ROACH II">ROACH II</option>
	    %end
	    </select></td>
</tr>
</table>
<input type="submit" name="save" value="save" method="GET">
</fieldset>
</form>

%include footer
