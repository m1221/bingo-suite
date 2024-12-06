const gameModeSelection = document.getElementById("game-mode-selection");
const minRange = document.getElementById("range-min");
const maxRange = document.getElementById("range-max");
const newCardButton = document.getElementById("new-card-button");
const toggleAnimButton = document.getElementById("toggle-anim-button");
const toggleCardTextButton = document.getElementById("toggle-card-text-button");
const gameModeDescriptions = document.getElementById("game-mode-descriptions");
const numberGenerationMenu = document.getElementById("number-generation-menu");
const imageTableSingle = document.getElementById("image-table-single");
const numberTableSingle = document.getElementById("number-table-single");
const imageTableMulti = document.getElementById("image-table-multi");
const numberTableMulti = document.getElementById("number-table-multi");
const bingoMachineAnim = document.getElementById("bingo-machine");
const bingoMachineContainer = document.getElementById("bingo-machine-container");
const bigImageContainer = document.getElementById("big-image-container");
// image-multi-pool; image-single-pool; number-multi-pool; number-single-pool
let poolSelection = "select-a-game-mode"; 
let buttonClickSound = new Audio("../audio/click.wav");
let rollingSound = new Audio("../audio/rolling-sound.wav")
let clangSound_01 = new Audio("../audio/clang-01.wav");
let clangSound_02 = new Audio("../audio/clang-02.wav");
let bButtonsEnabled = false;
let bAnimEnabled = false;
let bBingoMachineIMGValid = false;
let bShowCardText = false;

// additional setup
let animFilepath = "../image/bingo-ball-machine.gif";
let drawnCardTexts = [];
numberGenerationMenu.style.display = "none";
minRange.value = 1;
maxRange.value = 25;
let numberPool = null;
let numberPools = null;
gameModeSelection.value = "select-a-game-mode";
updateTableDisplay(null);
updatePlayAnimButton(bAnimEnabled);
updateCardTextButton(bShowCardText);

/* temp for testing
numberPool = Array.from({length: 25}, (e, i)=> i + 1);
numberPools = {};
for (const letter of "BINGO"){
    numberPools[letter] = [].concat(numberPool);
}*/

// check for valid BingoMachineImage
let testImage = document.createElement("img");
testImage.src = animFilepath;
setTimeout(function(){
    bButtonsEnabled = true;
    if (testImage.naturalHeight > 0){
        bBingoMachineIMGValid = true;
    }
}, 200);


function activateBingoMachine(){
    buttonClickSound.play();
    if (bButtonsEnabled == false) return;
    if (poolSelection == "number-multi-pool" && numberPools == null) return;
    if (poolSelection == "number-single-pool" && numberPool == null) return;
    // 0. disable ALL buttons
    setButtonsEnabled(false);

    // 1. get new card from pool
    let pool_ID = null;
    let newCardID, random_pool;
    switch (poolSelection) {
        case "image-multi-pool":
            pool_ID = "BINGO"[Math.floor(Math.random() * 5)];
            random_pool = imagePools[pool_ID];
            newCardID = popRandom(random_pool);
            break;
        case "image-single-pool":
            newCardID = popRandom(imagePool);
            break;
        case "number-multi-pool":
            pool_ID = "BINGO"[Math.floor(Math.random() * 5)];
            random_pool = numberPools[pool_ID];
            newCardID = popRandom(random_pool);
            break;
        case "number-single-pool":
            newCardID = popRandom(numberPool);
            break;    
        default:
            // TODO: display message to user -> ask them to select a game mode
            // only hide the message after the user has selected a game mode...
            setTimeout(function(){
                setButtonsEnabled(true);
            }, 300);
            return;
    }
    
    // 2. show card (and possible bingo machine anim)
    let bingo_machine_time = 0;
    if (bAnimEnabled && bBingoMachineIMGValid) {
        bingo_machine_time = 6000;
        playBingoMachineAnim();
        playBingoMachineAudio();
        setTimeout(function(){ FadeOutBingoMachine(); }, 6000);
        setTimeout(function(){ bingoMachineAnim.src = ""; }, 7000);
        setTimeout(function(){ displayBigCard(newCardID, pool_ID)}, bingo_machine_time + 1200);
    }
    else {
        bingo_machine_time = -1500;
        displayBigCard(newCardID, pool_ID);
    }
    
    // 3. update table and reset 
    setTimeout(function(){
        addCardToTable(pool_ID, newCardID);
        hideBigCard();
        setButtonsEnabled(true);
    }, bingo_machine_time + 4000);

}

