$(document).ready(function () {
    link = "/agency/client-search/";
        $.ajax({
            type: 'GET',
            url: link,
            data: {
                term: $("#client_search").val(),
            },
            success: function (response) {

              $('#client_list').html(response)
              }
        });
    link = "/agency/country/";

        $.ajax({
            type: 'GET',
            url: link,
            data: {

            },
            success: function (response) {

              $('#ccountry').html(response)
              }
        });

});
$('#client_search').on('keyup', function (event) {
        link = "/agency/client-search/";
            $.ajax({
                type: 'GET',
                url: link,
                data: {
                    term: $("#client_search").val(),
                },
                success: function (response) {
                   $('#client_list').html(response)
                   }
            });
    });
$('#sort_up').on('click', function (event) {
    console.log('aszdasD')
    link = "/agency/client-search/";
        $.ajax({
            type: 'GET',
            url: link,
            data: {
                term: $("#client_search").val(),
                order:"up",
            },
            success: function (response) {
                 $('#sort_down').removeClass('active-sort')
                $('#sort_up').addClass('active-sort')
                    $('#client_list').html(response)
                       }
        });
});
$('#sort_down').on('click', function (event) {
    console.log('aszdasD')
    link = "/agency/client-search/";
        $.ajax({
            type: 'GET',
            url: link,
            data: {
                term: $("#client_search").val(),
                order:"down",
            },
            success: function (response) {
                $('#sort_down').addClass('active-sort')
                $('#sort_up').removeClass('active-sort')
               $('#client_list').html(response)
               }
        });
});
function validEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};
    $('#add_client_btn').on('click', function (event) {
        console.log('aaaa')

        if ($("#cfirst_name").val().length <= 0) {
            $('#cfirst_error').text('Please enter First Name')
            $('#cdiv_first').addClass('error')
        }
        if ($("#clast_name").val().length <= 0) {
            $('#clast_error').text('Please enter Last Name')
            $('#cdiv_last').addClass('error')
        }
        if ($("#cbusiness_name").val().length <= 0) {
            $('#cbusiness_error').text('Please enter Business Name')
            $('#cdiv_business').addClass('error')
        }
        if ($("#cemail").val().length <= 0) {
            $('#cemail_error').text('Please enter Email')
            $('#cdiv_email').addClass('error')
        }


        if ($("#cfirst_name").val().length > 0 && $("#clast_name").val().length > 0 && $(
                "#cbusiness_name").val().length > 0 &&
            $("#cemail").val().length > 0) {
            $('#loader').removeClass('rw_loader_none')
            link = "/agency/addclient/";
            $.ajax({
                type: 'POST',
                url: link,
                data: {
                    first_name: $("#cfirst_name").val(),
                    last_name: $("#clast_name").val(),
                    business_name: $("#cbusiness_name").val(),
                    email: $("#cemail").val(),
                    time_zone: $("#ctime_zone").val(),
                    country: $("#ccountry").val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (response) {
                    $('#loader').addClass('rw_loader_none')
                    if (response['status'] == 'unsuccess') {
                        $('#cerror').text(response['message'])
                    } else {
                        location.reload()
                    }

                }
            });
        }
    });
    $('#cfirst_name').on('keyup change', function (event) {
        if ($("#cfirst_name").val().length > 0) {
            $("#cfirst_error").text('')
            $('#cdiv_first').removeClass('error')
        }
    });
    $('#clast_name').on('keyup change', function (event) {
        if ($("#clast_name").val().length > 0) {
            $("#clast_error").text('')
            $('#cdiv_last').removeClass('error')
        }
    });
    $('#cbusiness_name').on('keyup change', function (event) {
        if ($("#cbusiness_name").val().length > 0) {
            $("#cbusiness_error").text('')
            $('#cdiv_business').removeClass('error')
        }
    });
    $('#cemail').on('keyup change', function (event) {
        if ($("#cemail").val().length > 0) {
            $("#cemail_error").text('')
            $("#cerror").text('')
            $('#cdiv_email').removeClass('error')
        }
        if (validEmail($("#cemail").val())) {
            $('#cemail_error').text('')
            $('#cdiv_email').removeClass('error')
        } else {
            $('#cemail_error').text('Please enter valid E-mail')
            $('#cdiv_email').addClass('error')

        }
    });
    $('#ctime_zone').on('change', function (event) {
        if ($("#ctime_zone").val().length > 0) {
            $("#ctime_error").text('')
            $('#cdiv_time').removeClass('error')
        }
    });
$(document).ready(function () {

var newE = $("#client_list").html()

$("#client_list").on('click', 'li > a', function(e){
 console.log('asdasdasd')

   $(".agency_offcanvas").addClass("active");

  e.stopPropagation();
});
});

$(document).ready(function () {
  $(".rw_custom_dropdown .select2-selection").on("click", function (e) {
    console.log('asddfasdasdasdasdasdas')
    e.stopPropagation();
    if ($(this).parents(".rw_custom_dropdown").hasClass("rw_inp_focus")) {
      $(this).parents(".rw_custom_dropdown").removeClass("rw_inp_focus");
    } else {
      $(".rw_custom_dropdown.active").removeClass("rw_inp_focus");
      $(this).parents(".rw_custom_dropdown").addClass("rw_inp_focus");
    }
  });
  $(document).on("click", function (e) {
    if ($(e.target).is(".rw_custom_dropdown") === false) {
      $(".rw_custom_dropdown").removeClass("rw_inp_focus");
    }
  });
});


