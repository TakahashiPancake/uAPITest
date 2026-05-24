from apitest.core.assertion import AssertResponseTime as _AssertResponseTime
from apitest.core.assertion import AssertStatus as _AssertStatus
from apitest.common import create_logger as _create_logger

_logger = _create_logger('core_test')

class Test(
  # 断言响应时间
  _AssertResponseTime,

  # 断言响应状态
  _AssertStatus,
):

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

    # 断言服务器响应时间小于等于...
    elif 'less_equal' in response_time_assertions:
      self.assertResponseTimeLessEqual(response_time, response_time_assertions.get('less_equal'))

  def test_status_code(self, status_code: int, status_code_assertions: dict) -> None:
    """
    测试响应状态码

    Args:
      status_code:            响应状态码
      status_code_assertions: 响应状态断言

    """
    # 响应状态断言为空时
    if not status_code_assertions:
      raise ValueError('响应状态断言不能为空')

    # 断言响应状态码是...
    if 'is' in status_code_assertions:
      self.assertStatusCodeIs(status_code, status_code_assertions.get('is'))

    # 断言响应状态码不是...
    elif 'is_not' in status_code_assertions:
      self.assertStatusCodeIsNot(status_code, status_code_assertions.get('is_not'))

    # 断言响应状态码在...
    if 'in' in status_code_assertions:
      self.assertStatusCodeIn(status_code, status_code_assertions.get('in'))

    # 断言响应状态码不在...
    elif 'not_in' in status_code_assertions:
      self.assertStatusCodeNotIn(status_code, status_code_assertions.get('not_in'))

    # 断言响应状态类型是...
    if 'type_is' in status_code_assertions:
      self.assertStatusTypeIs(status_code, status_code_assertions.get('type_is'))

    # 断言响应状态类型不是...
    elif 'type_is_not' in status_code_assertions:
      self.assertStatusTypeIsNot(status_code, status_code_assertions.get('type_is_not'))

    # 断言响应状态类型在...
    if 'type_in' in status_code_assertions:
      self.assertStatusTypeIn(status_code, status_code_assertions.get('type_in'))

    # 断言响应状态类型不在...
    elif 'type_not_in' in status_code_assertions:
      self.assertStatusTypeNotIn(status_code, status_code_assertions.get('type_not_in'))
