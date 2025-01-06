from asyncpg import UniqueViolationError
from asyncpg.pool import Pool

from branchtalk_api.application import interfaces
from branchtalk_api.domain.entities.users import User
from branchtalk_api.domain.exceptions.user import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
    UserNotFoundById,
    UserNotFoundByUsername,
)
from branchtalk_api.infrastructure.data_mappers.user import UserDataMapper


class UserRepository(
    interfaces.UserReader,
    interfaces.UserSaver,
):
    def __init__(
        self,
        pool: Pool,
        mapper: UserDataMapper,
    ):
        self._pool = pool
        self._mapper = mapper

    async def get_by_id(self, user_id: int) -> User:
        async with self._pool.acquire() as connection:
            query = 'SELECT id, username, email, password_hash FROM users WHERE id = $1'
            result = await connection.fetchrow(query, user_id)
            if not result:
                raise UserNotFoundById(user_id)

            return self._mapper.record_to_entity(record=result)

    async def get_by_username(self, username: str) -> User:
        async with self._pool.acquire() as connection:
            query = 'SELECT id, username, email, password_hash FROM users WHERE username = $1'
            result = await connection.fetchrow(query, username)
            if not result:
                raise UserNotFoundByUsername(username)

            return self._mapper.record_to_entity(record=result)

    async def save(self, user: User) -> None:
        try:
            async with self._pool.acquire() as connection:
                async with connection.transaction():
                    stmt = 'INSERT INTO users (username, email, password_hash) VALUES ($1, $2, $3)'
                    await connection.execute(stmt, user.username, user.email, user.password)
        except UniqueViolationError as e:
            if 'username' in str(e):
                raise UsernameAlreadyExists(user.username)
            if 'email' in str(e):
                raise EmailAlreadyExists(user.email)
