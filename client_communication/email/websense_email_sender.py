import client_communication.email.email_template_builder as etb
import client_communication.email.gmail_api_tools as gat


def send_new_bot_email(username, receiver, link='#'):
    subject = 'WebSenseAI: Your bot is ready!'
    template = etb.get_bot_ready_template(username=username, link=link)
    gat.send_email_with_template(receiver=receiver,
                                 subject=subject,
                                 html_content=template)
