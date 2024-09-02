# import asyncio
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Task
# from database import Base, test_session_factory, test_engine


async def insert_user(session: AsyncSession, user_id: int, username: str):
    new_user = User(id=user_id, username=username)
    session.add(new_user)
    await session.commit()


async def select_users(session: AsyncSession):
    query = select(User).options(selectinload(User.tasks))
    users = (await session.execute(query)).scalars().all()
    return users


async def select_user_by_user_id(session: AsyncSession, user_id: int):
    query = select(User).filter_by(id=user_id)
    user = (await session.execute(query)).scalar_one_or_none()
    return user


async def select_user_by_username(session: AsyncSession, username: str):
    query = select(User).filter_by(username=username)
    user = (await session.execute(query)).scalar_one_or_none()
    return user


async def update_user(session: AsyncSession, user_id: int, new_username: str):
    user = await select_user_by_user_id(session, user_id)
    user.username = new_username
    await session.commit()


async def delete_user(session: AsyncSession, user_id: int):
    query = (
        select(User)
        .options(selectinload(User.tasks))
        .filter_by(id=user_id)
    )
    user = (await session.execute(query)).scalar_one_or_none()
    await session.delete(user)
    await session.commit()


async def insert_task(session: AsyncSession, text: str, due: datetime, user_id: int):
    new_task = Task(text=text, due=due, user_id=user_id)
    session.add(new_task)
    await session.commit()


async def select_task_by_id(session: AsyncSession, task_id: int):
    query = select(Task).filter_by(id=task_id)
    task = (await session.execute(query)).scalar_one_or_none()
    return task


async def select_tasks_by_user(session: AsyncSession, user_id: int):
    query = select(User).options(selectinload(User.tasks)).filter_by(id=user_id)
    user = (await session.execute(query)).scalar_one_or_none()
    return user.tasks


async def update_task(
    session: AsyncSession,
    task_id: int,
    text: str = None,
    due: datetime = None,
    done: bool = None,
):
    task = await select_task_by_id(session, task_id)
    if task:
        task.text = text or task.text
        task.due = due or task.due
        task.done = task.done if done is None else done
        await session.commit()


async def delete_task(session: AsyncSession, task_id: int):
    task = await select_task_by_id(session, task_id)
    if task:
        await session.delete(task)
        await session.commit()


# async def main():
#     async with test_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     async with test_session_factory() as session:
#         print("_____________INSERT_________________")
#         await insert_user(session, 10, "@ihor")
#         await insert_user(session, 42, "@god")
#         print("_____________Print_________________")
#         print(await select_users(session))
#         print(await select_user_by_user_id(session, 42))
#         print(await select_user_by_username(session, "@ihor"))
#         print("_______________UPDATE/DELETE__________________")
#         await update_user(session, 10, "@iothor")
#         await insert_task(session, "Hello world!!!", datetime.now(), 42)
#         await insert_task(session, "Hello world 2!!!", datetime.now(), 42)
#         await delete_user(session, 42)
#         print(await select_users(session))
#         print("________________Tasks_____________________")
#         await insert_task(session, "Hello world!!!", datetime.now(), 10)
#         await insert_task(session, "Hello world 2!!!", datetime.now(), 10)
#         tasks = await select_tasks_by_user(session, 10)
#         print(tasks)
#         print("_______________UPDATE/DELETE__________________")
#         ids = [task.id for task in tasks]
#         await update_task(session, ids[0], text = "By world ):", done = True)
#         await delete_task(session, ids[1])
#         print(await select_tasks_by_user(session, 10))

# asyncio.run(main())
