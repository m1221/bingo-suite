let pathmap = {};
let imagePools = {};
imagePools['single-pool'] = [];

// 1. generate a single image pool
filepaths.forEach(path => {
    // 'BingoSuite/source-images/01_spider-web.png' -> spider web
    // 'BingoSuite/source-images/spider-web.png' -> spider web
    let split_path = path.split("/");
    let terminal = split_path[split_path.length - 1];
    if (terminal.search("_") != -1){
        terminal = terminal.split("_")[1];
    }
    let name = terminal.split(".")[0];
    pathmap[name] = path;
    imagePools['single-pool'].push(name);
});

// 2. generate multiple image pools
for (const letter of "BINGO"){
    imagePools[letter] = [].concat(imagePools['single-pool']);
}

function popRandom(array){
    if (array.length == 0){
        return undefined;
    }
    let random_index = Math.floor(Math.random() * array.length);
    return array.splice(random_index, 1)[0];
}

function getCardDisplayName(cardName){
    let displayName = cardName.replace("-", " ");
    let apostrophePos = displayName.lastIndexOf("aaa");
    if (apostrophePos != -1){
        displayName = displayName.slice(0, apostrophePos) + "'" + displayName.slice(apostrophePos + 3);
    }

    hyphen_pos = displayName.lastIndexOf("hhh");
    if (hyphen_pos != -1){
        displayName = displayName.slice(0, hyphen_pos) + "-" + displayName.slice(hyphen_pos + 3);
    }
    return displayName;
}