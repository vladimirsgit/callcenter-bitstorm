from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from sqlmodel import select

async def create_item(db_session: AsyncSession, item: Item):
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item
    

async def get_items(db_session: AsyncSession):
    query = select(Item)
    res = await db_session.execute(query)
    
    return res.scalars().all()
