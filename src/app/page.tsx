"use client";

import { useMemo } from "react";
import {
  decrement,
  increment,
  incrementByAmount,
  reset,
} from "@/lib/features/counter/counterSlice";
import { useAppDispatch, useAppSelector } from "@/lib/hooks";

export default function Home() {
  const dispatch = useAppDispatch();
  const count = useAppSelector((state) => state.counter.value);
  const doubled = useMemo(() => count * 2, [count]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-6 py-16 text-zinc-900">
      <main className="w-full max-w-xl rounded-2xl border border-zinc-200 bg-white p-10 shadow-sm">
        <header className="space-y-3">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-zinc-500">
            Redux Toolkit Example
          </p>
          <h1 className="text-3xl font-semibold tracking-tight">
            Counter with Next.js + Tailwind
          </h1>
          <p className="text-base text-zinc-600">
            This page reads and updates global state from the Redux store.
          </p>
        </header>

        <section className="mt-10 space-y-6">
          <div className="flex items-end justify-between">
            <div>
              <p className="text-sm text-zinc-500">Current value</p>
              <p className="text-4xl font-semibold text-zinc-900">{count}</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-zinc-500">Doubled</p>
              <p className="text-2xl font-medium text-zinc-700">{doubled}</p>
            </div>
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            <button
              className="rounded-lg border border-zinc-200 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:border-zinc-300 hover:bg-zinc-50"
              onClick={() => dispatch(decrement())}
              type="button"
            >
              Decrement
            </button>
            <button
              className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-800"
              onClick={() => dispatch(increment())}
              type="button"
            >
              Increment
            </button>
            <button
              className="rounded-lg border border-zinc-200 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:border-zinc-300 hover:bg-zinc-50"
              onClick={() => dispatch(incrementByAmount(5))}
              type="button"
            >
              Add 5
            </button>
            <button
              className="rounded-lg border border-red-200 px-4 py-2 text-sm font-medium text-red-600 transition hover:border-red-300 hover:bg-red-50"
              onClick={() => dispatch(reset())}
              type="button"
            >
              Reset
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
