from django.db import models


class Compute(models.Model):
    name = models.CharField(max_length=20)
    hostname = models.CharField(max_length=20)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=14, blank=True, null=True)
    type = models.IntegerField()

    def __unicode__(self):
        return self.hostname

class Instance(models.Model):
    compute = models.ForeignKey(Compute)
    name = models.CharField(max_length=20)
    uuid = models.CharField(max_length=36)
    # display_name = models.CharField(max_length=50)
    # display_description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name