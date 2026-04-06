export interface Card {
  id: number;
  list_id: number;
  title: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface List {
  id: number;
  board_id: number;
  title: string;
  created_at: string;
  cards: Card[];
}

export interface Board {
  id: number;
  title: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  lists: List[];
}

export interface BoardCreateInput {
  title: string;
  description?: string;
  is_active?: boolean;
}

export interface ListCreateInput {
  title: string;
  board_id: number;
}

export interface CardCreateInput {
  title: string;
  description?: string;
  list_id: number;
}

export interface ApiErrorBody {
  detail?: string;
}