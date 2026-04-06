import Link from "next/link";

export default function BoardNotFound() {
  return (
    <main className="mx-auto flex w-full max-w-4xl flex-1 flex-col gap-4 px-4 py-10 sm:px-6">
      <h1 className="text-3xl font-semibold">Board not found</h1>
      <p className="text-muted">
        The board does not exist or is not accessible with the current backend state.
      </p>
      <div>
        <Link href="/boards" className="btn-secondary">
          Return to boards
        </Link>
      </div>
    </main>
  );
}