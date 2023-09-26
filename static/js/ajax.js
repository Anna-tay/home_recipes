
new DataTable('#empTable', {
    'processing': true,
    'serverSide': true,
    'serverMethod': 'post',
    'ajax': {
        'url':'/ajax'
    },
    'lengthMenu': [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
    searching: true,
    sort: false,
    "serverSide": true,
    'columns': [
        { data: 'title' },
        { data: 'meal' },
        { data: 'owner' },
        { data: 'rating' },
    ]
});


