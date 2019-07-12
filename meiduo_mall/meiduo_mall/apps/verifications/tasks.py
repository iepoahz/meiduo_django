
from celery import task
import logging

from meiduo_mall import constants
from meiduo_mall.utils.yuntongxun.sms import CCP

logger = logging.getLogger("django")


@task
def send_sms_code(mobile, sms_code):
    """
    发送短信验证码
    :param mobile: 手机号
    :param sms_code: 验证码时效
    :return: None
    """

    time = str(constants.SMS_CODE_EXPIRES)
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, time], constants.SMS_CODE_TEMP_ID)
        print(result)
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
