slug_list = []
id_list = []
$(".category-item").click(function () {
    $(this).toggleClass("active_category");
    if ($(this).hasClass("active_category") === true) {
        slug_list.push($(this).data('slug'))
        id_list.push(parseInt($(this).data('id')))
        category_data_result(id_list)
    } else {
        slug_list = slug_list.filter(slug_list => slug_list !== $(this).data('slug'))
        id_list = id_list.filter(id_list => id_list !== parseInt($(this).data('id')))
        category_data_result(id_list)
    }
    if($('.active_category').length == 0){
        $('#total_result').prop("disabled", true);
    }else{
        $('#total_result').removeAttr("disabled");
    }
})

function category_data_result(category_id) {
    $.ajax({
        url: '/category-count-ajax/',
        method: 'GET',
        data: { 'category_id': category_id },
        success: function (data) {
            if (data['data'] == 0) {
                $("#total_result").text('See ' + $("#total_result").data('value') + ' Results')
            } else {
                $("#total_result").text('See ' + `${data['data']}` + ' Results')
            }
        }
    })
}

$('#total_result').on('click', function () {
    $.removeCookie("remove_category_id", { path: '/' });
    if ($('.active_category').length == 1) {
        window.location.href = `/category/${slug_list}`
    } else {
        window.location.href = `/search/?categories=${btoa(id_list)}`
    }
})

$('.ctegory-list-item a').on('click', function(){
    $.removeCookie("remove_category_id", { path: '/' });
})

$('#show-more-desc').on('click', function () {
    $('.desc_p').innerHTML = ""
    $('.desc_p').html(`${$('.desc_p').data('disc')}`)
})

$("#search-review-data").on('keyup', function () {
    $.ajax({
        url: '/search_filter/',
        method: 'GET',
        data: { "search_input": $(this).val() },
        async: false,
        success: function (data) {
            var li_counter = document.querySelector(".suggestions");
            li_counter.innerHTML = ""
            if (data['search'] != "") {

                for (let datas in data['data']['data_brand_name']) {
                    var new_li = document.createElement('li');
                    new_li.innerHTML = `Brand : <span class='name'> <a href="/brand/${data['data']['data_brand_name'][datas][1]}" class="text-center"> ${data['data']['data_brand_name'][datas][0]} </a> </span>`
                    li_counter.appendChild(new_li);
                }

                if (data['data']['data_brand_name'].length != 0 || data['data']['data_model_name'].length != 0){
                    var new_li = document.createElement('li');
                    new_li.innerHTML = "<hr style='margin:0; padding: 0px 26px; flex: 0 0 80%;'>";
                    li_counter.appendChild(new_li);
                }else {
                    var new_li = document.createElement('li');
                    new_li.innerHTML = "<span class='name'> No Data Founded </span>";
                    li_counter.appendChild(new_li);
                }

                for (let datas in data['data']['data_model_name']) {
                    var new_li = document.createElement('li');
                    new_li.innerHTML = "Model : " + `<span class='name'> <a href="/${data['data']['data_model_name'][datas][2]}/${data['data']['data_model_name'][datas][1]}" class="text-center"> ${data['data']['data_model_name'][datas][0]} </a> </span>`;
                    li_counter.appendChild(new_li);
                }
            }
        }
    })

    var count1 = $(".suggestions li").length;

    if (count1 > 0) {
        $(".filter-data").addClass("addlayer");
    }
    else {
        $(".filter-data").removeClass("addlayer");
    }
});

$(".cookie_close_btn").on("click", function () {
    $(".cookie_wrapper").addClass("d-none");
    $(".footer_wrapper").removeClass("cookie_pad");
});

$('.dropdown-toggle').on('click', function (event) {
    if (!$(event.target).hasClass('suggestions')) {
        $(".filter-data").removeClass("addlayer");
    }
});

$('.header-bottom-drops').on('click', function (e) {
    e.stopPropagation();
});

$(document).ready(function () {
    $.ajax({
        url: '/price-range/',
        method: 'GET',
        success: function (data) {
            var min_price = 0
            var max_price = parseInt(data['max_price'])
            price_range(min_price, max_price)
        }
    })
})

