function grey2RGB(val) {
  if (val < 1 * 0xFF) {
      return [0, 0, val, 0xFF];
  }
  if (val < 2 * 0xFF) {
      return [0, val % 0xFF, 0xFF, 0xFF];
  }
  if (val < 3 * 0xFF) {
      return [val % 0xFF, 0xFF, 0xFF, 0xFF];
  } else {
      return [0xFF, 0xFF, 0xFF, 0xFF];
  }
}

function whiteBlack(val) {
  if(val < 5)
      return [0, 0, 0, 255];
  else
      return [255, 255, 255, 255];
}

function grey2RGB2(val) {

  if (val < 1*0xFF)
      return [0, 0, val, 0xFF];
  if (val < 2*0xFF)
      return [0, val%0xFF, 0xFF, 0xFF];
  if (val < 3*0xFF)
      return [0, 0xFF, 0xFF-val%0xFF, 0xFF];
  if (val < 4*0xFF)
      return [val%0xFF, 0xFF, 0, 0xFF];
  if (val < 5*0xFF)
      return [0xFF, 0xFF-val%0xFF, 0, 0xFF];
  else
      return [0xFF, 0, 0, 0xFF];
}

const exp = Math.exp;
const sin = Math.sin;
const cos = Math.cos;
const sqrt = Math.sqrt;

let RESOL = 512;
let SIZE = 5;


let X1 = -5;
let X2 = +5;

let xx1 = X2 - X1;
let xx3 = X2 ** 3 - X1 ** 3;
let xx5 = X2 ** 5 - X1 ** 5;
let xx7 = X2 ** 7 - X1 ** 7;
let xx9 = X2 ** 9 - X1 ** 9;

function valueY(y, z, ss, cc) {
  let k = sqrt(y ** 2 + z ** 2);
  let val = 0;
  if (k == 0) {
      val = ss * (
          0.5 - (
              X2 * (2 * X2 ** 2 + 2 * X2 + 1) * exp(-2 * X2)
          ) / (
              2 * X2
          )
      )
  } else {
      val = cc * z ** 2 * exp(-2 * k) * (
          + xx1
          - xx3 / (3 * k)
          + xx5 * (2 * k + 1) / (20 * k ** 3)
          - xx7 * (4 * k ** 2 + 6 * k + 3) / (168 * k ** 5)
          + xx9 * (8 * k ** 3 + 24 * k ** 2 + 30 * k + 15) / (1728 * k ** 7)
      ) + ss * exp(-2 * k) * (
          (
              // - n * m * z * (X2 ** 2 - X1 ** 2)
              + xx3 / 3
              // + (X2 ** 4 - X1 ** 4) * m * n * z / (2 * k)
              - xx5 / (5 * k)
              + xx7 * (12 * k + 6) / (168 * k ** 3)
          )
      );
  }

  return val;
  //   return (
  //     z * z * exp(-2 * sqrt(yyzz)) * (
  //         X2 - X1
  //         - (X2 ** 3 - X1 ** 3) / (3 * sqrt(yyzz))
  //         + (X2 ** 5 - X1 ** 5) * ((2 / yyzz) + (1 / (yyzz) ** (3 / 2))) / 20
  //     )
  // )

}

function value2p_v2(y, z, alpha) {
  
  let val = 0;
  for(let x = X1; x <=X2; x += 0.01) {
      // let x_temp = cos(alpha)*x + sin(alpha)*z
      // z = -sin(alpha)*x + cos(alpha)*z
      // x = x_temp;
      val += z**2*exp(-2*sqrt(x**2+y**2+z**2));
      // val += (z**2 - 2*x**2)**2*exp(-3*sqrt(x**2+y**2+z**2));
  }    
  // console.log(val);
  return val;
}
function value3d_v2(y, z, alpha) {
  
  let val = 0;
  for(let x = X1; x <=X2; x += 0.01) {
      // let x_temp = cos(alpha)*x + sin(alpha)*z
      // z = -sin(alpha)*x + cos(alpha)*z
      // x = x_temp;
      val += (x**2 - 2*z**2)**2*exp(-2*sqrt(x**2+y**2+z**2));
      // val += (z**2 - 2*x**2)**2*exp(-3*sqrt(x**2+y**2+z**2));
  }    
  // console.log(val);
  return val;
}

