from app.extensions import supabase

def create_internal_user_with_supabase_code(user, role:str = "CLIENT") -> bool:
    user_id = user.id
    response = supabase.from_('user_roles').select("*").eq('user_id',user_id).execute()
    if not response.data:
        response_db = supabase.table('user_roles').insert({"user_id":user_id, "role": role}).execute()
        return True
    return False

