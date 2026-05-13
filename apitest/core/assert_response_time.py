import time as _time
from unittest import TestCase as _TestCase
from scapy.all import sr1
from apitest.core.util import safe_repr as _safe_repr
from apitest.core.util import IP as _IP, IPv6 as _IPv6, TCP as _TCP


class AssertResponseTime(_TestCase):

  @staticmethod
  def getBaseResponseTime(target, port=80, timeout=3) -> float | None:
    """
    获取基线响应时间

    - 通过和服务器的80端口建立连接计算响应时间

    Args:
      target:  目标 主机名/IP/地址
      port:    目标端口（默认80）
      timeout: 超时时间（默认3秒）

    Returns:
      响应时间（秒）

    """
    # 构造 TCP SYN 数据包
    # 尝试构造IPv4包
    try:
      packet = _IP(dst=target) / _TCP(dport=port, flags="S")

    except Exception as e:
      # 丢弃错误
      _ = e

      # 尝试获构造IPv6包
      packet = _IPv6(dst=target) / _TCP(dport=port, flags="S")

    # 记录发送前的时间
    start_time = _time.time()

    # 发送数据包并等待响应
    response = sr1(packet, timeout=timeout, verbose=0)

    # 记录收到响应后的时间
    end_time = _time.time()

    # 目标超时或无响应
    if response is None:
      raise TimeoutError('服务器连接超时')

    # 计算响应时间
    response_time = end_time - start_time

    # 返回响应时间
    return response_time


  def assertResponseTimeLess(self, response_time: float, expected_response_time: float, msg = None):
    if not response_time < expected_response_time:
      standard_msg = '响应时间 %s 不小于预期时间 %s' % (
        _safe_repr(response_time),
        _safe_repr(expected_response_time)
      )
      self.fail(self._formatMessage(msg, standard_msg))

  def assertResponseTimeLessEqual(self, response_time: float, expected_response_time: float, msg = None):
    if not response_time <= expected_response_time:
      standard_msg = '响应时间 %s 大于预期时间 %s' % (
        _safe_repr(response_time),
        _safe_repr(expected_response_time)
      )
      self.fail(self._formatMessage(msg, standard_msg))

