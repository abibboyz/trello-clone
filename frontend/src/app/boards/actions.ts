"use server";

import { revalidatePath } from "next/cache";
import { createBoard } from "@/lib/api";

export interface FormActionState {
  error?: string;
  success?: string;
}

const MAX_BOARD_TITLE = 255;
const MAX_BOARD_DESCRIPTION = 1000;

export async function createBoardAction(
  _previousState: FormActionState,
  formData: FormData,
): Promise<FormActionState> {
  const title = String(formData.get("title") ?? "").trim();
  const description = String(formData.get("description") ?? "").trim();

  if (!title) {
    return { error: "Board title is required." };
  }

  if (title.length > MAX_BOARD_TITLE) {
    return { error: "Board title cannot exceed 255 characters." };
  }

  if (description.length > MAX_BOARD_DESCRIPTION) {
    return { error: "Description cannot exceed 1000 characters." };
  }

  try {
    await createBoard({
      title,
      description: description || undefined,
      is_active: true,
    });
    revalidatePath("/boards");
    return { success: "Board created." };
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Could not create board.";
    return { error: message };
  }
}