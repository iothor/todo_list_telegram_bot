import asyncio
from datetime import datetime

import pytest

from sqlalchemy import select

from db.models import User, Task
from db.queries import (
    insert_user,
    update_user,
    delete_user,
    select_users,
    select_user_by_user_id,
    select_user_by_username,
    insert_task,
    update_task,
    delete_task,
    select_task_by_id,
    select_tasks_by_user,
)

@pytest.mark.asyncio
async def test_select_users(session):
    users = await select_users(session)
    
    assert len(users) == 2


@pytest.mark.asyncio
async def test_select_user_by_user_id(session):
    user = await select_user_by_user_id(session, 42)
    assert user.username == "@bob"


@pytest.mark.asyncio
async def test_select_user_by_username(session):
    user = await select_user_by_username(session, "@bob")
    assert user.id == 42


@pytest.mark.asyncio
async def test_insert_user(session):
    await insert_user(session, 55, "@alice")

    query = select(User).filter_by(id=55)
    user = (await session.execute(query)).scalar_one_or_none()

    assert user is not None
    assert user.username == "@alice"


@pytest.mark.asyncio
async def test_update_user(session):
    await update_user(session, 42, "@another_bob")

    query = select(User).filter_by(id=42)
    user = (await session.execute(query)).scalar_one_or_none()

    assert user.username == "@another_bob"


@pytest.mark.asyncio
async def test_delete_user(session):
    await delete_user(session, 24)

    query = select(User).filter(User.id==24)
    user = (await session.execute(query)).scalar_one_or_none()

    assert user is None


@pytest.mark.asyncio
async def test_select_task_by_id(session):
    task = await select_task_by_id(session, 123)

    assert task.text == "hi"


@pytest.mark.asyncio
async def test_select_tasks_by_user(session):
    tasks = await select_tasks_by_user(session, 42)

    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_insert_task(session):
    await insert_task(session, "test_task", datetime.now(), 42)

    query = select(Task).filter(Task.text.contains("test"))
    task = (await session.execute(query)).scalar_one_or_none()

    assert task.text == "test_task"
    assert task.user_id == 42


@pytest.mark.asyncio
async def test_update_task(session):
    await update_task(session, 123, text="hello_2", done=True)

    query = select(Task).filter_by(id=123)
    task = (await session.execute(query)).scalar_one_or_none()

    assert task.text == "hello_2"
    assert task.done


@pytest.mark.asyncio
async def test_delete_task(session):
    await delete_task(session, 123)

    query = select(Task).filter(Task.id==123)
    task = (await session.execute(query)).scalar_one_or_none()

    assert task is None
