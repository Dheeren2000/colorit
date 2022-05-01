// importing the popupModal 
import { popupModal } from './drag_drop.js'


// getting the all btns tag required
const close_btn = document.getElementById('close-password-modal');
const change_btn = document.getElementById('change-pasword-btn');
const clear_btn = document.getElementById('clear-form');

// getting all the input field tags
const old_password = document.getElementById('old-password');
const new_password = document.getElementById('new-password');
const confirm_password = document.getElementById('con-new-password');

// getting all the error tags
const old_error = document.getElementById('old-pass-error');
const new_error = document.getElementById('new-pass-error');
const confirm_error = document.getElementById('con-new-pass-error');

// getting the all show password tags
const show_old_pass = document.getElementById('show-old-password');
const show_new_pass = document.getElementById('show-new-password');

// function to show the password of the selected input
var showPassword = (inputField, icon) => {
    if (inputField.type === "password") {
        inputField.type = "text";
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    } else {
        inputField.type = "password";
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    }
}

// on toggle show password 

show_old_pass.addEventListener('click', (event) => {
    showPassword(old_password, show_old_pass.querySelector('i'));
});

show_new_pass.addEventListener('click', (event) => {
    showPassword(new_password, show_new_pass.querySelector('i'));
});


// function to stop every propagation
function stopEverything(event) {
    event.stopPropagation();
    event.preventDefault();
}


//function to check the input is valid or not 
function isValid(id, regx = new RegExp('^[\s\S]*'), error_id, msg, regmsg) {
    var tagVal = $(id).val();

    if (tagVal == "") {
        $(error_id).html(msg);
        $(error_id).show();

        return false;
    } else if (!regx.test(tagVal)) {

        if (tagVal.length > 20) {
            $(error_id).html("Too Long Password");
        } else {
            $(error_id).html(regmsg);
        }

        $(error_id).show();

        return false;
    } else {
        $(error_id).hide();
        return true;
    }
}

//function to check passwords are matched or not
function isMatched() {
    var pass = $(new_password).val();
    var con_pass = $(confirm_password).val();

    if (pass == con_pass) {
        $(confirm_error).hide();
        return true;
    }
    $(confirm_error).html("Password does not match");
    $(confirm_error).show();
    return false;
}

//function to check wether input is empty or not
function isEmpty(id, error_id, msg) {
    var tagVal = $(id).val();

    if (tagVal == "") {
        $(error_id).html(msg);
        $(error_id).show();

        return false;
    } else if (tagVal === null) {
        $(error_id).html(msg);
        $(error_id).show();

        return false;
    } else {
        $(error_id).hide();
        return true;
    }
}

function form_validation() {

    // Regular expression for validation 
    var pass_rgx = new RegExp("^([A-Za-z0-9_\.@\$!]{8,20})$");

    var old_pass = isEmpty(old_password,
        old_error,
        "*Please, enter your current password");

    var new_pass = isValid(new_password,
        pass_rgx,
        new_error,
        "*Please, enter the new password",
        "*Weak Password");

    var con_new_pass = isEmpty(confirm_password,
        confirm_error,
        "*Please, confirm your new password") && isMatched();


    console.log('res : ', old_pass && new_pass && con_new_pass)
    return (old_pass && new_pass && con_new_pass);
}

$(document).ready(function() {

    $(change_btn).click(function(e) {
        if (form_validation()) {

            var formData = new FormData();
            formData.append('current-password', old_password.value);
            formData.append('new-password', new_password.value);

            fetch('/resetPassword', { method: 'POST', body: formData })
                .then(res => {
                    return res.json();
                }).then(result => {

                    console.log('Results : ', result);

                    if (!result['current-match']) {
                        old_error.innerHTML = "Wrong Password is given.";
                        $(old_error).show();
                    } else {
                        old_error.innerHTML = "";
                        $(old_error).hide();

                        if (result['new-match']) {
                            new_error.innerHTML = "Password is same as your previous password, Please enter new password";
                            $(new_error).show();
                        } else {
                            new_error.innerHTML = "";
                            $(new_error).hide();
                            if (result['success']) {
                                $(close_btn).click();
                                popupModal('Done', 'Your Password has been changed successfully!!!');
                            } else {
                                $(clear_btn).click()
                                $(close_btn).click();
                                popupModal('Error', 'Your Password cannot be changed... ');
                            }
                        }
                    }

                });

        }
    });

    // on click close btn
    $(clear_btn).click(function() {
        $(old_password).val('');
        $(new_password).val('');
        $(confirm_password).val('');

        old_password.type = "password";
        new_password.type = "password";

        show_old_pass.querySelector('i').classList.remove('fa-eye');
        show_old_pass.querySelector('i').classList.add('fa-eye-slash');

        show_new_pass.querySelector('i').classList.remove('fa-eye');
        show_new_pass.querySelector('i').classList.add('fa-eye-slash');

        var errors = document.querySelectorAll('.error-text');
        errors.forEach(e => {
            $(e).hide();
        });
    });

    $(close_btn).click(() => {
        clear_btn.click();
    });
});