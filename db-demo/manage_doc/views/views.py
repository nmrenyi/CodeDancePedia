"""
Test API about docs
By Liu Chang
"""

from manage_doc.models import Document
from manage_doc.utils import gen_response


def show_all(request):
    """Show all the docs in db

    Args:
        request: http_request

    Returns:

    """
    all_data = str([
        {
            'id': doc.id,
            'status': doc.status,
            'content': doc.content,
        }
        for doc in Document.objects.all()
    ])
    return gen_response(200, all_data)


def add(request):
    """Add a doc

    Args:
        request: http_request

    Returns:

    """
    return gen_response(200, 'nothing added')
