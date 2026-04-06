import Link from "next/link";
import { notFound } from "next/navigation";
import { CardCreateForm } from "@/components/forms/card-create-form";
import { ListCreateForm } from "@/components/forms/list-create-form";
import { ApiError, getBoard } from "@/lib/api";

interface BoardDetailPageProps {
  params: Promise<{ id: string }>;
}

async function loadBoard(boardId: number) {
  try {
    const board = await getBoard(boardId);
    return { board, error: null as string | null, notFoundState: false };
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return { board: null, error: null, notFoundState: true };
    }

    const message =
      error instanceof ApiError
        ? `${error.message} (status ${error.status})`
        : "Could not load board details.";
    return { board: null, error: message, notFoundState: false };
  }
}

export default async function BoardDetailPage({ params }: BoardDetailPageProps) {
  const { id } = await params;
  const boardId = Number(id);

  if (!Number.isInteger(boardId) || boardId <= 0) {
    notFound();
  }

  const { board, error, notFoundState } = await loadBoard(boardId);

  if (notFoundState || !board) {
    if (notFoundState) {
      notFound();
    }

    const fallbackMessage = error ?? "Could not load board details.";
    return (
      <main className="mx-auto flex w-full max-w-4xl flex-1 flex-col gap-4 px-4 py-10 sm:px-6">
        <Link href="/boards" className="text-sm font-medium text-accent hover:underline">
          Back to boards
        </Link>
        <h1 className="text-3xl font-semibold">Board details</h1>
        <p className="error-banner">{fallbackMessage}</p>
      </main>
    );
  }

  return (
    <main className="mx-auto flex w-full max-w-[1400px] flex-1 flex-col gap-6 px-4 py-8 sm:px-6 md:px-8">
      <header className="space-y-3">
        <Link href="/boards" className="text-sm font-medium text-accent hover:underline">
          Back to boards
        </Link>
        <h1 className="text-balance text-3xl font-semibold md:text-4xl">{board.title}</h1>
        <p className="text-muted">{board.description || "No description for this board."}</p>
      </header>

      <section className="flex gap-4 overflow-x-auto pb-4">
        {board.lists.map((list) => (
          <article key={list.id} className="card-panel min-h-[320px] min-w-72 p-4 shadow-card">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-lg font-semibold">{list.title}</h2>
              <span className="text-xs text-muted">{list.cards.length} cards</span>
            </div>

            {list.cards.length === 0 ? (
              <p className="rounded-lg border border-dashed border-panel-border p-3 text-sm text-muted">
                No cards yet.
              </p>
            ) : (
              <ul className="space-y-2">
                {list.cards.map((card) => (
                  <li key={card.id} className="rounded-xl border border-panel-border bg-white p-3">
                    <h3 className="text-sm font-semibold">{card.title}</h3>
                    <p className="mt-1 text-sm text-muted">
                      {card.description || "No description provided."}
                    </p>
                  </li>
                ))}
              </ul>
            )}

            <CardCreateForm boardId={boardId} listId={list.id} />
          </article>
        ))}

        <ListCreateForm boardId={boardId} />
      </section>
    </main>
  );
}