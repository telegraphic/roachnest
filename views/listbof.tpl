%#status.tpl: CASPER GUI Template for status page

%include header title='Listing bit files on %s'%roach

%if(flashmsg != 0):
<div class="{{flashmsg[1]}}">{{flashmsg[0]}}</div>
%end

<table>
<thead>
<tr>
	<th>Filename</th>
	<th>Actions</th>
</tr>
</thead>

<tbody>
%for bof in boflist:
<tr>
  <td>{{bof}}</td>
  <td><a href="/progdev/{{bof}}" title="Program FPGA"><span class="ss_sprite ss_cog_go "> &nbsp; </span></a></td>
</tr> 
%end
</tbody>
</table>


<hr class="space" />
 
<a href="/">&laquo; Return to overview</a>

%include footer
