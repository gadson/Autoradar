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


push_to_fcm("", "", "test Title", "messagebody")
