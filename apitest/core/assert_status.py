from typing import \
  Union as _Union, \
  List as _List,   \
  Tuple as _Tuple, \
  overload
from unittest import TestCase as _TestCase
from apitest.core.util import safe_repr as _safe_repr



class AssertStatus(_TestCase):
  """接口测试用例基类"""

  def assertStatusCodeIs(self, status_code: int, status_code_expected: int, msg = None) -> None:
    """断言。如果响应状态码不等于预期，则失败。"""
    if not status_code == status_code_expected:
      msg = self._formatMessage(msg, '响应状态码 %s 不等于 %s' % (
        _safe_repr(status_code),
        _safe_repr(status_code_expected)
      ))
      raise self.failureException(msg)

  def assertStatusCodeIsNot(self, status_code: int, status_codes_expected: int, msg = None) -> None:
    """断言。如果响应状态码等于预期，则失败。"""
    if not status_code != status_codes_expected:
      msg = self._formatMessage(msg, '响应状态码 %s 等于 %s' % (
        _safe_repr(status_code),
        _safe_repr(status_codes_expected)
      ))
      raise self.failureException(msg)

  def assertStatusCodeIn(
    self,
    status_code: int,
    status_codes_expected: _Union[_List[int], _Tuple[int]],
    msg = None
  ):
    """断言。如果响应状态码不在预期的容器中，则失败。"""
    if status_code not in status_codes_expected:
      standard_msg = '响应状态码 %s 不在 %s 中' % (
        _safe_repr(status_code),
        _safe_repr(status_codes_expected)
      )
      self.fail(self._formatMessage(msg, standard_msg))

  def assertStatusCodeNotIn(
    self,
    status_code: int,
    status_codes_expected: _Union[_List[int], _Tuple[int]],
    msg = None
  ):
    """断言。如果响应状态码在预期的容器中，则失败。"""
    if status_code in status_codes_expected:
      standard_msg = '响应状态码 %s 在 %s 中' % (
        _safe_repr(status_code),
        _safe_repr(status_codes_expected)
      )
      self.fail(self._formatMessage(msg, standard_msg))

  @overload
  def assertStatusTypeIs(self, status_code: int, status_type_expected: str, msg = None): ...

  @overload
  def assertStatusTypeIs(self, status_code: int, status_type_expected: int, msg = None): ...

  def assertStatusTypeIs(self, status_code: int, status_type_expected, msg = None):
    """断言。如果响应状态码不是预期的状态类型，则失败。"""
    self.__assertStatusTypeBase(status_code, status_type_expected, assertion_type ='is', msg = msg)

  @overload
  def assertStatusTypeIsNot(self, status_code: int, status_type_expected: str, msg = None): ...

  @overload
  def assertStatusTypeIsNot(self, status_code: int, status_type_expected: int, msg = None): ...

  def assertStatusTypeIsNot(self, status_code: int, status_type_expected, msg = None):
    """断言。如果响应状态码是预期的状态类型，则失败。"""
    self.__assertStatusTypeBase(status_code, status_type_expected, assertion_type ='is_not', msg = msg)

  def assertStatusTypeIn(
    self,
    status_code: int,
    status_types_expected: _Union[_List[_Union[int, str]], _Tuple[_Union[int, str]]],
    msg = None
  ):
    """断言。如果响应状态码符合预期的状态类型集，则失败。"""
    for status_type_expected in status_types_expected:
      self.__assertStatusTypeBase(
        status_code,
        status_type_expected,
        status_types_container = status_types_expected,
        assertion_type = 'in',
        msg = msg
      )

  def assertStatusTypeNotIn(
    self,
    status_code: int,
    status_types_expected: _Union[_List[_Union[int, str]], _Tuple[_Union[int, str]]],
    msg = None
  ):
    """断言。如果响应状态码符合预期的状态类型集，则失败。"""
    for status_type_expected in status_types_expected:
      self.__assertStatusTypeBase(
        status_code,
        status_type_expected,
        status_types_container = status_types_expected,
        assertion_type = 'not_in',
        msg = msg
      )

  @staticmethod
  def __get_status_prefix(status_type: str) -> int | None:
    """
    获取状态码的前缀

    Args:
      status_type: 状态类型

    Returns:
      状态码前缀

    """
    match status_type:
      case 'informational':
        return 100
      case 'success':
        return 200
      case 'redirection':
        return 300
      case 'client_error':
        return 400
      case 'server_error':
        return 500
      case _:
        raise ValueError(f'Unknown status type: {status_type}')

  def __assertStatusTypeBase(
    self,
    status_code: int,
    status_type_expected: _Union[int, str],
    status_types_container: _Union[_List[_Union[int, str]], _Tuple[_Union[int, str]], None] = None,
    assertion_type: _Union[str, None] = None,
    msg = None
  ) -> None:
    status_prefix: int

    # 整数
    if isinstance(status_type_expected, int):
      # 状态码前缀
      status_prefix = (status_type_expected // 100) * 100
    # 字符串
    elif isinstance(status_type_expected, str):
      # 状态码前缀
      status_prefix = self.__get_status_prefix(status_type_expected)
    # 错误
    else:
      raise TypeError('status must be int or str')

    a = status_code - status_prefix

    match assertion_type:
      case 'is':
        if not 0 <= a < 100:
          standard_msg = '响应状态码 %s 不属于响应状态 %s' % (
            _safe_repr(status_code),
            _safe_repr(status_type_expected)
          )
          self.fail(self._formatMessage(msg, standard_msg))
      case 'is_not':
        if 0 <= a < 100:
          standard_msg = '响应状态码 %s 属于响应状态 %s' % (
            _safe_repr(status_code),
            _safe_repr(status_type_expected)
          )
          self.fail(self._formatMessage(msg, standard_msg))
      case 'in':
        if not 0 <= a < 100:
          standard_msg = '响应状态码 %s 不属于响应状态 %s' % (
            _safe_repr(status_code),
            _safe_repr(status_types_container)
          )
          self.fail(self._formatMessage(msg, standard_msg))
      case 'not_in':
        if 0 <= a < 100:
          standard_msg = '响应状态码 %s 属于响应状态 %s' % (
            _safe_repr(status_code),
            _safe_repr(status_types_container)
          )
          self.fail(self._formatMessage(msg, standard_msg))
      case _:
        raise ValueError(f'Unknown assertion type: {assertion_type}')


