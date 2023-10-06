$(document).ready(function () {

    // setting up the data tables with all the attributes
    dataTable = new DataTable('#data-table', {
        'processing': true,
        'serverSide': true,
        'serverMethod': 'post',
        'ajax': {
            'url':'/ajax'
        },
        'lengthMenu': [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
        searching: true,
        sort: false,
        'columns': [
            { data: 'title' },
            { data: 'meal' },
            { data: 'owner' },
            { data: 'rating' },
            { data: 'id', visible: false},
        ]
    });

    // making the rows clickable
    // Add a click event handler to the rows
    $('#data-table tbody').on('click', 'tr', function () {
        var data = dataTable.row(this).data();
        // You can access data.id, data.name, data.age for the clicked row
        // Perform actions based on the clicked row data
        console.log("Clicked row data:", data);
        // Example: Redirect to a new page with the row's ID
        window.location.href = '/view/' + data.id;
    });


});


