%#status.tpl: CASPER GUI - Spectrometer quick look (for D-PAD transient)

%include header title='Spectrometer: quick look'

<span class="span-6 colborder">
<h3>Control registers</h3>
<form name="register_vals" action="spectrometer" method="GET">
<table>
<thead>
<tr>
    <th>Register</th>
    <th>Value</th>
</tr>
</thead>
<tbody>

<tr>
    <td>
    <a class="tip" href="readint/gain">gain
        <span>
            <strong>gain:</strong> a 32 bit number used in quantising down from 36 bit to 8 before accumulation.<br />
            <em><strong>usage:</strong> hexadecimal, maximum value is FFFFFFFF, minimum is 00000000</em>
            </em>
        </span>
    </a>
    </td>
    <td>
    <input type="hidden" name="gain_old" value="{{reg["gain"]}}" />
    <input type="text" class="spectrometer_reg" name="gain_new" value="{{reg["gain"]}}" />
    </td>
</tr>

<tr>
    <td>
    <a class="tip" href="readint/fft_shift">fft_shift
        <span>
            <strong>fft_shift:</strong> a 9 bit number used to select which of the 9 stages of the 2^9 FFT 
            to shift data to prevent overflows.<br /> 
            <em><strong>usage:</strong>binary, a value of 1 shifts at the first stage, 10 at the second stage,
            111 at the first three stages etc.</em>
        </span>
    </a>
    </td>
    <td>
    <input type="hidden" name="fft_shift_old" value="{{reg["fft_shift"]}}" />
    <input type="text" class="spectrometer_reg" name="fft_shift_new" value="{{reg["fft_shift"]}}" />
    </td>
</tr>
 	
<tr>
    <td>
    <a class="tip" href="readint/acc_len">acc_len
        <span>
            <strong>acc_len:</strong> a 10 bit number used to control how many accumulations are done.<br /> 
            <em><strong>usage:</strong>decimal, up to 1023. 1ms is about 976 (250MHz * 1ms / 256 chans) </em>
        </span>
    </a>
    </td>
    <td>
    <input type="hidden" name="acc_len_old" value="{{reg["acc_len"]}}" />
    <input type="text" class="spectrometer_reg" name="acc_len_new" value="{{reg["acc_len"]}}" />
    </td>
</tr>


</tbody>
</table>
<input type="submit" value="Update registers &raquo;" name="update" />
</form>
<hr class="space" />

<h3>Register values</h3> 
<table>
<thead>
<tr>
    <th>Register</th>
    <th>Value</th>
</tr>
</thead>
<tbody>
<tr>
    <td>
    <a class="tip" href="readint/acc_cnt">acc_cnt
        <span>
            <strong>acc_cnt:</strong> a counter incremented after every accumulated spectrum is outputted.
        </span>
    </a>
    </td>
    <td>
    {{reg["acc_cnt"]}}
    </td>
</tr>

<tr>
    <td>
    <a class="tip" href="readint/fft_of">fft_of
        <span>
            <strong>fft_of:</strong> is the FFT overflowing? If this equals 1, that is bad, and you should
            increase the fft_shift, or lower the input power to the ADC.
        </span>
    </a>
    </td>
    <td>
    {{reg["fft_of"]}}
    </td>
</tr>


</tbody>
</table>

<form name="resync" action="spectrometer" method="GET">
<input type="submit" value="Reset &raquo;" name="reset" />
</form>


</span>

<span class="span-16 last">
<div class="plot_snap">
<img src="/files/temp.png" />
</div>
<h3>Notes</h3>
%for msg in flashmsgs:
<div class="success">{{msg}}</div>
%end
<div class="success">{{bytes}} bytes read from {{snap_id}} as {{fmt}} data.</div>
%if(reg["fft_of"] == 1):
<div class="error">Warning: the FFT is overflowing!</div>
%end


</span>


<hr class="space" />



%include footer

