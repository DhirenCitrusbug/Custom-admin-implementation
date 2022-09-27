$(document).ready(function () {
    console.log('avi gayu')
    $("#keyword_phone").select2({
        dropdownParent: $("#keyword_trigger_modal"),
        placeholder: "Select Phone Number",
        allowClear: false,
        minimumResultsForSearch: -1,
    });
    $("#datebased_trigger").select2({
        dropdownParent: $("#date_trigger_modal"),
        placeholder: "Select Date Field",
        allowClear: false,
        minimumResultsForSearch: -1,
    });
    $("#tag_based").select2({
        dropdownParent: $("#select_tag_trigger_modal"),
        placeholder: "Add Tag",
        allowClear: false,
        minimumResultsForSearch: -1,
    });
    $("#time").select2({
        dropdownParent: $("#time_delay_modal"),
        placeholder: "Add Tag",
        allowClear: false,
        minimumResultsForSearch: -1,
    });
    $("#tag_action").select2({
        dropdownParent: $("#select_tag_action_modal"),
        placeholder: "Add Tag",
        allowClear: false,
        minimumResultsForSearch: -1,
    });
    $("#before_days").select2({
        dropdownParent: $("#date_trigger_modal"),
        placeholder: "Select Before Day",
        allowClear: false,
        minimumResultsForSearch: -1,
    });
});
$(".trigg_add_btn").click(function () {
    $(".campaigns_trigger ").each(function(){
            console.log($('.campiagns_plus').length);
    });
  $(".trigger_overlay").addClass("active");
  var matched = $('');
    $('#div_length').val()
});
$(document).on("click", function (e) {
    $(".trigger_overlay").removeClass("active");
});
$('#add_trigger').on('click', function(event){
    console.log($('#trigger_div'))
    if ($('#add_trigger_value').val()==''){
        $('#Trigger_modal').modal('show')
//        $('#add_trigger_value').val('true')
    }
});


$('.close_trigger').on('click', function(event){
    console.log($('#trigger_div'))
    $(this).closest(".trigger_value_div").css("display",'none');
    $('#trigger_div').css("display",'none')
    $('#add_trigger_value').val('')

});
$('.trigger_back').on('click', function(event){

    $(this).closest(".modal").modal("hide");
    $('#Trigger_modal').modal("show");
//    $('body').append("<div class='modal-backdrop fade show'></div>")

});
$('#trigger_next').on('click', function(event){
    console.log($("input[name='radio']:checked").val())
    if ($("input[name='radio']:checked").val()=="0"){
        $('#Trigger_modal').modal("hide")
        $('#keyword_trigger_modal').modal('show');

//        $('body').append("<div class='modal-backdrop fade show'></div>")


    }else if ($("input[name='radio']:checked").val()=="1"){
        $('#Trigger_modal').modal("hide")
        $('#date_trigger_modal').modal("show")
//         $('body').append("<div class='modal-backdrop fade show'></div>")

    }else if ($("input[name='radio']:checked").val()=="2"){
       $('#Trigger_modal').modal("hide")
        $('#select_tag_trigger_modal').modal("show")
//         $('body').append("<div class='modal-backdrop fade show'></div>")
    }
});
$('.text_msg_click').on('click', function(event){
    $('#text_message_modal').modal("show")
    var order = $(this).attr('order-id');
    $("input[name='order']").val(order);
});
$('.time_delay_click').on('click', function(event){
    $('#time_delay_modal').modal("show")
    var order = $(this).attr('order-id');
    $("input[name='order']").val(order);
});
$('.wait_until_click').on('click', function(event){
    $('#wait_until_modal').modal("show")
    var order = $(this).attr('order-id');
    $("input[name='order']").val(order);
});
$('.tag_click').on('click', function(event){
    $('#select_tag_action_modal').modal("show")
    var order = $(this).attr('order-id');
    $("input[name='order']").val(order);
});
$('.action_close').on('click', function(event){
    $(this).closest(".trigger_action").css("display",'none');

});

$('#text_save').on('click', function(event){
    $(".trigger_action").append()
});


