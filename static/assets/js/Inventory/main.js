(function($) {

	"use strict";
  /* DT Init */
  $('table').DataTable({
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

  let delete_btn = document.querySelector('#inventory-deactivate');

  if(delete_btn){
    delete_btn.addEventListener('click', function(event){
      event.stopPropagation();

      if (!confirm('Deactivate Item?')){ return 0; }
      let form = document.querySelector('#inventory-form')
      form.attributes.action.value = '/inventory/deactivate/';
      form.submit();
    })
  }

})(jQuery);
