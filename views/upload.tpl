%#status.tpl: CASPER GUI Template for status page

%include header title='D-PAD control centre'


<form action="/upload/do" method="POST" enctype="multipart/form-data">
  <input type="text" name="name" />
  <input type="file" name="data" />
  <input type="submit" name="submit" value="upload">
</form>


<hr class="space">

%include footer
