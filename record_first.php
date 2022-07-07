<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <script
  src="https://code.jquery.com/jquery-3.6.0.js"
  integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk="
  crossorigin="anonymous"></script>
  <!-- <script src="controller.js"></script> -->
  <!-- <script src="main.js"></script> -->
  <script src="record_first.js"></script>
  <script src="motion_recorder.js"></script>
</head>

<body>

<canvas id="canvas" style="display: none;"> </canvas> <br />
<input type="text" id="first_times" value="first" style="display: none;">

<h1> RECORD FIRST MOVIE </h1>
FIRST MOVIE OUTPUT:
<input type="text" id="first_label"> <br /> <br />
<?php
  echo '<video id="first_video" width="640" height="480"></video> <br />';
  echo '<div id="first_state" style="color: black;"> NOT RECORDED... </div>';
?>
<input type="submit" id="first_start" value="FIRST RECORD START">
<input type="submit" id="first_stop" value="FIRST RECORD STOP">

</body>
</html>
