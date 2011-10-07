%#plot_snap.tpl: CASPER GUI template for plotting (via matplotlib) data from snap (32 bit) blocks.

%include header title='Snap Data: %s'%snap_id

<!-- {{avg}} -->

<div class="fmt_sel">
<a href="/snap/{{snap_id}}/bytes/{{bytes}}/fmt/int8">int8</a>
<a href="/snap/{{snap_id}}/bytes/{{bytes}}/fmt/int16">int16</a>
<a href="/snap/{{snap_id}}/bytes/{{bytes}}/fmt/int32">int32</a>
<a href="/snap/{{snap_id}}/bytes/{{bytes}}/fmt/uint8">uint8</a>
<a href="/snap/{{snap_id}}/bytes/{{bytes}}/fmt/uint16">uint16</a>
<a href="/snap/{{snap_id}}/bytes/{{bytes}}/fmt/uint32">uint32</a>
</div>

<div class="byte_sel">
<a href="/snap/{{snap_id}}/bytes/256/fmt/{{fmt}}">256</a>
<a href="/snap/{{snap_id}}/bytes/512/fmt/{{fmt}}">512</a>
<a href="/snap/{{snap_id}}/bytes/1024/fmt/{{fmt}}">1024</a>
<a href="/snap/{{snap_id}}/bytes/2048/fmt/{{fmt}}">2048</a>
<a href="/snap/{{snap_id}}/bytes/4096/fmt/{{fmt}}">4096</a>
</div>


<div class="plot_snap">

<img src="/files/temp.png" />
</div>
<p>

<!--<form name="writereg" action="snap" method="POST">
<fieldset>
    Replot as
    <select name="numbytes">        
        <option value="256">256</option>
        <option value="512">512</option>
        <option value="1024">1024</option>
        <option value="2048">2048</option>
        <option value="4096" selected="selected">4096</option>
        <option value="8192">8192</option>
        <option value="16384">16384</option>
    </select>
    
    bytes of 

    <select name="bits">
        <option value="8" selected="selected">8 bits</option>
        <option value="16">16 bits</option>
        <option value="32">32 bits</option>
    </select>
    
    <select name="format">
        <option value="uint">unsigned</option>
        <option value="int" selected="selected">signed</option>
    </select>
    
    data &nbsp;&nbsp;

<input type="submit" value="Go &raquo;" name="submit" />


</fieldset>
</form> -->

<hr class="space" />
 
<a href="/listreg">&laquo; Return to register listing</a>

%include footer
