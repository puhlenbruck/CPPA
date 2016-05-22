function register() {
	var userDetails = {
		username : $('#un').val(),
		password : $('#pw').val(),
		password2 : $('#pwc').val(),
	}

	var errmsg = "<ul>"
	var showmsg = false;
	if (!validateUsername(userDetails.username)) {
		errmsg += "<li>Username must be between 3 and 50 characters, and contain only letters, numbers, hyphen, underscore, period and space</li>"
		$('#un').css('background-color', '#ec7979')
		showmsg = true
	}
	if (!validatePassword(userDetails.password, userDetails.password2)) {
		errmsg += "<li>password must be between 6 and 160 characters long</li>"
		$('#pw').css('background-color', '#ec7979')
		showmsg = true
	}
	if (!comparePassword(userDetails.password, userDetails.password2)) {
		errmsg += "<li>passwords do not match</li>"
		$('#pwc').css('background-color', '#ec7979')
		showmsg = true
	}
	if (showmsg) {
		errmsg += "</ul>"
		$('#error').html(errmsg)
		$('#error').show()
		return
	} else {
		$('#error').hide()
		$('#signup-form').submit()
	}
}

function validateUsername(un) {
	if (/^(?=.{3,50}$)(?![_.-])(?!.*[_.-]{2})[ \.a-zA-Z0-9_-]+([^._-])$/
			.test(un)) {
		$('#un-err').hide()
		$('#un').css('background-color', '#ffffff')
		return true;
	} else {
    $('#un-err').html('Must be at least 3 characters long')
		$('#un-err').show()
		return false;
	}
}

function validatePassword(pw) {
	if (/^.{6,160}$/.test(pw)) {
		$('#pw-err').hide()
		$('#pw').css('background-color', '#ffffff')
		return true;
	} else {
    $('#pw-err').html('Must be at least 6 characters long')
		$('#pw-err').show()
		return false;
	}
}

function comparePassword(p1, p2) {
	if (p1 !== p2) {
    $('#pwc-err').html('Passwords do not match')
		$('#pwc-err').show()
		$('#pwc').css('background-color', '#ffffff')
		return false
	} else {
		$('#pwc-err').hide()
		return true;
	}
}

$(document).ready(function() {
	$('#un').keyup(function() {
		validateUsername($('#un').val())
	})
	$('#pw').keyup(function() {
		validatePassword($('#pw').val())
	})
	$('#pwc').keyup(function() {
		comparePassword($('#pw').val(), $('#pwc').val())
	})
})
