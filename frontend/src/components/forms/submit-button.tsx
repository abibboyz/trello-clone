"use client";

import { useFormStatus } from "react-dom";

interface SubmitButtonProps {
  idleText: string;
  pendingText: string;
}

export function SubmitButton({ idleText, pendingText }: SubmitButtonProps) {
  const { pending } = useFormStatus();

  return (
    <button className="btn-primary" type="submit" disabled={pending}>
      {pending ? pendingText : idleText}
    </button>
  );
}