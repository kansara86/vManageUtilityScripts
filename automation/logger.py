import logging
import os
from functools import wraps


class Log(logging.Logger):
    def __init__(self, name, logging_level=logging.DEBUG, log_file='network-standards.log', stream_to_stdout=True):
        super(Log, self).__init__(name)

        root_dir = os.path.dirname(os.path.dirname(__file__))
        self.log_file_path = os.path.join(root_dir, log_file)
        self.stream_to_stdout = stream_to_stdout
        self.formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

        self.log_file_handler = logging.FileHandler(self.log_file_path)
        self.log_file_handler.setFormatter(self.formatter)
        self.addHandler(self.log_file_handler)
        
        if self.stream_to_stdout:
            self.log_stream_handler = logging.StreamHandler()
            self.log_stream_handler.setFormatter(self.formatter)
            self.addHandler(self.log_stream_handler)
        
        self.setLevel(logging_level)

    def log_this(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.debug('In function {}'.format(func.__name__))
            try:
                result = func(*args, **kwargs)
                return result
            except KeyboardInterrupt as ke:
                self.error('Exception: KeyboardInterrupt, {}'.format(', '.join(ke.args)))
                raise
            except Exception as e:
                self.error('Exception: {}, {}'.format(e.__class__.__name__, ', '.join(e.args)))
                raise
            finally:
                self.debug('Exiting function {}'.format(func.__name__))
        return wrapper
    
    def __del__(self):
        self.removeHandler(self.log_file_handler)
        self.log_file_handler.close()
        if self.stream_to_stdout:
            self.removeHandler(self.log_stream_handler)
            self.log_stream_handler.close()

