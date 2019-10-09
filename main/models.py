from django.db import models
from django.utils.timezone import now

# Simpliest Model:
# Language
#       - Library 1
#                  - Method 1
#                  - Method 2
#                  ...
#       - Library 2
#       ...

class Language(models.Model):
    language_name = models.CharField(max_length=100)
    library_count = models.IntegerField(default=0)
    date_added = models.DateTimeField("Date created", default=now)

    def __str__(self):
        return str(self.language_name)

class Library(models.Model):
    library_name = models.CharField(max_length=100)
    method_count = models.IntegerField(default=0)
    date_added = models.DateTimeField("Date created", default=now)
    parent_language = models.ForeignKey(Language, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Libraries"

    def __str__(self):
        return str(self.library_name)

class Method(models.Model):
    method_name = models.CharField(max_length=100)
    use_example = models.CharField(max_length=200, default="")
    short_description = models.CharField(max_length=200, default="")
    long_description = models.TextField(blank=True, default="")
    date_added = models.DateTimeField("Date created", default=now)
    parent_library = models.ForeignKey(Library, blank=True, null=True, on_delete=models.CASCADE)
    parent_language = models.ForeignKey(Language, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.method_name)