from resources.Message import ClsMessage, MessagesCode


class Result:
    def __init__(self, code, culture_name = 'en-US', error = ''):
        self.code = code
        self.culture_name = culture_name
        self.error = error

    def get_result(self):
        message = ClsMessage.get(self.code, self.culture_name)
        if message is None:
            message = ClsMessage.get(self.code, 'en-US')
            if message is None:
                message = ClsMessage.get(MessagesCode.NO_MESSAGE_WAS_FOUND.value, 'en-US')

        result = {
                "code": message.CODE,
                "description": message.DESCRIPTION,
                "errorResult": self.error
            }
        return result
