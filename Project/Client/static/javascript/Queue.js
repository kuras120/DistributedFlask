
function getStatus(taskID, refresh) {
    $.ajax({
        url: `/account/task_status/${taskID}`,
        method: 'GET'
    })
    .done((res) => {
        if (refresh) {
            $('#tasks').find('.task-id').each(function () {
                if (res.data.task_id === $(this).text()) {
                    $(this).parent().replaceWith(`
                <tr>
                    <td class="task-id">${res.data.task_id}</td>
                    <td>${res.data.task_status}</td>
                    <td>${res.data.task_result}</td>
                </tr>`)
                }
            });
        }
        else {
            const html = `
                <tr>
                    <td class="task-id">${res.data.task_id}</td>
                    <td>${res.data.task_status}</td>
                    <td>${res.data.task_result}</td>
                </tr>`;
            $('#tasks').prepend(html);
        }

        const taskStatus = res.data.task_status;
        if (taskStatus === 'finished' || taskStatus === 'failed') return false;
        setTimeout(function() {
            getStatus(res.data.task_id, true);
        }, 1000);
    })
    .fail((err) => {
        console.log(err)
    });
}

function queue() {
    $.ajax({
        url: '/account/queue_task',
        data: {
            taskName: $('#taskName').val(),
            resolutionSelect: $('#resolutionSelect').val(),
            fileSelect: $('#fileSelect').val()
        },
        method: 'POST'
    })
    .done((res) => {
        getStatus(res.data.task_id, false);
    })
    .fail((err) => {
        alert("File already exists.");
        console.log(err);
    });
}

