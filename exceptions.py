class DataFetchError(RuntimeError):
    def __init__(self, message):
        super(DataFetchError, self).__init__("Error fetching data from sensors: {}".format(message))


class DataParseError(RuntimeError):
    def __init__(self, message):
        super(DataParseError, self).__init__("Error parsing data: {}".format(message))
