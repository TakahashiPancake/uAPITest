__all__ = ['Test']

from uapitest.core.test.response_time import TestResponseTime as _TestResponseTime
from uapitest.core.test.status import TestStatus as _TestStatus
from uapitest.core.test.headers import TestHeaders as _TestHeaders
from uapitest.core.test.content_size import TestContentSize as _TestContentSize

class Test(
  _TestResponseTime,
  _TestStatus,
  _TestHeaders,
  _TestContentSize
): ...

