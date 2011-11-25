% import lib.config as config
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>{{config.title}} | {{title}}</title>

  <link rel="shortcut icon" type="image/x-icon" href="{{config.favicon}}">
  
	<!-- CASPER GUI CSS -->
	<link rel="stylesheet" href="/files/styles.css" type="text/css" media="screen, projection">
	<link rel="stylesheet" href="{{config.branding_css}}" type="text/css" media="screen, projection">

    <!-- Framework CSS -->
    <link rel="stylesheet" href="/files/blueprint/screen.css" type="text/css" media="screen, projection">
    <link rel="stylesheet" href="/files/blueprint/print.css" type="text/css" media="print">
    <link rel="stylesheet" href="/files/blueprint/sprite.css" type="text/css" media="screen, projection">

	<!-- old IE fixing stylesheet -->
    <!--[if lt IE 8]><link rel="stylesheet" href="blueprint/ie.css" type="text/css" media="screen, projection"><![endif]-->

    <!-- Import fancy-type plugin for the sample page. -->
    <link rel="stylesheet" href="/files/blueprint/plugins/fancy-type/screen.css" type="text/css" media="screen, projection">
  </head>
  <body>

      <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="/files/flot/excanvas.min.js"></script><![endif]-->
      <script language="javascript" type="text/javascript" src="/files/flot/jquery.js"></script>
      <script language="javascript" type="text/javascript" src="/files/flot/jquery.flot.js"></script>
      <script language="javascript" type="text/javascript" src="/files/flot/jquery.flot.navigate.js"></script>
      <script language="javascript" type="text/javascript" src="/files/flot/jquery.flot.crosshair.js"></script>
  
  <hr class="space" />
    <div class="container">
    <div id="header">
    <span class="span-3">
      <a href="/">
        <img src="{{config.branding_logo}}" />
      </a>
    </span>
    <span class="span-18 headtext last">
      <h1>{{config.title}}</a></h1>
    </span>
    </div>
    <hr />