function addCardToTable(pool_id, card_name){
    let card = document.createElement("div");
    card.className = "table-card";

    let card_symbol;
    if (poolSelection.search("image") > -1) {
        card_symbol = document.createElement("img");
        card_symbol.src = pathmap[card_name];
    } else if (poolSelection.search("number") > -1) {
        card_symbol = document.createElement("p");
        card_symbol.className = "card-number";
        card_symbol.textContent = card_name;
    }
    
    let card_text = document.createElement("div");
    card_text.textContent = card_name;
    card_text.className = "card-text";
    card_text.style.visibility = bShowCardText ? "visible" : "hidden";

    card.appendChild(card_symbol);
    card.appendChild(card_text);
    drawnCardTexts.push(card_text);

    switch (poolSelection) {
        case "image-multi-pool":
            document.getElementById(`img-row-${pool_id}`).appendChild(card);
            break;
        case "image-single-pool":
            imageTableSingle.appendChild(card);
            break;
        case "number-multi-pool":
            document.getElementById(`num-row-${pool_id}`).appendChild(card);
            break;
        case "number-single-pool":
            numberTableSingle.appendChild(card);
            break;    
        default:
            break;
    }  
}

/* BingoMachineAnim - BEGIN */
function playBingoMachineAnim() {
    let timestamp = new Date().getTime();
    let queryString = "?t=" + timestamp; // use queryString to avoid cache reload
    bingoMachineContainer.classList.remove("bingo-machine-fadeOut");
    bingoMachineContainer.classList.add("bingo-machine-fadeIn");
    bingoMachineAnim.src = "../image/bingo-ball-machine.gif" + queryString;
}

function FadeOutBingoMachine() {
    bingoMachineContainer.classList.remove("bingo-machine-fadeIn");
    bingoMachineContainer.classList.add("bingo-machine-fadeOut");
}
/* BingoMachineAnim - END */

function playBingoMachineAudio(){
    setTimeout(function(){ rollingSound.play(); }, 1000);
    setTimeout(function(){ 
        let sound_to_play = Math.random() > 0.5 ? clangSound_01 : clangSound_02;
        sound_to_play.play(); 
    }, 5500);
    
}

function displayBigCard(card_name, pool_id){
    if (bigImageContainer.hasChildNodes()){
        bigImageContainer.innerHTML = "";
    }
    
    bigImageContainer.style.visibility = "visible";
    let bigCardSymbol;
    let bigCardText = null;
    if (poolSelection.search("image") > -1) {
        bigCardSymbol = document.createElement("img");
        bigCardSymbol.src = pathmap[card_name];
        // text at bottom of card
        bigCardText = document.createElement("div");
        bigCardText.textContent = card_name;
        bigCardText.className = "card-text"; 
        bigCardText.style.fontSize = "5vh";
        bigImageContainer.appendChild(bigCardText);
    } else if (poolSelection.search("number") > -1) {
        bigCardSymbol = document.createElement("p");
        bigCardSymbol.className = "card-number";
        bigCardSymbol.style.fontSize = "128px";
        bigCardSymbol.textContent = card_name;
    }
    let bigCardPoolID = document.createElement("div");
    bigCardPoolID.className = "pool-id-text";
    bigCardPoolID.textContent = pool_id;
    bigCardPoolID.style.fontSize = "10vh";

    bigImageContainer.appendChild(bigCardSymbol);
    bigImageContainer.appendChild(bigCardPoolID);
}

