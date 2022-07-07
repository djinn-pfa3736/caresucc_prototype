$(function() {

  var canvas = document.getElementById('canvas');
  const recordTimes = document.getElementById('first_times');
  var label = document.getElementById('first_label');

  const video = document.getElementById('first_video');

  const recStart = document.getElementById('first_start');
  const recStop = document.getElementById('first_stop');

  var display = document.getElementById('first_state');
  navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false,
  }).then(stream => {
      video.srcObject = stream;
      video.play();
  }).catch(e => {
    console.log(e);
  });

  // firstRecorder = new MotionRecorder(recordTimes, label, video, canvas, recStart, recStop, display);
  firstRecorder = new MotionRecorder(recordTimes, label, video, canvas, recStart, recStop, display);

  setInterval("firstRecorder.pushFrame()", 1000/60);

});
