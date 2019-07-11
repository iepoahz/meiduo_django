from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from meiduo_mall.meiduo_mall.utils.captcha.captcha import captcha


class ImageCodeView(APIView):
    """
    图片验证码
    """

    def get(self, request, image_code_id):
        """
        获取图片验证码
        """
        # 生成验证码图片
        text, image = captcha.generate_captcha()

        # 连接redis数据库
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)

        # 指定返回的数据类型
        return HttpResponse(image, content_type="images/jpg")