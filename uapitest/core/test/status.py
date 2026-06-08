from uapitest.core.assertion import AssertStatus as _AssertStatus
from uapitest.core.test.util import logger_test as _logger_test

class TestStatus(_AssertStatus):

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
      _logger_test.info(f'成功: 响应状态码 {status_code} 是 {status_code_assertions.get("is")}')

    # 断言响应状态码不是...
    elif 'is_not' in status_code_assertions:
      self.assertStatusCodeIsNot(status_code, status_code_assertions.get('is_not'))
      _logger_test.info(f'成功: 响应状态码 {status_code} 不是 {status_code_assertions.get("is_not")}')

    # 断言响应状态码在...
    if 'in' in status_code_assertions:
      self.assertStatusCodeIn(status_code, status_code_assertions.get('in'))
      _logger_test.info(f'成功: 响应状态码 {status_code} 在 {status_code_assertions.get("in")} 中')

    # 断言响应状态码不在...
    elif 'not_in' in status_code_assertions:
      self.assertStatusCodeNotIn(status_code, status_code_assertions.get('not_in'))
      _logger_test.info(f'成功: 响应状态码 {status_code} 不在 {status_code_assertions.get("not_in")} 中')

    # 断言响应状态类型是...
    if 'type_is' in status_code_assertions:
      self.assertStatusTypeIs(status_code, status_code_assertions.get('type_is'))
      _logger_test.info(f'成功: 响应状态码 {status_code} 的类型是 {status_code_assertions.get("type_is")}')

    # 断言响应状态类型不是...
    elif 'type_is_not' in status_code_assertions:
      self.assertStatusTypeIsNot(status_code, status_code_assertions.get('type_is_not'))
      _logger_test.info(f'成功: 响应状态码 {status_code} 的类型不是 {status_code_assertions.get("type_is_not")}')

    # 断言响应状态类型在...
    if 'type_in' in status_code_assertions:
      self.assertStatusTypeIn(status_code, status_code_assertions.get('type_in'))
      _logger_test.info(f'成功: 响应状态码 {status_code} 的类型在 {status_code_assertions.get("type_in")} 中')

    # 断言响应状态类型不在...
    elif 'type_not_in' in status_code_assertions:
      self.assertStatusTypeNotIn(status_code, status_code_assertions.get('type_not_in'))
      _logger_test.info(f'成功: 响应状态码 {status_code} 的类型不在 {status_code_assertions.get("type_not_in")} 中')

