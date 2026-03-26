const canvas = document.getElementById("screenCanvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    const displayWidth = screenWidth;
    const displayHeight = screenHeight;

    canvas.style.width = displayWidth + 'px';
    canvas.style.height = displayHeight + 'px';

    const dpr = window.devicePixelRation || 1;

    canvas.wdith = displayWidth * dpr;
    canvas.height = displayHeight * dpr;
}

function toPixels(normX, normY) {
    return {
        x: normX * canvas.width,
        y: normY * canvas.height
    };
}

let input = {
    active: false,
    startTime: 0,
    x: 0,
    y: 0
};

canvas.addEventListener("pointerdown", (e) => {
    const rect = canvas.getBoundingClientRect();

    input.active = true;
    input.startTime = performance.now();
    input.x = e.clientX - rect.left;
    input.y = e.clientY - rect.top;
    console.log(input.x, input.y)
});

canvas.addEventListener("pointerup", () => {
    input.active = false;
})

let slash = {
  startTime: performance.now(),
  duration: 1000, // ms
  x: 200,
  y: 200,
  radius: 30
};

function getProgress() {
  return (performance.now() - slash.startTime) / slash.duration;
}

function drawSlash(progress) {
  const length = 200;
  const filled = length * Math.min(progress, 1);

  ctx.save();
  ctx.translate(slash.x, slash.y);
  ctx.rotate(Math.PI / 4); // diagonal

  // background
  ctx.fillStyle = "#333";
  ctx.fillRect(-length / 2, -5, length, 10);

  // fill
  ctx.fillStyle = "red";
  ctx.fillRect(-length / 2, -5, filled, 10);

  ctx.restore();

  // target circle
  ctx.beginPath();
  ctx.arc(slash.x, slash.y, slash.radius, 0, Math.PI * 2);
  ctx.strokeStyle = "white";
  ctx.stroke();
}

function checkHit(progress) {
  if (!input.active) return;

  // distance check
  const dx = input.x - slash.x;
  const dy = input.y - slash.y;
  const dist = Math.sqrt(dx * dx + dy * dy);

  const inRange = dist <= slash.radius;

  // timing window (example: must hit before bar fills)
  const timingGood = progress < 1;

  if (inRange && timingGood) {
    console.log("SUCCESS");

    // reset slash
    slash.startTime = performance.now();
  }
}

function loop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const progress = getProgress();

  drawSlash(progress);
  checkHit(progress);

  requestAnimationFrame(loop);
}

requestAnimationFrame(loop);



function drawScreen() {
    const bgColor = "black";

    canvas.style.backgroundColor = bgColor;
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
drawScreen();