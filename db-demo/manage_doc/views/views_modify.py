"""Modify API for admin
    By Liu Chang
"""
import json

from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from manage_doc.utils import gen_response
from manage_doc.models import Document
from manage_user.models import User


return_status = {
            "code": 200,
            "message": "操作成功~"
        }
error_code = {
    "non_field": 1,
    "null": 2,
    "negative": 3,
    "data_type_error": 4,
    "document_id_invalid": 5,
    "document_exist": 6,
    "document_deleted": 7,
    "user_id_invalid": 8,
    "user_not_admin": 9,
    "unknown_type": 10,
    "content_empty": 11,
    "db_validation_err": 12,
    "json_decode_err": 13,
}

type_del = "delete"
type_fetch = "fetch"
type_modify = "modify"
type_restore = "restore"


def set_return_status(code, message):
    """
    Set return status
    """
    return_status["code"] = code
    return_status["message"] = message


def check_fields(expected_fields, fields):
    """
    检查前端返回的Json串对应的字段是否都有
    """
    for field in expected_fields:
        if field not in fields:
            set_return_status(400, json.dumps({
                "code": error_code["non_field"],
                "detail": "{}字段不存在~".format(field)
            }))
            return False
    return True


def check_string_valid(name, string):
    """
    检查字符串是否合法
    """
    # 如果本来就是int，合法
    if isinstance(string, int):
        return True

    # 如果是字符串，判断一下
    if isinstance(string, str):
        if not string:
            # set_return_status(400, "{} shouldn't be null!".format(name))
            set_return_status(400, json.dumps({
                "code": error_code["null"],
                "detail": "{}不应该为空~".format(name)
            }))
            return False
        if string.isdigit() is False:
            # set_return_status(400, "{} should be a positive integer!".format(name))
            set_return_status(400, json.dumps({
                "code": error_code["negative"],
                "detail": "{}应该为正整数~".format(name)
            }))
            return False
        return True

    # 如果都不是，报错
    set_return_status(400, json.dumps({
        "code": error_code["data_type_error"],
        "detail": "{}的类型应该是整型或者字符串类型~".format(string)
    }))
    return False


def check_user(user_id, api):
    """
    检查用户有关的一切合法性
    """
    if check_string_valid("user_id", user_id) is False:
        return False
    user = User.objects.filter(pk=user_id).first()
    if not user:
        if api == 'modify':
            set_return_status(400, json.dumps({
                "code": error_code["user_id_invalid"],
                "detail": "用户id{}非法~".format(user_id)
            }))
        else:
            set_return_status(400, "用户id{}非法~".format(user_id))
        return False
    if user.is_admin is False:
        if api == 'modify':
            set_return_status(400, json.dumps({
                "code": error_code["user_not_admin"],
                "detail": "该用户不是管理员，无权限进行此操作~"
            }))
        else:
            set_return_status(400, "该用户不是管理员，无权限进行此操作~")
        return False
    return True


def check_document(document_id):
    """
        检查文档有关的一切合法性
    """
    if check_string_valid("document_id", document_id) is False:
        return None
    document = Document.objects.filter(pk=document_id).first()
    if not document:
        set_return_status(400, json.dumps({
            "code": error_code["document_id_invalid"],
            "detail": "文档id{}非法~".format(document_id)
        }))
        return None
    return document


def check_type(op_type):
    """
    检查操作类型是否正确
    """
    if op_type not in (type_del, type_fetch, type_modify, type_restore):
        set_return_status(400, json.dumps({
            "code": error_code["unknown_type"],
            "detail": "未知操作~"
        }))
        return False
    return True


def check_content(content):
    """
    检查是否有内容
    """
    if not content:
        set_return_status(400, json.dumps({
            "code": error_code["content_empty"],
            "detail": "请直接删除该文档~"
        }))
        return False
    return True


def transac_fetch(user_id, document):
    """
    Fetch operation
    """
    if document.status == 0:
        set_return_status(200, json.dumps({"user_id": user_id, "content": document.content}))
    else:
        set_return_status(400, json.dumps({
            "code": error_code["document_deleted"],
            "detail": "该文档已经被删除了~"
        }))


def transac_modify(user_id, document, received_data):
    """
    Modify operation
    """
    if document.status == 1:
        set_return_status(400, json.dumps({
            "code": error_code["document_deleted"],
            "detail": "该文档已经被删除了~"
        }))
        return
    if "content" not in received_data.keys():
        set_return_status(400, json.dumps({
            "code": error_code["non_field"],
            "detail": "content字段不存在~"
        }))
        return
    content = received_data["content"]
    if check_content(content):
        try:
            # 如果save失败了，数据库内容不会改动
            document.content = content
            document.full_clean()
            document.save()
        except ValidationError:
            set_return_status(400, json.dumps({
                "code": error_code["db_validation_err"],
                "detail": "文档验证失败~"
            }))
        set_return_status(200, json.dumps({"user_id": user_id}))
        return


def transac_del(user_id, document):
    """
    Delete operation
    """
    if document.status == 1:
        set_return_status(400, json.dumps({
            "code": error_code["document_deleted"],
            "detail": "该文档已经被删除了~"
        }))
        return
    try:
        document.status = 1
        document.full_clean()
        document.save()
    except ValidationError:
        set_return_status(400, json.dumps({
            "code": error_code["db_validation_err"],
            "detail": "文档验证失败~"
        }))
    set_return_status(200, json.dumps({"user_id": user_id}))
    return


