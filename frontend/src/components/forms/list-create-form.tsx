"use client";

import { useActionState, useEffect, useRef } from "react";
import { createListAction, type FormActionState } from "@/app/boards/[id]/actions";
import { SubmitButton } from "@/components/forms/submit-button";

const initialState: FormActionState = {};

interface ListCreateFormProps {
  boardId: number;
}

export function ListCreateForm({ boardId }: ListCreateFormProps) {
  const [state, formAction] = useActionState(createListAction, initialState);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    if (state.success) {
      formRef.current?.reset();
    }
  }, [state.success]);

  return (
    <form action={formAction} className="card-panel h-fit min-w-72 space-y-3 p-4 shadow-card" ref={formRef}>
      <input type="hidden" name="boardId" value={boardId} />
      <h3 className="text-base font-semibold">Add list</h3>
      {state.error ? <p className="error-banner text-sm">{state.error}</p> : null}
      {state.success ? <p className="success-banner text-sm">{state.success}</p> : null}
      <label className="sr-only" htmlFor="list-title">
        List title
      </label>
      <input
        id="list-title"
        className="input-field"
        type="text"
        name="title"
        maxLength={255}
        required
        placeholder="To Do"
      />
      <SubmitButton idleText="Create list" pendingText="Creating..." />
    </form>
  );
}