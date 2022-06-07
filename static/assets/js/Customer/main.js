(function($) {

	"use strict";
  /* DT Init */
  $('table').DataTable({
    dom: 'Bfrtip',
    buttons: [
      {
            extend: 'print',
            text: '<i class="mdi mdi-file m-0"></i>',
            className:'btn btn-success'
        }
    ],
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

})(jQuery);
