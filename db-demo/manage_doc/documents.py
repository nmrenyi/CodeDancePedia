'''
Supervisor of the db change for Elastic Search
# The name of this file must be documents.py to meet django_elasticsearch_dsl need
# see more at https://django-elasticsearch-dsl.readthedocs.io/en/latest/quickstart.html

By RenYi
'''

from django_elasticsearch_dsl import Document as ESDocument
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import fields
from .models import Document as MyDocument


@registry.register_document
class ElasticSearchDocument(ESDocument):
    '''
    Elastic Search Management Class
    '''
    class Index:
        '''
        Elastic Search Index Management
        '''
        # Name of the Elasticsearch index
        name = 'mydocument' # must be lowercase for es requirements
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    content = fields.TextField(
        analyzer="ik_max_word",
        search_analyzer="ik_smart",
    )
    title = fields.TextField(
        analyzer="ik_max_word",
        search_analyzer="ik_smart",
    )
    class Django:
        '''
        Django Supervisor for Elastic Search
        can auto update ES when encountering db change
        '''
        model = MyDocument # The model associated with this ES Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'status',
            'src'
            # 'content', # configured manually above (Due to Chinese analyzer)
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
        # queryset_pagination = 5000