function price_range(min_price, max_price) {
    $(".price-range").on('keyup change', function () {
        var see_result = $("#price-result")[0];
        var show_total_reviews = see_result.innerHTML;
        if ($(this).hasClass('min')) {
            min_price = $(this).val()
            if (parseInt(min_price) >= parseInt(max_price)) {
                $("#error_max_price").html('')
                $("#error_min_price").html('Min Price must be lower.')
            } else if (parseInt(min_price) < parseInt(max_price)) {
                $("#error_min_price").html('')
                $("#error_max_price").html('')
            } else if (min_price == "" || max_price == "") {
                $("#error_min_price").html('')
                $("#error_max_price").html('')
            }
        }
        else if ($(this).hasClass('max')) {
            max_price = $(this).val()
            if (parseInt(min_price) >= parseInt(max_price)) {
                $("#error_min_price").html('')
                $("#error_max_price").html('Max Price must be higher.')
            } else if (parseInt(min_price) < parseInt(max_price)) {
                $("#error_max_price").html('')
                $("#error_min_price").html('')
            } else if (min_price == "" || max_price == "") {
                $("#error_max_price").html('')
                $("#error_min_price").html('')
            }
        }

        $.ajax({
            url: '/price-range/',
            method: 'GET',
            data: { 'min_price': min_price, 'max_price': max_price },
            success: function (data) {
                if (data['total_review'] == 0 & (min_price == "" || max_price == "")) {
                    see_result.innerHTML = show_total_reviews
                }
                else {
                    see_result.innerHTML = `See ${data['total_review']} Results`
                }
            }
        })
    })
}

var advance_search_url;
var advance_search_review_responce;
function more_filter_ajax(min_year, max_year, min_weight, max_weight, min_battery, max_battery, min_suspension_travel, max_suspension_travel,
    keywords, motor_type, bike_class,
    suspension, accessories_fenders,
    accessories_lights, accessories_racks) {

    var data_responce = {
        "min_year": min_year,
        "max_year": max_year,
        "min_weight": min_weight,
        "max_weight": max_weight,
        "motor_type": motor_type,
        "min_battery": min_battery,
        "max_battery": max_battery,
        "bike_class": bike_class,
        "suspension": suspension,
        "min_suspension_travel": min_suspension_travel,
        "max_suspension_travel": max_suspension_travel,
        "accessories_fenders": accessories_fenders,
        "accessories_lights": accessories_lights,
        "accessories_racks": accessories_racks,
        "keywords": keywords,
    }
    $.ajax({
        url: '/more-filter/',
        method: 'GET',
        data: data_responce,
        async:false,
        success: function (data) {
            advance_search_url = this.url.replace('/more-filter/', '/search/')
            advance_search_review_responce = data
            var see_result = $('#more-filter-see-result')[0]
            see_result.innerHTML = `See ${data['total_reviews'].length} Results`
            if(advance_search_url != '/search/'){
                $('#more-filter-see-result').removeAttr("disabled");
            } else{
                $('#more-filter-see-result').prop("disabled", true);
            }
        },
    })
}

$("#more-filter-see-result").on("click", function(){
    window.location.href = `${advance_search_url}`
    // window.location.href = `${advance_search_url}&reviews=${btoa(advance_search_review_responce['total_reviews'])}`
})

