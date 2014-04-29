class ReviewerNode:
    def __init__(self, uId):
        self.auth = 1
        self.hub = 1
        self.user_id = uId
        self.linkTo = []
        self.linkedBy = []
    def __hash__(self):
        return self.user_id.__hash__()
    def __cmp__(self, other):
        return cmp(self.user_id, other.user_id)
    def __str__(self):
        return self.user_id
