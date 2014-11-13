# Create your views here.
from django.template.response import TemplateResponse
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import link
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from video.serializers import VideoUploadSerializer, VideoSerializer
from video.models import Video
from account.forms import mob as account_forms
from account.models import User
from django import forms

class SignupForm(account_forms.SignupForm):

    username = forms.RegexField(account_forms.USERNAME_RE,
                                max_length=30,
                                label="Username",
                                widget=forms.TextInput(attrs=account_forms.attrs_dict),
                                error_messages={
                                    'invalid': '用户名只能由数字字母组合',
                                    'required': '用户名不能为空',
                                })


def video_default_authenticate(request):
    default_username = '虫虫视频玩家'
    try:
        user = User.objects.get(username=default_username)
    except User.DoesNotExist:
        form = SignupForm(dict(username=default_username,
                               password='sfnvksdjqwe'))
        form.is_valid()
        user = form.save()
    token = Token.objects.get_or_create(user=user)
    request.user = user
    request.auth = token


class VideoViewSet(viewsets.ModelViewSet):
    model = Video
    authentication_classes = ()
    permission_classes = ()
    serializer_class = VideoUploadSerializer

    def create(self, request, *args, **kwargs):
        self.serializer_class = VideoUploadSerializer
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        video_default_authenticate(request)
        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def pre_save(self, obj):
        obj.user = self.request.user

    play_wap_template = 'video/wap/play.html'

    play_web_template = 'video/web/play.html'

    list_wap_template = 'video/wap/list.html'

    index_template = 'video/web/index.html'

    @link()
    def play(self, request, *args, **kwargs):
        if request.GET.get('src') == 'wap':
            template_name = self.play_wap_template
        else:
            template_name = self.play_web_template
        object = self.get_object()
        return TemplateResponse(request=request,
                                template=template_name,
                                context=dict(
                                    video=object,
                                ),
                                content_type='text/html')

    def list(self, request, *args, **kwargs):
        self.serializer_class = VideoSerializer
        self.object_list = self.filter_queryset(self.get_queryset()).order_by('-created')

        page = self.paginate_queryset(self.object_list)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)
        self.serializer_class = VideoUploadSerializer
        data = serializer.data

        template_name = self.index_template
        if request.GET.get('src') == 'wap':
            template_name = self.list_wap_template

        return TemplateResponse(request=request,
                                template=template_name,
                                context=dict(
                                    title='',
                                    data=data,
                                    video_list=self.object_list
                                ),
                                content_type='text/html',
                                )
