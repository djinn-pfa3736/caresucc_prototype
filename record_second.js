$(function() {

  var canvas = document.getElementById('canvas');
  const recordTimes = document.getElementById('second_times');
  var label = document.getElementById('second_label');

  const video = document.getElementById('second_video');

  const recStart = document.getElementById('second_start');
  const recStop = document.getElementById('second_stop');

  var display = document.getElementById('second_state');
  navigator.mediaDevices.getUserMedia({
      video: true,
      audio: false,
  }).then(stream => {
      video.srcObject = stream;
      video.play();
  }).catch(e => {
    console.log(e);
  });

  // secondRecorder = new MotionRecorder(recordTimes, label, video, canvas, recStart, recStop);
  secondRecorder = new MotionRecorder(recordTimes, label, video, canvas, recStart, recStop, display);

  setInterval("secondRecorder.pushFrame()", 1000/60);
}
