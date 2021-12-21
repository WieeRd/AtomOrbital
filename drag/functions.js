let sin = Math.sin;
let cos = Math.cos;

let position1 = { x: 0, y: 0 };
let position2 = { x: 0, y: 0 };
let delta = { x: 0, y: 0 };
let vectors = { x: [100, 0, 0], y: [0, 100, 0], z: [0, 0, 100] };

const canvas = document.getElementById("vector");
const ctx = canvas.getContext("2d");

const P2R = 0.01;
function calcDegree(deltaP) {
    let deltaR = { z: - deltaP.x * P2R, y: - deltaP.y * P2R };
    return deltaR;
}

function rotateZ(vector, degree) {
    let tempX = vector[0];
    vector[0] = cos(degree) * vector[0] - sin(degree) * vector[1];
    vector[1] = sin(degree) * tempX + cos(degree) * vector[1];
    return vector;
}

function rotateY(vector, degree) {
    let tempX = vector[0];
    vector[0] = cos(degree) * vector[0] + sin(degree) * vector[2];
    vector[2] = - sin(degree) * tempX + cos(degree) * vector[2];
    return vector;
}

// function calcVector(deltaR) {
//     if (deltaR.z >= deltaR.y) {
//         //z axis
//         for (let key in vectors) {
//             rotateZ(vectors[key], deltaR.z);
//         }

//     } else if (deltaR.z < deltaR.y) {
//         //y axis
//         for (let key in vectors) {
//             rotateY(vectors[key], deltaR.y);
//         }
//     }
// }

function calcVector(deltaR) {
    for (let key in vectors) {
        rotateZ(vectors[key], deltaR.z);
    }
    for (let key in vectors) {
        rotateY(vectors[key], deltaR.y);
    }
}

function draw() {

    calcVector(calcDegree(delta));
    console.log(vectors);
    
    ctx.strokeWidth = 10;

    let color = {x: 'red', y: 'green', z: 'blue'};
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let key in vectors) {
        ctx.strokeStyle = color[key];
        ctx.beginPath();
        ctx.moveTo(250, 250);
        ctx.lineTo(250 + vectors[key][1], 250 - vectors[key][2]);
        ctx.stroke();
    }
}

let isClick = false;

document.onmousedown = (e) => {
    isClick = true;
    position2 = { x: e.clientX, y: e.clientY };
}

document.onmouseup = (e) => {
    isClick = false;
}

document.addEventListener("mousemove", (e) => {
    if(isClick) {
        delta = { x: position2.x - e.clientX, y: position2.y - e.clientY };
        position2 = { x: e.clientX, y: e.clientY };
        draw();
    }
});

draw();

//setInterval(draw, 100);