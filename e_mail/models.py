from cgitb import text
from django.db import models
from tinymce.models import HTMLField
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import re
from django.template.defaultfilters import slugify


def increment_email_id():
    last_email = E_mail.objects.all().order_by('id').last()
    if not last_email:
        return 'DMEMA0000001'
    email_id = last_email.email_id
    email_int = int(email_id.split('DMEMA')[-1])
    width = 7
    new_email_int = email_int + 1
    formatted = (width - len(str(new_email_int))) * "0" + str(new_email_int)
    new_email_no = 'DMEMA' + str(formatted)
    return new_email_no 


def textify(html):
    # remove html tags and continuous white spaces
    text_only = re.sub('[ \t]+', ' ', strip_tags(html))
    #strip single spaces in teh begining of each line
    return text_only.replace('\n ', '\n').strip()
     


# Create your models here.
class E_mail(models.Model):
    id = models.AutoField('id', primary_key=True)
    email_id = models.CharField('email_id', max_length=20, default=increment_email_id)
    title = models.CharField('title', max_length=100, unique=True)
    description = models.CharField('description', max_length=100)
    subject = models.CharField('subject', max_length=100)
    body_html = HTMLField(default="<h1>hi</hi>")
    body_txt = models.TextField('body_txt')
    slug = models.SlugField('slug', max_length=255, )


    def __str__(self):
        return self.email_id
 
    def get_title(self):
        return self.title

    def get_html(self):
        return self.body_html

    def get_text(self):
        return self.body_txt

    def get_description(self):
        return self.description

    def get_subject(self):
        return self.subject

    def get_slug(self):
        return self.slug

    

    def save(self, *args, **kwargs):
        if not self.slug:
            name = self.title
            self.slug = slugify(name)
        if not self.body_txt:
            self.body_txt = textify(self.body_html)
        return super(E_mail, self).save(*args, **kwargs)