export default function BoardsLoading() {
  return (
    <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-6 px-4 py-8 sm:px-6 md:px-8">
      <div className="h-8 w-52 animate-pulse rounded bg-stone-200" />
      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="card-panel h-72 animate-pulse bg-white/70 p-4" />
        <div className="card-panel h-72 animate-pulse bg-white/70 p-4" />
      </div>
    </main>
  );
}