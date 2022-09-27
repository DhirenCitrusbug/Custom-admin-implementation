//Mobile Menu
/* $('.rw_hamburger').click(function(){
  $(this).toggleClass('open');
  $('.rw_sidebar').toggleClass('open');
}); */
hide = true;
$("body").on("click", function () {
  if (hide) $(".rw_sidebar").removeClass("open");
  hide = true;
});

// add and remove .active
$("body").on("click", ".rw_hamburger", function () {
  var self = $(".rw_sidebar");

  if (self.hasClass("open")) {
    $(".rw_sidebar").removeClass("open");
    return false;
  }

  $(".rw_sidebar").removeClass("open");

  self.toggleClass("open");
  hide = false;
});

//Agency Header title
$(".agency_header_title").on("click", function (e) {
  $(".agency_header_title h3").toggleClass("active");
  e.stopPropagation();
});

$(document).on("click", function (e) {
  if ($(e.target).is(".agency_header_title") === false) {
    $(".agency_header_title h3").removeClass("active");
  }
});

$(document).on("click", function (e) {
  if ($(".modal-backdrop").length > 1) {
    $(".modal-backdrop").last().css("display", "none");
  }
});

//Profile DropDown
$(".header_profile a").on("click", function (e) {
  $(".header_profile_dropdown").toggleClass("active");
  e.stopPropagation();
});

$(document).on("click", function (e) {
  if ($(e.target).is(".header_profile a") === false) {
    $(".header_profile_dropdown").removeClass("active");
  }
});
//Select2
$(document).ready(function () {
  $("#multiple").select2({
    placeholder: "Add list name",
    allowClear: false,
  });
  $("#multiple2").select2({
    dropdownParent: $("#add_contact_tolist"),
    placeholder: "Add Tag",
    allowClear: false,
    dropdownPosition: "auto",
  });
  $(".double_optin_keyword").select2({
    minimumResultsForSearch: -1,
    placeholder: "Enter keyword",
    allowClear: false,
    width: 100,
  });
  $("#edit_cont").select2({
    dropdownParent: $(".edit_contacts"),
    placeholder: "Add Tag",
    allowClear: false,
    minimumResultsForSearch: -1,
  });
  $("#edit_acctive_camp").select2({
    dropdownParent: $(".edit_contacts"),
    placeholder: "Active Campaigns",
    allowClear: false,
    minimumResultsForSearch: -1,
  });
  $("#active_campaigns").select2({
    dropdownParent: $("#add_contact_tolist"),
    placeholder: "Active Campaigns",
    allowClear: false,
    minimumResultsForSearch: -1,
  });
  $("#add_cont").select2({
    dropdownParent: $("#add_contact_tolist"),
    placeholder: "Add Tag",
    allowClear: false,
    minimumResultsForSearch: -1,
  });

  $("#trigger_keywords").select2({
    placeholder: "Add Keywords",
    allowClear: false,
  });
  $(".tag_added").select2({
    placeholder: "Add Tag",
    allowClear: false,
  });
  $(".trigger_select_tags").select2({
    placeholder: "Add Tag",
    allowClear: false,
  });
  $("#datebased_trigger").select2({
    placeholder: "Add Date Fields",
    allowClear: false,
  });
});

//Date picker
$(function () {
  $("#rw_datepicker").datepicker({ dateFormat: "dd/mm/yy" });
});
$(function () {
  $("#datepicker").datepicker({

    dateFormat: "dd/mm/yy",
    minDate: 0,
   }).val();
});
$(function () {
  $("#rw_datepicker2").datepicker();
});
$(function () {
  $("#rw_datepicker3").datepicker();
});
$(function () {
  $("#rw_datepicker4").datepicker();
});
$(function () {
  $("#datepicker2").datepicker({ dateFormat: "dd/mm/yy" , minDate: 1, }).val();
});
$(function () {
  $("#datepicker3").datepicker({ dateFormat: "dd/mm/yy" }).val();
});
$(function () {
  $("#rw_date_month3").datepicker({
    dateFormat: "mm-dd",
    dropdownParent: $(".add_contact"),
  });
});
$(function () {
  $("#rw_date_month4").datepicker({
    dateFormat: "mm-dd",
    dropdownParent: $(".add_contact"),
  });
});

