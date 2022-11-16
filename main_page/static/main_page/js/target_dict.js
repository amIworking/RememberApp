let title_width = document.getElementById('test').offsetWidth;
let items = document.querySelectorAll('.dict_item');
items.forEach(element => {
    element.style.width=title_width+'px';
    
});