function more_filter_inputs() {
    var min_year;
    var max_year;
    var min_weight;
    var max_weight;
    var motor_type = [];
    var bike_class = []
    var suspension = []
    var min_battery;
    var max_battery;
    var min_suspension_travel;
    var max_suspension_travel;
    var accessories_fenders;
    var accessories_lights;
    var accessories_racks;
    var keywords;
    $('.year-range').on('change', function () {
        if ($(this).hasClass('min')) {
            min_year = $(this).val()
            if (parseInt(min_year) > parseInt(max_year)) {
                $("#error_max_year").html('')
                $("#error_min_year").html('Min Year must be lower.')
            } else if (parseInt(min_year) <= parseInt(max_year)) {
                $("#error_min_year").html('')
                $("#error_max_year").html('')
            } else if (min_year == "" || max_year == "") {
                $("#error_min_year").html('')
                $("#error_max_year").html('')
            }
            // if (min_year == ""){
            //     min_year = []
            // }
        }
        if ($(this).hasClass('max')) {
            max_year = $(this).val()
            if (parseInt(min_year) > parseInt(max_year)) {
                $("#error_min_year").html('')
                $("#error_max_year").html('Max Year must be higher.')
            } else if (parseInt(min_year) <= parseInt(max_year)) {
                $("#error_max_year").html('')
                $("#error_min_year").html('')
            } else if (min_year == "" || max_year == "") {
                $("#error_max_year").html('')
                $("#error_min_year").html('')
            }
            // if (max_year = ""){
            //     max_year = []
            // }
        }

        more_filter_ajax(min_year, max_year, min_weight, max_weight, min_battery, max_battery, min_suspension_travel, max_suspension_travel,
            keywords, motor_type, bike_class,
            suspension, accessories_fenders,
            accessories_lights, accessories_racks)
    })

    $('.weight-range').on('keyup change', function () {
        if ($(this).hasClass('min')) {
            min_weight = $(this).val()
            if (parseInt(min_weight) >= parseInt(max_weight)) {
                $("#error_max_weight").html('')
                $("#error_min_weight").html('Min Weight must be lower.')
            } else if (parseInt(min_weight) < parseInt(max_weight)) {
                $("#error_max_weight").html('')
                $("#error_min_weight").html('')
            } else if (min_weight == "" || max_weight == "") {
                $("#error_max_weight").html('')
                $("#error_min_weight").html('')
            }
            if (min_weight == ""){
                min_weight = []
            }
        }
        if ($(this).hasClass('max')) {
            max_weight = $(this).val()
            if (parseInt(min_weight) >= parseInt(max_weight)) {
                $("#error_min_weight").html('')
                $("#error_max_weight").html('Max Weight must be higher.')
            } else if (parseInt(min_weight) < parseInt(max_weight)) {
                $("#error_min_weight").html('')
                $("#error_max_weight").html('')
            } else if (min_weight == "" || max_weight == "") {
                $("#error_min_weight").html('')
                $("#error_max_weight").html('')
            }
            if (max_weight == ""){
                max_weight = []
            }
        }

        more_filter_ajax(min_year, max_year, min_weight, max_weight, min_battery, max_battery, min_suspension_travel, max_suspension_travel,
            keywords, motor_type, bike_class,
            suspension, accessories_fenders,
            accessories_lights, accessories_racks)
    })

    $('.battery-capacity').on('keyup change', function () {
        if ($(this).hasClass('min')) {
            min_battery = $(this).val()
            if (parseInt(min_battery) >= parseInt(max_battery)) {
                $("#error_max_battery_capacity").html('')
                $("#error_min_battery_capacity").html('Min Capacity must be lower.')
            } else if (parseInt(min_battery) < parseInt(max_battery)) {
                $("#error_max_battery_capacity").html('')
                $("#error_min_battery_capacity").html('')
            } else if (min_battery == "" || max_battery == "") {
                $("#error_max_battery_capacity").html('')
                $("#error_min_battery_capacity").html('')
            }
            if (min_battery == ""){
                min_battery = []
            }
        }
        if ($(this).hasClass('max')) {
            max_battery = $(this).val()
            if (parseInt(min_battery) >= parseInt(max_battery)) {
                $("#error_min_battery_capacity").html('')
                $("#error_max_battery_capacity").html('Max Capacity must be higher.')
            } else if (parseInt(min_battery) < parseInt(max_battery)) {
                $("#error_min_battery_capacity").html('')
                $("#error_max_battery_capacity").html('')
            } else if (min_battery == "" || max_battery == "") {
                $("#error_min_battery_capacity").html('')
                $("#error_max_battery_capacity").html('')
            }
            if (max_battery == ""){
                max_battery = []
            }
        }
        more_filter_ajax(min_year, max_year, min_weight, max_weight, min_battery, max_battery, min_suspension_travel, max_suspension_travel,
            keywords, motor_type, bike_class,
            suspension, accessories_fenders,
            accessories_lights, accessories_racks)
    })

    $('.suspension-travel').on('keyup change', function () {
        if ($(this).hasClass('min')) {
            min_suspension_travel = $(this).val()
            if (parseInt(min_suspension_travel) >= parseInt(max_suspension_travel)) {
                $("#error_max_suspension_travel").html('')
                $("#error_min_suspension_travel").html('Min Suspension Travel must  be lower.')
            } else if (parseInt(min_suspension_travel) < parseInt(max_suspension_travel)) {
                $("#error_max_suspension_travel").html('')
                $("#error_min_suspension_travel").html('')
            } else if (min_suspension_travel == "" || max_suspension_travel == "") {
                $("#error_max_suspension_travel").html('')
                $("#error_min_suspension_travel").html('')
            } 
            if (min_suspension_travel == ""){
                min_suspension_travel = []
            }
        }
        if ($(this).hasClass('max')) {
            max_suspension_travel = $(this).val()
            if (parseInt(min_suspension_travel) >= parseInt(max_suspension_travel)) {
                $("#error_min_suspension_travel").html('')
                $("#error_max_suspension_travel").html('Max Suspension Travel must be higher.')
            } else if (parseInt(min_suspension_travel) < parseInt(max_suspension_travel)) {
                $("#error_min_suspension_travel").html('')
                $("#error_max_suspension_travel").html('')
            } else if (min_suspension_travel == "" || max_suspension_travel == "") {
                $("#error_min_suspension_travel").html('')
                $("#error_max_suspension_travel").html('')
            } 
            if (max_suspension_travel == ""){
                max_suspension_travel = []
            }
        }
        more_filter_ajax(min_year, max_year, min_weight, max_weight, min_battery, max_battery, min_suspension_travel, max_suspension_travel,
            keywords, motor_type, bike_class,
            suspension, accessories_fenders,
            accessories_lights, accessories_racks)
    })

    $('.keyword-search').on('keyup change', function () {
        keywords = $(this).val()
        if(keywords == ""){
            keywords = []
        }
        more_filter_ajax(min_year, max_year, min_weight, max_weight, min_battery, max_battery, min_suspension_travel, max_suspension_travel,
            keywords, motor_type, bike_class,
            suspension, accessories_fenders,
            accessories_lights, accessories_racks)
    })

    $('.more-filter').on('change', function () {
        motor_type = [];
        suspension = [];
        bike_class = [];
        if ($('#hub-motor').is(':checked')) {
            motor_type_hub_motor = $('#hub-motor').val();
            motor_type.push(motor_type_hub_motor)
        }

        if ($('#mid-drive-motor').is(':checked')) {
            motor_type_mid_drive_motor = $('#mid-drive-motor').val();
            motor_type.push(motor_type_mid_drive_motor)

        }

        if ($('#bike-class-1').is(':checked')) {
            class_1 = $('#bike-class-1').val()
            bike_class.push(class_1)
        }

        if ($('#bike-class-2').is(':checked')) {
            class_2 = $('#bike-class-2').val()
            bike_class.push(class_2)
        }

        if ($('#bike-class-3').is(':checked')) {
            class_3 = $('#bike-class-3').val()
            bike_class.push(class_3)
        }

        if ($('#bike-class-other').is(':checked')) {
            class_other = $('#bike-class-other').val()
            bike_class.push(class_other)
        }

        if ($('#suspension-none').is(':checked')) {
            suspension_rigid = $('#suspension-none').val()
            suspension.push(suspension_rigid)
        }

        if ($('#suspension-front').is(':checked')) {
            suspension_hardtail = $('#suspension-front').val()
            suspension.push(suspension_hardtail)
        }

        if ($('#suspension-rear').is(':checked')) {
            suspension_softail = $('#suspension-rear').val()
            suspension.push(suspension_softail)
        }

        if ($('#suspension-full').is(':checked')) {
            suspension_full_suspension = $('#suspension-full').val()
            suspension.push(suspension_full_suspension)
        }

        if ($('#accessories-fenders').is(':checked')) {
            accessories_fenders = $('#accessories-fenders').val()
        } else {
            accessories_fenders = []
        }

        if ($('#accessories-lights').is(':checked')) {
            accessories_lights = $('#accessories-lights').val()
        } else {
            accessories_lights = []
        }

        if ($('#accessories-racks').is(':checked')) {
            accessories_racks = $('#accessories-racks').val()
        } else {
            accessories_racks = []
        }

        more_filter_ajax(min_year, max_year, min_weight, max_weight, min_battery, max_battery, min_suspension_travel, max_suspension_travel,
            keywords, motor_type, bike_class,
            suspension, accessories_fenders,
            accessories_lights, accessories_racks)
    })
}

