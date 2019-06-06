
function getStatus(taskID, task_name, file_name, refresh) {
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
                    <td class="task-id" style="display: none">${res.data.task_id}</td>
                    <td>${task_name} - ${file_name}</td>
                    <td>${res.data.task_status}</td>
                    <td>${res.data.task_result}</td>
                </tr>`)
                }
            });
        }
        else {
            $('#tasks').append(
                `<tr>
                    <td class="task-id" style="display: none">${res.data.task_id}</td>
                    <td>${task_name} - ${file_name}</td>
                    <td>${res.data.task_status}</td>
                    <td>${res.data.task_result}</td>
                </tr>`
            );
        }

        let taskStatus = res.data.task_status;
        if (taskStatus === 'finished' || taskStatus === 'failed') {
            if($(`#uploadedFileSelect option:contains('${task_name}.mp4')`).length === 0) {
                $('#uploadedFileSelect').append(
                    `<option value='/static/DATA/${res.home_catalog}/${task_name}.mp4'>${task_name}.mp4</option>`
                );
            }
            return false;
        }
        setTimeout(function() {
            getStatus(res.data.task_id, task_name, file_name, true);
        }, 1000);
    })
    .fail((err) => {
        console.log(err)
    });
}
function checkForBlank()
	{
	
		if(document.getElementById('taskName').value=="")
		{
			alert('podaj nazwe zadania')
		}
		else  if(document.getElementById('fileSelect').value=="Choose...")
			{
				alert('wybierz plik wejsciowy');
				return false;
			}

					else if(document.getElementById('resolutionSelect').value=="Choose...")
			{
				alert('wybierz rozdzielczosc');
				return false;
			}
			else queue();
	}

function queue() {
    $.ajax({
    url: '/account/queue_task',
    data: {
        taskName: $('#taskName').val(),
        fileSelect: $('#fileSelect').val(),
        resolutionSelect: $('#resolutionSelect').val()
    },
    method: 'POST'
    })
    .done((res) => {
        console.log(res);
        getStatus(res.data.task_id, res.data.task_name, res.data.task_file, false)
    })
    .fail((err) => {
        console.log(err)
    });
}

$(document).ready(function () {
    if (window.location.pathname === '/account/') {
        let player = $('#player');

        $.ajax({
            url: '/account/tasks',
            method: 'GET'
        })
        .done((res) => {
            console.log(res);
            res.forEach(function (value) {
                console.log(value);
                getStatus(value.data.task_id, value.data.task_name, value.data.task_file, false)
            })
        })
        .fail((error) => {
           console.log(error)
        });

        $('#uploadedFileSelect').on('change', function(e) {
            player.hide();
            let option = this.options[e.target.selectedIndex];
            if (option.text.indexOf(".mp4") >= 0) {
                player.find('#movie').attr('src', option.value + '?' + (new Date()).toString());
                player[0].load();
                player.show();
            }
        });
    }
});
