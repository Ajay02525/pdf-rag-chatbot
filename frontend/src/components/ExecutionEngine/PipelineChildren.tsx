import { PipelineChild } from "@/types/pipeline";

interface Props {
  children: PipelineChild[];
}

export default function PipelineChildren({ children }: Props) {

  return (
    <div className="mt-5 border-l bg-[var(--assistant-bg)] pl-5">

      <div className="font-medium mb-3">
        Internal Execution
      </div>

      {children.map((child) => (

        <div
          key={child.id}
          className="mb-4"
        >

          <div className="font-medium">
            {child.title}
          </div>

          <div className="ml-3 mt-2 space-y-1">

            {Object.entries(child.fields).map(([k, v]) => (

              <div
                key={k}
                className="flex justify-between text-sm"
              >

                <span className="text-[var(--muted)]">
                  {k}
                </span>

                <span className="text-[var(--muted)] px-1 py-1 rounded-md text-xs font-medium bg-[var(--hover)]">
                  {String(v)}
                </span>

              </div>

            ))}

          </div>

        </div>

      ))}

    </div>
  );
}