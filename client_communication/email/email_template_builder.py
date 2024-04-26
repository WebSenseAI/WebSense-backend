from jinja2 import Environment, FileSystemLoader

def get_bot_ready_template(username, link="#"):
    env = Environment(loader=FileSystemLoader('templates/email'))
    template = env.get_template('bot_ready.html')
    data = {
        "username" : username,
        "link" : link
    }
    return template.render(data)