more_filter_inputs()

total_compare_count = []
$(".compare-btn").on('click', function () {
    var get_cookies = $.cookie("id")
    compate_count = parseInt($('.count-icon').html())
    if (get_cookies == undefined || get_cookies == ""){
        if ($(this).hasClass('added') === true) {
            compate_count -= 1
            total_compare_count = total_compare_count.filter(total_compare_count => total_compare_count !== $(this).data('id'))
        } else {
            compate_count += 1
            total_compare_count.push($(this).data('id'))
        }
        $.cookie("id", total_compare_count, { path: '/' });
        $('.count-icon').html(compate_count)
    }
    else if(get_cookies){
        var new_cookies = $.map(get_cookies.split(","), function(val){return parseInt(val);})
        if ($(this).hasClass('added') === true) {
            compate_count -= 1
            new_cookies = new_cookies.filter(new_cookies => new_cookies !== $(this).data('id'))
        } else {
            compate_count += 1
            new_cookies.push($(this).data('id'))
        }
        $.cookie("id", new_cookies, { path: '/' });
        $('.count-icon').html(compate_count)
    }
})

var category_id_list = []
$(".remove-category-cross").on('click', function(){
    var get_removed_cookies = $.cookie("remove_category_id");
    if (get_removed_cookies == undefined || get_removed_cookies == ""){
        category_id_list.push(parseInt($(this).data("id")))
        $.cookie("remove_category_id", category_id_list, { path: '/' });
    }
    else if(get_removed_cookies){
        var new_cookies = $.map(get_removed_cookies.split(","), function(val){return parseInt(val);})
        new_cookies.push($(this).data('id'))
        $.cookie("remove_category_id", new_cookies, { path: '/' });
    }
})

