from app.extensions import supabase


def insert_new_question(bot_id:str, question: str, response: str):
    action = supabase.from_('chat_repo').insert({
        "question" : question,
        "answer" :  response,
        "bot_id" : bot_id
    })
    response = action.execute()
    return response.data

