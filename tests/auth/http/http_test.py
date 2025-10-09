import pytest
from faker.proxy import Faker
from httpx import AsyncClient

from city_api.infrastructure.auth.handler.change_password import ChangePasswordRequest
from city_api.infrastructure.auth.handler.log_in import LoginInRequest
from city_api.infrastructure.auth.handler.sign_up import SignUpRequest


@pytest.mark.parametrize(
    'token, expected_status',
    [('valid_access_token', 200), ('invalid_access_token', 401)],
)
async def test_get_behavior_with_valid_and_invalid_token(
    clean_http_client: AsyncClient, token: str, expected_status: int, request
) -> None:
    response = await clean_http_client.get(
        '/test_end/test_security',
        cookies={'access_token': request.getfixturevalue(token)},
    )

    assert response.status_code == expected_status


@pytest.fixture
def sign_up_request(faker: Faker) -> SignUpRequest:
    return SignUpRequest(email=faker.pystr(), password=faker.pystr())


async def test_sign_up(
    sign_up_request: SignUpRequest,
    clean_http_client: AsyncClient,
) -> None:
    response = await clean_http_client.post(
        '/auth/signup',
        json={'email': sign_up_request.email, 'password': sign_up_request.password},
    )
    assert response.status_code == 201


async def test_sign_up_user_already_exist_error(
    sign_up_request: SignUpRequest,
    clean_http_client: AsyncClient,
) -> None:
    await clean_http_client.post(
        '/auth/signup',
        json={'email': sign_up_request.email, 'password': sign_up_request.password},
    )
    response = await clean_http_client.post(
        '/auth/signup',
        json={'email': sign_up_request.email, 'password': sign_up_request.password},
    )

    assert response.status_code == 403
    assert response.json()['detail'] == 'User with this login or email already exist'


@pytest.fixture
def log_in_request(faker: Faker) -> LoginInRequest:
    return LoginInRequest(email=faker.pystr(), password=faker.pystr())


@pytest.fixture
async def user_signed_up(
    clean_http_client: AsyncClient, log_in_request: LoginInRequest
):
    await clean_http_client.post(
        '/auth/signup',
        json={'email': log_in_request.email, 'password': log_in_request.password},
    )


async def test_login_in(
    log_in_request: LoginInRequest,
    clean_http_client: AsyncClient,
    user_signed_up,
) -> None:
    response = await clean_http_client.post(
        '/auth/login',
        json={'email': log_in_request.email, 'password': log_in_request.password},
    )
    assert response.status_code == 204


async def test_login_user_not_exist_error(
    log_in_request: LoginInRequest,
    clean_http_client: AsyncClient,
) -> None:
    response = await clean_http_client.post(
        '/auth/login',
        json={'email': log_in_request.email, 'password': log_in_request.password},
    )
    assert response.status_code == 409
    assert response.json()['detail'] == "User with this login or email doesn't exist"


async def test_login_user_wrong_password_error(
    log_in_request: LoginInRequest,
    clean_http_client: AsyncClient,
    user_signed_up,
) -> None:
    response = await clean_http_client.post(
        '/auth/login',
        json={
            'email': log_in_request.email,
            'password': f'{log_in_request.password}_trash',
        },
    )
    assert response.status_code == 403
    assert response.json()['detail'] == 'Wrong password'


@pytest.fixture
def change_password_request(faker: Faker) -> ChangePasswordRequest:
    return ChangePasswordRequest(
        email=faker.pystr(),
        current_password=faker.pystr(),
        new_password=faker.pystr(),
    )


@pytest.fixture
async def user_signed_up_and_logged_in(
    clean_http_client: AsyncClient, change_password_request: ChangePasswordRequest
):
    await clean_http_client.post(
        '/auth/signup',
        json={
            'email': change_password_request.email,
            'password': change_password_request.current_password,
        },
    )
    await clean_http_client.post(
        '/auth/login',
        json={
            'email': change_password_request.email,
            'password': change_password_request.current_password,
        },
    )


async def test_change_password(
    change_password_request: ChangePasswordRequest,
    clean_http_client: AsyncClient,
    user_signed_up_and_logged_in,
) -> None:
    response = await clean_http_client.post(
        '/auth/change_password',
        json={
            'email': str(change_password_request.email),
            'current_password': change_password_request.current_password,
            'new_password': 'change_password_request.new_password',
        },
    )

    assert response.status_code == 204


async def test_change_password_logged_out_error(
    change_password_request: ChangePasswordRequest, clean_http_client: AsyncClient
) -> None:
    response = await clean_http_client.post(
        '/auth/change_password',
        json={
            'email': str(change_password_request.email),
            'current_password': change_password_request.current_password,
            'new_password': change_password_request.new_password,
        },
    )

    assert response.status_code == 403
    assert response.json()['detail'] == "You're logged out"


async def test_change_password_same_password_error(
    change_password_request: ChangePasswordRequest,
    clean_http_client: AsyncClient,
    user_signed_up_and_logged_in,
) -> None:
    response = await clean_http_client.post(
        '/auth/change_password',
        json={
            'email': str(change_password_request.email),
            'current_password': change_password_request.current_password,
            'new_password': change_password_request.current_password,
        },
    )

    assert response.status_code == 403
    assert response.json()['detail'] == 'New password must differ from current password'


async def test_change_password_wrong_password_error(
    change_password_request: ChangePasswordRequest,
    clean_http_client: AsyncClient,
    user_signed_up_and_logged_in,
) -> None:
    response = await clean_http_client.post(
        '/auth/change_password',
        json={
            'email': str(change_password_request.email),
            'current_password': f'{change_password_request.current_password}_trash',
            'new_password': change_password_request.current_password,
        },
    )

    assert response.status_code == 403
    assert response.json()['detail'] == 'Wrong password'


@pytest.fixture
def logout_request(faker: Faker) -> LoginInRequest:
    return LoginInRequest(
        email=faker.pystr(),
        password=faker.pystr(),
    )


async def test_logout(
    logout_request: LoginInRequest,
    clean_http_client: AsyncClient,
    user_signed_up_and_logged_in,
) -> None:
    response = await clean_http_client.post('/auth/logout')
    assert response.status_code == 204


async def test_logout_user_already_logged_out_error(
    logout_request: LoginInRequest,
    clean_http_client: AsyncClient,
    user_signed_up_and_logged_in,
) -> None:
    await clean_http_client.post('/auth/logout')
    response = await clean_http_client.post('/auth/logout')
    assert response.status_code == 403
    assert response.json()['detail'] == 'User already logged out'
