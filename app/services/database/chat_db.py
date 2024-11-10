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



def get_questions_and_count(bot_id:str):
    action = supabase.schema('public').rpc('chat_get_conversations_by_bot', {'botid': bot_id}).execute()
    return action.data, len(action.data)

def get_unique_users(bot_id:str):
    action = supabase.schema('public').rpc('chat_get_unique_user_count', {'botid': bot_id}).execute()
    return action.data, len(action.data)
    