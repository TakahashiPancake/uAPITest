import sys as _sys
import logging


def create_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
  """
  创建一个配置好的日志器，包含控制台输出和文件输出。
  """
  logger = logging.getLogger(name)

  # 避免重复添加Handler
  if logger.handlers:
    return logger

  logger.setLevel(level)

  # 定义日志格式
  formatter = logging.Formatter(
    '[ %(name)-10s ] %(asctime)-24s | %(levelname)-8s | %(message)s'
  )

  # 过滤器 - 输出到stdout
  class StdOutFilter(logging.Filter):
    def filter(self, record):
      return record.levelno <= logging.INFO

  # 过滤器 - 输出到stderr
  class StdErrFilter(logging.Filter):
    def filter(self, record):
      return record.levelno > logging.INFO

  # 控制台handler（warning级别以下）
  console_handler_stdout = logging.StreamHandler(_sys.stdout)
  console_handler_stdout.addFilter(StdOutFilter())
  console_handler_stdout.setLevel(logging.DEBUG)
  console_handler_stdout.setFormatter(formatter)
  logger.addHandler(console_handler_stdout)

  # 控制台handler（warning级别至warning级别以上）
  console_handler_stderr = logging.StreamHandler(_sys.stderr)
  console_handler_stderr.addFilter(StdErrFilter())
  console_handler_stderr.setLevel(logging.WARNING)
  console_handler_stderr.setFormatter(formatter)
  logger.addHandler(console_handler_stderr)

  # Todo: 加入文件handler
  # 文件handler
  #file_handler = logging.FileHandler('app.log', encoding='utf-8')
  #file_handler.setLevel(logging.DEBUG)
  #file_handler.setFormatter(formatter)
  #logger.addHandler(file_handler)

  return logger

