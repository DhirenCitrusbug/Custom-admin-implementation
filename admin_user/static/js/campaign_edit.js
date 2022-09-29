$(document).ready(function () {

    var start_time =  $('#start_time_val').val()
    var end_time =  $('#end_time_val').val()

    if ( start_time.indexOf("a.m.") >= 0){
        $('#start_time').val(start_time.replace(' a.m.','-AM')).change();
    }else if(start_time.indexOf("midnight") >= 0){
        $('#start_time').val(start_time.replace('midnight','12-AM')).change();
    }else if(start_time.indexOf("noon") >= 0){
        $('#start_time').val(start_time.replace('noon','12-PM')).change();
    }
    else{
        $('#start_time').val(start_time.replace(' p.m.','-PM')).change();
    }
    if ( end_time.indexOf("a.m.") >= 0){
        $('#end_time').val(end_time.replace(' a.m.','-AM')).change();
    }else if(end_time.indexOf("midnight") >= 0){
        $('#end_time').val(end_time.replace('midnight','12-AM')).change();
    }else if(end_time.indexOf("noon") >= 0){
        $('#end_time').val(end_time.replace('noon','12-PM')).change();
    }else{
        $('#end_time').val(end_time.replace(' p.m.','-PM')).change();
    }
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



    $("#time_edit").select2({
        dropdownParent: $("#edit_time_delay_popup"),
        placeholder: "Add Tag",
        allowClear: false,
        minimumResultsForSearch: -1,
    });

    $("#tag_action_edit").select2({
        dropdownParent: $(".edit_tag_action"),
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

// $('#campaign_name').on('focusout',function(event){
//     $('#campaign_name').attr('type', 'hidden');
//     $(".main_error").text('')
//     $('#camp_name').text($('#campaign_name').val());
//     $("input[name='campaign_form_name']").val($('#campaign_name').val())
// });

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

$('#time_val').on('keypress', function (event) {
    var regex = new RegExp("^[0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
});
$('#time_val_edit').on('keypress', function (event) {
    var regex = new RegExp("^[0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
        event.preventDefault();
        return false;
    }
});

$('#time_delay_btn').on('click', function(event){
    var valid = true;
    console.log($('#time').val());
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


$("#add_coupon").on("click", function (e) {

        console.log($('#coupon_code').val())

        if ($('#coupon_code').val().length <= 0) {
            e.stopPropagation();
            $(".trigger_overlays").addClass("active");
            $("#ul_coupon").addClass("active");
            $("#ul_tag").removeClass("active");
            $("#ul_referral_camp").removeClass("active");
        } else {
            var message = $('#message').val()
            var coupon = $('#coupon_code').val()
            console.log(message.search(coupon))
            if (message.search(coupon) <= -1) {
                e.stopPropagation();
                $(".trigger_overlays").addClass("active");
                $("#ul_coupon").addClass("active");
                $("#ul_tag").removeClass("active");
                $("#ul_referral_camp").removeClass("active");
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
    $("#ul_referral_camp").removeClass("active");
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
$("#message_edit").on('keyup', function () {
    $("#char_edit").text($("#message_edit").val().length + "/160 characters")
    $("#div_message").removeClass('error')
    $('#message_error').text('')
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






$('#text_edit_save').on('click', function(event){
    var valid = true;
    // console.log($('#message_edit').val());
    if ($('#message_edit').val().trim().length <= 0 ){
        $('#edit_message_error').text('Please enter Message')
//        $("#div_campaign_name").addClass('error')
        valid=false;
    }
    if (valid==true){
        $('#text_message_edit_form').submit()
    }
});

$('#wait_until_edit_save').on('click', function(event){
    var valid = true;
    // console.log($('#hour_edit').val());
    // console.log($('#minute_edit').val());
    if ($('#hour_edit').val() == ""){
        $('#edit_wait_error').text('Please select Hour')
        valid=false;
    }else if ($('#minute_edit').val() == ""){
        $('#edit_wait_error').text('Please select Minute')
        valid=false;
    }
    if (valid==true){
        $('#wait_until_edit_form').submit()
    }
});

$('#time_delay_edit_save').on('click', function(event){
    var valid = true;
    // console.log($('#time_val_edit').val());
    if ($('#time_val_edit').val().length <= 0){
        $('#edit_time_val_error').text('Please enter Time')
        $('#div_time_val_edit').addClass('error')
        valid=false;
    }else{
        if($('#time_edit').val() == 'minute'){
            if ($('#time_val_edit').val() > 59){
                $('#edit_time_val_error').text('Please enter valid minutes')
                $('#div_time_val_edit').addClass('error')
                valid=false;
            }
        }
        if($('#time_edit').val() == 'hours'){
            if ($('#time_val_edit').val() > 23){
                $('#edit_time_val_error').text('Please enter valid hours')
                $('#div_time_val_edit').addClass('error')
                valid=false;
            }
        }
        if($('#time_edit').val() == 'day'){
            if ($('#time_val_edit').val() > 366){
                $('#edit_time_val_error').text('Please enter valid days')
                $('#div_time_val_edit').addClass('error')
                valid=false;
            }
        }
    }
    if (valid==true){
        $('#time_delay_edit_form').submit()
    }
});

$('#tag_action_edit_save').on('click', function(event){
    var valid = true;
    // console.log($('#tag_action_edit').val());
    if ($('#tag_action_edit').val()==""){
        $('#edit_action_error').text('Please add Tags')
        valid=false;
    }
    if (valid==true){
        $('#tag_action_edit_form').submit()
    }
});






$(".edit_cam_action").on("click", function(){
    console.log("AAA")
    var model_id = $(this).attr('model-id');
    console.log(model_id)
    $.ajax({
        type : 'GET',
        url : '/client/campaign-edit-getdata/'+model_id ,
        data : {
            model_id : model_id,
        },
        success: function(response){
            console.log(response)
            console.log(response['data']['id'],'*********************************');
            $("input[name='cam_action_id']").val(response['data']['id'])
            if(response['data']['action']['action_type'] == "text_message"){
                console.log("Text")
                $('#message_edit').val(response['data']['action']['action_value']).change()
                $('#edit_text_popup').modal('show');
                $('#text_delete').attr("href","/client/campaign-action-delete/"+model_id)
            }
            else if(response['data']['action']['action_type'] == "wait_until"){
                console.log("Wait")
                console.log(response['data']['action']['action_value'])
                $('#hour_edit').val(response['data']['action']['action_value']['hour']).change()
                $('#minute_edit').val(response['data']['action']['action_value']['minute']).change()
                $('#time_am_edit').val(response['data']['action']['action_value']['time_am']).change()
                $('#edit_wait_until_popup').modal('show');
                $('#wait_until_delete').attr("href","/client/campaign-action-delete/"+model_id)
            }
            else if(response['data']['action']['action_type'] == "time_delay"){
                console.log("Time")
                console.log(response['data']['action']['action_value'])
                $('#time_edit').val(response['data']['action']['action_value']['time']).change()
                $('#time_val_edit').val(response['data']['action']['action_value']['time_val']).change()
                $('#edit_time_delay_popup').modal('show');
                $('#time_delay_delete').attr("href","/client/campaign-action-delete/"+model_id)
            }
            else if(response['data']['action']['action_type'] == "tag_action"){
                console.log("Tag")
                console.log(response['data']['action']['action_value'])
                var features = response['data']['action']['action_value'].map(function (idx, elem) {
                    return idx['id'];
                });
                console.log(features);
                $('#tag_action_edit').val(features).change()
                $('#edit_tag_action_popup').modal('show');
                $('#tag_action_delete').attr("href","/client/campaign-action-delete/"+model_id)
            }
        }
    });
});


$('#add_trigger').on('click', function(event){
    console.log($('#trigger_div'))
    if ($('#add_trigger_value').val()==''){
        $('#Trigger_modal').modal('show')
//        $('#add_trigger_value').val('true')
    }
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
    console.log($('#before_day').val());
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





$("#edit_add_coupon").on("click", function (e) {
    var message = $('#message_edit').val()
    var match = true;
    $('#edit_ul_coupon > li').each(function(idx, li){
        if (message.search(li['innerText'].trim()) > -1){
            match = false;
            return match;
        }
    });
    console.log(match);
    if (match == false){
        $(".trigger_overlays").removeClass("active");
    }else{
        e.stopPropagation();
        $(".trigger_overlays").addClass("active");
        $("#edit_ul_coupon").addClass("active");
        $("#edit_ul_tag").removeClass("active");
        $("#edit_ul_referral_camp").removeClass("active");
    }
});

$("#edit_add_tag").on("click", function (e) {
    e.stopPropagation();
    $(".trigger_overlays").addClass("active");
    $("#edit_ul_tag").addClass("active");
    $("#edit_ul_coupon").removeClass("active");
    $("#edit_ul_referral_camp").removeClass("active");
});

$('body').on('click','li > .coupon_name', function(){
    console.log('asdasdfasghvdasghv')
    var abc =  $(this).attr('coupon-code')
    console.log(abc)
     $(".trigger_overlays").removeClass("active");
     $("#coupon_code").val(abc);
    $("#message_edit").val($("#message_edit").val()+"{{"+abc)
    $("#message_edit").val($("#message_edit").val()+"}}")
});



$('body').on('click','#edit_click_1', function(){
     $(".trigger_overlays").removeClass("active");
    $("#message_edit").val($("#message_edit").val()+"{{"+$('#edit_click_1').text())
    $("#message_edit").val($("#message_edit").val()+"}}")
});
$('body').on('click','#edit_click_2', function(){
     $(".trigger_overlays").removeClass("active");
    $("#message_edit").val($("#message_edit").val()+"{{"+$('#edit_click_2').text())
    $("#message_edit").val($("#message_edit").val()+"}}")
});
$('body').on('click','#edit_click_3', function(){
     $(".trigger_overlays").removeClass("active");
    $("#message_edit").val($("#message_edit").val()+"{{"+$('#edit_click_3').text())
    $("#message_edit").val($("#message_edit").val()+"}}")
});
$('body').on('click','#edit_click_4', function(){
     $(".trigger_overlays").removeClass("active");
    $("#message_edit").val($("#message_edit").val()+"{{"+$('#edit_click_4').text())
    $("#message_edit").val($("#message_edit").val()+"}}")
});
$('body').on('click', '.edit_click_custom_field', function () {
    var custom_field_id = $(this).attr('custom-field-id')
    console.log(custom_field_id);
    $(".trigger_overlays").removeClass("active");
    $("#message_edit").val($("#message_edit").val() + "{{" + $('#edit_click_custom_field_'+custom_field_id).text())
    $("#message_edit").val($("#message_edit").val() + "}}")
});


$('#start_time').on('change', function(){
    var start_time = $(this).val()
    if ( start_time.indexOf("-AM") >= 0){
        var time = parseInt(start_time.replace('-AM',''));
        $('#end_time').empty()
        for (let index = 1; index <= 12; index++) {
            if( time < index){
                console.log(index);
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
// Referral Campaign
$('body').on('click', '.referral_name', function () {
    var referral_code = $(this).attr('referral-code')
    console.log(referral_code)
    $(".trigger_overlays").removeClass("active");
    $("#referral_code").val(referral_code);
    $("#message").val($("#message").val() + "{{" + referral_code)
    $("#message").val($("#message").val() + "}}")
});
$('body').on('click', '.referral_name', function () {
    var referral_code = $(this).attr('referral-code')
    console.log(referral_code)
    $(".trigger_overlays").removeClass("active");
    $("#edit_referral_code").val(referral_code);
    $("#message_edit").val($("#message_edit").val() + "{{" + referral_code)
    $("#message_edit").val($("#message_edit").val() + "}}")
});

$("#add_referral_camp").on("click", function (e) {
    console.log($('#referral_code').val())
    if ($('#referral_code').val().length <= 0) {
        e.stopPropagation();
        $(".trigger_overlays").addClass("active");
        $("#ul_referral_camp").addClass("active");
        $("#ul_tag").removeClass("active");
        $("#ul_coupon").removeClass("active");
    } else {
        var message = $('#message').val()
        var referral_camp = $('#referral_code').val()
        console.log(message.search(referral_camp))
        if (message.search(referral_camp) <= -1) {
            e.stopPropagation();
            $(".trigger_overlays").addClass("active");
            $("#ul_referral_camp").addClass("active");
            $("#ul_tag").removeClass("active");
            $("#ul_coupon").removeClass("active");
        } else {
            console.log('else condition')
            $(".trigger_overlays").removeClass("active");
        }
    }
});
$("#edit_referral_camp").on("click", function (e) {
    console.log($('#edit_referral_code').val())
    if ($('#edit_referral_code').val().length <= 0) {
        e.stopPropagation();
        $(".trigger_overlays").addClass("active");
        $("#edit_ul_referral_camp").addClass("active");
        $("#edit_ul_coupon").removeClass("active");
        $("#edit_ul_tag").removeClass("active");
    } else {
        var message = $('#message_edit').val()
        var referral_camp = $('#edit_referral_code').val()
        console.log(message.search(referral_camp))
        if (message.search(referral_camp) <= -1) {
            e.stopPropagation();
            $(".trigger_overlays").addClass("active");
            $("#edit_ul_referral_camp").addClass("active");
            $("#edit_ul_coupon").removeClass("active");
            $("#edit_ul_tag").removeClass("active");
        } else {
            console.log('else condition')
            $(".trigger_overlays").removeClass("active");
        }
    }
});