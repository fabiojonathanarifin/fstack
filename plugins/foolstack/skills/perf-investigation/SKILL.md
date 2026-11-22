---
name: perf-investigation
description: "Fix slowness with measurements, not guesses: record a trace or profile, find what actually limits it, change one thing, re-measure the same way, and report numbers with run counts. Use when a page, screen, query, API or build is slow, janky or uses too much memory."
---

# Performance investigation

The usual failure is confidently fixing the wrong thing. Every claim here comes from a measurement taken during a run, never from reading the code and guessing.

## 1. Decide before you measure

Write down the number that would change your mind ("time to interactive under 1.5s on /dial", "no frame over 16ms while scrolling the list") and how noisy the measurement is. Run it 3 to 5 times. If the spread between runs is bigger than the change you're chasing, stop and get a steadier measurement first.

## 2. Measure the real thing

Use the repo's `verify-<app>` skill when it has one, so the app runs the way users run it.

- **Web:** a Chrome performance trace (long tasks over 50ms, layout thrash, network waterfall), a heap snapshot for memory, Lighthouse for page load.
- **React Native:** the Hermes profiler, the in-app performance monitor (JS and UI frame rates), and a release build; dev builds lie about speed.
- **Backend and database:** request timing per step, `EXPLAIN ANALYZE` on the slow query, a count of queries per request (N+1).
- **Build:** the tool's own timing or stats output.

## 3. Find the limiter

Ask "why isn't this twice as fast?" and answer from the trace: the specific function, query, render, request or asset that takes the time. Then list what else the number could be measuring and rule each out: cached or skipped work, errors, code that never ran, a dev-mode cost, noise.

## 4. Fix one thing, then re-measure

Change the single biggest limiter. Re-run the exact same measurement the same number of times. Keep the change only if the number moved past the noise. One change per measurement, or you won't know which one worked.

## 5. Report

Before and after, run count, spread, the limiter you found, and the trace or profile file. If the number didn't move, say so and say what you learned.

When the fix is a pattern that will come back (a heavy import on the render path, a missing index, a query in a loop), hand it to `/correct` so a check stops it next time.
