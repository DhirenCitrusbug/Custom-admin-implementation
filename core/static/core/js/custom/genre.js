/*global $ */
'use strict';

var genre_data = {

    // ------------------------------------------------------------------------
    // Genre
    // ------------------------------------------------------------------------
    genre: {

        index: function () {
            $('#genre-table').DataTable({
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

    // ------------------------------------------------------------------------


};
