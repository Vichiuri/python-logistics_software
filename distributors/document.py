from django.db import models


class Document(models.Model):
    doc_name = models.CharField(max_length=100)

    def __str__(self):
        return self.doc_name
