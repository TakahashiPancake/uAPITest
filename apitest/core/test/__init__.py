__all__ = ['Test']

from apitest.core.test.response_time import TestResponseTime as _TestResponseTime
from apitest.core.test.status import TestStatus as _TestStatus

class Test(
  _TestResponseTime,
  _TestStatus,
): ...

