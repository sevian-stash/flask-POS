(function($) {

	"use strict";

  $('table').DataTable(); /*DT Init*/
  $('tbody').on('click','tr',function () { /*Row Selection for Search Field*/
    $('.selected').not(this).removeClass('selected');
    $(this).toggleClass('selected');
    document.querySelector('[name="search_id"]').value = $(this).attr('id');
  });
})(jQuery);
