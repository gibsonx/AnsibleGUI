from django.db import models

# Create your models here.


class Host(models.Model):
    hostname = models.CharField(max_length=16)
    ip = models.GenericIPAddressField(null=True,blank=True)
    port = models.IntegerField(null=True,blank=True)
    username = models.CharField(max_length=16,null=True,blank=True)
    password = models.CharField(max_length=16,null=True,blank=True)
    ssh_key = models.TextField(max_length=30,null=True,blank=True)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)

    def __str__(self):
        return self.hostname


class Group(models.Model):
    groupname = models.CharField(max_length=16)
    hosts = models.ManyToManyField(Host)

    def __str__(self):
        return self.groupname

class GroupVar(models.Model):
    key = models.CharField(max_length=16)
    value = models.CharField(max_length=16)
    group = models.ForeignKey(Group,on_delete=models.CASCADE,default='')

    def __str__(self):
        return self.key

class Tag(models.Model):
    usage = models.ManyToManyField(Host)
    name    = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name