%#status.tpl: CASPER GUI Template for status page

%include header title='HIPSR Control', subtitle='Home'

%if(flashmsgs != 0):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

<span class="span-7 colborder">
<h2 class="centertext"><a href="/listbof">Reprogram FPGA</a></h2>
</span>
<span class="span-8 colborder">
<h2 class="centertext"><a href="/listreg">List registers</a></h2></span>
<span class="span-7 last">
<h2 class="centertext"><a href="/poweron">Power ON</a></h2></span>



<hr class="space">

%include footer
