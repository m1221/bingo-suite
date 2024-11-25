const new_card_button = document.getElementById("new-card-button");
const table_single = document.getElementById("table-single");
const table_multi = document.getElementById("table-multi");
const bingo_machine_anim = document.getElementById("bingo-machine");
const bingo_machine_container = document.getElementById("bingo-machine-container");
const big_image_container = document.getElementById("big-image-container");
let pool_selection = "multiple-pool"; // multi-pool vs single-pool
let button_click_sound = new Audio("../audio/click.wav");
let rolling_sound = new Audio("../audio/rolling-sound.wav")
let clang_sound_01 = new Audio("../audio/clang-01.wav");
let clang_sound_02 = new Audio("../audio/clang-02.wav");
let buttons_enabled = false;
let bingo_ball_machine_filepath = "../image/bingo-ball-machine.gif";


// check for valid BingoMachineImage
let bingoMachineIMGvalid = false;
let test_image = document.createElement("img");
test_image.src = bingo_ball_machine_filepath;
setTimeout(function(){
    buttons_enabled = true;
    if (test_image.naturalHeight > 0){
        bingoMachineIMGvalid = true;
    }
}, 200);


function activateBingoMachine(){
    if (buttons_enabled == false) return;
    buttons_enabled = false;
    new_card_button.style.color = "#000000";
    button_click_sound.play();
    let pool_id = null;
    let new_card;
    if (pool_selection == "multiple-pool")
    {
        pool_id = "BINGO"[Math.floor(Math.random() * 5)];
        let random_pool = pools[pool_id];
        new_card = popRandom(random_pool);
    } else if ( pool_selection == "single-pool"){
        new_card = popRandom(pool);
    }
    

    let bingo_machine_time = 0;
    if (bingoMachineIMGvalid){
        bingo_machine_time = 6000;
        playBingoMachineAnim();
        playBingoMachineAudio();
        setTimeout(function(){ FadeOutBingoMachine(); }, 6000);
        setTimeout(function(){ bingo_machine_anim.src = ""; }, 7000);
        setTimeout(function(){ displayBigCard(new_card)}, bingo_machine_time + 1200);
    }
    else {
        bingo_machine_time = -1500;
        displayBigCard(new_card);
    }
    
    setTimeout(function(){
        addCardToTable(pool_id, new_card);
        hideBigCard();
        buttons_enabled = true;
        new_card_button.style.color = "#ffffff";
    }, bingo_machine_time + 4000);

}

function addCardToTable(pool_id, card_name){
    let card = document.createElement("div");
    card.className = "table-card";
    let card_image = document.createElement("img");
    card_image.src = pathmap[card_name];

    card.appendChild(card_image);
    
    if (pool_selection == "single-pool"){
        table_single.appendChild(card);
    }
    else if (pool_selection == "multiple-pool"){
        document.getElementById(`row-${pool_id}`).appendChild(card);
    }
    
}

/* BingoMachineAnim - BEGIN */
function playBingoMachineAnim() {
    let timestamp = new Date().getTime();
    let queryString = "?t=" + timestamp; // use queryString to avoid cache reload
    //bingo_machine_container
    bingo_machine_container.classList.remove("bingo-machine-fadeOut");
    bingo_machine_container.classList.add("bingo-machine-fadeIn");
    bingo_machine_anim.src = "../image/bingo-ball-machine.gif" + queryString;
}

function FadeOutBingoMachine() {
    bingo_machine_container.classList.remove("bingo-machine-fadeIn");
    bingo_machine_container.classList.add("bingo-machine-fadeOut");
}
/* BingoMachineAnim - END */

function playBingoMachineAudio(){
    setTimeout(function(){ rolling_sound.play(); }, 1000);
    setTimeout(function(){ 
        let sound_to_play = Math.random() > 0.5 ? clang_sound_01 : clang_sound_02;
        sound_to_play.play(); 
    }, 5500);
    
}

function displayBigCard(card_name){
    if (big_image_container.hasChildNodes()){
        big_image_container.removeChild(big_image_container.firstChild);
    }
    
    big_image_container.style.visibility = "visible";
    let big_card_image = document.createElement("img");
    big_card_image.src = pathmap[card_name];

    big_image_container.appendChild(big_card_image);
}

function hideBigCard(){
    big_image_container.style.visibility = "hidden";
}

function toggleGameMode(){
    if (! buttons_enabled) return;
    pool_selection = (pool_selection == "multiple-pool") ? "single-pool" : "multiple-pool";
    updateTableDisplay();
}

function updateTableDisplay(){
    // TODO: is using 'visible/hidden' the best way?
    // what about ... using position?
    if (pool_selection == "multiple-pool") {
        table_multi.style.display = "block";
        table_single.style.display = "none";
    }
    else if (pool_selection == "single-pool") {
        table_multi.style.display = "none";
        table_single.style.display = "flex";
    }
}