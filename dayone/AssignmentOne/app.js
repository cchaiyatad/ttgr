const tf = require('@tensorflow/tfjs-node');
const plotly = require('plotly')('TopgunTesa', 'c9ehVIlITupGYtDJh2wF');

function createData(num_pts){
    const xs = new Array();
    const ys = new Array();
    for(var i = 0; i < num_pts; i++){
        xs.push(i);
        ys.push((2 * i) + Math.random());
    }
    return {xs, ys};
}

function createModel(num_nodes){
    const model = tf.sequential();
    model.add(tf.layers.dense({units:1, inputShape: [1]}));
    model.add(tf.layers.dense({units: num_nodes, activation: 'relu'}));
    model.add(tf.layers.dense({units: 1}));
    
    model.compile({optimizer: tf.train.sgd(0.1), loss: 'meanSquaredError'});
    // print(typeof(model));
    return model;
}

async function trainModel(model, xs, ys, epochs){
    xs = tf.tensor1d(xs);
    ys = tf.tensor1d(ys);
    const lossHistory = new Array();
   
    await model.fit(xs, ys, {
        epochs: epochs,
        callbacks:{
            onEpochEnd: (epochs, log) => lossHistory.push(log.loss)
        }
    })
    return lossHistory;
}

async function predictModel(num_pts, xv) {
    var test = createData(num_pts);
    a = test.xs;
    b = test.ys;

    const model = createModel(8);
    const losses = await trainModel(model, a, b, 100);

    xv = tf.tensor1d(xv);
    const yv = model.predict(xv);
    return Array.from(yv.dataSync());
}

function plotResults(xv, yv){
    var data = [{x:xv, y:yv, type: 'linear'}];
    var layout = {fileopt : "overwrite", filename : "simple-node-example"};

    plotly.plot(data, layout, function (err, msg) {
	    if (err) return console.log(err);
    });
}
////
const xv = [10,20,30,40,50];

predictModel(30, xv).then((results)=>{
    console.log(results);
    plotResults(xv,results);
    // var loss = 0;
    // for(var i = 0; i < xv.length;i++){
    //     loss += Math.pow((((2 * xv[i]) + Math.random()) - results[i]), 2);
    // }
    // loss /= xv.length;
    // console.log(loss);
});
/////
module.exports = {createData, createModel, trainModel, predictModel}