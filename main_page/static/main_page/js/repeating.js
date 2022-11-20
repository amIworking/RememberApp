let target_dict = document.getElementById('target_dict').innerHTML;
res = target_dict.replace(/"/g, '\\\"').replace(/\'/g, '"');
const mydata = JSON.parse(res);
console.log(mydata);
let test = {}
for (const[key,value] of Object.entries(mydata)){
    test[key] = 0;
}
let random_word;

function randomizer(){
    insert_word = document.getElementById('question_word')
    let test_keys = Object.keys(test)
    if (test_keys.length>0){
        let rnd = Math.floor(Math.random()*test_keys.length);
        random_word = test_keys[rnd]
        insert_word.innerHTML = random_word
    }
}


function check1(){
    if (Object.keys(test).length>0){
        let answer = document.getElementById('ans').value;
        document.getElementById('ans').value=''
        question_word = document.getElementById('question_word').innerHTML;
        ans_res = document.getElementById('ans_res');
        if (mydata[question_word]==answer){
            test[question_word]++;
            ans_res.style.color = 'green';
            ans_res.innerHTML = `Right!\nYou answered right. ${3-test[question_word]} out of 3 times left`;
            if (test[question_word]==3){
            delete test[question_word];
            } 
        }
        else {
            ans_res.style.color = 'red';
            ans_res.innerHTML = `Wrong!\nThe right answer is "${mydata[question_word]}"`;
    }
    }
    if (Object.keys(test).length<=0) {
        alert('finished');
        let dict_name = document.getElementById('dict_name').innerHTML;
        location.href = `/adding_points/${dict_name}`;
    }
    randomizer()
    console.log(test)
    
}

function enter_cheсk(e){
    if (e.keyCode ===13){
        e.preventDefault();
        check1();

    }
}