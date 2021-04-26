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

    var form_data = new FormData($('#registration-form')[0]);
    form_data.append('form', "registration");
    
    $.ajax({
        type:'POST',
        url:'/',
        data: form_data,
        processData: false,
        contentType: false
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

$('#recovery-password-form').on('submit', function(e) {
    e.preventDefault();

    $.ajax({
    type:'POST',
    url:'/',
    data:{
        form:"recovery_password",
        email_recovery:$("#email-recovery-password").val()
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
