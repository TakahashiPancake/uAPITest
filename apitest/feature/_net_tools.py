import time as _time
from scapy.all import sr1
from apitest.util import IP as _IP, IPv6 as _IPv6, TCP as _TCP
from apitest.common import logger

class NetTools(object):

  @staticmethod
  def getResponseTime(target, port: int = 80, timeout: int = 3000) -> int | None:
    """
    获取响应时间

    - 通过和服务器的80端口（默认）建立连接计算响应时间

    Args:
      target:  目标 主机名/IP
      port:    目标端口（默认 80）
      timeout: 超时时间（默认 3000 毫秒）

    Returns:
      响应时间（秒）

    """
    # 构造 TCP SYN 数据包
    # 尝试构造IPv4包
    logger.debug(f'尝试获取目标响应基准时间')
    logger.debug(f'目标: {target}, 端口 {port}')
    try:
      packet = _IP(dst=target) / _TCP(dport=port, flags="S")

    except Exception as e:
      # 丢弃错误
      _ = e

      # 尝试获构造IPv6包
      packet = _IPv6(dst=target) / _TCP(dport=port, flags="S")

    # 记录发送前的时间
    start_time = _time.time()

    logger.debug(f'发送数据包: {packet}')

    # 发送数据包并等待响应
    response = sr1(packet, timeout = timeout / 1000, verbose=0)

    # 记录收到响应后的时间
    end_time = _time.time()

    # 目标超时或无响应
    if response is None:
      raise TimeoutError('服务器连接超时')

    logger.debug(f'响应数据包: {response}')

    # 计算响应时间
    response_time = int((end_time - start_time) * 1000)

    logger.debug(f'{target} {port} 端口响应时间: {response_time} 毫秒')

    # 返回响应时间（毫秒）
    return response_time


net_tools = NetTools()
