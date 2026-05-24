__all__ = ['Test', 'test_logger']

from apitest.core.test.response_time import TestResponseTime as _TestResponseTime
from apitest.core.test.status import TestStatus as _TestStatus
from apitest.common import create_logger as _create_logger

test_logger = _create_logger('core_test')

class Test(
  _TestResponseTime,
  _TestStatus,
):
  pass
