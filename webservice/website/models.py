# -*- coding: utf-8 -*-
import random, os, time
from PIL import Image,ImageDraw,ImageFont
from django.conf import settings
from website.cdn.model_register import *


def mock_processor_class(processor_class):
    from website.cdn.parsers import OperationRequest

    class MockOperationRequest(OperationRequest):

        def request(self):
            self.request_data = self.create_querydata()
            STATUS_CODE_SUCCESS = self.response_class.STATUS_CODE_SUCCESS
            response = self.response_class(STATUS_CODE_SUCCESS, 'receive finish')
            response.result = response.result_string(STATUS_CODE_SUCCESS)
            return response

    class MockProcessorMixin(object):

        request_class = MockOperationRequest

        def get_source_host(self):
            return 'gc.ccplay.com.cn'

    class MockProcessor(MockProcessorMixin, processor_class):
        pass
    return MockProcessor

if settings.DEBUG:
    Author.sync_processor_class = \
        mock_processor_class(AuthorProcessor)
    PackageVersion.sync_processor_class = \
        mock_processor_class(PackageVersionProcessor)

    Advertisement.sync_processor_class = \
        mock_processor_class(AdvertisementProcessor)

    Topic.sync_processor_class = \
        mock_processor_class(TopicProcessor)

    Category.sync_processor_class = \
        mock_processor_class(CategoryProcessor)

    ClientPackageVersion.sync_processor_class = \
        mock_processor_class(ClientPackageVersionProcessor)

    LoadingCover.sync_processor_class = \
        mock_processor_class(LoadingCoverProcessor)



def captcha(img_width=90, img_height=37, font_size=22):



    """
    background  #随机背景颜色
    line_color #随机干扰线颜色
    img_width = #画布宽度
    img_height = #画布高度
    font_color = #验证码字体颜色
    font_size = #验证码字体尺寸
    font = I#验证码字体
    """

    string = '012345679ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    #background = (random.randrange(230,255),random.randrange(230,255),random.randrange(230,255))
    background = (255, 255, 255)
    line_color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
    #img_width = 90
    #img_height = 37
    font_color = ['black','darkblue','darkred']
    #font_size = 22
    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf',font_size)

    #新建画布
    im = Image.new('RGB',(img_width,img_height), background)
    draw = ImageDraw.Draw(im)
    code = random.sample(string, 4)
    #新建画笔
    draw = ImageDraw.Draw(im)

    #画干扰线
    for i in range(random.randrange(6,8)):
        xy = (random.randrange(0,img_width),random.randrange(0,img_height),
              random.randrange(0,img_width),random.randrange(0,img_height))
        draw.line(xy,fill=line_color,width=1)

    #写入验证码文字
    x = 2
    for i in code:
        y = random.randrange(0,10)
        draw.text((x,y), i, font=font, fill=random.choice(font_color))
        x += 15

    verify = ''.join(code)

    return im, verify


def generate_captcha(request):
    img, verify = captcha()
    timestamp = str(time.time()).replace('.', '')
    static_path =  ''.join(['captcha/', timestamp, '.gif'])
    absolute_path = os.path.join(settings.PROJECT_PATH, 'static', static_path)
    request.session['verify'] = None
    try:
        img.save(absolute_path)
        request.session['verify'] = verify
    except IOError:
        static_path = None

    return static_path
