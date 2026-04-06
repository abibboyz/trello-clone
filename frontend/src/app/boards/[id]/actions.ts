"use server";

import { revalidatePath } from "next/cache";
import { createCard, createList } from "@/lib/api";

export interface FormActionState {
  error?: string;
  success?: string;
}

const MAX_LIST_TITLE = 255;
const MAX_CARD_TITLE = 255;
const MAX_CARD_DESCRIPTION = 2000;

export async function createListAction(
  _previousState: FormActionState,
  formData: FormData,
): Promise<FormActionState> {
  const boardId = Number(formData.get("boardId"));
  const title = String(formData.get("title") ?? "").trim();

  if (!Number.isInteger(boardId) || boardId <= 0) {
    return { error: "Board id is invalid." };
  }

  if (!title) {
    return { error: "List title is required." };
  }

  if (title.length > MAX_LIST_TITLE) {
    return { error: "List title cannot exceed 255 characters." };
  }

  try {
    await createList({ board_id: boardId, title });
    revalidatePath(`/boards/${boardId}`);
    return { success: "List created." };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not create list.";
    return { error: message };
  }
}

export async function createCardAction(
  _previousState: FormActionState,
  formData: FormData,
): Promise<FormActionState> {
  const boardId = Number(formData.get("boardId"));
  const listId = Number(formData.get("listId"));
  const title = String(formData.get("title") ?? "").trim();
  const description = String(formData.get("description") ?? "").trim();

  if (!Number.isInteger(boardId) || boardId <= 0) {
    return { error: "Board id is invalid." };
  }

  if (!Number.isInteger(listId) || listId <= 0) {
    return { error: "List id is invalid." };
  }

  if (!title) {
    return { error: "Card title is required." };
  }

  if (title.length > MAX_CARD_TITLE) {
    return { error: "Card title cannot exceed 255 characters." };
  }

  if (description.length > MAX_CARD_DESCRIPTION) {
    return { error: "Description cannot exceed 2000 characters." };
  }

  try {
    await createCard({
      list_id: listId,
      title,
      description: description || undefined,
    });
    revalidatePath(`/boards/${boardId}`);
    return { success: "Card created." };
  } catch (error) {
    const message = error instanceof Error ? error.message : "Could not create card.";
    return { error: message };
  }
}