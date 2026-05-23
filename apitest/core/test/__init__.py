from requests import Response as _Response
from apitest.core.assertion import AssertResponseTime as _AssertResponseTime
from apitest.common import create_logger as _create_logger
from apitest.feature import net_tools as _net_tools

_logger = _create_logger('core_test')

class Test(
  _AssertResponseTime
):

  def test_response_time(self, target_hostname: str, response: _Response, response_time_assertions: dict) -> None:
    """
    测试响应时间

    Args:
      target_hostname:          目标主机名
      response:                 requests响应
      response_time_assertions: 响应时间断言

    """

    # 总响应时间（毫秒）
    total_response_time = int(response.elapsed.total_seconds() * 1000)
    _logger.debug(f'总响应时间 {total_response_time} 毫秒')

    # 通过url获取响应基线时间
    base_response_time = _net_tools.get_response_time(target_hostname)

    # 服务器响应时间（约）（毫秒） = 总响应时间（毫秒） - 基线响应时间（毫秒）
    server_response_time = total_response_time - base_response_time
    if server_response_time < 0:
      server_response_time = 0

    _logger.debug(f'相对响应时间: {server_response_time} 毫秒')

    # 响应时间断言为空字典时
    if not response_time_assertions:
      raise ValueError('响应时间断言不能为空')

    # 断言服务器响应时间小于...
    if 'less' in response_time_assertions:
      self.assertResponseTimeLess(server_response_time, response_time_assertions.get('less'))

    # 断言服务器响应时间小于等于...
    elif 'less_equal' in response_time_assertions:
      self.assertResponseTimeLessEqual(server_response_time, response_time_assertions.get('less_equal'))

