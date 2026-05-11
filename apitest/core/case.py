from unittest import TestCase as _TestCase
from unittest import TestLoader as _TestLoader
import requests as _requests
import ddt as _ddt

_TestLoader.testMethodPrefix = 'api_test'


@_ddt.ddt
class TestCase(_TestCase):
  @_ddt.data(
    {'url': 'http://localhost/', 'method': 'GET'},
    {'url': 'http://localhost/', 'method': 'POST'}
  )
  @_ddt.unpack
  def api_test(self, method: str, url: str, **kwargs):
    response = _requests.request(method = method.upper(), url = url, **kwargs)

    ...


