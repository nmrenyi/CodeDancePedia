"""
views_search.py
processing requests
"""

from django.http import HttpResponse
import prometheus_client as prometheus


def index(request):
    """
    index
    """
    return HttpResponse('Hello World! Welcome to CodeDance Project!(Need runserver!)')

def metrics(request):
    '''
    Serve prometheus metrics
    ref to monolithic example repo
    '''
    metrics_page = prometheus.generate_latest(prometheus.REGISTRY)
    return HttpResponse(metrics_page,
                        content_type=prometheus.CONTENT_TYPE_LATEST)
