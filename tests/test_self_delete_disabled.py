import ttrpg


def test_self_delete_is_disabled():
    client = ttrpg.app.test_client()

    with client.session_transaction() as sess:
        sess["username"] = "existing_user"

    response = client.post(
        "/accounts/",
        data={"operation": "delete"},
        follow_redirects=False,
    )

    assert response.status_code == 403
