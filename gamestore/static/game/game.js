// Main structure from https://www.sitepoint.com/quick-tip-game-loop-in-javascript/

$(document).ready(function () {
    "use strict";

    var WIDTH = 700;
    var HEIGHT = 400;
    var HEIGHT_STATUS = document.getElementById("statusPane").clientHeight + 20;
    var canvas = document.getElementById("gameCanvas");
    var ctx = canvas.getContext("2d");
    var lastRender = 0;
    var defaultFont = 'bold 24px helvetica';
    var sadSkyColor = { r: 0, g: 37, b: 51 };
    var happySkyColor = { r: 0, g: 191, b: 255 };
    var skyColor = rgbToHex(happySkyColor);

    var imageCount = 0;
    var playerImage = loadImage("awesome-face.png");
    var sadPlayerImage = loadImage("sad-face.png");
    var cloud1 = loadImage("cloud1.png");
    var cloud2 = loadImage("cloud2.png");
    var cloud3 = loadImage("cloud3.png");
    var cloud4 = loadImage("cloud4.png");
    var patternImg = loadImage("wood-pattern.png");
    var pattern = undefined;
    var cloudImage = {
        1: cloud1,
        2: cloud2,
        3: cloud3,
        4: cloud4
    }
    var audio = new Audio('bensound-cute.mp3');
    var audioSad = new Audio('Plaint.mp3');
    var paused = false;
    var running = true;
    var gameOverTransition = 1;
    var gameOverTransitionSpeed = 0.0004;

    var tileWidth = 50;
    var groundHeight = 300;
    var playerSize = 40;

    var speed = 0.25;
    var worldSpeed = 0.1;
    var gravity = 0.001;
    var jumpSpeed = 0.5;
    var jumpDelay = 500; //ms

    /*
    * GAME STATE
    */
    var state = {
        x: WIDTH / 2,
        y: HEIGHT / 2,
        vy: 0,
        vx: 0,
        world: [],
        score: 0,
        offset: 0,
        onGround: false,
        jumpCount: 0,
        jumpCooldown: 0,
    };
    var pressedKeys = {
        left: false,
        right: false,
        up: false,
        down: false,
        addScore: false,
    };

    /*
    * INIT
    */
    function init() {
        pattern = ctx.createPattern(patternImg, 'repeat');
        window.addEventListener("keydown", keydown, false);
        window.addEventListener("keyup", keyup, false);
        audio.loop = true;
        audio.play();

        audioSad.volume = 0;
        audioSad.loop = true;
        audioSad.play();

        updateSize();
        start();
    }

    /*
    * START
    */
    function start() {
        console.log("start");
        running = true;
        lastRender = window.performance.now();
        state = {
            x: WIDTH / 2,
            y: HEIGHT / 2,
            vy: 0,
            vx: 0,
            world: [],
            score: 0,
            offset: 0,
            jumpCount: 0,
            jumpCooldown: 0,
            clouds: [],
        };
        state.clouds[0] = {
            x: 800,
            y: 50,
            speed: 0.12,
            type: 2,
        }
        state.clouds[1] = {
            x: 500,
            y: 20,
            speed: 0.05,
            type: 1,
        }
        state.clouds[2] = {
            x: 100,
            y: 100,
            speed: 0.04,
            type: 1,
        }

        for (var i = 0; i < 30; i++) {
            state.world[i] = generateTile();
        }
        // Make start tiles solid
        var leftSide = Math.floor((state.x + state.offset) / tileWidth);
        var rightSide = Math.floor((state.x + playerSize + state.offset) / tileWidth);
        state.world[leftSide] = 1;
        state.world[rightSide] = 1;

        window.requestAnimationFrame(mainLoop)
    }

    /*
    * HELPER FUNCTIONS
    */

    function interpolateColor(from, to, a) {
        if (a < 0) return rgbToHex(from);
        if (a > 1) return rgbToHex(to);
        var r = Math.round((1 - a) * from.r + a * to.r);
        var g = Math.round((1 - a) * from.g + a * to.g);
        var b = Math.round((1 - a) * from.b + a * to.b);
        var rgb = { r: r, g: g, b: b };
        return rgbToHex(rgb);
    }

    function rgbToHex(rgb) {
        var hexR = ("00" + Number(rgb.r).toString(16)).slice(-2);
        var hexG = ("00" + Number(rgb.g).toString(16)).slice(-2);
        var hexB = ("00" + Number(rgb.b).toString(16)).slice(-2);
        var result = "#" + hexR + hexG + hexB;
        return result;
    }

    function loadImage(path) {
        imageCount++;
        var image = new Image();
        image.src = path;
        image.onload = function () {
            imageCount--;
            if (imageCount === 0) {
                init();
            }
        };
        return image;
    }

    function generateTile() {
        return Math.round(Math.random() * 0.7);
    }

    function random(from, to) {
        return Math.random() * (to - from) + from;
    }

    function randomInt(from, to) {
        return Math.floor(Math.random() * (to - from + 1)) + from;
    }

    function updateSize() {
        canvas.height = HEIGHT;
        canvas.width = WIDTH;
        var message = {
            messageType: "SETTING",
            options: {
                "width": WIDTH,
                "height": HEIGHT + HEIGHT_STATUS
            }
        };
        window.parent.postMessage(message, "*");
    }

    /*
    * GAME LOGIC
    */
    function mainLoop(timestamp) {
        var delta = timestamp - lastRender;

        if (running) {
            gameOver(delta, gameOverTransitionSpeed);
            if (!paused) update(delta);
            draw();
            if (paused) {
                ctx.font = 'bold 48px helvetica';
                var message = 'PAUSED';
                var text = ctx.measureText(message);
                drawText(message, WIDTH / 2 - text.width / 2, HEIGHT / 2, 'bold 48px helvetica')
            }
        } else {
            gameOver(delta, -gameOverTransitionSpeed);
            draw()
            ctx.drawImage(sadPlayerImage, state.x, state.y, playerSize, playerSize);
            ctx.font = 'bold 48px helvetica';
            var message = 'Press space to restart';
            var text = ctx.measureText(message);
            drawText(message, WIDTH / 2 - text.width / 2, HEIGHT / 2, 'bold 48px helvetica')
        }
        lastRender = timestamp
        window.requestAnimationFrame(mainLoop)
    }

    function gameOver(delta, speed) {
        gameOverTransition += delta * speed;
        if (gameOverTransition > 1) gameOverTransition = 1;
        if (gameOverTransition < 0) gameOverTransition = 0;
        audio.volume = gameOverTransition;
        audioSad.volume = 1 - gameOverTransition;
        skyColor = interpolateColor(sadSkyColor, happySkyColor, gameOverTransition);
    }

    function update(delta) {
        state.jumpCooldown -= delta;
        state.vy += delta * gravity;

        // Move clouds
        var i = state.clouds.length
        while (i--) {
            var cloud = state.clouds[i];
            cloud.x -= delta * cloud.speed;

            if (cloud.x < -cloudImage[cloud.type].width) {
                state.clouds.splice(i, 1);
            }
        }

        // Spawn clouds
        if (state.clouds.length < 5 && Math.random() < 0.01) {
            var type = randomInt(1, 2)
            var cloud = {
                x: 1000,
                y: random(0, groundHeight - cloudImage[type].height) - 50,
                speed: random(0.01, 0.20),
                type: type,
            };
            state.clouds.push(cloud)
        }

        // Move world
        state.offset += delta * worldSpeed;
        state.score += delta * worldSpeed;
        state.x -= delta * worldSpeed;
        if (state.offset > tileWidth) {
            state.offset -= tileWidth;
            state.world.shift();
            state.world.push(generateTile());
        }
        handleInput();
        updatePositions(delta)
    }

    function updatePositions(delta) {

        // X movement
        state.x += state.vx * delta;
        if (checkCollision()) {
            state.x -= state.vx * delta;
            state.vx = 0;
        }

        // Y movement
        state.y += state.vy * delta;
        if (state.y + playerSize > HEIGHT) {
            console.log("GAME OVER");
            audioSad.currentTime = 0;
            running = false;
        }
        if (checkCollision()) {
            state.y = groundHeight - playerSize;
            state.vy = 0;
            state.jumpCount = 0;
        }

        // Clamp position to screen
        if (state.x + playerSize > WIDTH) {
            state.x = WIDTH - playerSize;
        }
        else if (state.x < 0) {
            state.x = 0;
        }
        if (state.y + playerSize > HEIGHT) {
            state.y = HEIGHT - playerSize;
        }
        else if (state.y < 0) {
            state.y = 0;
        }
    }

    function checkCollision() {
        var leftSide = Math.floor((state.x + state.offset) / tileWidth);
        var rightSide = Math.floor((state.x + playerSize + state.offset) / tileWidth);
        if (state.world[leftSide] === 1 || state.world[rightSide] === 1) {
            if (state.y + playerSize > groundHeight) {
                return true;
            }
        }
        return false;
    }

    /*
    * INPUT
    */

    // WASD
    var keyMap = {
        68: 'right',    //D
        65: 'left',     //A
        87: 'up',       //W
        83: 'down',     //S
        69: 'addScore',  //E
    }

    function handleInput() {
        state.vx = 0;
        if (pressedKeys.left) {
            state.vx = -speed;
        }
        if (pressedKeys.right) {
            state.vx = speed;
        }
        if (pressedKeys.up && state.jumpCount < 2 && state.jumpCooldown <= 0) {
            state.vy = -jumpSpeed;
            state.jumpCount++;
            state.jumpCooldown = jumpDelay;
        }
    }

    function keydown(event) {
        if (!running) {
            if (event.keyCode === 32) { //SPACE
                start();
            }
        } else {
            if (event.keyCode === 32) { //SPACE
                paused = !paused;
            }
        }
        if (event.keyCode === 89) { //Y
            HEIGHT++;
            updateSize();
        }
        if (event.keyCode === 72) { //H
            HEIGHT--;
            updateSize();
        }
        if (event.keyCode === 84) { //T
            WIDTH++;
            updateSize();
        }
        if (event.keyCode === 71) { //G
            WIDTH--;
            updateSize();
        }
        var key = keyMap[event.keyCode]
        pressedKeys[key] = true
    }
    function keyup(event) {
        var key = keyMap[event.keyCode]
        pressedKeys[key] = false
    }

    /*
    * RENDERING
    */
    function draw() {
        ctx.fillStyle = skyColor;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(playerImage, state.x, state.y, playerSize, playerSize);

        drawPlatforms();
        drawClouds();

        var message = 'Distance: ' + Math.floor(state.score);
        ctx.font = defaultFont;
        var text = ctx.measureText(message);
        drawText(message, WIDTH - text.width - 20, 20);
        var message = 'Move with WASD, you can jump twice';
        drawText(message, 0, 20);
    }
    function drawPlatforms() {
        var platform = false;
        var platformStart = 0;
        ctx.fillStyle = pattern;
        for (var i = 0; i < state.world.length; i++) {
            if (state.world[i] === 1 && !platform) {
                platform = true;
                platformStart = i;
            } else if (state.world[i] === 0 && platform) {
                //Make platform
                ctx.fillRect((platformStart * tileWidth) - state.offset, groundHeight, (i - platformStart) * tileWidth, HEIGHT - groundHeight);
                platform = false;
            }
        }
        if (platform) {
            ctx.fillRect((platformStart * tileWidth) - state.offset, groundHeight, (state.world.length - platformStart) * tileWidth, HEIGHT - groundHeight);
            platform = false;
        }
    }
    function drawClouds() {
        var i = state.clouds.length;
        while (i--) {
            var cloud = state.clouds[i];
            ctx.drawImage(cloudImage[cloud.type], cloud.x, cloud.y);
        }
    }
    function drawText(text, x, y, font) {
        ctx.fillStyle = "white";
        ctx.strokeStyle = "black";
        ctx.lineWidth = 1.5;
        if (font) ctx.font = font
        else ctx.font = defaultFont;
        ctx.fillText(text, x, y);
        ctx.strokeText(text, x, y);
    }

    /*
    * MESSAGE HANDLING
    */

    // SCORE
    $("#submit_score").click(function () {
        var msg = {
            "messageType": "SCORE",
            "score": state.score
        };
        window.parent.postMessage(msg, "*");
    });

    // SAVE
    $("#save").click(function () {
        var msg = {
            "messageType": "SAVE",
            "gameState": state
        };
        window.parent.postMessage(msg, "*");
    });

    // LOAD_REQUEST
    $("#load").click(function () {
        var msg = {
            "messageType": "LOAD_REQUEST",
        };
        window.parent.postMessage(msg, "*");
    });

    // LOAD
    window.addEventListener("message", function (evt) {
        if (evt.data.messageType === "LOAD") {
            state = evt.data.gameState;
            document.getElementById("scoreDisplay").innerHTML = state.score;
        } else if (evt.data.messageType === "ERROR") {
            alert(evt.data.info);
        }
    });
});