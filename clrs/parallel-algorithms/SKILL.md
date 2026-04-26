---
name: parallel-algorithms
description: Use when analyzing fork-join parallel algorithms, work/span bounds, greedy scheduling, slackness, determinacy races, parallel loops, matrix multiplication, merge sort, reductions, scans, stencils, or randomized parallel algorithms.
license: MIT
---

# Parallel Algorithms

## Overview

**Core principle:** analyze correctness before speed. A fork-join keyword says work may run in parallel; it does not prove race freedom, useful speedup, or production scalability.

## Shared CLRS Conventions

Use the parent `clrs` skill for mathematical formatting, theorem tone, and answer discipline. Keep every bound, recurrence, ratio, and inequality in display LaTeX blocks. Keep Markdown tables verbal; put the formulas in nearby display blocks.

## Output Discipline for Parallel Answers

Parallel-algorithm answers are notation-heavy, so formatting leaks are common. Do not announce that this skill is being used. Start with the review or solution.

Use prose names in sentences and tables, then put the notation in display blocks. For example, say "the work is quadratic" in prose, then show the bound below in a display block. Do not put work/span symbols, processor-count formulas, slackness ratios, or asymptotic bounds in table cells, headings, inline math, or inline code spans.

When a table needs a formula, write a verbal label in the cell, such as "quadratic work" or "polylogarithmic span," and put the exact expression immediately after the table.

Arithmetic is also a formula. Processor estimates such as a work term divided by a processor count plus a span term must be displayed in LaTeX blocks, not written as prose-line arithmetic with `+`, `=`, `/`, `÷`, powers, or asymptotic notation.

Safe pattern:

```markdown
The estimate for the first candidate is below.

$$
\frac{2048}{512} + 1 = 5
$$

The estimate for the second candidate is below.

$$
\frac{1024}{512} + 8 = 10
$$
```

Unsafe pattern:

```markdown
Version A: 2048 / 512 + 1 = 5 seconds.
```

## When to Use

Use this skill for:

- fork-join pseudocode using `spawn`, `sync`, or `parallel for`;
- serial projection, trace DAGs, strands, critical paths, and sequential consistency;
- work, span, speedup, parallelism, slackness, and greedy scheduling analysis;
- determinacy race reviews and shared-memory update patterns;
- parallel loops, matrix-vector multiplication, matrix multiplication, Strassen, parallel merge, and parallel merge sort;
- parallel reductions, scans, stencils, and randomized parallel algorithms;
- production reviews of textbook parallel algorithms, task granularity, scheduler overhead, work stealing, and coarsening.

Do **not** use this skill merely because code uses threads, async I/O, distributed systems, GPU kernels, or locks. Use it when the reasoning is fork-join task parallelism and work/span analysis.

## First Decision

| Situation | First obligation | Common trap |
| --- | --- | --- |
| Proposed parallel pseudocode | Check determinacy before speed | Reporting a span for racy code |
| Runtime comparison across processors | Use both work and span | Picking the lower-work version at every processor count |
| Parallel loop | Identify independent iterations | Parallelizing an accumulator update |
| Matrix or merge algorithm | Name the decomposition and combine step | Treating every merge as serial or every spawn as free |
| Production proposal | Estimate slackness and overhead | Spawning to individual elements |

## Fork-Join Semantics

`spawn` permits the child call to execute in parallel with the continuation. `sync` waits for spawned children in the current procedure. A `parallel for` describes independent loop iterations in the model, commonly implemented by recursive spawning.

The serial projection is obtained by deleting the parallel keywords. Use it to compute total work and to sanity-check the algorithm against the sequential computation.

A trace is a directed acyclic graph of strands. Edges represent serial order, spawn dependencies, return dependencies, and sync dependencies. The span is the longest path through this graph.

## Work, Span, and Scheduling Reference

Always name the three quantities before comparing algorithms:

$$
T_1 = \text{work}
$$

$$
T_\infty = \text{span}
$$

$$
T_P = \text{running time on } P \text{ processors}
$$

Use the work law and span law as lower bounds:

$$
T_P \ge \frac{T_1}{P}
$$

$$
T_P \ge T_\infty
$$

Speedup is bounded by the processor count:

$$
\frac{T_1}{T_P} \le P
$$

Parallelism is the ratio below:

$$
\frac{T_1}{T_\infty}
$$

Slackness compares available parallelism to processors:

$$
\frac{T_1}{P T_\infty}
$$

For greedy scheduling, use the bound below:

