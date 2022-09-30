
function passwordCheck() {
    var password;
    password=prompt('Enter your password:')
    if (password != 'BotsAreCool') {
        window.location.href='/';
    }
}
