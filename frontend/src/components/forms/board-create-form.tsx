"use client";

import { useActionState, useEffect, useRef } from "react";
import { createBoardAction, type FormActionState } from "@/app/boards/actions";
import { SubmitButton } from "@/components/forms/submit-button";

const initialState: FormActionState = {};

export function BoardCreateForm() {
  const [state, formAction] = useActionState(createBoardAction, initialState);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    if (state.success) {
      formRef.current?.reset();
    }
  }, [state.success]);

  return (
    <form action={formAction} className="card-panel space-y-4 p-5 shadow-card" ref={formRef}>
      <div>
        <h2 className="text-lg font-semibold">Create board</h2>
        <p className="text-sm text-muted">Add a new board to start organizing work.</p>
      </div>

      {state.error ? <p className="error-banner text-sm">{state.error}</p> : null}
      {state.success ? <p className="success-banner text-sm">{state.success}</p> : null}

      <label className="block text-sm font-medium" htmlFor="board-title">
        Board title
      </label>
      <input
        id="board-title"
        className="input-field"
        type="text"
        name="title"
        maxLength={255}
        placeholder="Engineering Roadmap"
        required
      />

      <label className="block text-sm font-medium" htmlFor="board-description">
        Description
      </label>
      <textarea
        id="board-description"
        className="input-field min-h-24"
        name="description"
        maxLength={1000}
        placeholder="Optional description"
      />

      <SubmitButton idleText="Create board" pendingText="Creating..." />
    </form>
  );
}