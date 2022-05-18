# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from skote.settings import SENDGRID_API

sg = SendGridAPIClient(SENDGRID_API)
def send_message_one(to,html_content,text_content,subject,sg=sg):
    message = Mail()

    message.to = [To(email=to)]
    message.cc = []
    message.bcc = []
    message.from_email=From(email='bookings@compliancemedicals.uk', name='Sarah Unokerieghan')
    message.reply_to = ReplyTo(
        email="bookings@compliancemedicals.uk",
        name="Compliance Medicals"
    )
    message.subject= subject
    message.content = [Content(mime_type='text/html', content=html_content), Content(mime_type='text/plain', content=text_content)]
    message.mail_settings = MailSettings(
        bypass_list_management=BypassListManagement(False),
        footer_settings=FooterSettings(False),
        sandbox_mode=SandBoxMode(False)
    )
    try:
        response = sg.send(message)
    except Exception as e:
        print(e.message)


