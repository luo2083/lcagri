import logging

class TestFilter(logging.Filter):
    def filter(self, record):
        if '----' in record.msg:
            return False
        else:
            return True