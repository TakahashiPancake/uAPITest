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
          'is_not': [301, 302],
          'type_is': 'informational',
          # informational: 响应状态码100+
          # success: 响应状态码200+
          # redirection: 响应状态码300+
          # client_error: 响应状态码400+
          # server_error: 响应状态码500+
          'type_is_not': ['informational', 'success', 'redirection', 'client_error', 'server_error'],
        },
        'headers':{
          'content-type': 'application/json',
        },
        'content':{
          'json'
        }
      }
    },
    {'url': 'https://www.baidu.com/', 'method': 'POST', 'assertions': {'IS_NOT': 200}},
  )
  @_ddt.unpack
  def api_test(self, method: str, url: str, assertions: dict, **kwargs):
    response = _requests.request(method = method.upper(), url = url, **kwargs)

    # 响应状态码断言

    if 'status' in assertions:

      # 获取断言信息
      code_assertions = assertions.get('status')

      # 断言响应状态码是...
      if 'is' in code_assertions:
        self.assertEqual(response.status_code, code_assertions.get('is'))

      # 断言响应状态码不是...
      elif 'is' in code_assertions:
        ...

      # 断言响应状态码前缀是...
      if 'like' in code_assertions:
        ...

      # 断言响应状态码前缀不是...
      elif 'not_like' in code_assertions:
        ...


    # 响应内容断言

    ...


