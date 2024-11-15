import Google.Utils.chat_message as chat_message

webhook_test_url = 'https://chat.googleapis.com/v1/spaces/AAAA9aaaByI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=HaO9qHqrqRROfFfGQVOJbdiax5Njzd7bHLCiYU7RoQU'
hyperlink_url = 'https://www.disney.com'
hyperlink_text = 'Google Workspace Audit'
message = 'Google Workspace report has been updated'

chat_message.message_helpdesk(webhook_test_url,hyperlink_text,hyperlink_url,message)