# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, username, password, email=''):
#         user = self.model(username=username,
#                           email=email)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, password):
#         user = self.create_user(username, password)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=40, unique=True)
#     email = models.EmailField(max_length=40, blank=True)
#     phone = models.CharField(max_length=16, blank=True)
#     is_admin = models.BooleanField(default=False)
#
#     objects = UserManager
#
#     USERNAME_FIELD = 'username'
#     EMAIL_FIELD = 'email'
#
#     class Meta:
#         ordering = ['id']
#
#     @property
#     def is_staff(self):
#         return self.is_admin

# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)            # 发布会标题
    limit = models.IntegerField()                      # 参加人数
    status = models.BooleanField()                     # 状态
    address = models.CharField(max_length=200)         # 地址
    start_time = models.DateTimeField('event time')   # 发布会时间
    create_time = models.DateTimeField(auto_now=True)  # 创建时间

    def __str__(self):
        return self.name

# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event)                       # 关联发布会的id
    realname = models.CharField(max_length=64)             # 姓名
    phone = models.CharField(max_length=16)
    email = models.EmailField(blank=True)
    sign = models.BooleanField(default=0)                           # 签到状态
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "phone")

    def __str__(self):
        return self.realname

class Pikamsg(models.Model):
    msg = models.CharField(max_length=150, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __repr__(self):
        return 'pika msg is {}'.format(self.msg)

    __str__ = __repr__