window.onload = () => {
    drawVisualization();
}

let sqrt = Math.sqrt;
let pow = Math.pow;
let random = Math.random;
let exp = Math.exp;
let sin = Math.sin;
let cos = Math.cos;
let PI = Math.PI;

const PERCENT = 0.5;
const BOHR_R = 5.2917721092e-11;

function drawVisualization() {
    // create the data table.

    // return;
    let data = {};
    data = new vis.DataSet();

    console.log("start!!!!!!");

    
    for (let theta = 0; theta < PI; theta += (PI / 36)) {
        console.log("theta: " + theta);
        let is_valid = (r) => {
            return calculate(r, theta, 0) > PERCENT;
        }

        let r = openBinarySearch(is_valid, 0.00001);

        console.log("r: " + r);

        for (let phi = 0; phi < 2*PI; phi += (PI/36)) {
            // console.log("phi: " + phi);
            let coordinate = reformCoordinate(r, theta, phi);
            // console.log(coordinate);
            data.add(coordinate);
        }
    }


    // specify options
    let options = {
        width: '100%',
        height: '100%',
        style: 'dot-color',
        showGrid: false,
        verticalRatio: 1.0,
        showLegend: false,
        cameraPosition: {
            horizontal: -0.35,
            vertical: 0.22,
            distance: 1.8
        }
    };

    // create our graph
    let container = document.getElementById('myOrbital');
    let graph = new vis.Graph3d(container, data, options);
}

function calculate(r, theta, phi) {
    let alpha = (cos(theta) ** 2) / (32 * (BOHR_R ** 4) * PI);
    let rest = -exp(-r / BOHR_R) * (r ** 2 + 4 * BOHR_R * r + 4 * BOHR_R ** 2) + 4 * (BOHR_R ** 2);
    return alpha * rest;
}

function openBinarySearch(is_valid, min_diff, init_val = 1, multiply = 2) {
    let val = init_val;

    while (!is_valid(val)) {
        val *= multiply;
    }

    return binarySearch(val / 2, val, is_valid, min_diff);
}

function binarySearch(lower, upper, is_valid, min_diff) {
    let val = (lower + upper) / 2;
    if ((upper - lower) < min_diff) {
        return val;
    }
    if (is_valid(val)) {
        return binarySearch(lower, val, is_valid, min_diff);
    } else {
        return binarySearch(val, upper, is_valid, min_diff);
    }
}

function reformCoordinate(r, theta, phi) {
    return { x: r * sin(theta) * cos(phi), y: r * sin(theta) * sin(phi), z: r * cos(theta) };
}
