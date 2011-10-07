%#hardware_add.tpl: CASPER GUI: add new hardware
%include header title='Add New Hardware'

<form action="/add" method="GET">
<fieldset>
	<legend>Add Hardware</legend>
<table>
<tr>
	<td><label for="hostname">Hostname</label></td>
	<td><input type="text" size="100" maxlength="100" name="hostname" /></td>
	</tr>
<tr>
	<td><label for="nickname">Nickname</label></td>
	<td><input type="text" size="100" maxlength="100" name="nickname" /></td>
</tr>
<tr>
	<td><label for="MAC_address">MAC Address</label></td>
	<td><input type="text" size="100" maxlength="100" name="MAC_address" /></td>
</tr>
<tr>
	<td><label for="IP_address">IP Address</label></td>
	<td><input type="text" size="100" maxlength="100" name="IP_address" /></td>
</tr>
<tr>
	<td><label for="location">Location</label></td>
	<td><input type="text" size="100" maxlength="100" name="location" /></td>
</tr>
<tr>
	<td><label for="notes">Notes</label></td>
	<td><input type="text" size="100" maxlength="100" name="notes" /></td>
</tr>
<tr>
	<td><label for ="serial">Serial</label></td>
	<td><input type="text" size="100" maxlength="100" name="serial" /></td>
</tr>
<tr>
	<td><label for="firmware">Firmware</label></td>
	<td><input type="text" size="100" maxlength="100" name="firmware" /></td>
</tr>
<tr>
	<td><label for="type">Type</label></td>
	<td><select name="type">
	    <option value="ROACH">ROACH</option>
	    <option value="iBOB">iBOB</option>
	    <option vlaue="ROACH II">ROACH II</option>
	    </select>
	</td>
</tr>
</table>
<input type="submit" name="save" value="save" method="GET">
</fieldset>
</form>

%include footer
