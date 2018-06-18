from django.db import models

# Create your models here.
class Authority(models.Model):
    authority = models.IntegerField()
    def __str__(self):
        return str(self.authority)
class User(models.Model):
    account = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    authority = models.ForeignKey('Authority',on_delete=models.CASCADE,)
    def __str__(self):
        return self.account

class Key(models.Model):
    account = models.CharField(max_length=30)
    file = models.FileField(upload_to="CertificateWeb/static/keys")
    def __str__(self):
        return self.account

class CerApply(models.Model):
    username = models.CharField(max_length=30)
    country = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    common = models.CharField(max_length=100)
    dsn = models.CharField(max_length=100)
    authority = models.ForeignKey('Authority',on_delete=models.CASCADE)
    def __str__(self):
        return self.username

class Certificate(models.Model):
    username = models.CharField(max_length=30)
    serialNumber = models.CharField(max_length=400)
    file = models.FileField(upload_to="CertificateWeb/static/certificate")
    def __str__(self):
        return self.username+" "+self.serialNumber

class ApplyForRevok(models.Model):
    username = models.CharField(max_length=30)
    serialNumber = models.CharField(max_length=400)
    authority = models.ForeignKey('Authority',on_delete=models.CASCADE)
    def __str__(self):
        return self.username+" "+self.serialNumber

class Revoke(models.Model):
    serialNumber = models.CharField(max_length=400)
    def __str__(self):
        return self.serialNumber