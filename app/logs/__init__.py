from app.logs.logger import AppLogger



Logger = AppLogger().get_logger()


__all__ = ['Logger']
