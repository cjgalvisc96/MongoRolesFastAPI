import pytest
from bson.objectid import ObjectId
from faker import Faker
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app import crud, schemas
from app.core.security import verify_password
from app.models.user import User

faker_data = Faker()


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    fake_email = faker_data.email()
    fake_password = faker_data.password(length=12)
    fake_full_name = faker_data.name()
    fake_phone_number = "3191231234"
    fake_account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=fake_email,
        password=fake_password,
        full_name=fake_full_name,
        phone_number=fake_phone_number,
        account_id=str(fake_account_id),
    )
    user = await crud.user.create(obj_in=user_in)
    assert type(user) is User
    assert user.email == fake_email
    assert user.full_name == fake_full_name
    assert user.phone_number == fake_phone_number
    assert user.account_id == fake_account_id
    assert hasattr(user, "hashed_password")
    assert verify_password(fake_password, user.hashed_password)


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient) -> None:
    users_created = []
    users_to_create = 5
    for _ in range(users_to_create):
        fake_email = faker_data.email()
        fake_password = faker_data.password(length=12)
        fake_full_name = faker_data.name()
        fake_phone_number = "3191231234"
        fake_account_id = ObjectId()
        user_in = schemas.UserCreate(
            email=fake_email,
            password=fake_password,
            full_name=fake_full_name,
            phone_number=fake_phone_number,
            account_id=str(fake_account_id),
        )
        user_created = await crud.user.create(obj_in=user_in)
        users_created.append(user_created)
    users = await crud.user.get_multi(skip=0, limit=users_to_create)
    assert len(users) == users_to_create
    assert type(users) is list
    assert type(users[0]) is User


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient) -> None:
    fake_email = faker_data.email()
    fake_password = faker_data.password(length=12)
    fake_full_name = faker_data.name()
    fake_phone_number = "3191231234"
    fake_account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=fake_email,
        password=fake_password,
        full_name=fake_full_name,
        phone_number=fake_phone_number,
        account_id=str(fake_account_id),
    )
    user = await crud.user.create(obj_in=user_in)
    user_2 = await crud.user.get(_id=user.id)
    assert user_2
    assert type(user_2) is User
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.asyncio
async def test_get_user_by_email(client: AsyncClient) -> None:
    fake_email = faker_data.email()
    fake_password = faker_data.password(length=12)
    fake_full_name = faker_data.name()
    fake_phone_number = "3191231234"
    fake_account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=fake_email,
        password=fake_password,
        full_name=fake_full_name,
        phone_number=fake_phone_number,
        account_id=str(fake_account_id),
    )
    user = await crud.user.create(obj_in=user_in)
    user_2 = await crud.user.get_by_email(email=fake_email)
    assert user_2
    assert type(user_2) is User
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient) -> None:
    fake_email = faker_data.email()
    fake_password = faker_data.password(length=12)
    fake_full_name = faker_data.name()
    fake_phone_number = "3191231234"
    fake_account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=fake_email,
        password=fake_password,
        full_name=fake_full_name,
        phone_number=fake_phone_number,
        account_id=str(fake_account_id),
    )
    user = await crud.user.create(obj_in=user_in)

    new_user_password = faker_data.password(length=12)
    new_user_full_name = faker_data.name()
    new_user_phone_number = "3191231235"
    user_in_update = schemas.UserUpdate(
        password=new_user_password,
        full_name=new_user_full_name,
        phone_number=new_user_phone_number,
    )
    await crud.user._update(_id=user.id, obj_in=user_in_update)

    user_updated = await crud.user.get(_id=user.id)
    assert user_updated
    assert type(user_updated) is User
    assert user.email == user_updated.email
    assert user_updated.full_name == new_user_full_name
    assert user_updated.phone_number == new_user_phone_number
    assert hasattr(user_updated, "hashed_password")
    assert verify_password(new_user_password, user_updated.hashed_password)


@pytest.mark.asyncio
async def test_remove_user(client: AsyncClient) -> None:
    fake_email = faker_data.email()
    fake_password = faker_data.password(length=12)
    fake_full_name = faker_data.name()
    fake_phone_number = "3191231234"
    fake_account_id = ObjectId()
    user_in = schemas.UserCreate(
        email=fake_email,
        password=fake_password,
        full_name=fake_full_name,
        phone_number=fake_phone_number,
        account_id=str(fake_account_id),
    )
    user = await crud.user.create(obj_in=user_in)
    user_id = user.id
    user_deleted = await crud.user._remove(_id=user_id)
    found_user_removed = await crud.user.get(_id=user_id)
    assert user_deleted == 1
    assert not found_user_removed


@pytest.mark.asyncio
async def test_get_users_by_account_id(client: AsyncClient) -> None:
    users_created = []
    users_to_create = 5
    fake_account_id = ObjectId()
    for _ in range(users_to_create):
        fake_email = faker_data.email()
        fake_password = faker_data.password(length=12)
        fake_full_name = faker_data.name()
        fake_phone_number = "3191231234"
        user_in = schemas.UserCreate(
            email=fake_email,
            password=fake_password,
            full_name=fake_full_name,
            phone_number=fake_phone_number,
            account_id=str(fake_account_id),
        )
        user_created = await crud.user.create(obj_in=user_in)
        users_created.append(user_created)
    users_found_by_account_id = await crud.user.get_by_account_id(
        account_id=fake_account_id, skip=0, limit=users_to_create
    )
    assert len(users_found_by_account_id) == users_to_create
    assert type(users_found_by_account_id) is list
    assert type(users_found_by_account_id[0]) is User
