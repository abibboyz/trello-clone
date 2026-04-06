"use client";

import { useActionState, useEffect, useRef } from "react";
import { createCardAction, type FormActionState } from "@/app/boards/[id]/actions";
import { SubmitButton } from "@/components/forms/submit-button";

const initialState: FormActionState = {};

interface CardCreateFormProps {
  boardId: number;
  listId: number;
}

export function CardCreateForm({ boardId, listId }: CardCreateFormProps) {
  const [state, formAction] = useActionState(createCardAction, initialState);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    if (state.success) {
      formRef.current?.reset();
    }
  }, [state.success]);

  return (
    <form action={formAction} className="mt-3 space-y-3" ref={formRef}>
      <input type="hidden" name="boardId" value={boardId} />
      <input type="hidden" name="listId" value={listId} />

      {state.error ? <p className="error-banner text-sm">{state.error}</p> : null}
      {state.success ? <p className="success-banner text-sm">{state.success}</p> : null}

      <label className="sr-only" htmlFor={`card-title-${listId}`}>
        Card title
      </label>
      <input
        id={`card-title-${listId}`}
        className="input-field"
        type="text"
        name="title"
        maxLength={255}
        required
        placeholder="Implement login flow"
      />

      <label className="sr-only" htmlFor={`card-description-${listId}`}>
        Card description
      </label>
      <textarea
        id={`card-description-${listId}`}
        className="input-field min-h-20"
        name="description"
        maxLength={2000}
        placeholder="Optional details"
      />

      <SubmitButton idleText="Create card" pendingText="Creating..." />
    </form>
  );
}