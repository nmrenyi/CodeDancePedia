"""This module manage request of user
    By Liu Chang
"""
import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from manage_user.models import User

from utils import get_user

ERR_USERNAME_NON = "用户名字段不存在~"
ERR_USERID_NON = "用户id字段不存在~"
ERR_BIO_NON = "用户简介字段不存在~"
ERR_PWD_NON = "密码字段不存在~"
ERR_PWD_CON_NON = "确认密码字段不存在~"

ERR_PWD_NOT_MATCH = "两次输入密码不一致~"
ERR_USERNAME_REPEAT = "该用户名已经使用过了~"
ERR_USER_VALIDATION = "用户数据格式错误，无法保存进数据库~"
ERR_JSON_DECODE = "Json解码错误~"
ERR_NOT_REGISTER = "您尚未注册，请先注册账号~"
ERR_WRONG_PWD = "密码错误了哟~"
ERR_USERID_VALID = "用户id无效~"
ERR_UNKNOWN_ASK = '未知的ask参数: {}~'
ERR_WRONG_METHOD = "请求方式错误~"


def gen_response(code: int, data: str):
    """Generate json response

    Args:
        code (int): return status code
        data (str): return body

    Returns:
        JsonResponse: response
    """
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


@csrf_exempt
def register(request):
    """用户注册
        逻辑：前端传用户名和密码，先检测用户名是否重复
        若重复，则返回失败信息
        若不重复，则返回成功信息和用户id，用户名

    Args:
        request (HttpRequest): request received from front_end

    Returns:
        JsonResponse: response sent to front_end
    """
    print(request)
    try:
        received_data = json.loads(request.body)
        print(received_data)
        # 判断received_data中是否各个字段都有
        if "username" not in received_data.keys():
            return gen_response(400, ERR_USERNAME_NON)
        if "password" not in received_data.keys():
            return gen_response(400, ERR_PWD_NON)
        if "password_confirmed" not in received_data.keys():
            return gen_response(400, ERR_PWD_CON_NON)

        username = received_data["username"]
        # 用户密码加密
        # 密码形式<algorithm>$<iterations>$<salt>$<hash>
        password = received_data["password"]
        password_confirm = received_data["password_confirmed"]

        # 首先检查password和password_confirm是否相同
        if password != password_confirm:
            return gen_response(400, ERR_PWD_NOT_MATCH)
        # 检查用户名是否存在
        if User.objects.filter(username=username).count() > 0:
            return gen_response(400, ERR_USERNAME_REPEAT)

        # 前端加email字段
        email = "CodeDance@mails.tsinghua.edu.cn"
        new_user = User(username=username, email=email, password=password,
                    is_admin=False, query_json="")
        try:
            new_user.full_clean()
            new_user.save()
        except ValidationError:
            return gen_response(400, ERR_USER_VALIDATION)

        return gen_response(200, json.dumps({
            "username": username,
            "user_id": new_user.get_pk(),
        }))
        # return gen_response(200, "Backend received data!")

    except (ValueError, TypeError):
        return gen_response(400, ERR_JSON_DECODE)


@csrf_exempt
def login(request):
    """用户登录
        逻辑：前端传用户名和密码，先检测用户名是否存在
        若不存在，则返回失败信息
        若存在，则返回成功信息和用户id，用户名

    Args:
        request (HttpRequest): HttpRequest received from front_end

    Returns:
        JsonResponse: JsonResponse sent to front_end
    """
    print(request)
    try:
        received_data = json.loads(request.body)
        print(received_data)
        # 判断received_data中是否各个字段都有
        if "username" not in received_data.keys():
            return gen_response(400, ERR_USERNAME_NON)
        if "password" not in received_data.keys():
            return gen_response(400, ERR_PWD_NON)

        username = received_data["username"]
        password = received_data["password"]

        user = User.objects.filter(username=username).first()
        if not user:
            return gen_response(400, ERR_NOT_REGISTER)

        if password != user.get_password():
            return gen_response(400, ERR_WRONG_PWD)

        return gen_response(200, json.dumps({
            "username": username,
            "user_id": user.get_pk(),
        }))

    except (ValueError, TypeError):
        return gen_response(400, ERR_JSON_DECODE)


def get_history(request):
    """
    Get user history

    """
    assert request.method == 'GET'

    user_id = request.GET.get('user_id')
    ask = request.GET.get('ask')
    user = get_user(user_id)
    if not user:
        return gen_response(400, ERR_USERID_VALID)
    query_str = user.query_json
    history_dict = {'data': []}
    if not query_str:
        return gen_response(200, json.dumps(history_dict))

    if ask == 'history':
        query_lst = json.loads(query_str)['data']
        print(query_lst)

        for qa in query_lst[::-1]:
            qa_dict = dict()
            qa_dict['label'] = qa['question']
            qa_dict['children'] = list()
            for response in qa['response']:
                # get doc content by doc id
                qa_dict['children'].append({
                    "label": response['answer'],
                    "children": [{"label": response['content']}]
                })
            history_dict['data'].append(qa_dict)

        print(history_dict)
        return gen_response(200, json.dumps(history_dict, ensure_ascii=False))

    if ask == 'clearHistory':
        user.query_json = ''
        try:
            user.full_clean()
            user.save()
        except ValidationError:
            return gen_response(400, ERR_USER_VALIDATION)
        return gen_response(200, json.dumps(history_dict, ensure_ascii=False))
    return gen_response(400, ERR_UNKNOWN_ASK.format(ask))


@csrf_exempt
def get_info(request):
    """
    Get or modify user info
    """
    # 获取用户信息
    if request.method == 'GET':
        print(request.GET)
        user_id = request.GET.get('user_id')
        print(user_id)
        user = get_user(user_id)
        if not user:
            return gen_response(400, ERR_USERID_VALID)

        # bio如果为NULL，而不仅仅只是空串
        bio = user.bio
        if not bio:
            bio = ""

        return gen_response(200, json.dumps({
            "user_id": user_id,
            "username": user.username,
            "bio": bio,
            "password": user.password
        }, ensure_ascii=False))

    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            if 'user_id' not in received_data.keys():
                return gen_response(400, ERR_USERID_NON)
            if 'username' not in received_data.keys():
                return gen_response(400, ERR_USERNAME_NON)
            if 'bio' not in received_data.keys():
                return gen_response(400, ERR_BIO_NON)
            if 'password' not in received_data.keys():
                return gen_response(400, ERR_PWD_NON)

            user_id = received_data['user_id']
            user = get_user(user_id)
            if not user:
                return gen_response(400, ERR_USERID_VALID)

            username = received_data['username']
            # 如何判断用户名重复？
            if User.objects.filter(username=username).count() > 1:
                return gen_response(400, ERR_USERNAME_REPEAT)

            user.username = username
            user.bio = received_data["bio"]
            user.password = received_data["password"]

            try:
                user.full_clean()
                user.save()
            except ValidationError:
                return gen_response(400, ERR_USER_VALIDATION)

            return gen_response(200, json.dumps({
                "username": username,
                "user_id": user.get_pk(),
                "bio": user.bio
            }, ensure_ascii=False))

        except (ValueError, TypeError):
            return gen_response(400, ERR_JSON_DECODE)

    return gen_response(400, ERR_WRONG_PWD)
