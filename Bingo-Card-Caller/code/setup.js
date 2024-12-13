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