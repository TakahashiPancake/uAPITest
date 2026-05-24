__all__ = ['Test']

from apitest.core.test.response_time import TestResponseTime as _TestResponseTime
from apitest.core.test.status import TestStatus as _TestStatus
from apitest.core.test.headers import TestHeaders as _TestHeaders
from apitest.core.test.content_size import TestContentSize as _TestContentSize

class Test(
  _TestResponseTime,
  _TestStatus,
  _TestHeaders,
  _TestContentSize
): ...

