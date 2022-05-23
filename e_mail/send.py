# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from typing import List
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from skote.settings import SENDGRID_API
from django.template import Template, Context

def render_template(template_str, context):
    template= Template(template_str)
    contexts = Context(context)
    return template.render(contexts)

sg = SendGridAPIClient(SENDGRID_API)
def send_message_one(to,html_content,text_content,subject, context=None,sg=sg):
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
    message.content = [Content(mime_type='text/html', content=render_template(html_content, context=context)), Content(mime_type='text/plain', content=render_template(html_content, context=context))]
    message.mail_settings = MailSettings(
        bypass_list_management=BypassListManagement(False),
        footer_settings=FooterSettings(False),
        sandbox_mode=SandBoxMode(False)
    )
    try:
        response = sg.send(message)
        return response
    except Exception as e:
        print(e.message)
        response = e.message
        return response


# 
class SendgridClient:
    def __init__(self, recipients: List, sender: str='bookings@compliancemedicals.uk'):
        self.sendgrid_client = SendGridAPIClient(SENDGRID_API)
        self.mail = Mail(from_email=sender, to_emails=recipients)
        self.mail.reply_to = ReplyTo(email="bookings@compliancemedicals.uk",name="Compliance Medicals")

    def set_template_data(self, data:dict):
        self.mail.dynamic_template_data = {
            **data
        }

    def set_template_id(self, template_id:str):
        self.mail.template_id = template_id

    def send(self):
        try:
            self.response = sg.send(self.mail)
        except Exception as e:
            print(e)
            self.response = e

