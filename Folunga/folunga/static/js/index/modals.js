//All modals!

$(document).ready(function(){
  $('.modal').modal();
})

function forgotPassword() {
  M.Modal.getInstance($('#forgot-password')).open()
}

function registration() {
  M.Modal.getInstance($('#registration')).open()
}