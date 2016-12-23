
class DNSDBException(Exception):
    def __init__(self, msg):
        self.msg = "{}".format(msg)

    def __str__(self):
        return self.msg


class QuotaLimit(DNSDBException):
    pass
