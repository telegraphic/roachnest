%#status.tpl: CASPER GUI Template for status page

%include header title='Flash Message'

%if(flashmsgs != 0 and flashmsgs != []):
<div class="success">
%for msg in flashmsgs:
{{msg}}<br />
%end
</div>
%end

 
<a href="/">&laquo; Return to overview</a>

%include footer
