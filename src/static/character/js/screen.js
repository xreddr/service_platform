const canvas = document.getElementById("screenCanvas");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
    const displayWidth = window.innerWidth;
    const displayHeight = window.innerHeight;

    canvas.style.width = displayWidth + 'px';
    canvas.style.height = displayHeight + 'px';

    const dpr = window.devicePixelRatio || 1;

    canvas.width = displayWidth * dpr;
    canvas.height = displayHeight * dpr;

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

let game = {
  hp: 5,
  maxHp: 5,
  score: 0
};

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

});

canvas.addEventListener("pointerup", () => {
    input.active = false;
})

let slash;

function initSlash() {
  const pos = randomBottomSpawn();

  slash = {
    startTime: performance.now(),
    duration: 3000,
    x: pos.x,
    y: pos.y,
    radius: 30,
    length: 300,
  };
}

function getProgress() {
  return (performance.now() - slash.startTime) / slash.duration;
}

function drawSlash(progress) {
  const length = slash.length;
  const filled = length * Math.min(progress, 1);

  ctx.save();
  ctx.translate(slash.x, slash.y);
  ctx.rotate(Math.PI / 9); // diagonal

  // background
  ctx.fillStyle = "#333";
  ctx.fillRect(-length / 2, -5, length, 10);

  // fill
  if (progress < 0.5) {
    ctx.fillStyle = "yellow";
  }
  else {
    ctx.fillStyle = "red";
  }
  
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

    if (progress < 0.5) {
      slash.radius += 0.5
      console.log("BONUS")
    }

    game.score += 1;
    // reset slash
    const pos = randomBottomSpawn();
    slash.duration -= 50;
    slash.radius -= 0.3;
    slash.x = pos.x;
    slash.y = pos.y;
    slash.startTime = performance.now();
  }
}

function randomBottomSpawn(
  slashLength = 300,
  marginX = 0.1,
  marginBottom = 0.1,
  marginTop = 0.05
) {
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;

  // --- NEW: account for slash size + rotation ---
  const halfLength = slashLength / 2;
  const safeOffset = halfLength * Math.SQRT2;

  const offsetX = safeOffset / width;
  const offsetY = safeOffset / height;

  // --- Clamp X range (respect margins + slash size) ---
  const minX = Math.max(marginX, offsetX);
  const maxX = Math.min(1 - marginX, 1 - offsetX);

  // --- Clamp Y range (bottom half + margins + slash size) ---
  const minY = Math.max(0.5 + marginTop, offsetY);
  const maxY = Math.min(1 - marginBottom, 1 - offsetY);

  const x = (minX + Math.random() * (maxX - minX)) * width;
  const y = (minY + Math.random() * (maxY - minY)) * height;

  return { x, y };
}

function loop() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const progress = getProgress();

  drawSlash(progress);
  checkHit(progress);
  if (progress >= 1) {
    // MISS
    game.hp -= 1;

    console.log("MISS", game.hp);

    const pos = randomBottomSpawn();
    slash.x = pos.x;
    slash.y = pos.y;

    slash.startTime = performance.now();
  }

  if (game.hp <= 0) {
    ctx.fillStyle = "red";  
    ctx.font = "40px Arial";
    ctx.fillText("GAME OVER", canvas.clientWidth / 2 - 120, canvas.clientHeight / 2);
    ctx.fillText("SCORE:" + game.score, canvas.clientWidth / 2 - 90, canvas.clientHeight / 2 + 60);
    return;
  }

  drawUI();

  requestAnimationFrame(loop);
}

requestAnimationFrame(loop);

function drawScreen() {
    const bgColor = "black";
    canvas.style.backgroundColor = bgColor;
}

function drawUI() {
  ctx.fillStyle = "white";
  ctx.font = "20px Arial";

  // Score (top-left)
  ctx.fillText("Score: " + game.score, 20, 30);

  // HP (top-right)
  ctx.fillText("HP: " + game.hp, canvas.clientWidth - 100, 30);
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
drawScreen();
initSlash();