from uuid import uuid4

class UuidUtil:
    @staticmethod
    def generateUUID():
        return str(uuid4())