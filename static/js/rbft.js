$(function() {
  var videoInput = document.getElementById('video');

  var ctracker = new clm.tracker();
  ctracker.init(pModel);
  ctracker.start(videoInput);

  function positionLoop() {
    requestAnimationFrame(positionLoop);
    var positions = ctracker.getCurrentPosition();
    // positions = [[x_0, y_0], [x_1,y_1], ... ]
    // do something with the positions ...
  }
  positionLoop();

  var canvasInput = document.getElementById('drawCanvas');
  var cc = canvasInput.getContext('2d');
  function drawLoop() {
    requestAnimationFrame(drawLoop);
    cc.clearRect(0, 0, canvasInput.width, canvasInput.height);
    ctracker.draw(canvasInput);
  }
  drawLoop();
});
