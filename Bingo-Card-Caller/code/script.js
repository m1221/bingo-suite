const body = document.querySelector("body");
const toolbar = document.getElementById("tool-bar");
const gameModeDropdown = document.getElementById("game-mode-dropdown");
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
const themeDropdown = document.getElementById("theme-dropdown");
const imagePanel_B = document.getElementById("img-row-B");
const imagePanel_I = document.getElementById("img-row-I");
const imagePanel_N = document.getElementById("img-row-N");
const imagePanel_G = document.getElementById("img-row-G");
const imagePanel_O = document.getElementById("img-row-O");
const numberPanel_B = document.getElementById("img-row-B");
const numberPanel_I = document.getElementById("img-row-I");
const numberPanel_N = document.getElementById("img-row-N");
const numberPanel_G = document.getElementById("img-row-G");
const numberPanel_O = document.getElementById("img-row-O");
const oddPanels = [imagePanel_B, imagePanel_N, imagePanel_O, numberPanel_B, numberPanel_N, numberPanel_O];
const evenPanels = [imagePanel_I, imagePanel_G, numberPanel_I, numberPanel_G];
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
gameModeDropdown.value = "select-a-game-mode";
updateTableDisplay(null);
updatePlayAnimButton(bAnimEnabled);
updateCardTextButton(bShowCardText);

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

    if (newCardID == undefined){
        // display helpful message
        setButtonsEnabled(true);
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
        addCardToTable(newCardID, pool_ID);
        hideBigCard();
        setButtonsEnabled(true);
    }, bingo_machine_time + 4000);

}

function addCardToTable(card_id, pool_ID){
    let card = document.createElement("div");
    card.className = "table-card";
    let cardName = getCardDisplayName(card_id);

    let card_symbol;
    if (poolSelection.search("image") > -1) {
        card_symbol = document.createElement("img");
        card_symbol.src = pathmap[card_id];
    } else if (poolSelection.search("number") > -1) {
        card_symbol = document.createElement("p");
        card_symbol.className = "card-number";
        card_symbol.textContent = cardName;
    }
    
    let card_text = document.createElement("div");
    card_text.textContent = cardName;
    card_text.className = "card-text";
    card_text.style.visibility = bShowCardText ? "visible" : "hidden";

    card.appendChild(card_symbol);
    card.appendChild(card_text);
    drawnCardTexts.push(card_text);

    switch (poolSelection) {
        case "image-multi-pool":
            document.getElementById(`img-row-${pool_ID}`).appendChild(card);
            break;
        case "image-single-pool":
            imageTableSingle.appendChild(card);
            break;
        case "number-multi-pool":
            document.getElementById(`num-row-${pool_ID}`).appendChild(card);
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

function displayBigCard(card_id, pool_id){
    if (bigImageContainer.hasChildNodes()){
        bigImageContainer.innerHTML = "";
    }
    
    let cardName = getCardDisplayName(card_id);
    bigImageContainer.style.visibility = "visible";
    let bigCardSymbol;
    let bigCardText = null;
    if (poolSelection.search("image") > -1) {
        bigCardSymbol = document.createElement("img");
        bigCardSymbol.src = pathmap[card_id];
        // text at bottom of card
        bigCardText = document.createElement("div");
        bigCardText.textContent = cardName;
        bigCardText.className = "card-text"; 
        bigCardText.style.fontSize = "5vh";
        bigImageContainer.appendChild(bigCardText);
    } else if (poolSelection.search("number") > -1) {
        bigCardSymbol = document.createElement("p");
        bigCardSymbol.className = "card-number";
        bigCardSymbol.style.fontSize = "128px";
        bigCardSymbol.textContent = cardName;
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
        gameModeDropdown.value = poolSelection;
        return;
    }
    poolSelection = gameModeDropdown.value;
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
        gameModeDropdown.removeAttribute('disabled');
        themeDropdown.removeAttribute('disabled');
        newCardButton.removeAttribute('disabled');
        toggleAnimButton.removeAttribute('disabled');
        toggleCardTextButton.removeAttribute('disabled');
    }
    else {
        gameModeDropdown.setAttribute('disabled', true);
        themeDropdown.setAttribute('disabled', true);
        newCardButton.setAttribute('disabled', true);
        toggleAnimButton.setAttribute('disabled', true);
        toggleCardTextButton.setAttribute('disabled', true);
    }
}

// add options to themeDropdown
for ([id, theme] of themes){
    let option = document.createElement("option");
    option.value = id;
    option.textContent = theme.displayName;
    themeDropdown.appendChild(option);
}

function updateTheme(){
    let newTheme = themes.get(themeDropdown.value);
    let oddPanelColor = newTheme.colors.get("odd-number-panel");
    let evenPanelColor = newTheme.colors.get("even-number-panel");

    body.style.backgroundColor = newTheme.colors.get("body-background");
    toolbar.style.background = newTheme.colors.get("toolbar");
    for (panel of oddPanels){
        panel.style.background = oddPanelColor;
    }
    for (panel of evenPanels){
        panel.style.background = evenPanelColor;
    }
    
    // other elements that might be modified according to theme:
    // card borders; buttons; letters on the side (of multiple pool bingo)
    // add blurred background image?
}

updateTheme();

// add spacers for table rows 
(function(){
    let tableRows = document.getElementsByClassName("table-row");
    for (row of tableRows){
        let spacer = document.createElement("div");
        spacer.className = "spacer";
        row.insertBefore(spacer, row.firstChild);
    }
})();