__all__ = ['APITest']

from urllib.parse import urlparse as _urlparse
from unittest import TestLoader as _TestLoader
import requests as _requests
import ddt as _ddt
from apitest.core.assert_status import AssertStatus as _AssertStatus
from apitest.core.assert_response_time import AssertResponseTime as _AssertResponseTime
from apitest.core.assert_headers import AssertHeaders as _AssertHeaders

_TestLoader.testMethodPrefix = 'api_test'

@_ddt.ddt
class APITest(
  # 断言响应时间
  _AssertResponseTime,

  # 断言响应状态
  _AssertStatus,

  # 断言响应头部
  _AssertHeaders
):
  @_ddt.data(
    #{
    #  'url': 'https://www.baidu.com/',
    #  'method': 'GET',
    #  'assertions': {
    #    'response_time': {
    #      'less': 100,
    #      'less_equal': 100
    #    },
    #    'status': {
    #      'is': 200,
    #      'is_not': 301,
    #      'in': [301, 302],
    #      'not_in': [301, 302],
    #      # informational: 响应状态码100+
    #      # success: 响应状态码200+
    #      # redirection: 响应状态码300+
    #      # client_error: 响应状态码400+
    #      # server_error: 响应状态码500+
    #      'type_is': 'informational',
    #      'type_is_not': 'success',
    #      'type_in':['informational', 'redirection'],
    #      'type_not_in':[],
    #    },
    #    'headers': {
    #    },
    #    'data': {
    #      size: ...
    #      data_type: ...
    #      data: ...
    #    }
    #  }
    #},
    {
      'url': 'https://app.pre.mieco.net/ht-printer/v1/c/res/app/upgrade/', 'method': 'get', 'assertions': {
        'response_time': {
          'less_equal': 100
        },
        'status': {
          'type_in': [201],
        },
        'headers': {
          'content-type': 'application/json'
        }
      }
    }
  )
  @_ddt.unpack
  def api_test(self, method: str, url: str, path: str = '', assertions: dict | None = None, **kwargs):

    # 发送请求，获取响应
    response = _requests.request(method = method.upper(), url = url + path, **kwargs)

    # 响应时间断言
    if 'response_time' in assertions:

      # 解析url
      parsed_url = _urlparse(url)

      # 目标主机
      target_hostname: str = ''

      # 通过url获取主机名
      if parsed_url.hostname:
        target_hostname = parsed_url.hostname

      # 无法获取主机名
      else:
        pass

      # 获取断言信息（响应时间）
      response_time_assertions = assertions.get('response_time')

      # 通过url获取响应基线时间
      base_response_time = self.getBaseResponseTime(target_hostname)

      # 服务器响应时间（约）（毫秒） = 总响应时间（毫秒） - 基线响应时间（毫秒）
      server_response_time = int((response.elapsed.total_seconds() - base_response_time) * 1000)
      if server_response_time < 0:
        server_response_time = 0

      # Todo: 打日志，服务器响应时间
      ...

      # 响应时间断言为空时
      if not response_time_assertions:
        raise ValueError('响应时间断言不能为空')

      # 断言服务器响应时间小于...
      if 'less' in response_time_assertions:
        self.assertResponseTimeLess(server_response_time, response_time_assertions.get('less'))

      # 断言服务器响应时间小于等于...
      elif 'less_equal' in response_time_assertions:
        self.assertResponseTimeLessEqual(server_response_time, response_time_assertions.get('less_equal'))

    # 响应状态码断言
    if 'status' in assertions:

      # 获取断言信息（状态码）
      code_assertions = assertions.get('status')

      # 获取响应状态码
      status_code = response.status_code

      # 响应状态断言为空时
      if not code_assertions:
        raise ValueError('响应状态断言不能为空')

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
      elif 'not_in' in code_assertions:
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
      elif 'type_not_in' in code_assertions:
        self.assertStatusTypeNotIn(status_code, code_assertions.get('type_not_in'))

    # 响应头部断言

    if 'headers' in assertions:

      headers_assertions = assertions.get('headers')

      # 断言响应头部包含
      self.assertHeadersContains(response.headers, headers_assertions)

    # 响应体断言

    ...