$('#edit_name_btn').on('click', function(event){
    $("#edit_name_modal").modal('show');
});
$('#name_btn').on('click', function(event){
    var valid = true;
    if ($('#campaign_name').val().trim().length <= 0 ){
        $('#campaign_name_error').text('Please enter Campaign Name')
        $("#div_campaign_name").addClass('error')
        valid=false;
    }
    if (valid==true){
        $('#name_form').submit()
    }
}); 
$('#text_save').on('click', function(event){
    var valid = true;
    if ($('#message').val().trim().length <= 0 ){
        $('#message_error').text('Please enter Message')
//        $("#div_campaign_name").addClass('error')
        valid=false;
    }
    if (valid==true){
        $('#text_message_form').submit()
    }
});

$('#wait_until_btn').on('click', function(event){
    var valid = true;
    if ($('#hour').val() == ""){
        $('#wait_error').text('Please select Hour')
        valid=false;
    }else if ($('#minute').val() == ""){
        $('#wait_error').text('Please select Minute')
        valid=false;
    }
    if (valid==true){
        $('#wait_until_form').submit()
    }
});

$('#time_val').on('keypress', function (event) {
    var regex = new RegExp("^[0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
});

$('#time_delay_btn').on('click', function(event){
    var valid = true;
    if ($('#time_val').val().length <= 0){
        $('#time_val_error').text('Please enter Time')
        $('#div_time_val').addClass('error')
        valid=false;
    }else{
        if($('#time').val() == 'minute'){
            if ($('#time_val').val() > 59){
                $('#time_val_error').text('Please enter valid minutes')
                $('#div_time_val').addClass('error')
                valid=false;
            }
        }
        if($('#time').val() == 'hours'){
            if ($('#time_val').val() > 23){
                $('#time_val_error').text('Please enter valid hours')
                $('#div_time_val').addClass('error')
                valid=false;
            }
        }
        if($('#time').val() == 'day'){
            if ($('#time_val').val() > 366){
                $('#time_val_error').text('Please enter valid days')
                $('#div_time_val').addClass('error')
                valid=false;
            }
        }
    }
    if (valid==true){
        $('#time_delay_form').submit()
    }
});


$('#keyword_save').on('click', function(event){
    var valid = true;
    if ($('#keyword_phone').val()==""){
        $('#keyword_phone_error').text('Please select Phone Number')
        valid=false;
    }
    if ($('#keyword').val().trim().length <= 0){
        $('#div_keyword').addClass('error')
        $('#keyword_error').text('Please enter Keyword')
        valid=false;
    }
    console.log($('#campaign_name').val())
    if($('#campaign_name').val().trim().length <= 0){
        console.log('asdasdasd')
        $(".main_error").text('Please enter Campaign Name')
    }
    if (valid==true){
//        $("input[name='campaign_form_name']").val($('#campaign_name').val())
        $('#keyword_form').submit()
    }
});

$('#datebased_btn').on('click', function(event){
    var valid = true;
    if ($('#datebased_trigger').val()==""){
        $('#datebased_error').text('Please add Date Fields')
        valid=false;
    }
    console.log($('#datebased_trigger').val())
    if($('#campaign_name').val().trim().length <= 0){
        console.log('asdasdasd')
        $(".main_error").text('Please enter Campaign Name')
    }
    if (valid==true){

        $('#date_based_form').submit()
    }
});
$('#tag_btn').on('click', function(event){
    var valid = true;
    if ($('#tag_based').val()==""){
        $('#datebased_error').text('Please add Tags')
        valid=false;
    }
    console.log($('#datebased_trigger').val())
    if($('#campaign_name').val().trim().length <= 0){
        console.log('asdasdasd')
        $(".main_error").text('Please enter Campaign Name')
    }
    if (valid==true){

        $('#tag_form').submit()
    }
});


$('#tag_action_btn').on('click', function(event){
    var valid = true;
    if ($('#tag_action').val()==""){
        $('#action_error').text('Please add Tags')
        valid=false;
    }
    if (valid==true){

        $('#tag_action_form').submit()
    }
});


//$('#send_check').on('click', function(event){
//    console.log($('#send_check').val(),'11111')
//    console.log($('#send_check:checked').is(':checked'))
//    $('#send_check').val($('#send_check:checked').is(':checked'))
//    console.log($('#send_check').val(),'222222')
//});
$('#double_keyword').on('keyup change', function (event) {
    if ($("#double_keyword").val().length > 0) {
        $("#double_keyword_error").text('')
        $('#div_double_keyword').removeClass('error')
    }
});
$('#double_message').on('keyup change', function (event) {
    if ($("#double_message").val().length > 0) {
        $("#double_message_error").text('')
    }
});
$('#limit_message').on('keyup change', function (event) {
    if ($("#limit_message").val().length > 0) {
        $("#limit_message_error").text('')
    }
});
$('#cancel_tag_based').on('change', function (event) {
    $("#cancel_tag_based_error").text('')
});
$('#cancel_keyword').on('keyup change', function (event) {
    if ($("#cancel_keyword").val().length > 0) {
        $("#cancel_keyword_error").text('')
    }
});
$('#cancel_message').on('keyup change', function (event) {
    if ($("#cancel_message").val().length > 0) {
        $("#cancel_message_error").text('')
    }
});

$('#double_optin').on('click', function(event){

     $("#div_double_keyword").removeClass('error')
     $('#double_keyword_error').text('')
     $('#double_message_error').text('')

});
$('#limit_multiple').on('click', function(event){
    console.log($('#limit_multiple:checked').is(':checked'))
    $('#limit_message_error').text('')
});
$('#cancel_trigger').on('click', function(event){
    console.log($('#cancel_trigger:checked').is(':checked'))
    $('#cancel_trigger_error').text('')
    $('#cancel_tag_based_error').text('')
    $('#cancel_message_error').text('')
    $('#cancel_keyword_error').text('')
    $('#div_cancel_keyword').removeClass('error')
});

$("#save_btn").on('click',function(e) {
    var valid=true;
    if ($('#double_optin:checked').is(':checked')){
        console.log('asdasdasdasasdasdas')
        if($('#double_keyword').val().trim().length <=0 ){
             $("#div_double_keyword").addClass('error')
             $('#double_keyword_error').text('Please enter Keyword')
            valid=false;
        }
        if($('#double_message').val().trim().length <=0 ){
             $("#div_double_message").addClass('error')
             $('#double_message_error').text('Please enter Message')
            valid=false;
        }
    }
    if ($('#limit_multiple:checked').is(':checked')){
         if($('#limit_message').val().trim().length <=0 ){
             $("#div_limit_message").addClass('error')
             $('#limit_message_error').text('Please enter Message')
            valid=false;
        }
    }
    if ($('#cancel_trigger:checked').is(':checked')){
        //   if ($('#on_reply:checked').is(':checked')){
        //        if ($('#cancel_keyword').val().trim().length <=0 ){
        //              $("#div_cancel_keyword").addClass('error')
        //              $('#cancel_keyword_error').text('Please enter Keyword')
        //             valid=false;
        //        }
        //        if ($('#cancel_message').val().trim().length <=0 ){
        //              $("#div_cancel_message").addClass('error')
        //              $('#cancel_message_error').text('Please enter Message')
        //              valid=false;
        //        }
        //   }
        //   if ($('#cancel_tag:checked').is(':checked')){
        //         if ($('#cancel_tag_based').val()==""){
        //              $('#cancel_tag_based_error').text('Please select Tag')
        //              valid=false;
        //         }
        //   }
          if( !$('#on_reply:checked').is(':checked') && !$('#cancel_tag:checked').is(':checked')){
                $('#cancel_trigger_error').text('Please select above condition')
                valid=false;
          }

    }
    if (valid==true){
        $('#setting_form').submit()
    }
});
// ----------------------------------------------
$('#on_reply').on('change', function(){
    $('#cancel_trigger_error').text('')
})
// ----------------------------------------------
$("#add_coupon").on("click", function (e) {

    console.log($('#coupon_code').val())

    if ($('#coupon_code').val().length <= 0) {
        e.stopPropagation();
        $(".trigger_overlays").addClass("active");
        $("#ul_coupon").addClass("active");
        $("#ul_tag").removeClass("active");
    } else {
        var message = $('#message').val()
        var coupon = $('#coupon_code').val()
        console.log(message.search(coupon))
        if (message.search(coupon) <= -1) {
            e.stopPropagation();
            $(".trigger_overlays").addClass("active");
            $("#ul_coupon").addClass("active");
            $("#ul_tag").removeClass("active");
        } else {
            console.log('else condition')
            $(".trigger_overlays").removeClass("active");
        }
    }


});

$("#add_tag").on("click", function (e) {
    e.stopPropagation();
     $(".trigger_overlays").addClass("active");
    $("#ul_tag").addClass("active");
    $("#ul_coupon").removeClass("active");
});
$('body').on('click','li > .coupon_name', function(){
    console.log('asdasdfasghvdasghv')
    var abc =  $(this).attr('coupon-code')
    console.log(abc)
     $(".trigger_overlays").removeClass("active");
     $("#coupon_code").val(abc);
    $("#message").val($("#message").val()+"{{"+abc)
    $("#message").val($("#message").val()+"}}")
});
$('body').on('click','#click_1', function(){
    console.log($('#click_1').text())
     $(".trigger_overlays").removeClass("active");
    $("#message").val($("#message").val()+"{{"+$('#click_1').text())
    $("#message").val($("#message").val()+"}}")
});
$('body').on('click','#click_2', function(){
    console.log($('#click_1').text())
     $(".trigger_overlays").removeClass("active");
    $("#message").val($("#message").val()+"{{"+$('#click_2').text())
    $("#message").val($("#message").val()+"}}")
});
$('body').on('click','#click_3', function(){
    console.log($('#click_1').text())
     $(".trigger_overlays").removeClass("active");
    $("#message").val($("#message").val()+"{{"+$('#click_3').text())
    $("#message").val($("#message").val()+"}}")
});
$('body').on('click','#click_4', function(){
    console.log($('#click_1').text())
     $(".trigger_overlays").removeClass("active");
    $("#message").val($("#message").val()+"{{"+$('#click_4').text())
    $("#message").val($("#message").val()+"}}")
});
$('body').on('click', '.click_custom_field', function () {
    var custom_field_id = $(this).attr('custom-field-id')
    console.log(custom_field_id);
    $(".trigger_overlays").removeClass("active");
    $("#message").val($("#message").val() + "{{" + $('#click_custom_field_'+custom_field_id).text())
    $("#message").val($("#message").val() + "}}")
});

$("#message").on('keyup', function () {
    $("#char").text($("#message").val().length + "/160 characters")
    $("#div_message").removeClass('error')
    $('#message_error').text('')
});


$('#start_time').on('change', function(){
    var start_time = $(this).val()
    console.log(start_time);
    if ( start_time.indexOf("-AM") >= 0){
        var time = parseInt(start_time.replace('-AM',''));
        $('#end_time').empty()
        for (let index = 1; index <= 12; index++) {
            if( time < index){
                $('#end_time').append(`<option value="${index}-AM">${index} AM </option>`)
            }
            $('#end_time').append(`<option value="${index}-PM">${index} PM </option>`)
        }
    }else{
        var time = parseInt(start_time.replace('-PM',''));
        $('#end_time').empty()
        for (let index = 1; index <= 12; index++) {
            if( time < index){
                $('#end_time').append(`<option value="${index}-PM">${index} PM </option>`)
            }
            $('#end_time').append(`<option value="${index}-AM">${index} AM </option>`)
        }
    }
})
$(document).ready(function(){
    $('#message').text('')
    $('#message').text($('#client_business_name').val()+':')
})

//Referral Campaign

$('body').on('click', '.referral_name', function () {
    var referral_code = $(this).attr('referral-code')
    console.log(referral_code)
    $(".trigger_overlays").removeClass("active");
    $("#referral_code").val(referral_code);
    $("#message").val($("#message").val() + "{{" + referral_code)
    $("#message").val($("#message").val() + "}}")
});
$("#add_referral_camp").on("click", function (e) {
    console.log($('#referral_code').val())
    if ($('#referral_code').val().length <= 0) {
        e.stopPropagation();
        $(".trigger_overlays").addClass("active");
        $("#ul_referral_camp").addClass("active");
    } else {
        var message = $('#message').val()
        var referral_camp = $('#referral_code').val()
        console.log(message.search(referral_camp))
        if (message.search(referral_camp) <= -1) {
            e.stopPropagation();
            $(".trigger_overlays").addClass("active");
            $("#ul_referral_camp").addClass("active");
        } else {
            console.log('else condition')
            $(".trigger_overlays").removeClass("active");
        }
    }
});