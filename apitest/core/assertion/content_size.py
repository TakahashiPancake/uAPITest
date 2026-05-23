from unittest import TestCase as _TestCase
from apitest.util import safe_repr as _safe_repr

class AssertContentSize(_TestCase):

  def assertContentSizeLess(self, content_size: int, content_size_expected: int, msg = None) -> None:
    if not content_size < content_size_expected:
      standard_msg = '响应体大小 %s （字节）不小于预期 %s （字节）' % (
        _safe_repr(content_size),
        _safe_repr(content_size_expected)
      )
      self.fail(self._formatMessage(msg, standard_msg))

  def assertContentSizeLessEqual(self, content_size: int, content_size_expected: int, msg = None) -> None:
    if not content_size <= content_size_expected:
      standard_msg = '响应体大小 %s （字节）大于预期 %s （字节）' % (
        _safe_repr(content_size),
        _safe_repr(content_size_expected)
      )
      self.fail(self._formatMessage(msg, standard_msg))

