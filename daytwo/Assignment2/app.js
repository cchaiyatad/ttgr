const tf = require('@tensorflow/tfjs-node');

async function createData(){
    //???
    mac_addrs = ["80:E1:26:07:C9:51", "80:E1:26:00:B4:04", "80:E1:25:00:D6:D7", "80:E1:26:07:C8:B0"];
    const xt = new Array();
    const yt = new Array();
    const dataset = tf.data.csv('file://../Assignment1/data.csv', {hasHeader: true});
    const v = await dataset.toArray();

    var tempArray = [1,1,1,1];
    const booleanArray = [false, false, false, false];
    for(var i = 0; i < v.length;i++){
        for(var j = 0; j < mac_addrs.length; j++){
            if(v[i] === mac_addrs[j]){ //macnumber
                if(booleanArray[j] == true){
                    xt.push(tempArray);
                    tempArray = new Array(); 
                }
                tempArray[j] = v[i]//ssid
            }
        }
        
    }
    return {xt, yt};
}

function createModel(){
    const model = tf.sequential();
    //??
    model.add(tf.layers.dense({units: 100, inputShape: [4]}));
    model.add(tf.layers.dense({units: 100, activation: 'relu'}));
    model.add(tf.layers.dense({units: 1}));
    
    model.compile({optimizer: tf.train.sgd(0.1), loss: 'meanSquaredError'});
    //??
    return model;
}

async function trainModel(model, data){
    data
    xs = tf.tensor2d(data.xs);
    ys = tf.tensor1d(data.ys);
    await model.fit(xs, ys, {
        epochs: 100
    })
    return model;
}

async function saveModel() {
    const data = await createData();
    const model = createModel();
    model = await trainModel(model, data)
    await model.save();
}
saveModel();






