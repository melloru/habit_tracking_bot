from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Habit


async def orm_add_habit(session: AsyncSession, data: dict):
    obj = Habit(
        name=data['name'],
        time=int(data['time'])
    )
    session.add(obj)
    await session.commit()
