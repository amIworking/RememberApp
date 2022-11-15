let cookies = document.cookie;
cookies_keys = Object.keys(cookies);
const check = ('username', 'email');


if (cookies.includes('username') && cookies.includes('email')){
    document.getElementById('nav1').remove()
}
else{document.getElementById('nav2').remove()}
