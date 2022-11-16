let minutes = document.getElementById("minutes");
let seconds = document.getElementById("seconds");
let speed = document.getElementById('speed');
let speed_text = document.getElementById('speed_text');
let totalSeconds = 0;
let timer;
function print(){
    let input = document.getElementById('textarea');
    if (input.value.length==1){
        clearInterval(timer);
        speed_text.style.visibility='visible';
        timer = setInterval(setTime, 1000); 
    }
    let text = document.getElementById('mainText').innerHTML;
    let text_list = Array.from(text)
    console.log(input.value, text, text_list.slice(0, input.value.length).join())
    if (input.value != text.slice(0, input.value.length)){
        input.style.color='red';
     }
     
    else if(input.value = text.slice(0, input.value.length)){
        input.style.color='green';
     }
     if(input.value==text){
        clearInterval(timer);
        alert(`You finished for ${minutes.innerHTML} minutes, ${seconds.innerHTML} seconds, Your speed is ${speed.innerHTML} letters in a minute`);
    }

}
function stop(){
    minutes.innerHTML,seconds.innerHTML='00'
    document.getElementById('textarea').value = ''
    clearInterval(timer)
}

function setTime() {
  ++totalSeconds;
  letters = document.getElementById('textarea').value.length;
  seconds.innerHTML = pad(totalSeconds % 60);
  minutes.innerHTML = pad(parseInt(totalSeconds / 60));
  input = document.getElementById('textarea');
  console.log(seconds);
  if (input.style.color == 'green'){
    speed.innerHTML = ((letters/totalSeconds)*60).toFixed(2);
  }

}

function pad(val) {
  let valString = val + "";
  if (valString.length < 2) {
    return "0" + valString;
  } else {
    return valString;
  }
}