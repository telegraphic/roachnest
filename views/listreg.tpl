%#status.tpl: CASPER GUI Template for status page

%include header title='Shared Registers'

%# Set up variables nicely
%snaplist   = data["snaplist"]
%snap64list = data["snap64list"]
%syslist    = data["syslist"]
%reglist    = data["reglist"]
%vals       = data["vals"]
%flashmsg   = data["flashmsg"]

%if(flashmsg != 0 and flashmsg != ""):
<div class="success">{{flashmsg}}</div>
%end


<span class="span-7 colborder">
<h3>Control registers</h3>

<table><tbody>
%for i in range(0,len(reglist)):
%regname, regval = reglist[i], vals[i]
<tr><td>{{regname}}</td><td>{{regval}}</td></tr>
%end
</table></tbody>


</span>

<span class="span-8 colborder">
<h3>Snap registers</h3>
%for register in snaplist:
  <h4><a href="snap/{{register}}/bytes/4096/fmt/int8">{{register}}</a></h4> 
%end

%if len(snap64list) > 0:
<h3>Snap 64 registers</h3>
%for register in snap64list:
  <h4><a href="snap64/{{register}}/bytes/4096">{{register}}</a></h4> 
%end
%end

<hr class="space">
<h3>System registers</h3>
%for register in syslist:
  <h4>{{register}}</h4> 
%end


</span>

<span class="span-7 last">
<h3>Write Register</h3>
<form name="writereg" action="listreg" method="GET">
<table><tbody>
    <tr>
        <td>Register:</td>
        <td><select name="regname" class="spectrometer_reg">
            %for register in reglist:
                <option value="{{register}}">{{register}}</option>
            %end
        </td> 
    </tr>
    <tr>
        <td>Value: </td>
        <td><input type="text" class="spectrometer_reg" name="regval" /></td>
    </tr>
        
</table>

<div>
        Dec <input type="radio" name="regtype" checked="checked" value="10" />
        Bin <input type="radio" name="regtype" value="2" />
        Hex <input type="radio" name="regtype" value="16" />
        Eval <input type="radio" name="regtype" value="eval" />
</div>           
<input type="submit" value="Write &raquo;" name="submit" />
</form>

<hr class="space">

<h3> Reset / resync</h3>
<form name="writereg" action="listreg" method="GET">
<input type="submit" value="Reset &raquo;" name="reset" />
</form>

<hr class="space">

<h3> <a href="/listreg"> Refresh </a></h3>

<hr class="space">

</span>


<hr class="space" />
 
<a href="/">&laquo; Return to overview</a>

%include footer
