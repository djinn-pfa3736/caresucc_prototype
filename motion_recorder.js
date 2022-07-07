class MotionRecorder {
  constructor(recTimes, labelObj, videoObj, canvasObj, recStart, recStop, display) {

    this.recordTimes = recTimes;

    this.label_input = labelObj;

    this.recOn = false;

    this.video = videoObj;
    this.canvas = canvasObj;

    this.ctx = this.canvas.getContext('2d');

    this.w = this.video.offsetWidth;
    this.h = this.video.offsetHeight;

    this.canvas.setAttribute('width', this.w);
    this.canvas.setAttribute('height', this.h);

    this.frames = {};
    this.frameCount = 0;

    this.start = recStart;
    this.stop = recStop;

    this.display = display;

    this.start.addEventListener('click', (e) => {
      // this.video.play();
      this.recOn = true;
      this.label = this.label_input.value;
      this.display.style.color="red";
      this.display.innerHTML = "RECORDING!!";
    });

    this.stop.addEventListener('click', (e) => {
      // this.video.pause();
      this.recOn = false;
      this.display.style.color="black";
      this.display.innerHTML = "FINISHED. NOW MOVING TO NEXT PAGE.";
      // console.log(this.frames);
      this.postProcess();
    });

  }

  pushFrame(frame) {
    if(this.recOn) {
      this.ctx.drawImage(this.video, 0, 0, this.w, this.h);
      var dataURL = this.canvas.toDataURL('image/webp');

      // console.log(dataURL);
      this.frames[this.frameCount] = dataURL;
      this.frameCount += 1;

      // var img = document.getElementById("image");
      // img.src = this.frames[0];
    }
  }

  clearBuffer() {
    this.frames = {};
  }

  postProcess() {
    var submit = {label: this.label, data: this.frames};
    var submit_json = JSON.stringify(submit);
    /*
    var xhr = new XMLHttpRequest();
    xhr.onload = function (e) {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          console.log(xhr.responseText);
        }
      }
    }
    xhr.open('POST', 'https://192.168.1.111/restore_movie.php', true);
    xhr.setRequestHeader('content-type', 'application/json');
    xhr.send(resString);
    */
    $.ajax({
      method: "POST",
      url: "https://192.168.1.111/restore_movie.php",
      data: submit_json,
      contentType: "application/json"
    }).done(function (data, textStatus, jqXHR) {
      console.log(data);
      console.log(this.recordTimes.value);

      if(this.recordTimes.value == 'first') {
        window.location.href = 'https://192.168.1.111/record_second.php';
      } else if (this.recordTimes.value == 'second'){
        window.location.href = 'https://192.168.1.111/summary.php';
      } else {
        window.location.href = 'https://192.168.1.111/deadend.php?message=' + this.times;
      }
    });
    this.clearBuffer();

  }
}
