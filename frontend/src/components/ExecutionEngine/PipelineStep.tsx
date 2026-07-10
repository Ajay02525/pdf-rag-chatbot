"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight, CheckCircle2 } from "lucide-react";

import { PipelineStep as Step } from "@/types/pipeline";

import PipelineChildren from "./PipelineChildren";

interface Props {
  step: Step;
}

export default function PipelineStep({ step }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div>

      <button
        onClick={() => setOpen(!open)}
        className="w-full flex justify-between items-center px-4 py-3 hover:bg-[var(--hover)]"
      >
        <div className="flex items-center gap-2">

          <CheckCircle2
            size={18}
            className="text-[var(--accent)]"
          />

          <span>{step.title}</span>

        </div>

        <div className="flex items-center gap-3">

          <span className="text-xs text-zinc-500">
            {step.duration_ms.toFixed(2)} ms
          </span>

          {open ? (
            <ChevronDown size={16} />
          ) : (
            <ChevronRight size={16} />
          )}

        </div>
      </button>

      {open && (
        <div className="px-6 pb-4 bg-[var(--assistant-bg)]">

          <div className="space-y-2">

            {Object.entries(step.fields).map(([key, value]) => (
              <div
                key={key}
                className="flex justify-between text-sm"
              >
                <span className="text-zinc-500">{key}</span>

                <span>
                  {typeof value === "object"
                    ? JSON.stringify(value)
                    : String(value)}
                </span>

              </div>
            ))}

          </div>

          {step.children.length > 0 && (
            <PipelineChildren
              children={step.children}
            />
          )}

        </div>
      )}

    </div>
  );
}