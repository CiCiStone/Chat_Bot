$(document).ready(function() {
    $('#message-form').on('submit', function(e) {
        e.preventDefault();
        var message = $('#message-input').val();
        var model = $('#model-select').val();
        if (message) {
            $.ajax({
                url: '/send_message',
                type: 'POST',
                data: {message: message, model: model},
                success: function(data) {
                    if (data.error) {
                        alert(data.error);
                    } else {
                        $('#conversation').append('<div class="dialogue-box user-message"><p>你: ' + data.message + '</p></div>');
                        $('#conversation').append('<div class="dialogue-box bot-response"><p>回复: ' + data.response + '</p></div>');
                        $('#message-input').val('');
                    }
                }
            });
        }
    });

    $('#create-dialog').on('click', function() {
        $.ajax({
            url: '/create_dialog',
            type: 'POST',
            success: function(data) {
                $('#dialog-list').empty();
                $.each(data.dialogs, function(key, dialog) {
                    $('#dialog-list').append('<li data-id="' + key + '" class="dialog-item' + (key === data.current_dialog_id ? ' active' : '') + '"><div class="dialog-text"><span class="dialog-name">' + dialog.name + '</span><input type="text" class="rename-input" value="' + dialog.name + '" style="display: none;"></div><div class="dialog-buttons"><button class="rename-dialog">重命名</button><button class="delete-dialog">删除</button></div></li>');
                });
                $('#conversation').empty();
            }
        });
    });

    $(document).on('click', '.dialog-item', function() {
        var dialog_id = $(this).data('id');
        $.ajax({
            url: '/select_dialog',
            type: 'POST',
            data: {dialog_id: dialog_id},
            success: function(data) {
                $('#dialog-list .dialog-item').removeClass('active');
                $('[data-id="' + data.current_dialog_id + '"]').addClass('active');
                $('#conversation').empty();
                $.each(data.conversations, function(index, conv) {
                    $('#conversation').append('<div class="dialogue-box ' + (conv.role === 'user' ? 'user-message' : 'bot-response') + '"><p>' + (conv.role === 'user' ? '你: ' : '回复: ') + conv.content + '</p></div>');
                });
            }
        });
    });

    $(document).on('click', '.delete-dialog', function(event) {
        event.stopPropagation();
        var dialog_id = $(this).parent().parent().data('id');
        $.ajax({
            url: '/delete_dialog',
            type: 'POST',
            data: {dialog_id: dialog_id},
            success: function(data) {
                $('#dialog-list').empty();
                $.each(data.dialogs, function(key, dialog) {
                    $('#dialog-list').append('<li data-id="' + key + '" class="dialog-item' + (key === data.current_dialog_id ? ' active' : '') + '"><div class="dialog-text"><span class="dialog-name">' + dialog.name + '</span><input type="text" class="rename-input" value="' + dialog.name + '" style="display: none;"></div><div class="dialog-buttons"><button class="rename-dialog">重命名</button><button class="delete-dialog">删除</button></div></li>');
                });
                $('#conversation').empty();
            }
        });
    });

    $(document).on('click', '.rename-dialog', function(event) {
        event.stopPropagation();
        var $parent = $(this).parent().parent();
        $parent.find('.dialog-name').hide();
        $parent.find('.rename-input').show().focus();
    });

    $(document).on('blur', '.rename-input', function() {
        var dialog_id = $(this).parent().parent().data('id');
        var new_name = $(this).val();
        $.ajax({
            url: '/rename_dialog',
            type: 'POST',
            data: {dialog_id: dialog_id, new_name: new_name},
            success: function(data) {
                $('#dialog-list').empty();
                $.each(data.dialogs, function(key, dialog) {
                    $('#dialog-list').append('<li data-id="' + key + '" class="dialog-item' + (key === data.current_dialog_id ? ' active' : '') + '"><div class="dialog-text"><span class="dialog-name">' + dialog.name + '</span><input type="text" class="rename-input" value="' + dialog.name + '" style="display: none;"></div><div class="dialog-buttons"><button class="rename-dialog">重命名</button><button class="delete-dialog">删除</button></div></li>');
                });
            }
        });
    });
});
