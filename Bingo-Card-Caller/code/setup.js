let pool = [];
let pathmap = {};
let pools = {}

filepaths.forEach(path => {
    // '../source-images/individual-icons/01_spider-web.png',
    let split_path = path.split("/");
    let terminal = split_path[split_path.length - 1];
    let name = (terminal.split("_")[1]).split(".")[0]
    pathmap[name] = path;
    pool.push(name);
});

for (const letter of "BINGO"){
    pools[letter] = [].concat(pool);
}

function popRandom(array){
    let random_index = Math.floor(Math.random() * array.length);
    return array.splice(random_index, 1)[0];
}
