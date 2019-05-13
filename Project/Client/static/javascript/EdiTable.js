let table = $('#files-table > tbody');

function removeElements() {
    let files = [];
    table.find('tr').each(function () {
        if ($(this).find('.check').prop('checked')) {
            $(this).find('td').each(function () {
                if ($(this).attr('datatype') === 'String') files.push($(this).text());
            });
            $(this).remove();
        }
    });
    let files_str = JSON.stringify(files);
    $.ajax({
        type : 'POST',
        url : '/account/delete_files',
        data : files_str,
        dataType : 'json'
    })
    .done(function() {
    });
}

$(document).ready( function() {
    $('#file-name, #addition-date')
        .each(function () {
            let th = $(this),
                thIndex = th.index(),
                inverse = false;
            th.click(function () {
                table.find('td').filter(function () {
                    return $(this).index() === thIndex;
                }).sortElements(function (a, b) {
                    return $.text([a]) > $.text([b]) ?
                        inverse ? -1 : 1
                        : inverse ? 1 : -1;
                }, function () {
                    // parentNode is the element we want to move
                    return this.parentNode;
                });
                inverse = !inverse;
            });
        });

    $('#check-all').click(function () {
        let master = $(this).find('.check');
        master.prop('checked', !master.prop('checked'));
        $(".check").prop('checked', master.prop('checked'));
    });

    $('#files-table td').click(function () {
        if ($(this).attr('contenteditable') !== 'true') {
            let checkbox = $(this).parent().find('.check');
            checkbox.prop('checked', !checkbox.prop('checked'));
        }
    });
});