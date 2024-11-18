from flask import Blueprint, request, jsonify, Response
from app.constants.http_status_codes import SUCCESS_CODE
from app.services.supabase_client_utils import get_user_info
from app.services.database.bots_db import create_new_bot, get_user_bot, get_bot_by_id, remove_user_bot, mark_bot_as_complete
from app.services.database.chat_db import get_basic_stats, get_comprehensive_stats
from app.errors.http_error_templates import create_returnable_internal_error_template
from app.constants.internal_errors import InternalErrorCode
from app.services.ai_tools.vectors import add_text_to_vector_db
from app.services.ai_tools.openai_utils import get_embedding
from app.services.ai_tools.text import split_multiple_texts
from app.services.webscraping.scrapWrapper import trainNewBot
from app.extensions import vx
from app.models.vector_model import VectorModel
from app.security import authorization_required
from concurrent.futures import ThreadPoolExecutor
from app.services.logging_manager import get_logger



# Blueprint for user routes
users_bp = Blueprint('users_bp', __name__)

executor = ThreadPoolExecutor()
logger = get_logger(__name__)

@users_bp.route('/userinfo')
@authorization_required
def userinfo():
    userinfo = get_user_info(request.authorization.token)
    return jsonify(userinfo.model_dump()), SUCCESS_CODE
    
    
@users_bp.route('/bot/new', methods=['POST'])
@authorization_required
def create_bot():
    data = request.json
    access_token = request.authorization.token
    response = create_new_bot(
        access_token=access_token,
        name = data['name'],
        website_url=data['website'],
        description=data['description'],
        first_message=data['message'],
        openai_key=data['key']
    )
    botid = response[0]["id"]
    
    def train_bot_and_create_collection(_botid,_website,_access_token):
        try:
            logger.info(f'bot training started for {_botid}')

            pages = trainNewBot(_website, False)
            logger.info(f'Extracted {len(pages)} pages.')

            splitted_text = split_multiple_texts(pages)

            embeddings = get_embedding(splitted_text)
            logger.info(f'Embeddings created')
            

            vector_model = VectorModel(splitted_text,embeddings)
            
            logger.info('adding to vector_db')
            add_text_to_vector_db(vector_model, _botid)

            logger.info('Bot ready...')
            mark_bot_as_complete(access_token=_access_token, bot_id=_botid)
        except Exception as e:
            logger.error("error occured")
            logger.exception(e)
    executor.submit(train_bot_and_create_collection,
                    botid, data['website'], access_token)
    return {}, SUCCESS_CODE


@users_bp.route('/bot/info', methods=['GET'])
@authorization_required
def get_bot_info_by_user():
    user = get_user_info(request.authorization.token)
    userid = user.id
    bot_info = get_user_bot(userid)
    if not bot_info:
        return create_returnable_internal_error_template(InternalErrorCode.BotNotExist)
    
    return jsonify(bot_info[0]), SUCCESS_CODE


@users_bp.route('/bot/info/<botid>', methods=['GET'])
def get_bot_info_by_id(botid):
    
    bot_info = get_bot_by_id(botid)
    if not bot_info:
        return create_returnable_internal_error_template(InternalErrorCode.BotNotExist)
    return jsonify(bot_info[0]), SUCCESS_CODE

@users_bp.route('/bot/update', methods=['PUT'])
@authorization_required
def update_bot():
    return jsonify(request.json), SUCCESS_CODE

@users_bp.route('/bot/remove', methods=['DELETE'])
@authorization_required
def remove_bot():
    userid = get_user_info(request.authorization.token).id
    data = remove_user_bot(userid)
    botid = data[0]["id"]
    vx.delete_collection(botid)
    # TODO: maybe remove the bot_related questions from chat_repo
    return {}, SUCCESS_CODE
    

@users_bp.route('/stats/basic')
@authorization_required
def get_basic_stat():
    access_token = request.authorization.token
    user = get_user_info(access_token=access_token)
    userid = user.id
    bot_info = get_user_bot(userid)[0]
    botid = bot_info["id"]
    data = get_basic_stats(botid,access_token)
    return jsonify(data)

@users_bp.route('/stats/comp')
@authorization_required
def get_comp_stat():
    access_token = request.authorization.token
    user = get_user_info(access_token=access_token)
    userid = user.id
    bot_info = get_user_bot(userid)[0]
    botid = bot_info["id"]
    data = get_comprehensive_stats(botid,access_token)
    return jsonify(data)



@users_bp.route('/statistics/basic')
@authorization_required
def get_basic_statistics():
    access_token = request.authorization.token
    user = get_user_info(access_token=access_token)
    userid = user.id
    bot_info = get_user_bot(userid)[0]
    botid = bot_info["id"]
    data = get_basic_stats(bot_id=botid,access_token=access_token)
    return jsonify(data), SUCCESS_CODE

@users_bp.route('/statistics/comprehensive')
@authorization_required
def get_comprehensive_statistics():
    access_token = request.authorization.token
    user = get_user_info(access_token=access_token)
    userid = user.id
    bot_info = get_user_bot(userid)[0]
    botid = bot_info["id"]
    data_raw = get_comprehensive_stats(bot_id=botid, access_token=access_token)
    
    time_periods = {}
    time_periods_raw = data_raw["time_of_day_counter"]
    for period in time_periods_raw:
        time_periods[period['time_of_day']] = period['count']

    data = {
        "message_count": data_raw["message_count"],
        "user_count": data_raw["user_count"],
        "countries" : data_raw["country_stats"] if data_raw["country_stats"] else [],
        "country_count" : len(data_raw["country_stats"]) if data_raw["country_stats"] else 0,
        "time_periods" : time_periods,
        "top_words" : data_raw["top_words_weekly"] if data_raw["top_words_weekly"] else []
    }

    return jsonify(data), SUCCESS_CODE