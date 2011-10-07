%#plot_snap.tpl: CASPER GUI template for plotting (via matplotlib) data from snap (32 bit) blocks.

%include header title='Snap Data: %s'%snap_id

<style type="text/css">
#placeholder .button {
    position: absolute;
    cursor: pointer;
}
#placeholder div.button {
    font-size: smaller;
    color: #999;
    background-color: #eee;
    padding: 2px;
}
.message {
    padding-left: 50px;
    font-size: smaller;
}
</style>

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

<script type="text/javascript">
$(function () {
    var d1 = {{data}};
   
    
    $.plot($("#placeholder"), [ d1 ]);
});
</script>


<div id="placeholder"></div>
<p id="hoverdata"></p>

<script type="text/javascript">
$.get("/is_ajax", function(data){
//alert("Data Loaded: " + data);
});
</script>

<hr class="space" />
 
<a href="/listreg">&laquo; Return to register listing</a>

%include footer
