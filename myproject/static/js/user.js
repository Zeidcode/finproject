const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');
const userFormErrorEls = document?.querySelectorAll('p.user_form_error')

signUpButton.addEventListener('click', () => {
    if (userFormErrorEls.length > 0) {
        userFormErrorEls.forEach(item => item.remove())}
    container.classList.add('right-panel-active')
});


signInButton.addEventListener('click', () => {
    if (userFormErrorEls.length > 0) {
        userFormErrorEls.forEach(item => item.remove())}
    container.classList.remove('right-panel-active')
});
