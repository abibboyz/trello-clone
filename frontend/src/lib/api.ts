import { env } from "@/lib/env";
import type {
  ApiErrorBody,
  Board,
  BoardCreateInput,
  Card,
  CardCreateInput,
  List,
  ListCreateInput,
} from "@/types/trello";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    cache: "no-store",
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let detail = "Request failed";
    try {
      const payload = (await response.json()) as ApiErrorBody;
      detail = payload.detail ?? detail;
    } catch {
      // Keep default detail when server body is not JSON.
    }

    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as T;
}

export async function getBoards(): Promise<Board[]> {
  return apiRequest<Board[]>("/boards/");
}

export async function getBoard(boardId: number): Promise<Board> {
  return apiRequest<Board>(`/boards/${boardId}`);
}

export async function createBoard(input: BoardCreateInput): Promise<Board> {
  return apiRequest<Board>("/boards/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getLists(): Promise<List[]> {
  return apiRequest<List[]>("/lists/");
}

export async function createList(input: ListCreateInput): Promise<List> {
  return apiRequest<List>("/lists/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getCards(): Promise<Card[]> {
  return apiRequest<Card[]>("/cards/");
}

export async function createCard(input: CardCreateInput): Promise<Card> {
  return apiRequest<Card>("/cards/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}