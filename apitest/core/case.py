import requests as _requests
import ddt as _ddt
from unittest import TestLoader as _TestLoader
from apitest.core.base import Base as _Base

_TestLoader.testMethodPrefix = 'api_test'


@_ddt.ddt
class TestCase(_Base):
  @_ddt.data(
    {
      'url': 'https://www.baidu.com/',
      'method': 'GET',
      'assertions': {
        'status': {
          'is': 200,
          'is_not': 301,
          #'in': [301, 302],
          #'not_in': [301, 302],
          # informational: 响应状态码100+
          # success: 响应状态码200+
          # redirection: 响应状态码300+
          # client_error: 响应状态码400+
          # server_error: 响应状态码500+
          'type_is': 'informational',
          'type_is_not': 'success',
          'type_in':['informational', 'redirection'],
          'type_not_in':[],
        },
        'headers':{
          'content-type': 'application/json',
        },
        'content-type': ...,
      }
    },
    {'url': 'https://app.pre.mieco.net/ht-printer/v1/c/res/app/upgrade/', 'method': 'get', 'assertions': {
      'status': {
        'type_is': 'success',
      }
    }}
  )
  @_ddt.unpack
  def api_test(self, method: str, url: str, assertions: dict, **kwargs):

    # 发送请求，获取响应
    response = _requests.request(method = method.upper(), url = url, **kwargs)

    # 响应状态码断言
    if 'status' in assertions:

      # 获取断言信息（状态码）
      code_assertions = assertions.get('status')

      # 获取响应状态码
      status_code = response.status_code

      # 断言响应状态码是...
      if 'is' in code_assertions:
        self.assertStatusCodeIs(status_code, code_assertions.get('is'))

      # 断言响应状态码不是...
      elif 'is_not' in code_assertions:
        self.assertStatusCodeIsNot(status_code, code_assertions.get('is_not'))

      # 断言响应状态码在...
      if 'in' in code_assertions:
        self.assertStatusCodeIn(status_code, code_assertions.get('in'))

      # 断言响应状态码不在...
      if 'not_in' in code_assertions:
        self.assertStatusCodeNotIn(status_code, code_assertions.get('not_in'))

      # 断言响应状态类型是...
      if 'type_is' in code_assertions:
        self.assertStatusTypeIs(status_code, code_assertions.get('type_is'))

      # 断言响应状态类型不是...
      elif 'type_is_not' in code_assertions:
        self.assertStatusTypeIsNot(status_code, code_assertions.get('type_is_not'))

      # 断言响应状态类型在...
      if 'type_in' in code_assertions:
        self.assertStatusTypeIn(status_code, code_assertions.get('type_in'))

      # 断言响应状态类型不在...
      if 'type_not_in' in code_assertions:
        self.assertStatusTypeNotIn(status_code, code_assertions.get('type_not_in'))

    # 响应内容断言

    ...


