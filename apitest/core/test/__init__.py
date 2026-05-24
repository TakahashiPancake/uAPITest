__all__ = ['Test']

from apitest.core.test.response_time import TestResponseTime as _TestResponseTime
from apitest.core.test.status import TestStatus as _TestStatus
from apitest.core.test.headers import TestHeaders as _TestHeaders

class Test(
  _TestResponseTime,
  _TestStatus,
  _TestHeaders,
): ...

