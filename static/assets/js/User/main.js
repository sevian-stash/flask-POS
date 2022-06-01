(function($) {

	"use strict";
  /* DT Init */
  $('#index-table').DataTable({
    columnDefs: [
      { type: 'natural-nohtml', targets:0 }
    ]
  }); 
  /* Row Selection for Search Field */
  $('#index-table tbody').on('click','tr',function () { 
    $('.selected').not(this).removeClass('selected');
    $(this).toggleClass('selected');
    document.querySelector('[name="search_id"]').value = $(this).attr('id');
  });

  let delete_btn = document.querySelector('#user-deactivate');

  if(delete_btn){
    delete_btn.addEventListener('click', function(event){
      event.stopPropagation();

      if (!confirm('Deactivate Account?')){ return 0; }
      let form = document.querySelector('#user-form')
      form.attributes.action.value = '/user/deactivate/';
      form.submit();
    })
  }

  /* Change Password Modal JS */
  /* Tooltip Init */
  $('[data-toggle="tooltip"]').tooltip();

  let change_password_form = document.querySelector('#user-change-password-form');
  let new_password = change_password_form.querySelector('#US_PASSWORD');
  let confirm_password = change_password_form.querySelector('#CFRM_PASSWORD');

  confirm_password.addEventListener('keyup', function(event) {
    if (confirm_password.value === new_password.value && (new_password.value).length >= 8 && (confirm_password.value).length >= 8){
      change_password_form.querySelector('#user-change-password-submit').disabled = false;
    }
    else{
      change_password_form.querySelector('#user-change-password-submit').disabled = true;
    }
  });
})(jQuery);
