from sqlalchemy.ext.asyncio import AsyncSession

class UserCRUD:
    def __init__(self, session: AsyncSession):
        self._session = session
