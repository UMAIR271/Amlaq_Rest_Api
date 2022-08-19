from urllib import response
from rest_framework import renderers
import json

class UserRenderers(renderers.JSONRenderer):
    charset = 'utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response =json.dumps({'errors':data})
        else:
            print(data)
            response = json.dumps(data)
            print(response)
        return response