export default function BoardDetailLoading() {
  return (
    <main className="mx-auto flex w-full max-w-[1400px] flex-1 flex-col gap-6 px-4 py-8 sm:px-6 md:px-8">
      <div className="h-6 w-32 animate-pulse rounded bg-stone-200" />
      <div className="h-10 w-80 animate-pulse rounded bg-stone-200" />
      <section className="flex gap-4 overflow-x-auto pb-4">
        <div className="card-panel h-96 min-w-72 animate-pulse bg-white/70 p-4" />
        <div className="card-panel h-96 min-w-72 animate-pulse bg-white/70 p-4" />
        <div className="card-panel h-64 min-w-72 animate-pulse bg-white/70 p-4" />
      </section>
    </main>
  );
}