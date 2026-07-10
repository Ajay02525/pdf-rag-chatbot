"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

import { ExecutionPipeline as Pipeline } from "@/types/pipeline";

import PipelineHeader from "./PipelineHeader";
import PipelineStep from "./PipelineStep";

interface Props {
  pipeline: Pipeline;
}

export default function ExecutionPipeline({ pipeline }: Props) {
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-4 rounded-xl border overflow-hidden bg-[var(--surface)] border-[var(--border)] shadow-sm transition-colors duration-200">

      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 hover:bg-[var(--hover)] transition-colors"
      >
        <div className="font-medium">
          AI Execution Pipeline
        </div>

        {open ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
      </button>

      {open && (
        <>
          <PipelineHeader header={pipeline.header} />

          <div className="divide-[var(--border)]">
            {pipeline.steps.map((step) => (
              <PipelineStep
                key={step.id}
                step={step}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}