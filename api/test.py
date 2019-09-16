import urllib
import json
import sys
from pyfcm import FCMNotification

def push_to_fcm(device_token, gcm_key, title=None, message=None, data=None, sound=None, badge=None):
    fcm_push_service = FCMNotification(api_key=gcm_key)
    fcm_push_service.notify_single_device(
        registration_id=device_token,
        message_title=title,
        message_body=message,
        data_message=data,
        sound=sound,
        badge=badge
    )


push_to_fcm("ePpquqf0Ew0:APA91bHZ--eFfFdg4SMAmmXliCa3gT5obLTy2zm3D4mnUTQ9n2GkG_--14sDaDtWg_jz7K18_yICUfSYMl4gWjB9TvRG1tz7-LOO4oNEbTHAvoaVADeejJV2VYproEnNOyXZE_iFj-KI", "AAAAqxOQx7w:APA91bERR9A5_nnk0tdm6fdiswEDi0KLpQyAWC2zrGoYR2LPHpUGCPg-lNlzcVoVicE8TpgvYncBwrP8dYprvLNRJlZPI1iyOAfmib7L7B4A5yUuJ0h0kmpcHSu-Z_pzWc0EMAOqdPWr", "test Title", "messagebody")