from uapitest.core.assertion import AssertContentSize as _AssertContentSize
from uapitest.core.test.util import logger_test as _logger_test

class TestContentSize(_AssertContentSize):
  def test_content_size(self, content_size: int, content_size_assertions: dict) -> None:

    if not content_size_assertions:
      raise ValueError('响应体大小断言不能为空')

    if 'less' in content_size_assertions:
      self.assertContentSizeLess(content_size, content_size_assertions.get('less'))
      _logger_test.info(f'成功: 响应体大小 {content_size} (字节) 小于 {content_size_assertions.get("less")} (字节)')

    elif 'less_equal' in content_size_assertions:
      self.assertContentSizeLessEqual(content_size, content_size_assertions.get('less_equal'))
      _logger_test.info(f'成功: 响应体大小 {content_size} (字节) 不大于 {content_size_assertions.get("less_equal")} (字节)')

