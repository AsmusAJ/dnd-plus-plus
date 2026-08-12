import ttrpg


def test_invalid_login_returns_login_page_with_error_message():
    client = ttrpg.app.test_client()

    response = client.post(
        '/accounts/',
        data={
            'operation': 'login',
            'username': 'no_such_user',
            'password': 'wrongpassword',
        },
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert b'Incorrect username or password' in response.data
