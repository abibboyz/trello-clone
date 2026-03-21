"""
Database models for Trello Clone application.

All models must be imported here so they are registered with the Base metadata
when this module is loaded. This is required for create_tables() to work properly.
"""

from app.models.board import Board
from app.models.list import List
from app.models.card import Card

__all__ = ["Board", "List", "Card"]
