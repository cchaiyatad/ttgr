const tf = require('@tensorflow/tfjs-node');

const xs = tf.randomNormal([10, 2]);

console.log(xs.shape);
xs.print();

xs.data().then(data => {
    console.log(data);
});

xs.array().then(array => {
    console.log(array);
});