$(document).on('click', ".reply_comment", function(){
    $('#parent_id').attr('value', $(this).data('parentid'))
    $("#cancel_reply").removeClass('d-none')
    $("#cancel_reply").html("<h3>Cancel Reply</h3>")
})

$("#cancel_reply").on('click', function(){
    $('#parent_id').attr('value', "")
    $("#cancel_reply").addClass('d-none')
})

var display_show_more_button;
$(document).on('click', ".upvote", function(){
    var comment_formating = $("#comment_formation").val()
    var upvote_comment = $(this).data('id')
    var id_class = $(this).data("id")
    var live_url = window.location.pathname
    $(`.${id_class}`).toggleClass("text-primary");
    var all_comments;

    if($("#show_more_comments").html() != "Less comments"){
        display_show_more_button = $("#show_more_comments").html()
    }

    if($("#show_more_comments").hasClass('all_comments') === true){
        $("#show_more_comments").html("Less comments")
        $(".replied_comments").empty()
        all_comments = 'True'
    } else {
        $("#show_more_comments").html(`${display_show_more_button}`)
        $(".replied_comments").empty()
        all_comments = 'False'
    }

    if($(this).hasClass("text-primary") === true){
        is_upvoted = true
    }else{
        is_upvoted = false
    }

    var data = {
        'upvote_comment':upvote_comment,
        'is_upvoted':is_upvoted,
        'url': live_url,
        'ip': GetUserIP(),
        'comment_formating':comment_formating,
        'all_comments' : all_comments,
    }
    $(".replied_comments").empty()
    display_comments(data)
})

