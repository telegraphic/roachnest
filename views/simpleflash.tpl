%#status.tpl: CASPER GUI Template for status page

%include header title='Flash Message'

%if(flashmsgs != 0):
<div class="success">{{flashmsgs}}</div>
%end

 
<a href="/">&laquo; Return to overview</a>

%include footer
