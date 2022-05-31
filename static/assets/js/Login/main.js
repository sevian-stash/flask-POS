(function($) {

	"use strict";



  /* Preview Password */
	$(".toggle-password").click(function() {

    console.log(this)
    $(this).toggleClass("fa-eye fa-eye-slash");
    let input = $(this).siblings('#password-field');
    console.log(input)
    if (input.attr("type") == "password") {
      input.attr("type", "text");
    } else {
      input.attr("type", "password");
    }
  });

  /* Fade in Sign Up */
  $("#to-sign-up").click(function() {

    $("#sign-in").fadeOut("slow", function() {
      $("#sign-up").fadeIn("slow");
      $("#sign-up").toggleClass("d-none");
    });
  });

  /* Fade in Sign In */
  $("#to-sign-in").click(function() {

    $("#sign-up").fadeOut("slow", function() {
      $("#sign-in").fadeIn("slow");
      $("#sign-up").toggleClass("d-none");
    });
  });

  /* Init Toggle Tip */
  $('[data-toggle="tooltip"]').tooltip()
})(jQuery);
