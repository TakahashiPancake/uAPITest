__all__ = ['APITest']

import copy as _copy
from urllib.parse import urlparse as _urlparse
from unittest import TestLoader as _TestLoader
import requests as _requests
import ddt as _ddt
from uapitest.core.test import Test as _Test
from uapitest.feature import net_tools as _net_tools
from uapitest.common import create_logger as _create_logger

_TestLoader.testMethodPrefix = 'api_test'

_logger = _create_logger('core_main')

@_ddt.ddt
class APITest(_Test):
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
          'type_in': [200],
        },
        'headers': {
          'content-type': 'application/json'
        },
        'content_size': {
          'less': 100
        }
      }
    }
  )
  @_ddt.unpack
  def api_test(
    self,
    method: str,
    url: str,
    params: dict | None = None,
    data: dict | None = None,
    json: dict | None = None,
    headers: dict | None = None,
    cookies: dict | None = None,
    files: dict | None = None,
    auth: list | None = None,
    timeout: float | None = None,
    allow_redirects: bool = False,
    proxies: dict | None = None,
    verify: bool | str | None = None,
    stream: bool | None = None,
    cert: str | None = None,
    assertions: dict | None = None # 断言
  ):

    # 输出接口、请求方法、请求参数等信息
    _logger.info(f'URL: {url}; Method: {method}')

    # 发送请求，获取响应
    response = _requests.request(
      method  = method.upper(),
      url     = url,
      params  = params,
      data    = data,
      json    = json,
      headers = headers,
      cookies = cookies,
      files   = files,
      auth    = auth,
      timeout = timeout,
      allow_redirects = allow_redirects,
      proxies = proxies,
      verify  = verify,
      stream  = stream,
      cert    = cert,
    )

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

      # 总响应时间（毫秒）
      total_response_time = int(response.elapsed.total_seconds() * 1000)
      _logger.debug(f'总响应时间 {total_response_time} 毫秒')

      # 通过url获取响应基线时间
      base_response_time = _net_tools.get_response_time(target_hostname)

      # 服务器响应时间（约）（毫秒） = 总响应时间（毫秒） - 基线响应时间（毫秒）
      server_response_time = total_response_time - base_response_time
      if server_response_time < 0:
        server_response_time = 0

      _logger.debug(f'相对响应时间: {server_response_time} 毫秒')

      # 获取断言信息（响应时间）
      response_time_assertions = assertions.get('response_time')

      # 测试响应时间
      self.test_response_time(server_response_time, response_time_assertions)

    # 响应状态码断言
    if 'status' in assertions:

      # 获取断言信息（状态码）
      code_assertions = assertions.get('status')

      # 获取响应状态码
      status_code = response.status_code

      self.test_status_code(status_code, code_assertions)

    # 响应头部断言
    if 'headers' in assertions:

      headers_assertions = assertions.get('headers')

      # 测试响应头部
      self.test_headers(response.headers, headers_assertions)

    # 响应体大小断言
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

      self.test_content_size(response_content_size, content_size_assertions)

    # 响应体断言

