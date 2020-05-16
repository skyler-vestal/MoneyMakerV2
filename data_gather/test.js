// Item request: A:18583427980 D:3035574093940040123 M:2578818544346804838
var fs = require("fs");
var content = fs.readFileSync("testData.info");
var meme = JSON.parse(content);
console.log(meme.itemInfo.itemid);
console.log(meme.itemInfo.float);