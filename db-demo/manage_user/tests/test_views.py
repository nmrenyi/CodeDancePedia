"""Test file for manage_user views.py
    By Liu Chang
"""
import json
import pytest
from manage_user.models import User
from manage_user.views import register, login


def gen_request(rf, url, data):
    """

    Args:
        rf: RequestFactory
        url: post_url
        data: request.body

    Returns:
        HttpRequest

    """
    # post urls end with slash
    content_type = 'application/json'
    return rf.post(path=url, content_type=content_type, data=data)


def gen_GET_request(rf, url, data):
    """
    Generate GET HttpRequest
    """
    return rf.get(path=url, content_type='application/json', data=data)


@pytest.fixture(scope="function")
def register_requests(rf):
    """Test user register

    Args:
        rf: Request Factory

    Returns:

    """
    post_url = '/user/register/'
    request_succ = [{
        "request": gen_request(rf, post_url, {
            "username": "user1",
            "password": "123456",
            "password_confirmed": "123456"
        }),
        "response": {
            "code": 200
        }
    }]

    request_no_field = [{
        "request": gen_request(rf, post_url, {
            "password": "123456",
            "password_confirmed": "123456"
        }),
        "response": {
            "code": 400,
            "data": "Username doesn't exist!",
        }
    }, {
        "request": gen_request(rf, post_url, {
            "username": "admin",
            "password_confirmed": "123456"
        }),
        "response": {
            "code": 400,
            "data": "Password doesn't exist!"
        }
    }, {
        "request": gen_request(rf, post_url, {
            "username": "admin",
            "password": "123456"
        }),
        "response": {
            "code": 400,
            "data": "Password_confirmed doesn't exist"
        }
    }]
    request_diff_password = [{
        "request": gen_request(rf, post_url, {
            "username": "user2",
            "password": "123457",
            "password_confirmed": "abcdef"
        }),
        "response": {
            "code": 400,
            "data": "Password is not equal to password_confirmed!"
        }
    }, {
        "request": gen_request(rf, post_url, {
            "username": "user3",
            "password": "tsinghua_university",
            "password_confirmed": "tsinhua _university"
        }),
        "response": {
            "code": 400,
            "data": "Password is not equal to password_confirmed!"
        }
    }]
    request_username_duplicate = [{
        "request": gen_request(rf, post_url, {
            "username": "admin",
            "password": "123456",
            "password_confirmed": "123456"
        }),
        "response": {
            "code": 400,
            "data": "Username already exists!"
        }
    }]
    request_blank_username = [{
        "request": gen_request(rf, post_url, {
            "username": "",
            "password": "123456",
            "password_confirmed": "123456"
        }),
        "response": {
            "code": 400,
            "data": "A naive data because we won't check that1"
        }
    }]
    request_invalid_json = [{
        "request": gen_request(rf, post_url, {
            'null'
        }),
        "response": {
            "code": 400,
            "data": "A naive data because we won't check that2"
        }
    }]
    request_list = request_succ + request_no_field + request_diff_password + \
                   request_username_duplicate + request_blank_username + \
                   request_invalid_json

    return request_list


@pytest.mark.django_db
def test_register(register_requests):
    """Test user register

    Returns:
        bool: successful or not
    """
    # insert a record of admin in advance
    admin = User(username="admin", email="CodeDance@mails.tsinghua.edu.cn",
                 password="123456", is_admin=True, query_json="")
    admin.full_clean()
    admin.save()

    for request in register_requests:
        print(request["request"])
        print(request["request"].body)
        response = register(request["request"])
        print(response)
        assert response.status_code == request["response"]["code"]


@pytest.fixture(scope="function")
def login_requests(rf):
    """

    Args:
        rf: RequestFactory, a fixture with scope="function"

    Returns:
        fixture
    """
    post_url = '/user/login/'
    request_succ = [{
        "request": gen_request(rf, post_url, {
            "username": "user1",
            "password": "qwerty123456"
        }),
        "response": {
            "code": 200,
            "data": json.dumps({
                "username": "user1",
                "user_id": 2
            })
        }
    }]

    request_no_field = [{
        "request": gen_request(rf, post_url, {
            "username": "user1"
        }),
        "response": {
            "code": 400,
            "data": "Password doesn't exist!"
        }
    }, {
        "request": gen_request(rf, post_url, {
            "password": "fdfsfsdasdfvfd"
        }),
        "response": {
            "code": 400,
            "data": "Username doesn't exist!"
        }
    }]

    request_not_register = [{
        "request": gen_request(rf, post_url, {
            "username": "user_k",
            "password": "user_k_password"
        }),
        "response": {
            "code": 400,
            "data": "You have not registered yet, please sign up first!"
        }
    }]

    request_invalid_password = [{
        "request": gen_request(rf, post_url, {
            "username": "user1",
            "password": "12dfs4dfd43247hfuehfu"
        }),
        "response": {
            "code": 400,
            "data": "Password is wrong!"
        }
    }, {
        "request": gen_request(rf, post_url, {
            "username": "user_2",
            "password": "1dsfd43gggdsfshfuehfu"
        }),
        "response": {
            "code": 400,
            "data": "Password is wrong!"
        }
    }]

    request_decode_error = [{
        "request": gen_request(rf, post_url, {
            'null'
        }),
        "response": {
            "code": 400,
            "data": "Decode Error of json"
        }
    }]
    request_list = request_succ + request_no_field + request_not_register +\
                   request_invalid_password + request_decode_error
    return request_list


@pytest.mark.django_db
def test_login(login_requests):
    """Test user login
    Args:
        login_requests: fixture
    Returns:
    """
    # tests are independent from each other,
    # so we should save some initial data into database first
    admin = User(username="admin", email="CodeDance@mails.tsinghua.edu.cn",
                 password="123456", is_admin=True, query_json="")
    user1 = User(username="user1", email="CodeDance@mails.tsinghua.edu.cn",
                 password="qwerty123456", is_admin=False, query_json="")
    user2 = User(username="user_2", email="CodeDance@mails.tsinghua.edu.cn",
                 password="asdfgh098765", is_admin=False, query_json="")
    user_lst = [admin, user1, user2]
    for user in user_lst:
        user.full_clean()
        user.save()

    for request in login_requests:
        response = login(request["request"])
        assert response.status_code == request["response"]["code"]
        print(response.content)
        print(type(json.loads(response.content)["data"]))
        # assert json.loads(response.content)["data"].startswith(request["response"]["data"])
