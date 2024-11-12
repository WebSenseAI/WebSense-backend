from app.extensions import supabase

def insert_new_question(bot_id:str, question: str, response: str, metadata: dict):
    action = supabase.from_('chat_repo').insert({
        "question" : question,
        "answer" :  response,
        "bot_id" : bot_id,
        "requester_metadata": metadata
    })
    response = action.execute()
    return response.data



def get_questions_and_count(bot_id:str, access_token:str):
    action = supabase.schema('public').rpc('chat_get_conversations_by_bot', {'botid': bot_id})
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    return response.data, len(response.data)

def get_unique_users(bot_id:str, access_token:str):
    action = supabase.schema('public').rpc('chat_get_unique_user_count', {'botid': bot_id})
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    return response.data, len(response.data)


def get_countries(bot_id:str, access_token:str):
    action = supabase.schema('public').rpc('chat_get_country_stats', {'botid': bot_id})
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    return response.data, len(response.data)

def get_time_periods(bot_id:str, access_token:str):
    action = supabase.schema('public').rpc('chat_get_time_of_day', {'botid' : bot_id})
    action.headers['Authorization'] = 'Bearer ' + access_token
    response = action.execute()
    return response.data
    