$(function () {
  $("smart_date_picker").datepicker({
    dateFormat: "dd/mm/yy",
    dropdownParent: $("#client_createnew_smart_list"),
  });
});

$(document).ready(function () {
  $(".rw_eye").on("click", function () {
    $(this).toggleClass("rw_eyeclose");
    var fieldType = $(this).siblings("input[type='password']").attr("type");
    if (fieldType == "password") {
      $(this).siblings("input[type='password']").attr("type", "text");
    } else {
      $(this).siblings("input[type='text']").attr("type", "password");
    }
  });
});
// Data Table
$(document).ready(function () {
  $("#admin_dashboard_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search Agency Name,Contact Name and Date",
      paginate: {
        next: '<img src="../static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="../static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 2, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
  // agency twillio
  $("#agency_twillio_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search Agency Name,Contact Name and Date",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 0, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
  //admin_user
  $("#admin_user_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search Agency Name, Contact Name and Date",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 2, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          null,
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
        "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });

  // agency dashboard
  $("#agency_dashboard_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search Client Name",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 1, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
        "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
  // Phone Data Table
  $("#camp_phone_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search name",
      paginate: {
        next: '<img src="/admin/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/admin/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
  // Custom field Data Table
  $("#compaign_custom_field").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search field/placeholder",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 3, "desc" ]],
    "columns": [
      null,
      null,
      null,
      { "searchable": false },
      { "searchable": false }
    ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });

  // Contact Data Table
  $("#rw_cl_contact_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search number/name",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 3, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          { "searchable": false },
          null,
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
         "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });


  // Phone Data Table
  $("#rw_cl_phone_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search number/name",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 2, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
         "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });

  // Client List Table
  $("#rw_cl_list_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search list name",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 2, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
         "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });

  // Client User Data Table
  $("#cm_user_tabl").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search users/email",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 2, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
  // Coupon Data Table
  $("#rw_coupon_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search name/date",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 1, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
   // Referral campaign Data Table
   $("#rw_referral_campaign_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search name/date",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 1, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
    // "columnDefs": [
    //   {
    //     "searchable": false,
    //     "targets": 0
    //   },
    // ],
    "columns": [
      null,
      null,
      { "searchable": false },
      { "searchable": false },
      { "searchable": false },
      { "searchable": false },
      { "searchable": false }
    ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
    // Broadcast Schedule List table
  $("#sch_broadcast").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search message",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 0, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
  // Campaigns table
  $("#client_campaigns_table").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search campaigns",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 1, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          { "searchable": false },
          { "searchable": false },
          { "searchable": false },
          { "searchable": false },
          { "searchable": false },
          { "searchable": false }
        ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });

  // Sent broadcast Data Table
  $("#rw_sent_brd_table").dataTable({
     language: {
      search: "",
      searchPlaceholder: "Search message",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 0, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });


  // Client tag Data Table
  $("#client_tags").dataTable({
     language: {
      search: "",
      searchPlaceholder: "Search by Name, Date",
      paginate: {
        next: '<img src="/static/images/icons/chevron_right.svg" alt="image">',
        previous:
          '<img src="/static/images/icons/chevron_left.svg" alt="image">',
      },
    },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
    "order": [[ 1, "desc" ]],
    aoColumnDefs: [
          {
             bSortable: true,
             aTargets: [ -1 ]
          }
        ],
        "columns": [
          null,
          null,
          { "searchable": false }
        ],
    "oLanguage": {
        "sEmptyTable": "No Records Found"
    }
  });
  //Add to campaigns
  $("#addto_campaings_id").dataTable({
    language: {
      search: "",
      searchPlaceholder: "Search campaign..",
    },
    bPaginate: false,
    bLengthChange: false,
    responsive: true,
  });
  //Add to list
  $("#add_tolist_id").dataTable({
    // language: {
    //   search: "",
    //   searchPlaceholder: "Search campaign..",
    // },
    bPaginate: true,
    bLengthChange: false,
    responsive: true,
  });
  //Static list
  $("#static_list_id").dataTable({
   language: {
      search: "",
      searchPlaceholder: "Search contacts..",
    },
    bPaginate: false,
    bLengthChange: false,
    responsive: true,
  });
  $("#static_list_id_edit").dataTable({
   language: {
      search: "",
      searchPlaceholder: "Search contacts..",
    },
    bPaginate: false,
    bLengthChange: false,
    responsive: true,
  });
});

//Option Dropdown
$(".action_btn").on("click", function (e) {
  e.stopPropagation();
  if ($(this).siblings(".action_submenu").hasClass("active")) {
    $(this).siblings(".action_submenu").removeClass("active");
  } else {
    $(".action_submenu.active").removeClass("active");
    $(this).siblings(".action_submenu").addClass("active");
  }
});
$(document).on("click", function (e) {
  if ($(e.target).is(".action_submenu") === false) {
    $(".action_submenu").removeClass("active");
  }
});
$(".remove_action").click(function () {
  $(this).parents(".action_submenu").removeClass("active");
});
/******** Input focus ********/
$(".rw_form_inputs input")
  .focus(function () {
    $(this).parents(".rw_form_inputs").addClass("rw_inp_focus");
  })
  .blur(function () {
    $(this).parents(".rw_form_inputs").removeClass("rw_inp_focus");
  });
$(".dropdown-toggle")
  .focus(function () {
    $(this).parents(".rw_form_inputs").addClass("rw_inp_focus");
  })
  .blur(function () {
    $(this).parents(".rw_form_inputs").removeClass("rw_inp_focus");
  });

/* $(document).ready(function () {
  $(".rw_custom_dropdown .select2-container")
    .focus(function () {
      console.log("hgljkljkl");
      $(this).parent(".rw_custom_dropdown").addClass("rw_inp_focus");
    })
    .blur(function () {
      $(this).parent(".rw_custom_dropdown").removeClass("rw_inp_focus");
    });
}); */
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
/******** Copy  ********/
function copy() {
  var copyText = document.getElementById("copyClipboard");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand("copy");

  $(".copied-success").fadeIn(800);
  $(".copied-success").fadeOut(800);
}
// Add remove inputs
/* $(".revenue_remove").hide(); */
//when the Add Field button is clicked

$("body").on("click", ".revenue_remove", function (e) {
  $(".next-referral").last().remove();
});

//Eye opacity
window.onload = function () {
  if (!$(".eye_pass").val() == "") {
    $(".eye_pass").next(".rw_eye").addClass("active");
  }

  $(".twilio_modal").on("show.bs.modal", function () {
    if (!$(".rw_input input").val() == "") {
      $(".rw_input input").next(".rw_eye").addClass("active");
    }
  });
};

//Spinner

$(".quanti-invitati-op").on("click", function () {
  var op = parseInt($(this).data("op"));

  var quantiInvitati = parseInt($(".quanti-invitati").val());
  var quantiInvitatiMin = parseInt($(".quanti-invitati").attr("min"));

  $(".quanti-invitati").val(Math.max(quantiInvitatiMin, quantiInvitati + op));
});
$(".quanti-invitati-op2").on("click", function () {
  var op = parseInt($(this).attr("data-op"));
  console.log(op);
  var quantiInvitati = parseInt($(".quanti-invitati2").val());
  var quantiInvitatiMin = parseInt($(".quanti-invitati2").attr("min"));

  $(".quanti-invitati2").val(Math.max(quantiInvitatiMin, quantiInvitati + op));
});

$(".quanti-invitati-op3").on("click", function () {
  var op = parseInt($(this).data("op"));

  var quantiInvitati = parseInt($(".quanti-invitati3").val());

  var quantiInvitatiMin = parseInt($(".quanti-invitati3").attr("min"));

  $(".quanti-invitati3").val(Math.max(quantiInvitatiMin, quantiInvitati + op));
});

//jQuery time
//var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".rw_next").click(function () {
  if (animating) return false;
  animating = true;

  current_fs = $(this).parents("fieldset");
  next_fs = $(this).parents("fieldset").next();

  $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

  //show the next fieldset
  next_fs.show();
  //hide the current fieldset with style
  current_fs.animate(
    { opacity: 0 },
    {
      step: function (now, mx) {
        opacity = 1 - now;
        next_fs.css({ opacity: opacity });
        // current_fs.css({
        //   position: "absolute",
        // });
      },
      duration: 0,
      complete: function () {
        current_fs.hide();
        animating = false;
      },
    }
  );
});

// $(".rw_prev").click(function () {
//   if (animating) return false;
//   animating = true;

//   current_fs = $(this).parents("fieldset");
//   previous_fs = $(this).parents("fieldset").prev();

//   $("#progressbar li")
//     .eq($("fieldset").index(current_fs))
//     .removeClass("active");

//   //show the previous fieldset
//   previous_fs.show();
//   //hide the current fieldset with style
//   current_fs.animate(
//     { opacity: 0 },
//     {
//       step: function (now, mx) {
//         opacity = 1 - now;
//         previous_fs.css({ opacity: opacity });
//       },
//       duration: 0,
//       complete: function () {
//         current_fs.hide();
//         animating = false;
//       },
//     }
//   );
// });
//Dashboard 7 Digit
var section = $(".dashboard_box_text h1");
var width = section.width();
if (width > 100) section.addClass("font_size");
else {
  section.removeClass("font_size");
}

//Search Input
$(".ag_search_icon").click(function () {
  $(".search_icon_input").toggleClass("search_active");
});

//Campaings Creation
$(".add_btn_box").on("click", function (e) {
  e.stopPropagation();
  if ($(this).siblings(".trigger_dropdown").hasClass("active")) {
    $(this).siblings(".trigger_dropdown").removeClass("active");
  } else {
    $(".trigger_dropdown.active").removeClass("active");
    $(this).siblings(".trigger_dropdown").addClass("active");
  }
});
$(document).on("click", function (e) {
  if ($(e.target).is(".trigger_dropdown") === false) {
    $(".trigger_dropdown").removeClass("active");
  }
});

$(document).on("click", function (e) {
  if ($(e.target).is(".trigger_overlay") === false) {
    $(".trigger_overlay").removeClass("active");
  }
});

$(".text_msg_click").click(function () {
  $(".text_message_box").addClass("active");
  $(".time_delay").removeClass("active");
  $(".wait_until").removeClass("active");
  $(".cancellation_trigger").removeClass("active");
});
$(".time_delay_click").click(function () {
  $(".time_delay").addClass("active");
  $(".text_message_box").removeClass("active");
  $(".wait_until").removeClass("active");
  $(".cancellation_trigger").removeClass("active");
});
$(".wait_until_click").click(function () {
  $(".wait_until").addClass("active");
  $(".time_delay").removeClass("active");
  $(".text_message_box").removeClass("active");
  $(".cancellation_trigger").removeClass("active");
});
$(".add_new_trigger").click(function () {
  $(".new_trigger").addClass("active");
  $(".wait_until").removeClass("active");
  $(".time_delay").removeClass("active");
  $(".text_message_box").removeClass("active");
  $(".cancellation_trigger").removeClass("active");
});
$(".activate_cancel").click(function () {
  $(".cancellation_trigger").addClass("active");
  $(".new_trigger").removeClass("active");
  $(".wait_until").removeClass("active");
  $(".time_delay").removeClass("active");
  $(".text_message_box").removeClass("active");
});
$(".camp_close").click(function () {
  $(this).parents(".campaigns_box").removeClass("active");
});
/* $(".compaign_add_trigger ul li a").click(function () {
  $(this).toggleClass("active");
}); */

$(".compaign_add_trigger ul li a").on("click", function (e) {
  e.stopPropagation();
  if ($(this).hasClass("active")) {
    $(this).removeClass("active");
  } else {
    $(".compaign_add_trigger ul li a.active").removeClass("active");
    $(this).addClass("active");
  }
});

$(".campaigns_trigger_inner").on("click", function (e) {
  e.stopPropagation();
  if ($(this).hasClass("active")) {
    $(this).removeClass("active");
  } else {
    $(".campaigns_trigger_inner.active").removeClass("active");
    $(this).addClass("active");
  }
});

$(".check_input").change(function () {
  /* $(".trigger_li").removeClass("orange_border"); */
  if ($(this).is(":checked")) {
    $(this).parents(".rw_checkbox").parents("li").addClass("orange_border");
  } else {
    $(this).parents(".rw_checkbox").parents("li").removeClass("orange_border");
  }
});

//Toastar
$(".btn-primary").click(function () {
  if (!$(".rw_success_toast").hasClass("active")) {
    $(".rw_success_toast").addClass("active");
  }
  setTimeout(function () {
    $(".rw_success_toast").removeClass("active");
  }, 3000);
});
$(".success_close").click(function () {
  $(".rw_success_toast").removeClass("active");
});

$(".btn-danger").click(function () {
  if (!$(".rw_error_toast").hasClass("active")) {
    $(".rw_error_toast").addClass("active");
  }
  setTimeout(function () {
    $(".rw_error_toast").removeClass("active");
  }, 3000);
});
$(".error_close").click(function () {
  $(".rw_error_toast").removeClass("active");
});

$(document).ready(function () {
  if (!$(".rw_success_toast").hasClass("active")) {
    $(".rw_success_toast").addClass("active");
  }
  setTimeout(function () {
    $(".rw_success_toast").removeClass("active");
  }, 3000);
});
$(".success_close").click(function () {
  $(".rw_success_toast").removeClass("active");
});

$(document).ready(function () {
  if (!$(".rw_error_toast").hasClass("active")) {
    $(".rw_error_toast").addClass("active");
  }
  setTimeout(function () {
    $(".rw_error_toast").removeClass("active");
  }, 3000);
});
$(".error_close").click(function () {
  $(".rw_error_toast").removeClass("active");
});

//Add Client Popup
$(".add_client").click(function (e) {
  $(".agency_offcanvas").addClass("active");
  e.stopPropagation();
});
$("#client_adnew_agency .popup_close").click(function () {
  $(".agency_offcanvas").removeClass("active");
});
//DropDown
$(".rw_cstm_dropdown").select2({
  minimumResultsForSearch: -1,
});


$("#client_adnew_agency .popup_close").click(function () {

     console.log('active')
  $(".offcanvas").removeClass("active");
  console.log('removeactive')
});

//Popup DropDown
$(".rw_popup_cstm_dropdown").select2({
  dropdownParent: $(".rw_select2_modal"),
  minimumResultsForSearch: -1,
});
// Broadcast Input Icon
/*$(document).on("click", function (e) {
  if ($(e.target).is(".input_submenu") === false) {
    $(".input_submenu").removeClass("active");
  }
});
$(".add_tag").click(function () {
  $(".trigger_overlays").addClass("active");
});
 $(document).on("click", function (e) {
  if ($(e.target).is(".trigger_overlay") === false) {
    $(".trigger_overlay").removeClass("active");
  }
}); */
$(function () {
//  $(".add_tag").on("click", function (e) {
//    e.stopPropagation();
//    $(".input_submenu").addClass("active");
//  });

  $(document).on("click", function (e) {
    if ($(e.target).is(".input_submenu") === false) {
      $(".input_submenu").removeClass("active");
    }
  });
//  $(".add_tag").on("click", function (e) {
//    $(".trigger_overlays").addClass("active");
//  });
  $(".trigger_overlays").on("click", function (e) {
    $(".trigger_overlays").removeClass("active");
    $(".input_submenu").removeClass("active");
  });
  $(".click_1").on("click", function (e) {
    $(".trigger_overlays").removeClass("active");
  });
  $(".click_2").on("click", function (e) {
    $(".trigger_overlays").removeClass("active");
  });
  $(".click_3").on("click", function (e) {
    $(".trigger_overlays").removeClass("active");
  });
  $(".click_4").on("click", function (e) {
    $(".trigger_overlays").removeClass("active");
  });
});

//Calender body
$(".date_input").click(function (e) {
  $(".modal").toggleClass("overflow_hidden");
  e.stopPropagation();
});
$(".date_input").change(function (e) {
  $(".modal").toggleClass("overflow_hidden");
  e.stopPropagation();
});

$(document).on("click", function (e) {
  if ($(e.target).is(".modal") === false) {
    $(".modal").removeClass("overflow_hidden");
  }
});
$('a').attr('draggable','false')