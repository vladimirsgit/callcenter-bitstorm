from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from sqlmodel import select

async def add_convo(db_session: AsyncSession, conversation: Conversation):
    db_session.add(conversation)
    await db_session.commit()
    await db_session.refresh(conversation)
    return conversation
    

async def read_convos(db_session: AsyncSession):
    query = select(Conversation)
    res = await db_session.execute(query)
    
    return res.scalars().all()
