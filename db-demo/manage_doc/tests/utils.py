"""
Some util functions for test
"""


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
