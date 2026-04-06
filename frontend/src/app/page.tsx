
import Link from "next/link";

export default function Home() {
  return (
    <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-6 py-16">
      <section className="hero-panel rounded-3xl p-8 shadow-card md:p-12">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-accent">
          Trello Clone Workspace
        </p>
        <h1 className="mt-4 text-balance text-4xl font-semibold leading-tight md:text-6xl">
          Build boards, lists, and cards with a production-ready flow.
        </h1>
        <p className="mt-5 max-w-2xl text-lg text-muted">
          This frontend is wired to your FastAPI backend and supports robust
          create and read experiences with clear loading, empty, and error
          states.
        </p>
        <div className="mt-8 flex flex-wrap items-center gap-4">
          <Link className="btn-primary" href="/boards">
            Open Boards
          </Link>
          <span className="text-sm text-muted">Next.js 16 + FastAPI</span>
        </div>
      </section>
    </main>
  );
}
