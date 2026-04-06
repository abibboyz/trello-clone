import Link from "next/link";
import { ApiError, getBoards } from "@/lib/api";
import { BoardCreateForm } from "@/components/forms/board-create-form";

export default async function BoardsPage() {
  try {
    const boards = await getBoards();

    return (
      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-8 px-4 py-8 sm:px-6 md:px-8">
        <header className="space-y-3">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-accent">
            Board Directory
          </p>
          <h1 className="text-3xl font-semibold md:text-4xl">Boards</h1>
          <p className="text-muted">
            Create a board and open it to manage lists and cards.
          </p>
        </header>

        <section className="grid items-start gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="card-panel p-5 shadow-card">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold">Available boards</h2>
              <span className="rounded-full border border-panel-border px-3 py-1 text-sm text-muted">
                {boards.length} total
              </span>
            </div>

            {boards.length === 0 ? (
              <p className="rounded-xl border border-dashed border-panel-border p-6 text-muted">
                No boards created yet. Use the form to create your first board.
              </p>
            ) : (
              <ul className="grid gap-3 md:grid-cols-2">
                {boards.map((board) => (
                  <li key={board.id} className="card-panel p-4 transition-transform hover:-translate-y-0.5">
                    <h3 className="text-lg font-semibold">{board.title}</h3>
                    <p className="mt-2 line-clamp-2 min-h-10 text-sm text-muted">
                      {board.description || "No description provided."}
                    </p>
                    <div className="mt-3 flex items-center justify-between text-xs text-muted">
                      <span>{board.lists.length} lists</span>
                      <Link className="btn-secondary" href={`/boards/${board.id}`}>
                        Open board
                      </Link>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <BoardCreateForm />
        </section>
      </main>
    );
  } catch (error) {
    const message =
      error instanceof ApiError
        ? `${error.message} (status ${error.status})`
        : "Could not load boards.";

    return (
      <main className="mx-auto flex w-full max-w-4xl flex-1 flex-col gap-4 px-4 py-10 sm:px-6">
        <h1 className="text-3xl font-semibold">Boards</h1>
        <p className="error-banner">{message}</p>
        <p className="text-sm text-muted">
          Confirm your FastAPI backend is running and reachable from the frontend server.
        </p>
      </main>
    );
  }
}