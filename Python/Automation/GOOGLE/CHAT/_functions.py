import requests
import json

def sendChatMessage(title, content, chat_group_target):
    chat_group_targets = [
        #chat_group_webhook_test_url
        'https://chat.googleapis.com/v1/spaces/AAAA9aaaByI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=HaO9qHqrqRROfFfGQVOJbdiax5Njzd7bHLCiYU7RoQU',
        #chat_group_webhook_helpdesk_url
        'https://chat.googleapis.com/v1/spaces/AAAANM5xDUo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=d9DXKzipuuwgahqp9k7pPqen7JcIqXg4xHjHkNVDxBY',
        #chat_group_webhook_network_admin_team_url
        'https://chat.googleapis.com/v1/spaces/AAAABGSq2C8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=0qkr9a-z556VjN4YPBiQLsS0Wftp14wT200HTKAtjL4',
        #chat_group_webhook_test_url
        'https://chat.googleapis.com/v1/spaces/AAAANM5xDUo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=3PhmpRta-dftXuU5TGJpto0ceTNVGK_WU2TJf37jT-E'
    ]
    
    # Set chat group target
    target = 0 if chat_group_target == 0 else chat_group_target
    webhook = chat_group_targets[target]
    
    # Define the message payload
    message_text = {
        "text": f"{content}"
        }
    
    # Convert the message payload to JSON
    json_message = json.dumps(message_text)

    # Set the headers for the request
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Send the POST request to the Google Chat webhook URL with the message payload
    response = requests.post(webhook, data=json_message, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message. Status code: {response.status_code}, Response content: {response.text}')

def main():
    title = "Test Title"
    content = "Test message content"
    targetChat = 0

    try:
        results = sendChatMessage(title, content, targetChat)        
    except Exception as err:
        print(f"An error occurred testing: {err}")


if __name__ == "__main__":
    main()