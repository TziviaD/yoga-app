from mailjet_rest import Client
import os
api_key = 'e8d5b45bbabcfe4b84fc5703e9c7b7c7'
api_secret = 'ef59861df3248c9b08d900043b4a8315' #evenetually take out and hide

mailjet = Client(auth=(api_key, api_secret), version='v3.1')
def send_test():
    data = {
    'Messages': [
        {
        "From": {
            "Email": "tzivdruin@gmail.com",
            "Name": "Tzivia"
        },
        "To": [
            {
            "Email": "druinsix@gmail.com",
            "Name": "Tzivia"
            }
        ],
        "Subject": "Greetings from Mailjet.",
        "TextPart": "My first Mailjet email",
        "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
