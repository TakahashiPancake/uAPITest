__all__ = ['APITest']

import copy as _copy
from urllib.parse import urlparse as _urlparse
from unittest import TestLoader as _TestLoader
import requests as _requests
import ddt as _ddt
from apitest.core.assertion import AssertStatus as _AssertStatus
from apitest.core.assertion import AssertResponseTime as _AssertResponseTime
from apitest.core.assertion import AssertHeaders as _AssertHeaders
from apitest.core.assertion import AssertContentSize as _AssertContentSize
from apitest.core.test import Test as _Test
from apitest.core.tool import TestTool as _TestTool
from apitest.common import create_logger as _create_logger

_TestLoader.testMethodPrefix = 'api_test'

_logger = _create_logger('core_main')

@_ddt.ddt
class APITest(
  # 测试
  _Test,

  # 断言响应时间
  _AssertResponseTime,

  # 断言响应状态
  _AssertStatus,

  # 断言响应头部
  _AssertHeaders,

  # 断言响应体大小
  _AssertContentSize,

  # 加入测试工具
  _TestTool
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
          'less_equal': 200
        },
        'status': {
          'type_in': [200],
        },
        'headers': {
          'content-type': 'application/json'
        },
        'content_size': {
          'less': 200
        }
      }
    }
  )
  @_ddt.unpack
  def api_test(self, method: str, url: str, assertions: dict | None = None, **kwargs):

    # 输出接口、请求方法、请求参数等信息
    _logger.info(f'URL: {url}; Method: {method}')

    # 发送请求，获取响应
    response = _requests.request(method = method.upper(), url = url, **kwargs)

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

      _logger.debug(f'目标主机: {target_hostname}')

      # 获取断言信息（响应时间）
      response_time_assertions = assertions.get('response_time')

      self.test_response_time(target_hostname, response, response_time_assertions)

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

    # 响应体大小断言
    #print(response.content, len(response.content + bytes('啊', encoding='utf-8')))
    #print(response.text, len(response.text + '啊'))
    if 'content_size' in assertions:

      content_size_assertions = assertions.get('content_size')

      response_content_bytes: bytes

      if isinstance(response.content, bytes):

        response_content_bytes = _copy.copy(response.content)

      else:

        # 默认使用utf-8解码html文本
        response_content_bytes = bytes(response.text, encoding='utf-8')

      # 响应体大小
      response_content_size: int = len(response_content_bytes)

      _logger.debug(f'响应体大小: {response_content_size} 字节')

      if not content_size_assertions:

        raise ValueError('响应体大小断言不能为空')

      if 'less' in content_size_assertions:

        self.assertContentSizeLess(response_content_size, content_size_assertions.get('less'))

      elif 'less_equal' in content_size_assertions:

        self.assertContentSizeLessEqual(response_content_size, content_size_assertions.get('less_equal'))

    # 响应体断言

