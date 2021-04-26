$('#new-story-form').on('submit', function(e) {
    e.preventDefault();
    
    $.ajax({
    type:'POST',
    url:'/feed',
    data:{
        form:"new-story-form",
        story_text:$("#story_text").val()
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