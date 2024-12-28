from concurrent.futures import ThreadPoolExecutor

from branchtalk_api.application import interfaces
from branchtalk_api.application.dto.user import UserCreateDTO
from branchtalk_api.domain.entities.users import User


class RegistrationInteractor:
    def __init__(
        self,
        user_saver: interfaces.UserSaver,
        hasher: interfaces.PasswordHasher,
        thread_pool: ThreadPoolExecutor,
    ):
        self._user_saver = user_saver
        self._hasher = hasher
        self._thread_pool = thread_pool

    async def __call__(self, data: UserCreateDTO):
        future_hashed_password = self._thread_pool.submit(self._hasher.hash, data.password)
        hashed_password = future_hashed_password.result()

        user = User(
            id=None,
            username=data.username,
            email=data.email,
            password=hashed_password.decode(),
        )

        await self._user_saver.save(user=user)
