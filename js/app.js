const tf = require('@tensorflow/tfjs-node');

async function loadModel(){
    const path = 'file://../saved_model/model/model.json';
    const model = await tf.loadLayersModel(path);
    return model;
}

function predict(model, value){
    const data = tf.tensor2d(value, [1,4]);
    let index = getMax(model.predict(data).dataSync());
    return index;
}

function getMax(array){
    var index = 0;
    for(var i = 0; i < array.length;i++){
        if(array[index] < array[i]){
            index = i;
        }
    }
    return index;
}

var value = [0,-50,0,0];
loadModel().then((model) => {
    var predictValue = predict(model,value);
    console.log(predictValue);
});