$$
T_P \le \frac{T_1}{P} + T_\infty
$$

This bound is within a factor of two of optimal. Expect near-perfect linear speedup only when slackness is much larger than one; a practical rule of thumb is to want about an order of magnitude of slackness, then verify with real overheads.

## Correctness Gate for Parallel Code

Before giving a span bound, answer these questions:

1. Which memory locations can two logically parallel strands access?
2. For each shared location, can at least one access write?
3. If yes, is there a synchronization, reduction, partitioning rule, or ownership proof that prevents a determinacy race?
4. If not, stop. The proposed parallel algorithm is nondeterministic; do not report an optimistic span as if the computation were correct.

A determinacy race occurs when two logically parallel instructions access the same memory location and at least one writes.

## Parallel Loop Pattern

For a parallel loop implemented by recursive spawning, the work matches the serial projection up to asymptotic loop-control overhead. The span adds logarithmic loop-control span to the worst iteration span:

$$
T_1 = \Theta(\text{serial projection work})
$$

$$
T_\infty = \Theta(\lg n) + \max_i T_{\infty,i}
$$

Use this only after proving iterations are independent or have a safe reduction.

## Matrix-Vector Multiplication Trap

Outer-loop parallelism is safe when each row owns its own output element. It has quadratic work and linear span:

$$
T_1 = \Theta(n^2)
$$

$$
T_\infty = \Theta(n)
$$

$$
\frac{T_1}{T_\infty} = \Theta(n)
$$

The naive nested loop below is not a better-span algorithm:

```text
parallel for each row
    parallel for each column
        add this product into the row output
```

The inner iterations race on the row output. A correct inner-parallel version must use a reduction tree or equivalent ownership discipline.

## Matrix Multiplication Reference

For the straightforward algorithm with the outer two loops parallel, the work is cubic and the span is linear:

$$
T_1 = \Theta(n^3)
$$

$$
T_\infty = \Theta(n)
$$

$$
\frac{T_1}{T_\infty} = \Theta(n^2)
$$

For recursive matrix multiplication with a temporary matrix for partial sums, the work is cubic and the span is polylogarithmic:

$$
T_1 = \Theta(n^3)
$$

$$
T_\infty = \Theta(\lg^2 n)
$$

$$
\frac{T_1}{T_\infty} = \Theta\!\left(\frac{n^3}{\lg^2 n}\right)
$$

For the parallel Strassen variant, use the bounds below:

$$
T_1 = \Theta(n^{\lg 7})
$$

$$
T_\infty = \Theta(\lg^2 n)
$$

$$
\frac{T_1}{T_\infty} = \Theta\!\left(\frac{n^{\lg 7}}{\lg^2 n}\right)
$$

## Parallel Merge Sort Reference

Naively spawning the two recursive sorts while keeping merge serial gives the same work as merge sort but only logarithmic parallelism:

$$
T_1 = \Theta(n \lg n)
$$

$$
T_\infty = \Theta(n)
$$

$$
\frac{T_1}{T_\infty} = \Theta(\lg n)
$$

The parallel merge pattern chooses the median of the larger subarray, finds its split point in the other subarray by binary search, writes the pivot to its final output position, and recursively merges the two disjoint sides. Each recursive side has at most a constant fraction of the total input, so the span is polylogarithmic.

For parallel merge:

$$
T_1 = \Theta(n)
$$

$$
T_\infty = \Theta(\lg^2 n)
$$

For parallel merge sort using that merge:

$$
T_1 = \Theta(n \lg n)
$$

$$
T_\infty = \Theta(\lg^3 n)
$$

$$
\frac{T_1}{T_\infty} = \Theta\!\left(\frac{n}{\lg^2 n}\right)
$$

Do not say merge is inherently serial. The textbook serial merge is serial; the parallel merge routine changes the merge step by partitioning output ranges.

## Reductions, Scans, Stencils, and Randomization

- Use a reduction when many parallel strands contribute to one associative result. Do not use shared read-modify-write updates.
- Use a scan when every position needs a prefix aggregate, not just the final aggregate.
- For stencils, reason about time-step dependencies before spatial parallelism. Neighbor independence at one time step does not remove the barrier between time steps.
- For randomized parallel algorithms, state whether randomness is for load balance, symmetry breaking, conflict avoidance, or expected work. Keep high-probability and expected bounds distinct.

## Worked Pattern: Processor-Count Crossover

Compare two candidate implementations with different work and span. First compute both estimates with the greedy-scheduling expression.

