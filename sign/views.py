# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth

from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

def index(request):
    return render(request, 'index.html')

# 分页器
def paginator1(request, list_name):
    paginator = Paginator(list_name, 2)
    page = request.GET.get('page', '')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts
# 登陆动作
def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user) # 登陆
            response = HttpResponseRedirect("/event_manage/")
            # response.set_cookie('user', username, 3600)  # 添加浏览器cookie
            request.session['user'] = username # 将Session信息记录到浏览器
            return response
        else:
            return render(request, "index.html", {"error": "username or password error!"})
    else:
        return render(request, "index.html")

# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '') # 读取浏览器的Cookie
    username = request.session.get('user', '') # 读取浏览器的Session
    event_lists = Event.objects.all()
    contacts = paginator1(request, event_lists)
    return render(request, 'event_manage.html', locals())

@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('event_name', '')
    if search_name:
        event_lists = Event.objects.filter(name__icontains=search_name)
        contacts = paginator1(request, event_lists)
        return render(request, 'event_manage.html', locals())
    else:
        search_name = request.GET.get('guest_name', '')
        guest_lists = Guest.objects.filter(realname__icontains=search_name)
        contacts = paginator1(request, guest_lists)
        return render(request, 'guest_manage.html', locals())

# 签到嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_lists = Guest.objects.all()
    contacts = paginator1(request, guest_lists)
    return render(request, 'guest_manage.html', locals())

# 签到页面
@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    username = request.session.get('user', '')
    return render(request, 'sign_index.html', locals())

# 签到动作
@login_required
def sign_index_action(request, eid):
    username = request.session.get('user', '')
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    # print(phone)
    if request.method == 'POST':
        result = Guest.objects.filter(phone=phone)
        print(result)
        if not result:
            hint = 'phone error.'
            return render(request,'sign_index.html', locals())
        result = Guest.objects.filter(phone=phone, event_id=eid)
        if not result:
            hint = 'event id or phone error.'
            return render(request, 'sign_index.html', locals())
        elif result[0].sign == 1:
            # print(type(result[0].sign))
            hint = 'user has sign in.'
            result = result[0]
            signed = Guest.objects.filter(event_id=eid, sign=1).count()
            return render(request, 'sign_index.html', locals())
        else:
            hint = 'sign in success!'
            result=result[0]
            Guest.objects.filter(phone=phone, event_id=eid).update(sign=1)
            signed = Guest.objects.filter(event_id=eid, sign=1).count()
            return render(request, 'sign_index.html', locals())
    else:
        return render(request, 'sign_index.html', locals())

@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/')
    return response


# rest_framework模块测试

from .serializers import GuestSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from util.response import JsonResponse
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from util.pagination import ForkNonePagination
# 分页相关
from util.mixins import PaginateMixin
# 数据导出
from util.excel_export import export, queryset_to_data
import logging

# logger = logging.getLogger(__name__)
logger = logging.getLogger('django')

class GuestViewSet(viewsets.ModelViewSet, PaginateMixin):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # 这个类使用的分页器
    pagination_class = ForkNonePagination
    # 这个类允许的用户
    # permission_classes = IsAuthenticated

    @list_route(methods=['post'])
    def create_guest(self, request):
        data = request.data

        realname = data['realname']
        phone = data['phone']
        email = data['email']
        event = data['eventid']
        if realname and phone and email and event:
            guest = Guest.objects.create(
                                realname=realname,
                                phone=phone,
                                email=email,
                                event_id=event)
            serializer = GuestSerializer(guest)
            return JsonResponse(msg='Create guest success', data=serializer.data)
        else:
            return JsonResponse(msg='parameter wrong', code=404)

    @list_route(methods=['post'])
    def change_name(self, request):
        data = request.data
        query_list = []
        change_name = data.get("changeName", '')
        real_name = data.get("realname", '')
        event_id = data.get("event", '')
        if real_name and event_id:
            query_list.append(Q(realname=real_name))
            query_list.append(Q(event=event_id))
        change_guest = self.queryset.filter(*query_list)

        if change_guest:
            if change_guest[0].realname == change_name:
                return JsonResponse(msg='Change name same as real name', code=400)
            change_guest.update(realname=change_name)
            logger.info('get change name success')
            return JsonResponse(msg='Change name success',data=change_name)
        else:
            return JsonResponse(msg='Real name or event id wrong', code=400)

    # url demo is http://127.0.0.1:8001/api_hzq/10/sign_up/
    @detail_route(methods=['get'])
    def sign_up(self, request, pk=None):
        data = request.data
        # print(pk)
        guest = self.queryset.filter(id=pk)
        if guest:
            if guest[0].sign == 1:
                return JsonResponse(msg='Guest has signed')
            else:
                guest.update(sign=1)
                serializer = GuestSerializer(guest, many=True)
                return JsonResponse(msg='Guest sign success', data=serializer.data)
        else:
            return JsonResponse(msg='Guest id error, no guest of this id')

    @list_route(methods=['get'])
    def get_all_guests(self, request):
        data = request.GET
        event_id = data.get('pk', '')
        # print('event_id:', event_id)
        if event_id:
            query_result = self.queryset.filter(event_id=event_id)
            serializer = GuestSerializer(query_result, many=True)
            # print(serializer)
            # if serializer.is_valid():
            return JsonResponse(msg='Get guest list success', data=serializer.data)
        else:
            # serializer = GuestSerializer(self.queryset, many=True)
            # return JsonResponse(msg='Get guest list success', data=serializer.data)
            # http://127.0.0.1:8001/api_hzq/get_all_guests/?page=2&per_page=5   获取分页的数据，页数为第2页，显示数据条数为5
            logger.info('Get guest msg success')
            return self.pagination_response(self.queryset)

    @list_route(['GET', 'POST'])
    def export(self, request):
        """
        导出所有用户信息
        :param request:
        :return:
        """
        host = request.get_host()  # 得到请求的地址
        # print('host:', host)

        data = queryset_to_data(self.queryset,
                                ["realname", "phone", "email", "sign", "create_time", "event_id"])
        column_names = [
            "姓名","电话","邮箱","签到状态","创建时间","事件ID",
        ]
        url = export("guestMsg", "用户信息", data, column_names)
        return JsonResponse(msg='export msg success', data={"url": host + url})