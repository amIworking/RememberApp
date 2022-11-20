
function tr_check(id){
    let dicts_check = document.getElementById(id);
    console.log(dicts_check.getElementsByTagName('tr').length)
    if (dicts_check.getElementsByTagName('tr').length<2){
        let table = document.getElementById('followed_table');
        let tag = document.createElement('tr');
        tag.setAttribute('class', 'm_text');
        tag.append('Nothing here');
        tag.style.textAlign='center';
        table.append(tag);
    };
}
