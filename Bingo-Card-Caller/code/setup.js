let imagePool = [];
let pathmap = {};
let imagePools = {}

// 1. generate a single image pool
filepaths.forEach(path => {
    // '../source-images/individual-icons/01_spider-web.png' -> spider-web
    let split_path = path.split("/");
    let terminal = split_path[split_path.length - 1];
    let name = (terminal.split("_")[1]).split(".")[0]
    pathmap[name] = path;
    imagePool.push(name);
});

// 2. generate multiple image pools
for (const letter of "BINGO"){
    imagePools[letter] = [].concat(imagePool);
}

function popRandom(array){
    let random_index = Math.floor(Math.random() * array.length);
    return array.splice(random_index, 1)[0];
}
