import logging as _logging


def create_logger(name: str = "app_logger", level: int = _logging.DEBUG) -> _logging.Logger:
  """
  创建一个配置好的日志器，包含控制台输出和文件输出。
  """
  logger = _logging.getLogger(name)

  # 避免重复添加Handler
  if logger.handlers:
    return logger

  logger.setLevel(level)

  # 定义日志格式
  formatter = _logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
  )

  # 控制台处理器
  console_handler = _logging.StreamHandler(sys.stdout)
  console_handler.setLevel(_logging.INFO)
  console_handler.setFormatter(formatter)
  logger.addHandler(console_handler)

  # 文件处理器
  file_handler = _logging.FileHandler('app.log', encoding='utf-8')
  file_handler.setLevel(_logging.DEBUG)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)

  return logger
