%#plot_snap.tpl: CASPER GUI template for plotting (via matplotlib) data from snap (32 bit) blocks.

%include header title='Snap Data: %s'%snap_id

<style type="text/css">
#placeholder {
  width: 800px;
  height: 600px;
  clear: all;
  padding: 10px;
  margin: 0 auto;
}
  
.tickLabel {
    font-size: large;
}

</style>


<div class="span-7 colborder">
  <h4>Data Format</h4>
  <table>
    <tbody>
      <tr>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/int8/op/{{op}}">int8</a></td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/int16/op/{{op}}">int16</a></td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/int32/op/{{op}}">int32</a></td>
      </tr>
      <tr>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/uint8/op/{{op}}">uint8</a>   </td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/uint16/op/{{op}}">uint16</a> </td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/uint32/op/{{op}}">uint32</a> </td>
      </tr>
      <tr>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/comp8/op/{{op}}">comp 8_8</a>   </td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/comp16/op/{{op}}">comp 16_16</a></td>
      </tr>
    </tbody>
  </table>
  </div>
<div class="span-8 colborder">
  <h4>Data Operations</h4>
  <table>
    <tbody>
      <tr>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/raw">raw data</a></td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/real">real part</a></td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/imag">imag part</a></td>
      </tr>
      <tr>     
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/decibels">decibels<br> </a>(10*log10)</td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/bits">number bits<br> </a>(log2(abs+1))</td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/raw">linear<br></a> (raw data)</td>
      </tr>
      <tr>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/powfftdb">FFT power</a><br> (decibels) </td>
        <td><a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/powfftlin">FFT power</a><br> (linear) </td>
      </tr>
    </tbody>
   </table>
</div>

  <div class="span-7 last">
  <h4>Bytes</h4>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/256/fmt/{{fmt}}/op/{{op}}">256</a>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/512/fmt/{{fmt}}/op/{{op}}">512</a>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/1024/fmt/{{fmt}}/op/{{op}}">1024</a>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/2048/fmt/{{fmt}}/op/{{op}}">2048</a>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/4096/fmt/{{fmt}}/op/{{op}}">4096</a>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/8192/fmt/{{fmt}}/op/{{op}}">8192</a>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/16384/fmt/{{fmt}}/op/{{op}}">16384</a>
<a href="/snap/{{roach["id"]}}/{{snap_id}}/bytes/32768/fmt/{{fmt}}/op/{{op}}">32768</a>
</div>

<hr class="space" />

<script type="text/javascript">
// This function plots the data
$(function () {
    var d1 = {{[[datum[0],datum[1]] for datum in data]}}; 
    data = [{ data: d1, color: "#003776"}]
    $.plot($("#placeholder"), data);
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

<p><a href="/listreg/{{roach["id"]}}">&laquo; Return to register listing</a></p>
<hr class="space" />
%include footer
