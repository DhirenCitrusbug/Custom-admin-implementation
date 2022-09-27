import sendgrid
import os

from django.conf import settings
from sendgrid.helpers.mail import Email, Substitution, Mail, Personalization
from python_http_client import exceptions
from reeach_will.settings import SENDGRID_API_KEY


def send_templated_email(to_email, email_temlpate_id, dynamic_data_for_template):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    personalization = Personalization()
    personalization.add_to(Email(to_email))
    mail = Mail()
    mail.from_email = Email(settings.FROM_EMAIL)
    mail.template_id = email_temlpate_id
    personalization.dynamic_template_data = dynamic_data_for_template
    mail.add_personalization(personalization)
    try:
        print('.......................Send')
        response = sg.client.mail.send.post(request_body=mail.get())
    except exceptions.BadRequestsError as e:
        print(e.body)
        pass
        # exit()


#    dyanmic_data_for_template = {
#     'plan_name':plan.name,
#     'plan_comments':plan_comments,
#     'features':features
# }
# send_templated_email(seller.email, SEND_PLAN_TO_SELLER_TEMPLATE_ID, dyanmic_data_for_template)