const newCardButton = document.getElementById("new-card-button");
const tableSingle = document.getElementById("table-single");
const tableMulti = document.getElementById("table-multi");
const bingoMachineAnim = document.getElementById("bingo-machine");
const bingoMachineContainer = document.getElementById("bingo-machine-container");
const bigImageContainer = document.getElementById("big-image-container");
let poolSelection = "multiple-pool"; // multi-pool vs single-pool
let buttonClickSound = new Audio("../audio/click.wav");
let rollingSound = new Audio("../audio/rolling-sound.wav")
let clangSound_01 = new Audio("../audio/clang-01.wav");
let clangSound_02 = new Audio("../audio/clang-02.wav");
let bButtonsEnabled = false;
let bAnimEnabled = true;
let bBingoMachineIMGValid = false;
let bShowCardText = false;
let animFilepath = "../image/bingo-ball-machine.gif";
let drawnCardTexts = [];

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
    if (bButtonsEnabled == false) return;
    // 0. disable ALL buttons
    bButtonsEnabled = false;
    newCardButton.style.color = "#000000";
    buttonClickSound.play();

    // 1. get new card from pool
    let pool_id = null;
    let new_card;
    if (poolSelection == "multiple-pool")
    {
        pool_id = "BINGO"[Math.floor(Math.random() * 5)];
        let random_pool = pools[pool_id];
        new_card = popRandom(random_pool);
    } else if ( poolSelection == "single-pool"){
        new_card = popRandom(pool);
    }
    
    // 2. show card (and possible bingo machine anim)
    let bingo_machine_time = 0;
    if (bAnimEnabled && bBingoMachineIMGValid) {
        bingo_machine_time = 6000;
        playBingoMachineAnim();
        playBingoMachineAudio();
        setTimeout(function(){ FadeOutBingoMachine(); }, 6000);
        setTimeout(function(){ bingoMachineAnim.src = ""; }, 7000);
        setTimeout(function(){ displayBigCard(new_card, pool_id)}, bingo_machine_time + 1200);
    }
    else {
        bingo_machine_time = -1500;
        displayBigCard(new_card, pool_id);
    }
    
    // 3. update table and reset 
    setTimeout(function(){
        addCardToTable(pool_id, new_card);
        hideBigCard();
        bButtonsEnabled = true;
        newCardButton.style.color = "#ffffff";
    }, bingo_machine_time + 4000);

}

function addCardToTable(pool_id, card_name){
    let card = document.createElement("div");
    card.className = "table-card";
    let card_image = document.createElement("img");
    card_image.src = pathmap[card_name];
    let card_text = document.createElement("div");
    card_text.textContent = card_name;
    card_text.className = "card-text";
    card_text.style.visibility = bShowCardText ? "visible" : "hidden";

    card.appendChild(card_image);
    card.appendChild(card_text);
    drawnCardTexts.push(card_text);
    
    if (poolSelection == "single-pool"){
        tableSingle.appendChild(card);
    }
    else if (poolSelection == "multiple-pool"){
        document.getElementById(`row-${pool_id}`).appendChild(card);
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
    let bigCardImage = document.createElement("img");
    bigCardImage.src = pathmap[card_name];
    let bigCardText = document.createElement("div");
    bigCardText.textContent = card_name;
    bigCardText.className = "card-text"; 
    bigCardText.style.fontSize = "5vh";
    let bigCardPoolID = document.createElement("div");
    bigCardPoolID.className = "pool-id-text";
    bigCardPoolID.textContent = pool_id;
    bigCardPoolID.style.fontSize = "10vh";

    bigImageContainer.appendChild(bigCardImage);
    bigImageContainer.appendChild(bigCardText);
    bigImageContainer.appendChild(bigCardPoolID);
}

function hideBigCard(){
    bigImageContainer.style.visibility = "hidden";
}

function toggleGameMode(){
    if (! bButtonsEnabled) return;
    poolSelection = (poolSelection == "multiple-pool") ? "single-pool" : "multiple-pool";
    updateTableDisplay();
}

function togglePlayAnim(){
    if (! bButtonsEnabled) return;
    bAnimEnabled = (bAnimEnabled == false) ? true : false;
}

function updateTableDisplay(){
    if (poolSelection == "multiple-pool") {
        tableMulti.style.display = "block";
        tableSingle.style.display = "none";
    }
    else if (poolSelection == "single-pool") {
        tableMulti.style.display = "none";
        tableSingle.style.display = "flex";
    }
}

function toggleCardText(){
    if (! bButtonsEnabled) return;
    bShowCardText = bShowCardText ? false : true;
    let textVisibility = bShowCardText ?  "visible" : "hidden";
    for (cardText of drawnCardTexts) {
        cardText.style.visibility = textVisibility;
    }
}