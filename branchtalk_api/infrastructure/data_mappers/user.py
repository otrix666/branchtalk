from asyncpg import Record

from branchtalk_api.domain.entities.users import User


class UserDataMapper:
    @staticmethod
    def record_to_entity(record: Record) -> User:
        return User(
            id=record['id'],
            username=record['username'],
            email=record['email'],
            password=record['password_hash'],
        )
