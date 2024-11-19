from app.extensions import supabase
from app.services.logging_manager import get_logger

logger = get_logger(__name__)

def create_new_bot(access_token, name, website_url, description, first_message, openai_key,owned_by=None):
    action = supabase.schema('public').from_('bots').insert({"website_url": website_url,
                                              "name": name,
                                              "description": description,
                                              "first_message": first_message,
                                              "openai_key": openai_key})
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    
    return response.data

def mark_bot_as_complete(access_token, bot_id):
    action = supabase.schema('public').from_('bots').update({"is_ready": True}).eq('id',bot_id)
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    
    return response.data

def get_user_bot(userid, access_token):
    action = supabase.schema('public').from_('bots').select('*').eq('owned_by',userid)
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    return response.data

def get_bot_by_id(botid,access_token):
    action = supabase.schema('public').from_('bots').select('*').eq('id',botid)
    action.headers["Authorization"] = "Bearer " + access_token
    response = action.execute()
    return response.data

def remove_user_bot(userid, access_token):
    action = supabase.schema('public').table('bots').delete().eq('owned_by', userid)
    action.headers["Authorization"] = 'Bearer ' + access_token
    response = action.execute()

    action_collections = supabase.schema('scrap_collections').rpc('vector_remove_collection', {
        "collection_id" : response.data[0]["id"]
    })
    action_collections.headers["Authorization"] = 'Bearer ' + access_token
    response_collections = action_collections.execute()
    return response.data, response_collections.data