function GetUserIP(){
  var ret_ip;
  $.ajaxSetup({async: false});
  $.get('https://api.ipify.org/?format=json', function(r){
    ret_ip = r.ip;
  });
  return ret_ip;
}

var is_notification_checked = true;
$("#add_comment_form").submit(function(event){
    event.preventDefault();
    // $("#user_ip").val(GetUserIP())
    $("#post_commnet").prop("disabled", true);

    var name = $("#add_comment_name").val()
    var email = $("#add_comment_name").val()
    var description = $("#description").val()
    var comment_type_id = $("#comment_type_id").val()
    var user_ip = $("#user_ip").val()
    var parent_id = $("#parent_id").val()
    var is_notification = $("#is_notification").val()
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val()

    console.log(description, '=====================');

    var data = {
        'csrf_token':csrf_token,
        'name': name,
        'email':email,
        'description':description,
        'comment_type_id':comment_type_id,
        'user_ip':user_ip,
        'parent_id':parent_id,
        'is_notification':is_notification,
        'user_ip':GetUserIP(),
    }

    $.ajax({
        url:'/add-new-comment/',
        method:'POST',
        data:data,
        success: function(data){
            $("#comment-submited").html("Comment Submited.");
            $("#add_comment_form")[0].reset();
            $('#parent_id').removeAttr('value')
            $("#add_comment_email").attr("placeholder", "Email");
            $("#add_comment_form").hide();
            $("#cancel_reply").addClass('d-none')
            is_notification_checked = true;
            // $("#parent_id").val("")
            $("#add_comment_email").attr('required',false);
            setTimeout(function(){
                $("#comment-submited").html("")
                $("#post_commnet").prop("disabled", false);
                $("#add_comment_form").show()
            }, 5000);
        }
    })
    return false;
})


$("#add_comment_email").on("keyup", function(){
    var EmailRegex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(is_notification_checked == true){
        $("#is_notification").prop('checked', true);
    }

    if($("#is_notification").prop("checked") == true && $(this).val() == ""){
        $(this).css("border-color", "red");
        $(this).attr("placeholder", "Email is Requeired now.");
        $(this).attr('required',true);
    } else if($("#is_notification").prop("checked") == false && $(this).val() == ""){
        $(this).css("border-color", "");
    } else if($("#is_notification").prop("checked") == true && EmailRegex.test($(this).val()) === true){
        $(this).css("border-color", "");
    } else if($("#is_notification").prop("checked") == true && EmailRegex.test($(this).val()) === false){
        $(this).css("border-color", "red");
        $(this).attr("placeholder", "Email is Requeired now.");
        $(this).attr('required',true);
    } else if($("#is_notification").prop("checked") == false && EmailRegex.test($(this).val()) === true){
        $(this).css("border-color", "");
    } else if($("#is_notification").prop("checked") == false && EmailRegex.test($(this).val()) === false){
        $(this).css("border-color", "red");
    }
    is_notification_checked = false;
})

$("#is_notification").on("click", function(){
    var EmailRegex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(!$(this).is(":checked")){
        $("#is_notification").val("False")
        $("#add_comment_email").css("border-color", "");
        $("#add_comment_email").attr('required',false);
        $("#add_comment_email").attr("placeholder", "Email");
    } else if ($(this).is(":checked")){
        $("#is_notification").val("True")
        $("#add_comment_email").attr('required',true);
        if(EmailRegex.test($("#add_comment_email").val()) === false){
            $("#add_comment_email").css("border-color", "red");
            $("#add_comment_email").attr("placeholder", "Email is Requeired now.");
        }
    }
})

function display_comments(data){
    $.ajax({
        url:'/display-comments/',
        method:"GET",
        data: data,
        success:function(data){
            $("#comment_container").append(data)
        }
    })
}

$(document).ready(function(){
    var live_url = window.location.pathname
    var data = {
        'url': live_url,
        'ip': GetUserIP(),
    }
    display_comments(data)
})


