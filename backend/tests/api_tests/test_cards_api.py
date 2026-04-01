import pytest


@pytest.mark.asyncio
async def test_create_card_success(client):
    board_response = await client.post(
        "/boards/",
        json={"title": "Board For Card", "description": "Board", "is_active": True},
    )
    board_id = board_response.json()["id"]

    list_response = await client.post(
        "/lists/",
        json={"title": "Done", "board_id": board_id},
    )
    list_id = list_response.json()["id"]

    response = await client.post(
        "/cards/",
        json={"title": "Card 1", "description": "Card description", "list_id": list_id},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["list_id"] == list_id
    assert data["title"] == "Card 1"


@pytest.mark.asyncio
async def test_create_card_list_not_found(client):
    response = await client.post(
        "/cards/",
        json={"title": "Card 404", "description": "Invalid list", "list_id": 99999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "List 99999 not found"


@pytest.mark.asyncio
async def test_get_all_cards_returns_created_card(client):
    board_response = await client.post(
        "/boards/",
        json={"title": "Board For Card Read", "description": "Board", "is_active": True},
    )
    board_id = board_response.json()["id"]

    list_response = await client.post(
        "/lists/",
        json={"title": "Todo Cards", "board_id": board_id},
    )
    list_id = list_response.json()["id"]

    await client.post(
        "/cards/",
        json={"title": "Card Read", "description": "Read me", "list_id": list_id},
    )

    response = await client.get("/cards/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(card["title"] == "Card Read" for card in data)


@pytest.mark.asyncio
async def test_get_one_card_not_found(client):
    response = await client.get("/cards/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"
