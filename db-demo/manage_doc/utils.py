"""Some utility functions for manage_doc
    By Liu Chang
"""
from django.http import JsonResponse


def gen_response(code: int, data: str):
    """

    Args:
        code: status_code
        data: request.body

    Returns:
        JsonResponse

    """
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code, charset='utf-8', json_dumps_params={'ensure_ascii': False})
