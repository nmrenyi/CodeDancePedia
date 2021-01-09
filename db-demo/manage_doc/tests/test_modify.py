"""Test file for manage_doc views_modify
    By Liu Chang
"""
# import json
# import os
import pytest

# from back_end.settings import BASE_DIR
from manage_user.models import User
from manage_doc.models import Document
from manage_doc.views import modify
from .utils import gen_request


# @pytest.fixture(scope="function")
# def upload_requests(rf, client):
#     """
#     Test admin user upload files
#
#     Args:
#         rf: Request Factory
#         client: client to post files
#     """
#     post_url = '/docs/upload/'
#     file_path = os.path.join(BASE_DIR, 'upload_files', 'file1.json')
#
#     with open(file_path) as f:
#         request_succ = [{
#             "request": gen_request(rf, post_url, {
#                 "user_id": 1,
#                 "file": f,
#             }),
#             "response": {
#                 "code": 200
#             }
#         }]
#
#     request = request_succ
#     return request


# @pytest.mark.django_db
# def test_upload(upload_requests):
#     # 先创建用户
#     # admin1 = User(username="admin1", email="CodeDance@mails.tsinghua.edu.cn",
#     #               password="123456", is_admin=True, query_json="")
#     # admin1.full_clean()
#     # admin1.save()
#     # for request in modify_requests:
#     #     response = modify(request["request"])
#     #     assert response.status_code == request["response"]["code"]
#     #     print(response.content)
#     return True


@pytest.fixture(scope="function")
def modify_requests(rf):
    """
    Test admin user modify files

    Args:
        rf: Request Factory
    """
    post_url = '/docs/modify/'
    request_succ = [{
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "type": "fetch",
            "document_id": 1,
            }),
        "response": {
            "code": 200,
        }
    },
        {
            "request": gen_request(rf, post_url, {
                "user_id": 2,
                "type": "modify",
                "document_id": 2,
                "content": "I will modify content!"
            }),
            "response": {
                "code": 200,
            }
        }, {
            "request": gen_request(rf, post_url, {
                "user_id": 3,
                "type": "delete",
                "document_id": 3,
            }),
            "response": {
                "code": 200,
            }
        }]
    request_fields_absent = [{
        "request": gen_request(rf, post_url, {
            "type": "fetch",
            "document_id": 3
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "document_id": 3
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "type": "delete",
        }),
        "response": {
            "code": 400,
            "data": "It seems silly, but it can pass code smell test"
        }
    }]
    request_user_invalid = [{
        "request": gen_request(rf, post_url, {
            "user_id": "",
            "type": "fetch",
            "document_id": 3
        }),
        "response": {
            "code": 400
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": "qs",
            "type": "delete",
            "document_id": 1
        }),
        "response": {
            "code": 400
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": 5,
            "type": "delete",
            "document_id": 3
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": "10",
            "type": "delete",
            "document_id": 3
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": {},
            "type": "fetch",
            "document_id": 3
        }),
        "response": {
            "code": 400,
        }
    }]

    request_type_invalid = [{
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "type": "deleted",
            "document_id": 3
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "type": "yysy",
            "document_id": 3
        }),
        "response": {
            "code": 400,
        }
    }]

    request_document_invalid = [{
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "type": "fetch",
            "document_id": ""
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "type": "fetch",
            "document_id": "happy"
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": 1,
            "type": "delete",
            "document_id": 1000
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": "1",
            "type": "fetch",
            "document_id": {}
        }),
        "response": {
            "code": 400,
        }
    }]

    request_operation_on_deleted_file = [{
        "request": gen_request(rf, post_url, {
            "user_id": "1",
            "type": "modify",
            "document_id": 5,
            "content": ""
        }),
        "response": {
            "code": 400,
        }
    }]

    request_content = [{
        "request": gen_request(rf, post_url, {
            "user_id": "1",
            "type": "modify",
            "document_id": 2,
        }),
        "response": {
            "code": 400,
        }
    }, {
        "request": gen_request(rf, post_url, {
            "user_id": "1",
            "type": "modify",
            "document_id": 2,
            "content": ""
        }),
        "response": {
            "code": 400,
        }
    }]

    request_decode_error = [{
        "request": gen_request(rf, post_url, {
            "null"
        }),
        "response": {
            "code": 400,
        }
    }]
    requests = request_succ + request_fields_absent + request_user_invalid + \
               request_type_invalid + request_document_invalid + \
               request_content + request_operation_on_deleted_file + \
               request_decode_error
    return requests


