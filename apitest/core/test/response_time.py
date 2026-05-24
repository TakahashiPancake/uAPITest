from apitest.core.assertion import AssertResponseTime as _AssertResponseTime
from apitest.core.test.util import logger_test as _logger_test

class TestResponseTime(_AssertResponseTime):

  def test_response_time(self, response_time: int, response_time_assertions: dict) -> None:
    """
    测试响应时间

    Args:
      response_time:            响应时间
      response_time_assertions: 响应时间断言

    """
    # 响应时间断言为空字典时
    if not response_time_assertions:
      raise ValueError('响应时间断言不能为空')

    # 断言服务器响应时间小于...
    if 'less' in response_time_assertions:
      self.assertResponseTimeLess(response_time, response_time_assertions.get('less'))
      _logger_test.info(f'成功: 响应时间 {response_time} 毫秒小于预期 {response_time_assertions.get("less")}')

    # 断言服务器响应时间小于等于...
    elif 'less_equal' in response_time_assertions:
      self.assertResponseTimeLessEqual(response_time, response_time_assertions.get('less_equal'))
      _logger_test.info(f'成功: 响应时间 {response_time} 毫秒不大于预期 {response_time_assertions.get("less_equal")}')
