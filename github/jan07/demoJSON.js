const fs = require('fs');

const rawdata = fs.readFileSync('./v.json');
let jsondata = JSON.parse(rawdata);

console.log(jsondata);

