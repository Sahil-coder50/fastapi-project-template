class UserService:

    def __init__(self, repo):
        self.repo = repo

    def create_user(self, data):
        return self.repo.create(data)