const { createData, createModel, trainModel, predictModel } = require('../AssignmentOne/app');

//2.1
test("Create Data", () =>{
    expect(createData(10).xs.length).toBe(10);
});
//2.2
test("Create Model", () =>{
    var model = createModel(20);
    expect(model.layers.length).toBe(3);
    // expect(model.layers[0].unit)
});
//2.3
test("Train model", async () =>{
    var test = createData(25);
    a = test.xs;
    b = test.ys;
    const model = createModel(100);
    trainModel(model, a, b, 10).then((results)=>{
        expect(results.length).toBe(12);
    });
});

//2.4
test("", () =>{
    const xv = [10,20,30,40,50];
    predictModel(30,xv).then((results)=>{
        var loss = 0;
        for(var i = 0; i < xv.length;i++){
           loss += Math.pow((((2 * xv[i]) + Math.random()) - results[i]), 2);
        }
        loss /= xv.length;
        expect(loss < 0.1).toBe(true);
    })
});

//2.5
test("", () =>{
    const xv = [10,20,30,40,50];
    predictModel(5,xv).then((results)=>{
        var loss = 0;
        for(var i = 0; i < xv.length;i++){
           loss += Math.pow((((2 * xv[i]) + Math.random()) - results[i]), 2);
        }
        loss /= xv.length;
        expect(loss > 0.2).toBe(true);
    })
    
});

