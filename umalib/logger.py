import logging

def getlogger(name: str = __name__, level: str = "DEBUG") -> logging.Logger:
    """
    ロガーを取得する関数

    Parameters:
        name (str, optional): ロガーの名前。デフォルトは__name__（呼び出し元のモジュール名）。
        level (str, optional): ログレベルの文字列。"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" のいずれかを指定できます。デフォルトは"DEBUG"。

    Returns:
        logging.Logger: 指定された名前とログレベルで設定されたロガー。
    """
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    level = log_levels.get(level, logging.DEBUG)
    logging.basicConfig(
        level=level,
        format="{asctime} [{levelname:.4}] {name}: {message}",
        style="{",
    )
    for logger_name in logging.root.manager.loggerDict.keys():
        if logger_name != name:
            logging.getLogger(logger_name).setLevel(logging.WARNING)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger