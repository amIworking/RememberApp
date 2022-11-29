let target_dict = document.getElementById('target_dict').innerHTML;
res = target_dict.replace(/"/g, '\\\"').replace(/\'/g, '"');
let mydata = JSON.parse(res);
const COUNT = 3;
console.log(mydata);
let test = {}
for (const[key,value] of Object.entries(mydata)){
    test[key] = [0,0];
}
AMOUNT_COUNT = Object.keys(test).length*COUNT;
let random_word;
let correct_flag = document.getElementById('correct_flag');
let secion_count = 0;

const PROGRESS = document.querySelector('progress')

PROGRESS.setAttribute('value', 22);


function swithcing_words(){
    let newData= {};
    let newTest= {};
    for (const[key,value] of Object.entries(mydata)){
    newTest[value] = [0,0];
    newData[value] = key;
    }
    mydata = newData;
    test = newTest;
    console.log(mydata,test);
    randomizer();
}

function randomizer(){
    PROGRESS.setAttribute('value', (secion_count/AMOUNT_COUNT)*100);
    insert_word = document.getElementById('question_word')
    let test_keys = Object.keys(test)
    if (test_keys.length>0){
        let rnd = Math.floor(Math.random()*test_keys.length);
        random_word = test_keys[rnd]
        insert_word.innerHTML = random_word
    }
}

function correcting(){
    secion_count++;
    test[question_word][0]++;
    ans_res.style.color = 'green';
    ans_res.innerHTML = `Right!\nYou answered right. ${1+COUNT-test[question_word][0]} out of ${COUNT} times left`;
    if (test[question_word][0]==COUNT){
        delete test[question_word];
        }
    correct_flag.style.display='none';
    randomizer();
}

function check1(){
    if (Object.keys(test).length<=0) {

        alert('finished');
        let dict_name = document.getElementById('dict_name').innerHTML;
        location.href = `/adding_points/${dict_name}`;
    }
    let answer = document.getElementById('ans').value;
    document.getElementById('ans').value='';
    question_word = document.getElementById('question_word').innerHTML;
    ans_res = document.getElementById('ans_res');
    if (mydata[question_word]==answer){
        correct_flag.style.display='none';
        test[question_word][0]++;
        secion_count++;
        ans_res.style.color = 'green';
        ans_res.innerHTML = `Right!\nYou answered right. ${1+COUNT-test[question_word][0]} out of ${COUNT} times left`;
        if (test[question_word][1]==0){
            delete test[question_word];
            secion_count+=COUNT-1;
            ans_res.innerHTML = `Right!\nYou answered right.`;
            }
        else if (test[question_word][0]==COUNT){
            delete test[question_word];
            }
        }
    else {
        test[question_word][1]++;
        ans_res.style.color = 'red';
        ans_res.innerHTML = `Wrong!\nThe right answer is "${mydata[question_word]}"`;
        correct_flag.style.display='inline';
        }    


    if (Object.keys(test).length<=0) {
        alert('finished');
        let dict_name = document.getElementById('dict_name').innerHTML;
        location.href = `/adding_points/${dict_name}`;
    }
    console.log(test)
    randomizer()
}

function check_answer(){
    let answer = document.getElementById('ans').value;
    question_word = document.getElementById('question_word').innerHTML;
    if (mydata[question_word]==answer){
            test[question_word][0]++;
            secion_count++;
            ans_res.style.color = 'green';
            ans_res.innerHTML = `Right!\nYou answered right. ${1+COUNT-test[question_word][0]} out of 3 times left`;
            if (test[question_word][1]==0){
            delete test[question_word];
            secion_count+=COUNT-1;
            ans_res.innerHTML = `Right!\nYou answered right.`;
            }
            else if (test[question_word][0]==COUNT){
            delete test[question_word];
            }
            document.getElementById('ans').value='';
            console.log(test)
            randomizer();
    }
    if (Object.keys(test).length<=0) {
        alert('finished');
        let dict_name = document.getElementById('dict_name').innerHTML;
        location.href = `/adding_points/${dict_name}`;
    }

}

function enter_cheсk(e){
    if (e.keyCode ===13){
        e.preventDefault();
        check1();

    }
}