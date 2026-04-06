## Trello Clone Frontend

This frontend is built with Next.js 16 (App Router) and connects to the FastAPI backend in the sibling backend folder.

## Prerequisites

1. Node.js 20+.
2. The FastAPI backend running locally (default: http://127.0.0.1:8000).

## Environment

Create frontend/.env.local with:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

You can also set API_BASE_URL if you want a server-only override.

## Run

From the frontend directory:

```bash
npm install
npm run dev
```

Open http://localhost:3000.

## Routes

1. /: Landing page with quick entry to boards.
2. /boards: Board index (list boards + create board).
3. /boards/[id]: Board workspace (read board with nested lists/cards + create list + create card).

## Supported Operations (Current Backend Contract)

The UI intentionally matches the currently available FastAPI endpoints.

1. Boards: create, list, and fetch by id.
2. Lists: create and read via board payload.
3. Cards: create and read via board payload.

Not yet supported by backend endpoints:

1. Update/edit board/list/card.
2. Delete board/list/card.
3. Reorder operations.
4. Pagination and server-side filtering.

## Validation and UX

1. Form validation mirrors backend constraints.
2. Loading, empty, and error states are implemented on boards and board detail routes.
3. Server Actions are used for create flows to avoid browser CORS issues when backend does not expose CORS middleware.

## Quality Checks

```bash
npm run lint
npm run build
```

## Notes

If backend host/port changes, update NEXT_PUBLIC_API_URL (or API_BASE_URL).