def transac_restore(user_id, document):
    """
    Restore operation
    """
    if document.status == 0:
        set_return_status(400, json.dumps({
            "code": error_code["document_exist"],
            "detail": "文档已经存在，无需恢复~"
        }))
        return

    try:
        document.status = 0
        document.full_clean()
        document.save()
    except ValidationError:
        set_return_status(400, json.dumps({
            "code": error_code["db_validation_err"],
            "detail": "文档验证失败~"
        }))
    set_return_status(200, json.dumps({"user_id": user_id,
                                       "content": document.content}))


def transaction(user_id, op_type, document, received_data):
    """
    op_type: 操作类型
    document: 执行事务的文档
    user_id: 对应的用户编号
    """
    if op_type == type_fetch:
        transac_fetch(user_id, document)
        return

    if op_type == type_modify:
        transac_modify(user_id, document, received_data)
        return

    if op_type == type_del:
        transac_del(user_id, document)
        return

    if op_type == type_restore:
        transac_restore(user_id, document)

    return


@csrf_exempt
def modify(request):
    """
    经过重构的modify函数
    """
    # 进入对应的函数时，改变全局变量为最开始的值
    set_return_status(200, "操作成功~")
    assert request.method == "POST"
    try:
        received_data = json.loads(request.body)
        fields = received_data.keys()
        expected_fields = ["type", "user_id", "document_id"]
        # 各字段都有
        if check_fields(expected_fields, fields):
            user_id = received_data["user_id"]
            document_id = received_data["document_id"]
            op_type = received_data["type"]
            # user_id格式正确&user是管理员&&操作类型正确&&文档正确
            if check_user(user_id, "modify") and check_type(op_type):
                document = check_document(document_id)
                print(document_id)
                # 如果document存在
                if document:
                    transaction(user_id=user_id,
                                   op_type=op_type,
                                   document=document,
                                   received_data=received_data)
                    return gen_response(return_status["code"], return_status["message"])

    except (ValueError, TypeError) as exception:
        set_return_status(400, json.dumps({
            "code": error_code["json_decode_err"],
            "detail": "Json解码失败~ {}".format(exception)
        }))

    return gen_response(return_status["code"], return_status["message"])


def check_cookies(expected_fields, cookies):
    """
    Check cookies fields
    """
    dic = cookies.keys()
    for field in expected_fields:
        if field not in dic:
            set_return_status(405, "Cookies没有{}字段~".format(field))
            return False
    return True


def check_upload_file_format(received_data):
    """
    后端检查文件基本格式是否正确
    """
    if 'data' in received_data.keys() and received_data['data'] is not None \
            and 'paragraphs' in received_data['data'][0].keys():
        return True
    set_return_status(401, "您上传的文档格式错误~")
    return False


def transac_upload(received_data):
    """
    Transac upload files
    """
    id_range = []
    if check_upload_file_format(received_data):
        paragraphs = received_data["data"][0]["paragraphs"]
        i, count = 0, len(paragraphs)
        print(count)
        for paragraph in paragraphs:
            i += 1
            if 'context' in paragraph.keys() and 'title' in paragraph.keys():
                content = paragraph["context"]
                title = paragraph["title"]
                new_document = Document(content=content, status=0, title=title, src=0)
                try:
                    new_document.full_clean()
                    new_document.save()
                    if i in (1, count):
                        id_range.append(new_document.id)
                        print(new_document.id)
                except ValidationError:
                    set_return_status(403, "文档验证失败~")
                    return False
            else:
                continue
        if len(id_range) > 1:
            set_return_status(200, json.dumps({"document_id": "{}~{}"
                                                .format(id_range[0], id_range[1])}))
            return True
        if len(id_range) == 1:
            set_return_status(200, json.dumps({"document_id": id_range[0]}))
            return True

        set_return_status(402, json.dumps("您上传的文档中缺乏title或者context字段~"))
        return False
    return False


@csrf_exempt
def upload(request):
    """

    Args:
        request: HttpRequest

    Returns:
        JsonResponse

    """
    # 进入upload函数时，先改变全局变量为最开始的值
    set_return_status(200, "操作成功~")
    # 与前端对接request的user_id，判断是否有权限
    # assert request.method == "POST"
    print(type(request.body))

    if check_cookies(expected_fields=['user_id', 'username'], cookies=request.COOKIES):
        user_id = request.COOKIES['user_id']
        if check_user(user_id, "upload"):
            # utf-8 or gbk or utf-8-sig
            try:
                string = request.FILES.get('file').read().decode("utf-8")
                string = string.strip(b'\xef\xbb\xbf'.decode()).strip()

                try:
                    received_data = json.loads(string)
                    transac_upload(received_data)
                except (ValueError, TypeError) as exception:
                    set_return_status(406, "Json解码失败~ {}".format(exception))
            except (UnicodeDecodeError, UnicodeError):
                set_return_status(407, "请上传以utf-8格式编码的文件~")

    return gen_response(return_status['code'], return_status['message'])
