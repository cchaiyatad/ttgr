const tf = require('@tensorflow/tfjs-node');

async function getData(filename){
    const dataset = tf.data.csv(filename, {hasHeader: true});
    const v = await dataset.toArray();
    return v;
}
function createData(filename){
    getData(filename);
    // for(var v = )
}