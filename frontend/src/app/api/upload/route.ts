import { NextRequest } from "next/server";

export const runtime = "nodejs";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function POST(req: NextRequest) {
  const formData = await req.formData();

  const response = await fetch(`${BACKEND_URL}/upload`, {
    method: "POST",
    body: formData,
    signal: req.signal,
  });

  if (!response.ok) {
    return new Response(await response.text(), {
      status: response.status,
    });
  }

  return new Response(await response.text(), {
    status: response.status,
    headers: {
      "Content-Type": "application/json",
    },
  });
}