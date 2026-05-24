from apitest.util import CaseInsensitiveDict as _CaseInsensitiveDict
from apitest.core.assertion import AssertHeaders as _AssertHeaders
from apitest.core.test.util import logger_test as _logger_test

class TestHeaders(_AssertHeaders):

  def test_headers(self, headers: _CaseInsensitiveDict, headers_assertions: _CaseInsensitiveDict) -> None:
    """
    测试响应头部

    Args:
      headers:            响应头部
      headers_assertions: 响应头部断言

    """
    # 响应时间断言为空字典时
    if not headers_assertions:
      raise ValueError('响应时间断言不能为空')

    # 断言响应头部
    self.assertHeadersContains(headers, headers_assertions)
    _logger_test.info(f'成功: {headers_assertions} 在响应头部 {headers} 中')

