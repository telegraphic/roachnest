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
    $.ajaxSetup({ cache: false });
    
    // get data from bottle via JSON
    // TODO: need to figure out how to allow async
    var d1 = [];

    $.ajax({
      url: "/ajax_snap/{{roach['id']}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/{{op}}",
      async: false,
      dataType: 'json',
      success: function (json) {
        d1 = json.data;
      }
    });
    
    var data = [{ data: d1, color: "#003776"}];
    
    var options = {
        legend: { show: false },
        series: {
            lines: { show: true },
            points: { show: false }
        },
        selection: { mode: "xy" }
    };

    // Plot inital values (nb: this line contains embedded python!)
    var plot = $.plot($("#placeholder"), data, options);

    // Enable zooming
    $("#placeholder").bind("plotselected", function (event, ranges) {
        // clamp the zooming to prevent eternal zoom
        if (ranges.xaxis.to - ranges.xaxis.from < 0.00001)
            ranges.xaxis.to = ranges.xaxis.from + 0.00001;
        if (ranges.yaxis.to - ranges.yaxis.from < 0.00001)
            ranges.yaxis.to = ranges.yaxis.from + 0.00001;
        
        // do the zooming
        plot = $.plot($("#placeholder"), data,
                      $.extend(true, {}, options, {
                          xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
                          yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }
                      }));
        
        // don't fire event on the overview to prevent eternal loop
        overview.setSelection(ranges, true);
    });

    // add zoom out button 
    $("input.resetPlot").click(function () {
      $.plot($("#placeholder"), data, options);
    });

    // add AJAX refresh
    $("input.refreshPlot").click(function () {
      $.ajax({
        url: "/ajax_snap/{{roach['id']}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/{{op}}",
        async: false,
        dataType: 'json',
        success: function (json) {
          d1 = json.data;
        }
      });
    
      data = [{ data: d1, color: "#003776"}];      
      $.plot($("#placeholder"), data, options);
    });
    
    
    // autorefresh functionality
    var refresher;
    $("input.autoRefresh").click(function () {
      
      // Refresh every two seconds
      if($(".autoRefresh").is(':checked')) {
        
         refresher = setInterval(function() { 
          $.ajax({
            url: "/ajax_snap/{{roach['id']}}/{{snap_id}}/bytes/{{bytes}}/fmt/{{fmt}}/op/{{op}}",
            async: false,
            dataType: 'json',
            success: function (json) {
              d1 = json.data;
            }
          });
          
          data = [{ data: d1, color: "#003776"}];      
          $.plot($("#placeholder"), data, options);           
        }, 2000);
        
      } else {
        // Stop refreshing
        clearInterval(refresher);
      }
    });

});
</script>


<div id="placeholder"></div>


<hr class="space" />

<input class="resetPlot" type="button" value="Zoom out" />
<input class="refreshPlot" type="button" value="Refresh data" />
<p><input class="autoRefresh" type="checkbox" /> <label for="autoRefresh">Enable auto refresh</label></p>

<p><a href="/listreg/{{roach["id"]}}">&laquo; Return to register listing</a></p>
<hr class="space" />
%include footer