$("#show_more_comments").on("click", function(){
    $(this).toggleClass('all_comments')
    var comment_formating = $("#comment_formation").val()
    if($("#show_more_comments").html() != "Less comments"){
        display_show_more_button = $("#show_more_comments").html()
    }
    // console.log(this_html, '========');
    var all_comments;

    if($(this).hasClass('all_comments') === true){
        $("#show_more_comments").html("Less comments")
        $(".replied_comments").empty()
        all_comments = 'True'
    } else {
        $("#show_more_comments").html(`${display_show_more_button}`)
        $(".replied_comments").empty()
        all_comments = 'False'
    }

    var live_url = window.location.pathname
    var data = {
        'ip':GetUserIP(),
        'url':live_url,
        'all_comments' : all_comments,
        'comment_formating':comment_formating,
    }

    display_comments(data)
})


$(document).on('click', '.sub_comments', function(){
    var parent_comment_id = $(this).data("parent")
    var is_sub_comment = $(this).data("issubcomment")

    var data = {
        'ip':GetUserIP(),
        'parent_comment_id':parent_comment_id,
        'is_sub_comment': is_sub_comment
    }

    $(this).hide()

    $.ajax({
        url:'/display-sub-comments/',
        method:'GET',
        data:data,
        success:function(data){
            if(is_sub_comment == 'True'){
                $(`.${parent_comment_id}_container`).append(data)
            } else{
                $(`.${parent_comment_id}_replied_comments`).append(data)
            }
        }
    })
})


$("#comment_formation").on("change", function(){
    var comment_formating = $(this).val()
    var all_comments;

    if($("#show_more_comments").html() != "Less comments"){
        display_show_more_button = $("#show_more_comments").html()
    }

    if($("#show_more_comments").hasClass('all_comments') === true){
        $("#show_more_comments").html("Less comments")
        $(".replied_comments").empty()
        all_comments = 'True'
    } else {
        $("#show_more_comments").html(`${display_show_more_button}`)
        $(".replied_comments").empty()
        all_comments = 'False'
    }

    var data = {
        'url':live_url,
        'all_comments' : all_comments,
        'comment_formating':comment_formating,
        'ip':GetUserIP(),
    }
    $(".replied_comments").empty()
    display_comments(data)
})

$("#contact_us_form").submit(function(event){
    event.preventDefault()
    var EmailRegex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if(EmailRegex.test($("#contact_us_email").val()) === false){
        $("#contact_us_email").css("border-color", "red");
        $("#contact_us_email").attr("placeholder", "Email is Requeired now.");
        $("#contact_us_email").attr('required',true);
    }else{
        $("#send_message").prop("disabled", true);
        var user_name = $("#contact_us_name").val()
        var user_email = $("#contact_us_email").val()
        var description = $("#contact_us_description").val()

        var data = {
            "contact_us_name":user_name,
            "contact_us_email":user_email,
            "contact_us_description":description,
        }

        $.ajax({
            url:'/send-message/',
            method:'POST',
            data:data,
            success: function(data){
                $("#contact_us_form")[0].reset();
                $("#contact_us_email").css("border-color", "");
                $("#contact_us_form").hide()
                $("#message_submited").removeClass("d-none")
            }
        })
    }
    return false
})
     
var remove_filtered_tags;
$(".search-filter-tags").on("click", function(){
    console.log("-*/-*/-*/-*/-*/-*/-*/-*/-*/")
    var this_key = $(this).data("key")
    var this_value = $(this).data("value")
    var this_url_path = window.location.href.split("?")
    var this_url_list = this_url_path[1].split("&")

    if (this_key.includes("accessories")){
        this_value = "Yes"
    }

    if (isNaN(this_value)){
        this_value = this_value.replace(" ","+")
    }

    if (remove_filtered_tags == undefined){
        remove_filtered_tags = this_url_list
    }

    for (let tag in this_url_list){
        if(this_url_list[tag].includes(this_key) && this_url_list[tag].includes(this_value)){
            remove_filtered_tags = remove_filtered_tags.filter(remove_filtered_tags => remove_filtered_tags !== this_url_list[tag])
        }
    }
    console.log(remove_filtered_tags)
    this_url_path[1] = remove_filtered_tags.join("&")

    if(remove_filtered_tags.length < 1){
        window.location.href = `/`
    } else {
        window.location.href = `${this_url_path.join("?")}`
    }
})

