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
  <script src="record_second.js"></script>
  <script src="motion_recorder.js"></script>
</head>

<body>

<canvas id="canvas" style="display: none"> </canvas> <br />
<input type="text" id="second_times" value="second" style="display: none;">

<h1> RECORD SECOND MOVIE </h1>
SECOND MOVIE OUTPUT:
<input type="text" id="second_label"> <br /> <br />
<?php
  echo '<video id="second_video" width="640" height="480"></video> <br />';
  echo '<div id="second_state" style="color: black;"> NOT RECORDED... </div>';
?>
<input type="submit" id="second_start" value="SECOND RECORD START">
<input type="submit" id="second_stop" value="SECOND RECORD STOP">

</body>
</html>
