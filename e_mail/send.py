from django.core.mail import send_mail, EmailMessage


def send_email(email_temp,to):
    message = EmailMessage(subject=email_temp.subject, body=email_temp.body_html, from_email='sarahunoke@gmail.com', to=to)
    message.content_subtype='html'
    message.send()
    return 'sent'
