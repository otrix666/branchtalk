import bcrypt

from branchtalk_api.application import interfaces


class BcryptPasswordHasher(interfaces.PasswordHasher):
    def hash(self, raw_password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(raw_password.encode(), salt)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())
