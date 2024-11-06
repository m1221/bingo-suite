let pool = [];
let pathmap = {};

filepaths.forEach(path => {
    // '../source-images/individual-icons/01_spider-web.png',
    let split_path = path.split("/");
    let terminal = split_path[split_path.length - 1];
    let name = (terminal.split("_")[1]).split(".")[0]
    pathmap[name] = path;
    pool = pool.concat(name);
    /*
    for (const letter of "BINGO"){
        pool = pool.concat(`${letter}_${name}`);
    }*/

});

function popRandom(array){
    let random_index = Math.floor(Math.random() * array.length);
    return array.splice(random_index, 1)[0];
}
