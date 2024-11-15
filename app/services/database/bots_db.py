from app.extensions import supabase
from app.services.logging_manager import get_logger

logger = get_logger(__name__)

def create_new_bot(access_token, name, website_url, description, first_message, openai_key,owned_by=None):
    action = supabase.from_('bots').insert({"website_url": website_url,
                                              "name": name,
                                              "description": description,
                                              "first_message": first_message,
                                              "openai_key": openai_key})
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    
    return response.data

def mark_bot_as_complete(access_token, bot_id):
    action = supabase.from_('bots').update({"is_ready": True}).eq('id',bot_id)
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
    # logger.info('removal info', response.data)
    return response.data