function hideBigCard(){
    bigImageContainer.style.visibility = "hidden";
}

function updateGameMode(){
    if (! bButtonsEnabled) {
        gameModeSelection.value = poolSelection;
        return;
    }
    poolSelection = gameModeSelection.value;
    updateTableDisplay(poolSelection);
}

function getNewTextColor(bActive){
    let newTextColor = bActive ? "#ffffff" : "#a2a2a2";
    return newTextColor;
}

function updatePlayAnimButton(bActive){
    let newText = bActive ? "Anim is ON" : "Anim is OFF";
    toggleAnimButton.textContent = newText;
    toggleAnimButton.style.color = getNewTextColor(bActive);
}

function togglePlayAnim(){
    if (! bButtonsEnabled) return;
    buttonClickSound.play();
    bAnimEnabled = bAnimEnabled ? false : true;
    updatePlayAnimButton(bAnimEnabled);
}

function updateTableDisplay(poolSelection){
    imageTableSingle.style.display = "none";
    numberTableSingle.style.display = "none";
    imageTableMulti.style.display = "none";
    numberTableMulti.style.display = "none";
    gameModeDescriptions.style.display = "none";
    numberGenerationMenu.style.display = "none";

    switch (poolSelection) {
        case "image-multi-pool":
            imageTableMulti.style.display = "inline"; // inline vs block? i forgot the difference
            break;
        case "number-multi-pool":
            if (numberPools == null) {
                numberGenerationMenu.style.display = "inline-grid";
                break;
            }
            numberTableMulti.style.display = "inline";
            break;
        case "image-single-pool":
            imageTableSingle.style.display = "flex";
            break;
        case "number-single-pool":
            if (numberPool == null) {
                numberGenerationMenu.style.display = "inline-grid";
                break;
            }
            numberTableSingle.style.display = "flex";
            break;
        default:
            gameModeDescriptions.style.display = "inline";
            break;
    }
}

function updateCardTextButton(bActive){
    let newText = bActive ? "Card Text is ON" : "Card Text is OFF";
    toggleCardTextButton.textContent = newText;
    let newTextColor = getNewTextColor(bActive);
    toggleCardTextButton.style.color = newTextColor;
}

function toggleCardText(){
    if (! bButtonsEnabled) return;
    buttonClickSound.play();
    bShowCardText = bShowCardText ? false : true;
    let textVisibility = bShowCardText ?  "visible" : "hidden";
    for (cardText of drawnCardTexts) {
        cardText.style.visibility = textVisibility;
    }
    updateCardTextButton(bShowCardText);
}

function generateNumberPools(){
    buttonClickSound.play();
    let range = Number(maxRange.value) - Number(minRange.value);
    if (range < 24) {
        // TODO: display user-friendly message
        console.log("please range diff >= 24");
        return;
    }
    let temp =  Array.from({length: range}, (e, i)=> i + Number(minRange.value));
    if (poolSelection == "number-single-pool") {
        numberPool = [].concat(temp);
    } else if (poolSelection == "number-multi-pool") {
        numberPools = {};
        for (const letter of "BINGO"){
            numberPools[letter] = [].concat(temp);
        }
    }
    updateGameMode();
}

function setButtonsEnabled(bool) {
    bButtonsEnabled = bool;
    newCardButton.style.color = bool ? "#ffffff" : "#000000";
    if (bool) {
        gameModeSelection.removeAttribute('disabled');
        newCardButton.removeAttribute('disabled');
        toggleAnimButton.removeAttribute('disabled');
        toggleCardTextButton.removeAttribute('disabled');
    }
    else {
        gameModeSelection.setAttribute('disabled', true);
        newCardButton.setAttribute('disabled', true);
        toggleAnimButton.setAttribute('disabled', true);
        toggleCardTextButton.setAttribute('disabled', true);
    }
}