var page_filtered_data = []
var page_filtered_brands = []
var page_filtered_categories = []
var page_filtered_model_name = []
var page_filtered_trim = []
var page_filtered_accessories = []
var page_filtered_bike_class = []
var page_filtered_keyword = []
var page_filtered_suspention = []
var page_filtered_motor_type = []
$(".page-filtered-data").on("click", function(){
    var this_tag = $(this).data("tag")
    var this_value = $(this).data("value")
    var all_filtered_tags = $('.page-filtered-data').map((_,el) => el).get()
    var data = {}
    for (let tag in all_filtered_tags){
         if (all_filtered_tags[tag].getAttribute('data-tag') != this_tag || all_filtered_tags[tag].getAttribute('data-value') != this_value){
             if (all_filtered_tags[tag].getAttribute('data-tag') == "brands"){
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_brands ) == -1){
                    page_filtered_brands.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = page_filtered_brands
                }
                brands = `&brands=${page_filtered_brands}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "category"){
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_categories ) == -1){
                    page_filtered_categories.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = page_filtered_categories
                }
                categories = `&category=${page_filtered_categories}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "model_name"){
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_model_name ) == -1){
                    page_filtered_model_name.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = page_filtered_model_name
                }
                model_name = `&model_name=${page_filtered_model_name}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "trim"){
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_trim ) == -1){
                    page_filtered_trim.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = page_filtered_trim
                }
                trim = `&trim=${page_filtered_trim}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "accessories"){
                if (jQuery.inArray(all_filtered_tags[tag].getAttribute('data-value'), page_filtered_accessories ) == -1){
                    if (all_filtered_tags[tag].getAttribute('data-value') == "Fenders"){
                        page_filtered_accessories.push(data["accessories_fenders"] = "Yes")
                    }
                    if (all_filtered_tags[tag].getAttribute('data-value') == "Lights"){
                        page_filtered_accessories.push(data["accessories_lights"] = "Yes")
                    }
                    if (all_filtered_tags[tag].getAttribute('data-value') == "Front Rack" || all_filtered_tags[tag].getAttribute('data-value') == "Rear Rack"){
                        page_filtered_accessories.push(data["accessories_racks"] = "Yes")
                    }
                }
                accessories = `&accessories=${page_filtered_accessories}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "bike_class"){
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_bike_class ) == -1){
                    page_filtered_bike_class.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = page_filtered_bike_class
                }
                bike_class = `&bike_class=${page_filtered_bike_class}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "suspension"){
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_suspention ) == -1){
                    page_filtered_suspention.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = page_filtered_suspention
                }
                suspension = `&suspension=${page_filtered_suspention}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "motor_type"){
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_motor_type ) == -1){
                    page_filtered_motor_type.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = page_filtered_motor_type
                }
                motor_type = `&motor_type=${page_filtered_motor_type}`
            }
            else if (all_filtered_tags[tag].getAttribute('data-tag') == "keywords"){
                console.log("keyword===", all_filtered_tags[tag].getAttribute('data-value'))
                if (jQuery.inArray( all_filtered_tags[tag].getAttribute('data-value'), page_filtered_keyword ) == -1){
                    page_filtered_keyword.push(all_filtered_tags[tag].getAttribute('data-value'))
                    data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = all_filtered_tags[tag].getAttribute('data-value').split(",")
                }
                keyword = `&keywords=${page_filtered_keyword}`
            }
            else {
                data[`${all_filtered_tags[tag].getAttribute('data-tag')}`] = all_filtered_tags[tag].getAttribute('data-value')
            }
         }


    }
    console.log(data, 'asd asgsuyasduyasuyvdsuydsvu');

    $.ajax({
        url:"/more-filter/",
        method:"GET",
        data:data,
        success:function(data){
//            console.log(this.url)
//            console.log("--------------------------------------")
            advance_search_url = this.url.replace('/more-filter/', '/search/')
            window.location.href = `${advance_search_url}`
//             console.log(advance_search_url, '=============');
        }
    })
   
})