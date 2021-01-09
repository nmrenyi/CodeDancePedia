"""Models for manage_doc app
    By Liu Chang

"""
from django.db import models


# Create your models here.
class Document(models.Model):
    """Document model

    """
    # 文档id
    id = models.AutoField(primary_key=True)
    # 是否已经被删除
    STATUS_CHOICES = (
        (0, 'existent'),
        (1, 'deleted')
    )
    status = models.IntegerField(choices=STATUS_CHOICES)

    # 文档内容
    content = models.TextField()
    # 文档标题
    title = models.TextField(default="")
    SRC_CHOICES = (
        (-1, 'default'),          # initialized status
        (0, 'upload'),           # 13887577~
        (1, 'cmrc'),             # 1~3057
        (2, 'search.train'),    # 3508~7692335
        (3, 'zhidao.train'),    # 7692336~9500276
        (4, 'search.dev'),      # 9500277~9716056
        (5, 'zhidao.dev'),      # 9716057~9775518
        (6, 'search.test'),     # 9775519~13062638
        (7, 'zhidao.test'),     # 13062639~13887576
    )
    src = models.IntegerField(default=-1, choices=SRC_CHOICES)
