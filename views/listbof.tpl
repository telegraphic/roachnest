%#status.tpl: CASPER GUI Template for status page

%include header title='Listing bit files on %s'%roach["hostname"]

%if(flashmsg != 0):
<div class="{{flashmsg[1]}}">{{flashmsg[0]}}</div>
%end


<div class="back" ><a href="/status/{{roach['id']}}">&laquo; Return to {{roach['nickname']}} overview</a> </div>
<div class="forward"> <a href="/listreg/{{roach['id']}}"> List registers &raquo;</a></div>

<hr class="space" />

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
  <td><a href="/progdev/{{roach["id"]}}/{{bof}}" title="Program FPGA"><span class="ss_sprite ss_cog_go "> &nbsp; </span></a></td>
</tr> 
%end
</tbody>
</table>


<hr class="space" />
 
<div class="back" ><a href="/status/{{roach['id']}}">&laquo; Return to {{roach['nickname']}} overview</a> </div>
<div class="forward"> <a href="/listreg/{{roach['id']}}"> List registers &raquo;</a></div>

%include footer
