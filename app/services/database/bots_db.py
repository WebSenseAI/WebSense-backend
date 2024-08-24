from app.extensions import supabase


def create_new_bot(access_token, name, website_url, description, first_message, openai_key,owned_by=None):
    action = supabase.from_('bots').insert({"website_url": website_url,
                                              "name": name,
                                              "description": description,
                                              "first_message": first_message,
                                              "openai_key": openai_key})
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    return response.data


def get_user_bot(userid):
    response = supabase.from_('bots').select('*').eq('owned_by',userid).execute()
    return response.data

def get_bot_by_id(botid):
    response = supabase.from_('bots').select('*').eq('id',botid).execute()
    return response.data

def remove_user_bot(userid):
    response = supabase.table('bots').delete().eq('owned_by', userid).execute()
    print(response)
    return response.count