const tf = require('@tensorflow/tfjs-node');

async function run() {
    const dataset = tf.data.csv('file://./car.csv', {hasHeader: true});
    const v = await dataset.take(2).toArray();
    v.forEach((line) => {
        console.log(line);  
    });      
}

run();