class ApiError(Exception):
    def __init__(self, status):
        super().__init__(status)
        self.status = status


class InvalidApiKeyError(Exception):
    def __init__(self, status):
        super().__init__(status)
        self.status = status


class ApiQuotaExceededError(Exception):
    def __init__(self, status):
        super().__init__(status)
        self.status = status


class TooManyRequestsError(Exception):
    def __init__(self, status):
        super().__init__(status)
        self.status = status


class StationNotFoundError(Exception):
    def __init__(self, status):
        super().__init__(status)
        self.status = status