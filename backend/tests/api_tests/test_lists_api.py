import pytest

@pytest.mark.asyncio
async def test_create_list_success(client):
    board_response = await client.post(
        "/boards/",
        json={"title": "Board For List", "description": "Board", "is_active": True},
    )
    board_id = board_response.json()["id"]

    response = await client.post(
        "/lists/",
        json={"title": "Todo", "board_id": board_id},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["board_id"] == board_id
    assert data["title"] == "Todo"


@pytest.mark.asyncio
async def test_create_list_board_not_found(client):
    response = await client.post(
        "/lists/",
        json={"title": "Todo", "board_id": 99999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Board 99999 not found"


@pytest.mark.asyncio
async def test_get_all_lists_returns_created_list(client):
    board_response = await client.post(
        "/boards/",
        json={"title": "Board For List Read", "description": "Board", "is_active": True},
    )
    board_id = board_response.json()["id"]

    await client.post(
        "/lists/",
        json={"title": "In Progress", "board_id": board_id},
    )

    response = await client.get("/lists/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(lst["title"] == "In Progress" for lst in data)


@pytest.mark.asyncio
async def test_get_one_list_not_found(client):
    response = await client.get("/lists/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "List not found"