Candidate A:

$$
T_1 = 2048
$$

$$
T_\infty = 1
$$

Candidate B:

$$
T_1 = 1024
$$

$$
T_\infty = 8
$$

At the target processor count:

$$
P = 512
$$

The estimates are:

$$
\frac{2048}{512} + 1 = 5
$$

$$
\frac{1024}{512} + 8 = 10
$$

Choose candidate A at the target processor count, even though candidate B has less work. The crossover point is found by equating the two estimates:

$$
\frac{2048}{P} + 1 = \frac{1024}{P} + 8
$$

$$
P = \frac{1024}{7}
$$

Below that processor count, the lower-work candidate can win. Above it, the lower-span candidate can win.

## Production Translation

Textbook fork-join algorithms teach decomposition, race freedom, and work/span tradeoffs. They are not automatically production implementations.

Require these checks before approving custom parallel code:

1. **Granularity:** coarsen below a measured threshold; do not spawn to individual elements.
2. **Scheduler overhead:** account for task allocation, work-stealing queues, synchronization, and wakeups.
3. **Slackness:** verify enough excess parallelism for the target processor count.
4. **Memory behavior:** check cache locality, bandwidth, false sharing, and NUMA effects.
5. **Tail latency:** benchmark median and tail latency; parallelism can improve average time while worsening jitter.
6. **Library fit:** prefer tuned runtime or library implementations unless the custom algorithm has a measured reason to exist.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Reporting a better span for nested matrix-vector multiplication while ignoring the row-output race | Stop at the race; require a reduction before any inner-loop span claim |
| Treating the lower-work implementation as always better | Compare work and span at the target processor count and find the crossover when needed |
| Saying parallel merge sort has an inherently serial merge step | Distinguish serial merge from the parallel merge routine and give the work/span consequences |
| Assuming more processors always reduce latency | Apply the span law, slackness, scheduler overhead, and production benchmark requirements |
| Spawning to leaves in a service because the asymptotic span is small | Require coarsening and a measured granularity threshold |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Analyzing span before race freedom | Check determinacy first; a racy computation has no valid deterministic speedup claim |
| Confusing work with wall-clock time | Work is the one-processor total; wall-clock time depends on processors and scheduling |
| Treating span as the only bottleneck | Work law and span law both apply |
| Calling every accumulator update a parallel loop | Use reductions or scans for aggregate updates |
| Treating fork-join keywords as scheduling guarantees | They express possible parallelism, not mandatory execution or zero overhead |
| Hand-rolling textbook code by default | Extract the model and proof obligation; prefer tuned libraries when production constraints matter |
| Leaking work/span notation into prose or tables | Use verbal labels in prose and put the exact expression in a display block |
| Treating plain-text arithmetic as non-math | Display every processor estimate, crossover calculation, ratio, and bound in a LaTeX block |

## Answer Template

For a parallel-algorithm review, answer in this order:

1. State the computation and the proposed parallel decomposition.
2. Check determinacy races and ownership of writes.
3. Give the serial projection and work.
4. Identify the critical path and span.
5. Compute parallelism and slackness when a processor count is relevant.
6. Apply the greedy-scheduling estimate or laws.
7. Translate to production: granularity, scheduler overhead, memory behavior, and library alternatives.

## Verification Pressure Tests

Use these prompts to check whether this skill is working:

1. "A developer parallelizes both loops of matrix-vector multiplication and updates the row output in the inner loop. Review the claim that the span improves."
2. "Two implementations have different work and span. One is faster on a small machine, and the other is intended for a larger machine. Decide which to deploy and show the crossover."
3. "A latency-sensitive service proposes recursive fork-join merge sort with spawning down to elements. Review it using work/span, slackness, races, and production constraints."
4. "Explain why naive parallel recursive merge sort has poor parallelism and how parallel merge changes the span."
5. "Choose between reduction and scan for a parallel aggregate problem, and identify the race that a shared accumulator would create."

Static checks for this skill:

- `SKILL.md` lives at `clrs/parallel-algorithms/SKILL.md`.
- Frontmatter name is `parallel-algorithms`, the description starts with `Use when`, and the license is `MIT`.
- The parent `clrs` skill lists `parallel-algorithms` under current chapter skills.
- Formulas are in display LaTeX blocks, not headings, table cells, inline math, or inline code spans.
- The skill includes RED failures for races, work/span processor crossover, and production overreach.
- The text contains no session narrative or source-chapter self-label headings.
