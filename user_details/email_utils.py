from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_password_reset_email(subject, template_name, context, from_email, to_email):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)