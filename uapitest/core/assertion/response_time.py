from unittest import TestCase as _TestCase
from uapitest.util import safe_repr as _safe_repr


class AssertResponseTime(_TestCase):

  def assertResponseTimeLess(self, response_time: int, expected_response_time: int, msg = None):
    if not response_time < expected_response_time:
      standard_msg = '响应时间 %s （毫秒）不小于预期时间 %s （毫秒）' % (
        _safe_repr(response_time),
        _safe_repr(expected_response_time)
      )
      self.fail(self._formatMessage(msg, standard_msg))

  def assertResponseTimeLessEqual(self, response_time: int, expected_response_time: int, msg = None):
    if not response_time <= expected_response_time:
      standard_msg = '响应时间 %s （毫秒）大于预期时间 %s （毫秒）' % (
        _safe_repr(response_time),
        _safe_repr(expected_response_time)
      )
      self.fail(self._formatMessage(msg, standard_msg))