function value3d(y, z) {
  let k = sqrt(y ** 2 + z ** 2);
  let val = 4*xx1*z**4*exp(-3*k)-(2*xx3*(z**2*exp(-3*k)*(2*k+3*z**2)))/(3*k)+(xx5*exp(-3*k)*(2*z**2*k+2*y**2*(k+6*z**2)+3*z**4*(3*k+5)))/(10*(y**2+z**2)**(3/2))
  //-(3*xx7*(exp(-3*k)*(2*y**4+3*y**2*z**2*(2*k+z**2+2)+z**4*(9*k+3*z**2+5))))/(28*(y**2+z**2)**(5/2));
  // 4*xx1*z**4*exp((-2*k))
  // - (4*xx3*(z**2*exp((-2*k))*(k+z**2)))/(3*k)
  // + (xx5*exp((-2*k))*(z**2*k+y**2*(k+4*z**2)+z**4*(2*k+5)))/(5*(y**2+z**2)**(3/2))
  // + (xx7*exp((-2*k))*(-6*y**4-2*y**2*z**2*(6*k+2*z**2+9)-z**4*(18*k+4*z**2+15)))/(42*(y**2+z**2)**(5/2));
  return val;
}

let values = []

//let arr = Array.from({length: RESOL}, () => Array.from({length: RESOL}, () => Array.from({length: 3}, () => 0)));
let arr = [];

const canvas = document.getElementById("orbital");
const ctx = canvas.getContext("2d");
const orbitalImg = ctx.createImageData(RESOL, RESOL);

// console.log(value3d_v2(0.5, 0.1));

function createImgY(alpha) {
  return new Promise((resolve) => {
      let t0 = new Date();
      let cc = cos(alpha) ** 2
      let ss = sin(alpha) ** 2
      let y;
      let z;
      let val;
      let len = 0;
      for (let h = 0; h < RESOL; h++) {
          for (let w = 0; w < RESOL; w++) {
              z = -SIZE * (2 * h / RESOL - 1)
              y = +SIZE * (2 * w / RESOL - 1)

              //z = SIZE * (2 * h / (RESOL - 1) - 1);
              //y = SIZE * (2 * w / (RESOL - 1) - 1);
              /* if (y == 0 && z == 0) {
                  val = valueY(0, z + 1e-161, ss, cc);
                  //val = value2p_v2(0, z + 1e-161, 0);
                  // val = 0;
              } else {
                  val = valueY(y, z, ss, cc);
                  //val = value2p_v2(y, z, 0);
              } */
              val = valueY(y, z, ss, cc);

              let color = grey2RGB(val*10);
              for (let i = 0; i < 4; i++) {
                  orbitalImg.data[len + i] = color[i];
              }
              len += 4;
              //arr = arr.concat(grey2RGB(val));
              //ctx.fillStyle = `rgb(${grey2RGB(val).join(',')})`;
              //ctx.fillRect(w*2, h*2, 2, 2);
          }
      }
      ctx.putImageData(orbitalImg, 0, 0);
      t1 = new Date();
      console.log(`${t1 - t0}ms`);
      resolve();
  });
}

function render3d() {
  return new Promise((resolve) => {
      let t0 = new Date();
      let y;
      let z;
      let val;
      let len = 0;
      for (let h = 0; h < RESOL; h++) {
          for (let w = 0; w < RESOL; w++) {
              z = -SIZE * (2 * h / RESOL - 1)
              y = +SIZE * (2 * w / RESOL - 1)

              if (y == 0 && z == 0) {
                  val = value3d_v2(y + 1e-100, z + 1e-100, Math.PI/2);
              } else {
                  val = value3d_v2(y, z, Math.PI/2);
              }

              let color = grey2RGB(val*5);
              for (let i = 0; i < 4; i++) {
                  orbitalImg.data[len + i] = color[i];
              }
              len += 4;
              //arr = arr.concat(grey2RGB(val));
              //ctx.fillStyle = `rgb(${grey2RGB(val).join(',')})`;
              //ctx.fillRect(w*2, h*2, 2, 2);
          }
      }
      ctx.putImageData(orbitalImg, 0, 0);
      t1 = new Date();
      console.log(`${t1 - t0}ms`);
      resolve();
  });
}

function render(i) {
  if (i <= 12) {
      createImgY(Math.PI * i / 12).then(() => {
          setTimeout(function () {
              render(i + 1);
          }, 10);
      });
  }
  //createImgY(Math.PI / 2);
  //console.log(arr);
}

document.onkeydown = e => {
  if (e.key == 'Enter') {
      render(0);
  }
};