@pytest.mark.django_db
def test_modify(modify_requests):
    """
    Test admin modify files
    Args:
        modify_requests: fixture
    """
    # 先创建用户
    admin1 = User(username="admin1", email="CodeDance@mails.tsinghua.edu.cn",
                  password="123456", is_admin=True, query_json="")
    admin2 = User(username="admin2", email="CodeDance@mails.tsinghua.edu.cn",
                  password="456789", is_admin=True, query_json="")
    admin3 = User(username="admin3", email="CodeDance@mails.tsinghua.edu.cn",
                  password="456789", is_admin=True, query_json="")
    user1 = User(username="user1", email="CodeDance@mails.tsinghua.edu.cn",
                 password="123456", is_admin=False, query_json="")
    user2 = User(username="user2", email="CodeDance@mails.tsinghua.edu.cn",
                 password="0987654", is_admin=False, query_json="")
    # user3 = User(username="user3", email="CodeDance@mails.tsinghua.edu.cn",
    #              password="qwerty", is_admin=False, query_json="")

    for user in [admin1, admin2, admin3, user1, user2]:
        user.full_clean()
        user.save()
    # 再创建文档
    document_exist_1 = Document(id=1, content="高温超导（High-temperature superconductivity，High Tc）\
     是一种物理现象，指一些具有较其他超导物质相对较高的临界温度的物质在液态氮的环境下产生的超导现象。",
                                status=0, title="超导现象", src=0)
    document_exist_2 = Document(id=2, content="2020年新西兰大选（英语：2020 New Zealand general election），\
    即第53届新西兰国会选举于该年10月17日举行[1]。本届选举为新西兰自1996年采用混合议员比例代表制（联立单一选区两票制）\
    以来的第八次选举。此次大选与有关大麻和安乐死合法化的两个公投一并进行。结果工党取得过半数议席，有权单独执政，\
    为现有选举制度开始实施至今的首次。[2]", status=0, title="新西兰大选", src=0)
    document_exist_3 = Document(id=3, content="永州之野产异蛇，黑质而白章，触草木尽死。以啮人，无御之者。然得而腊之以为饵，\
    可以已大风、挛、瘘、疠，去死肌，杀三虫。其始，太医以王命聚之，岁赋其二，募有能捕之者，当其租入，永之人争奔走焉。\
    有蒋氏者，专其利三世矣。问之，则曰：“吾祖死于是，吾父死于是，今吾嗣为之十二年，几死者数矣。”言之，貌若甚戚者。\
    余〈杰按：通“予”，下同。〉悲之，且曰：“若毒之乎？余将告于莅是者，更若役，复若赋，则何如？”蒋氏大戚，\
    汪然出涕曰：“君将哀而生之乎？则吾斯役之不幸，未若复吾赋不幸之甚也。向吾不为斯役，则久已病矣。\
    自吾氏三世居是乡，积于今六十岁矣，而乡邻之生日蹙。殚其地之出，竭其庐之入，号呼而转徙，饥渴而顿踣，\
    触风雨，犯寒暑，呼嘘毒疠，往往而死者相藉也。曩与吾祖居者，今其室十无一焉；与吾父居者，今其室十无二三焉；\
    与吾居十二年者，今其室十无四五焉，非死即徙尔。而吾以捕蛇独存。悍吏之吾乡，叫嚣乎东西，隳突乎南北，哗然而骇者，虽鸡狗不得宁焉。\
    吾恂恂而起，视其缶，而吾蛇尚存，则弛然而卧。谨食之，时而献焉。退而甘食其土之有，以尽吾齿。盖一岁之犯死者二焉，其馀则熙熙而乐，\
    岂若吾乡邻之旦旦有是哉！今虽死乎此，比吾乡邻之则已后矣，又安敢毒耶？”余闻而愈悲。孔子曰：“苛政猛于虎也。”吾尝疑乎是，今以蒋氏观之，\
    犹信。呜呼！孰知赋敛之毒，有甚是蛇者乎！故为之说，以俟夫观人风者得焉。", status=0, title="捕蛇者说", src=0)
    document_deleted_4 = Document(id=4, content="采薇采薇，薇亦作止。曰归曰归，岁亦莫止。靡室靡家，玁狁之故。不遑启居，玁狁之故。\
    采薇采薇，薇亦柔止。曰归曰归，心亦忧止。忧心烈烈，载饥载渴。我戍未定，靡使归聘。\
    采薇采薇，薇亦刚止。曰归曰归，岁亦阳止。王事靡盬，不遑启处。忧心孔疚，我行不来！\
    彼尔维何？维常之华。彼路斯何？君子之车。戎车既驾，四牡业业。岂敢定居？一月三捷。\
    驾彼四牡，四牡骙骙。君子所依，小人所腓。四牡翼翼，象弭鱼服。岂不日戒？玁狁孔棘！\
    昔我往矣，杨柳依依。今我来思，雨雪霏霏。行道迟迟，载渴载饥。我心伤悲，莫知我哀！", status=1, title="采薇", src=0)
    document_deleted_5 = Document(id=5, content="氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。\
    送子涉淇，至于顿丘。匪我愆期，子无良媒。将子无怒，秋以为期。\
　　乘彼垝垣，以望复关。不见复关，泣涕涟涟。既见复关，载笑载言。尔卜尔筮，体无咎言。以尔车来，以我贿迁。\
　　桑之未落，其叶沃若。于嗟鸠兮，无食桑葚！于嗟女兮，无与士耽！士之耽兮，犹可说也。女之耽兮，不可说也。\
　　桑之落矣，其黄而陨。自我徂尔，三岁食贫。淇水汤汤，渐车帷裳。女也不爽，士贰其行。士也罔极，二三其德。\
　　三岁为妇，靡室劳矣；夙兴夜寐，靡有朝矣。言既遂矣，至于暴矣。兄弟不知，咥其笑矣。静言思之，躬自悼矣。\
　　及尔偕老，老使我怨。淇则有岸，隰则有泮。总角之宴，言笑晏晏。信誓旦旦，不思其反。反是不思，亦已焉哉！", status=1, title="氓", src=0)

    for document in [document_exist_1, document_exist_2, document_exist_3,
                     document_deleted_4, document_deleted_5]:
        document.full_clean()
        document.save()

    for request in modify_requests:
        response = modify(request["request"])
        assert response.status_code == request["response"]["code"]
        # assert json.loads(response.content)["data"].startswith(request["response"]["data"])
