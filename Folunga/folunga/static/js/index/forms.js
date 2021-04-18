$('#login-form').on('submit', function(e) {
    e.preventDefault();
    
    $.ajax({
    type:'POST',
    url:'/',
    data:{
        form:"login",
        username:$("#username").val(),
        password:$("#password").val()
    }
    })
    .done(function(data) {
    if (data.error) {
        M.toast({html: data.error, classes: 'rounded'})
    } else {
        M.toast({html: data.success, classes: 'rounded'})
        setTimeout(function () { location.reload(true); }, 1200);
    }
    });
});

$('#registration-form').on('submit', function(e) {
    e.preventDefault();
    
    $.ajax({
    type:'POST',
    url:'/',
    data:{
        form:"registration",
        first_name:$("#first_name").val(),
        last_name:$("#last_name").val(),
        date_birth:$("#date_birth").val(),
        username:$("#username_registration").val(),
        email:$("#email_registration").val(),
        password:$("#password_registration").val(),
        password2:$("#password2_registration").val()
    }
    })
    .done(function(data) {
    if (data.error) {
        M.toast({html: data.error, classes: 'rounded'})
    } else {
        M.toast({html: data.success, classes: 'rounded'})
        setTimeout(function () { location.reload(true); }, 1500);
    }
    });
});