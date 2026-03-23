const canvas = document.getElementById("screenCanvas");
const ctx = canvas.getContext("2d");

let aspectRatio = 1;

function resizeCanvas() {
    const screenWidth = window.innerWidth;

    const displayWidth = screenWidth;
    const displayHeight = screenWidth * aspectRatio;

    canvas.style.width = displayWidth + 'px';
    canvas.style.height = displayHeight + 'px';

    const dpr = window.devicePixelRation || 1;

    canvas.wdith = displayWidth * dpr;
    canvas.height = displayHeight * dpr;
}

function drawScreen() {
    const bgColor = "black";

    canvas.style.backgroundColor = bgColor;
}

function onLoad() {
    resizeCanvas();
    drawScreen();
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
drawScreen();