/*global $ */
'use strict';

$(document).ready(function(){
    // ---------- Review Category Server-side processing START  ----------
    $('#reviewcategory-table').DataTable({
        pageLength: 25,
        responsive: true,
        order: [[ 0, "desc" ]],
        columnDefs: [{
            orderable: false,
            targets: [-1, -2]
        },],

        // Ajax for pagination
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'name', name: 'name' },
            { data: 'slug', name: 'slug' },
            { data: 'reviews', name: 'reviews' },
            { data: 'actions', name: 'actions' },
        ],
    });
    // ---------- Review Category Server-side processing END  ----------

    // ---------- Review Brand Server-side processing START  ----------
    $('#reviewbrand-table').DataTable({
        pageLength: 25,
        responsive: true,
        order: [[ 0, "desc" ]],
        columnDefs: [{
            orderable: false,
            targets: [-1, -2]
        },],

        // Ajax for pagination
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'name', name: 'name' },
            { data: 'slug', name: 'slug' },
            { data: 'reviews', name: 'reviews' },
            { data: 'actions', name: 'actions' },
        ],
    });
    // ---------- Review Brand Server-side processing END  ----------

    // ---------- Review Server-side processing START  ----------
    $('#review-table').DataTable({
        pageLength: 25,
        responsive: true,
        order: [[ 0, "desc" ]],
        columnDefs: [{
            orderable: false,
            targets: -1
        },],

        // Ajax for pagination
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'name', name: 'name' },
            { data: 'create_by__full_name', name: 'create_by__full_name' },
            { data: 'status', name: 'status' },
            { data: 'actions', name: 'actions' },
        ],
    });
    // ---------- Review Server-side processing END  ----------


    // ---------- Pages Server-side processing START  ----------
    $('#pages-table').DataTable({
        pageLength: 25,
        responsive: true,
        order: [[ 0, "desc" ]],
        columnDefs: [{
            orderable: false,
            targets: -1
        },],

        // Ajax for pagination
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'page_title', name: 'page_title' },
            { data: 'create_by__full_name', name: 'create_by__full_name' },
            { data: 'status', name: 'status' },
            { data: 'actions', name: 'actions' },
        ],
    });
    // ---------- Pages Server-side processing END  ----------

    // // ---------- Menus Server-side processing START  ----------
    // $('#menus-table').DataTable({
    //     pageLength: 25,
    //     responsive: true,
    //     order: [[ 0, "desc" ]],
    //     columnDefs: [{
    //         orderable: false,
    //         targets: -1
    //     },],
    //     "dataSrc": function ( json ) {
    //         console.log(json)
    //     },
    //     "bSort":false,
    //     info: false,
    //     // Ajax for pagination
    //     "language":
    //     {
    //         "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
    //     },
    //     processing: true,
    //     serverSide: true,
    //     ajax: {
    //         url: window.pagination_url,
    //         type: 'get',
    //     },
    //     "drawCallback": function (settings) {
    //         // Here the response
    //         var response = settings.json['data'];
    //     },
    //     columns: [
    //         { data: 'id', name: 'id' },
    //         { data: 'name', name: 'name' },
    //         { data: 'menu_location', name: 'menu_location' },
    //         { data: 'actions', name: 'actions' },
    //     ],
    // });
    // // ---------- Menus Server-side processing END  ----------

    // ---------- Trusted accessories Server-side processing START  ----------
    $('#trustedaccessories-table').DataTable({
        pageLength: 25,
        responsive: true,
        order: [[ 0, "desc" ]],
        columnDefs: [{
            orderable: false,
            targets: -1
        },],

        // Ajax for pagination
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'name', name: 'name' },
            { data: 'status', name: 'status' },
            { data: 'actions', name: 'actions' },
        ],
    });
    // ---------- Trusted accessories Server-side processing END  ----------

    // ---------- Trusted accessories Server-side processing START  ----------
    $('#comments-table').DataTable({
        pageLength: 25,
        responsive: true,
        order: [[ 0, "desc" ]],
        columnDefs: [{
            orderable: false,
            targets: [-1, -4, -5]
        },],

        // Ajax for pagination
        "language":
        {
            "processing": "<b><i class='fa fa-refresh fa-spin'></i>&nbsp;Loading....</b>",
        },
        processing: true,
        serverSide: true,
        ajax: {
            url: window.pagination_url,
            type: 'get',
            data: function ( d ) {
                return $.extend( {}, d, {
                    "comment_data": $('#comment_data').val()
                });
            }
        },
        columns: [
            { data: 'id', name: 'id' },
            { data: 'name', name: 'name' },
            { data: 'description', name: 'description', createdCell: function(td, cellData, rowData, row, col) {
                    $(td).addClass('show_description');
                }
            },
            { data: 'in_response_to', name: 'in_response_to' },
            { data: 'create_at', name: 'create_at' },
            { data: 'is_approved', name: 'is_approved', render: is_approved_button},
            { data: 'actions', name: 'actions' },
        ],
        "createdRow": function( row, data, dataIndex){
                if(data['is_approved'] == false){
                    $(row).css('background', '#fcf9e8');
                }
            }
    });

    function is_approved_button(data, type, row, meta){
        if(data === true){
            return '<button onclick="approve_disapprove('+row['id']+', false)" title="Disapprove" class="btn btn-success btn-xs" style="width: 70px;" >Disapprove</button>'
        }else{
            return '<button onclick="approve_disapprove('+row['id']+', true)" title="Approve" class="btn btn-success btn-xs" style="width: 70px;">Approve</button>'
        }
    }

    // ---------- Trusted accessories Server-side processing END  ----------

});

var userroles = {
    // ------------------------------------------------------------------------
    // Users
    // ------------------------------------------------------------------------
    users: {
        index: function () {
            $('#user-table').DataTable({
                pageLength: 25,
                responsive: true,
                order: [[ 0, "desc" ]],
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },],

                // Ajax for pagination
                processing: true,
                serverSide: true,
                ajax: {
                    url: window.pagination_url,
                    type: 'get',
                },
                columns: [
                    { data: 'id', name: 'id' },
                    { data: 'username', name: 'username' },
                    { data: 'name', name: 'name' },
                    { data: 'mobile', name: 'mobile' },
                    { data: 'dob', name: 'dob' },
                    { data: 'is_active', name: 'is_active' },
                    { data: 'created_at', name: 'created_at' },
                    { data: 'actions', name: 'actions' }
                ],
            });

        },

        details: function () {
            $('.groups-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available groups',
                selectedListLabel: 'Chosen groups',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }
    },

    // ------------------------------------------------------------------------
    // Groups
    // ------------------------------------------------------------------------
    groups: {
        index: function () {
            $('#group-table').DataTable({
                pageLength: 25,
                responsive: true,
                order: [[ 0, "desc" ]],
                columnDefs: [{
                    orderable: false,
                    targets: -1
                },]
            });
        },
        details: function () {
            $('.permissions-select').bootstrapDualListbox({
                nonSelectedListLabel: 'Available user permissions',
                selectedListLabel: 'Chosen user permissions',
                preserveSelectionOnMove: 'moved',
                moveOnSelect: false
            });
        }
    },
};
