def text_error_logs(message, text_error):
    text = {
        f"@{message.from_user.username} вызвал text_error\n"
        f"чат: {message.chat.username}\n"
        f"ошибка: {text_error}\n"
        f"text сообщения:{message.text}"}
    return text

def callback_error_logs(call, callback_error):
    text = {
        f"@{call.from_user.username} вызвал callback_error\n"
        f"чат: {call.chat.username}\n"
        f"ошибка: {callback_error}\n"
        f"Имя callback:{call.data}"}
    return text