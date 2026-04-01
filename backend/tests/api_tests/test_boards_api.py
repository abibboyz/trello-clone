import pytest


@pytest.mark.asyncio
async def test_create_board_success(client):
    response = await client.post(
        "/boards/",
        json={"title": "Board A", "description": "Main board", "is_active": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["title"] == "Board A"


@pytest.mark.asyncio
async def test_get_all_boards_returns_created_board(client):
    await client.post(
        "/boards/",
        json={"title": "Board B", "description": "Another board", "is_active": True},
    )

    response = await client.get("/boards/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(board["title"] == "Board B" for board in data)


@pytest.mark.asyncio
async def test_get_one_board_success(client):
    create_response = await client.post(
        "/boards/",
        json={"title": "Board C", "description": "Board detail", "is_active": True},
    )
    board_id = create_response.json()["id"]

    response = await client.get(f"/boards/{board_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == board_id
    assert data["title"] == "Board C"


@pytest.mark.asyncio
async def test_get_one_board_not_found(client):
    response = await client.get("/boards/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Board not found"
