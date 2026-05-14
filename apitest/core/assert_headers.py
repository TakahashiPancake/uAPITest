from unittest import TestCase as _TestCase
from apitest.core.util import safe_repr as _safe_repr
from apitest.core.util import CaseInsensitiveDict as _CaseInsensitiveDict

class AssertHeaders(_TestCase):
  def assertHeadersContains(self, headers: _CaseInsensitiveDict, headers_subset: _CaseInsensitiveDict, msg=None):
    """检查HTTP头部是否包含子集"""

    missing = []
    mismatched = []
    for key, value in headers_subset.items():
      if key not in headers:
        missing.append(key)
      elif value != headers[key]:
        mismatched.append('%s, 期望值: %s, 实际值: %s' % (
          _safe_repr(key),
          _safe_repr(value),
          _safe_repr(headers[key])
        ))

    if not (missing or mismatched):
      return

    standard_msg = ''
    if missing:
      standard_msg = 'HTTP头部缺失键: %s' % ','.join(_safe_repr(m) for m in
                                             missing)
    if mismatched:
      if standard_msg:
        standard_msg += '; '
      standard_msg += 'HTTP头部值不匹配: %s' % ','.join(mismatched)

    self.fail(self._formatMessage(msg, standard_msg))