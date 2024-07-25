from app.extensions import supabase


def create_new_bot(name, website_url, description, first_message, openai_key,owned_by=None):
    response = supabase.from_('bots').insert({"website_url": website_url,
                                              "name": name,
                                              "description": description,
                                              "first_message": first_message,
                                              "openai_key": openai_key}).execute()
    print(response)
