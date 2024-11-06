const button = document.getElementsByClassName("button")[0];
const table = document.getElementById("table");
const bingo_machine_anim = document.getElementById("bingo-machine");
const bingo_machine_container = document.getElementById("bingo-machine-container");
const big_image_container = document.getElementById("big-image-container");
let button_click_sound = new Audio("../audio/click.wav");
let rolling_sound = new Audio("../audio/rolling-sound.wav")
let clang_sound_01 = new Audio("../audio/clang-01.wav");
let clang_sound_02 = new Audio("../audio/clang-02.wav");
let button_enabled = false;
bingo_ball_machine_filepath = "../image/bingo-ball-machine.gif";


// check for valid BingoMachineImage
let bingoMachineIMGvalid = false;
let test_image = document.createElement("img");
test_image.src = bingo_ball_machine_filepath;
setTimeout(function(){
    button_enabled = true;
    if (test_image.naturalHeight > 0){
        bingoMachineIMGvalid = true;
    }
}, 200);


function activateBingoMachine(){
    if (button_enabled == false) return;
    button_enabled = false;
    button.style.color = "#000000";
    button_click_sound.play();
    let new_card = popRandom(pool);

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
        addCardToTable(new_card);
        hideBigCard();
        button_enabled = true;
        button.style.color = "#ffffff";
    }, bingo_machine_time + 4000);

}

function addCardToTable(card_name){
    let card = document.createElement("div");
    card.className = "table-card";
    let card_image = document.createElement("img");
    card_image.src = pathmap[card_name];

    card.appendChild(card_image);
    table.appendChild(card);
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