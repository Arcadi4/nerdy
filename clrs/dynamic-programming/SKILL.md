---
name: dynamic-programming
description: Use when solving CLRS dynamic programming problems, deriving optimal substructure recurrences, choosing memoization or bottom-up tables, reconstructing optimal choices, analyzing overlapping subproblems, LCS, matrix-chain multiplication, rod cutting, optimal BSTs, or DP production tradeoffs.
license: MIT
---

# Dynamic Programming

## Overview

Dynamic programming is not "try every recurrence and cache it." CLRS Chapter 14 teaches a discipline: prove the subproblems are independent, choose state variables that preserve all information needed for future choices, compute each distinct subproblem once, and store enough choice information to reconstruct the requested solution.

**Core principle:** before writing a table, identify the choice, prove optimal substructure by cut-and-paste, verify overlapping subproblems, then decide whether the answer needs only values or also reconstruction metadata.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide proof style. Keep recurrences, bounds, thresholds, and probability sums in display LaTeX blocks rather than inline prose.

## Output Discipline for DP Answers

When a prompt asks for a CLRS DP answer, start with the answer itself. Do not mention reading skill files, planning the response, recalling the chapter, checking requirements, or applying this skill. Those sentences are scratch-work and violate the parent `clrs` skill. If a task requires reading files first, do it silently; the delivered answer must not say that it happened.

Use prose for names such as "the value table" or "the split table," then put formal notation in a display block. Do not put table entries, index inequalities, dimensions, recurrences, bounds, matrix names, prefix names, key names, or probability symbols in inline math or inline code spans. For CLRS DP answers, inline mathematical notation is not "small enough" to be safe. If a sentence needs notation, split it into a prose sentence followed by a display block.

Forbidden answer fragments:

- "Let `$m[i,j]$` denote..."
- "where `$1\le i\le j\le n$`"
- "matrix `$A_i$` has dimensions `$p_{i-1}\times p_i$`"
- "If `$x_i=y_j$`, use..."
- "store `root[i,j]`"

Correct pattern:

```markdown
Let the value table store the minimum scalar multiplication cost for the interval below.

$$
A_i\cdots A_j
$$

The legal indices are below.

$$
1\le i\le j\le n
$$

The split position must be in the range below.

$$
i\le k<j
$$

The running time is below.

$$
\Theta(n^3)
$$

The value and split tables use the space below.

$$
\Theta(n^2)
$$
```

Do not write a compliance checklist unless the user explicitly asks for one. If a checklist is required by a testing prompt, put it after the complete answer and keep all symbols inside display blocks there too.

Safe answer pattern:

```markdown
## Subproblem

Let the value table store the minimum cost for multiplying the matrix interval below.

$$
A_i\cdots A_j
$$
```

## When to Use

Use this skill for:

- Optimization problems with repeated subproblems, state choices, memoization, bottom-up tables, or reconstruction of optimal decisions.
- CLRS Chapter 14 examples: rod cutting, matrix-chain multiplication, longest common subsequence, and optimal binary search trees.
- Problems asking whether a recurrence has optimal substructure, overlapping subproblems, or a valid subproblem graph.
- Exercise-style formulations such as longest path in a DAG, longest palindromic subsequence, printing neatly, edit distance, Viterbi, seam carving, bitonic Euclidean TSP, string breaking, inventory planning, and knapsack-like selection.
- Engineering questions where a textbook DP table must be adapted for memory pressure, streaming input, latency, sparse states, or solution reconstruction.

Do **not** use this skill merely because a problem has recursion. Divide-and-conquer with disjoint subproblems belongs with `divide-and-conquer`; greedy choice belongs elsewhere unless the prompt asks why greedy fails or how DP differs.

## The CLRS Four-Step Method

1. **Characterize an optimal solution.** Name the last or first choice and the subproblems created by that choice.
2. **Define the optimal value recursively.** Include base cases, legal indices, and what each table entry means.
3. **Compute values once.** Use bottom-up order when all subproblems are needed; use memoized top-down when the reachable state space is sparse or naturally demand-driven.
4. **Construct an optimal solution.** If the user needs decisions, store argmin or argmax choices while filling the value table, or prove reconstruction from values alone is sufficient.

Skipping the fourth step is valid only when the requested output is the optimal value alone.

## First Decision: Does DP Actually Apply?

| Question | Required answer before tabling | Failure mode |
| --- | --- | --- |
| What choice defines the solution? | Root, split point, last character, first cut, transition, or action. | Recurrence has no semantic meaning. |
| What is the state? | The minimal parameters that determine all future possibilities. | Prefix-only state fails for interval problems; bloated state explodes. |
| Are subproblems independent? | Solutions can be spliced without sharing a forbidden resource. | Longest simple path fails because subpaths compete for vertices. |
| Are subproblems overlapping? | The naive recursion revisits a polynomial-size set of states. | Divide-and-conquer may not benefit from memoization. |
| What output is needed? | Value only, one optimal solution, all optimal solutions, or decision policy. | Missing choice table makes reconstruction impossible or expensive. |
| What order computes dependencies? | Increasing length, increasing prefix size, DAG topological order, or demand recursion. | Table reads uninitialized entries. |

## Quick Reference: Chapter Examples

| Problem | State | Choice | Base case | Fill order | Reconstruction |
| --- | --- | --- | --- | --- | --- |
| Rod cutting | Rod length | First cut length | Length zero revenue is zero | Increasing length | Store first cut for each length |
| Matrix-chain multiplication | Matrix interval | Split between two adjacent subchains | One matrix costs zero | Increasing chain length | Store best split for each interval |
| Longest common subsequence | Prefix lengths | Match both last symbols, or drop one last symbol | Empty prefix has length zero | Row-major over prefixes | Store arrows or walk values backward |
| Optimal BST | Contiguous key interval | Root key of the interval | Empty subtree contains one dummy key | Increasing interval length | Store best root for each interval |

Runtime usually follows:

$$
\text{number of subproblems}\times\text{choices per subproblem}
$$

Equivalently, inspect the subproblem graph: vertices are distinct subproblems, and edges are dependencies.

## Rod Cutting Reference

Use rod cutting to explain overlapping subproblems and reconstruction. With prices for piece lengths, define the best revenue for a rod length by choosing the first piece cut off.

$$
r_0=0
$$

$$
r_n=\max_{1\le i\le n}(p_i+r_{n-i})
$$

The naive recursion is exponential because it recomputes the same shorter rods. The CLRS count satisfies:

$$
T(0)=1
$$

$$
T(n)=1+\sum_{j=0}^{n-1}T(j)
$$

$$
T(n)=2^n
$$

Bottom-up rod cutting fills revenues by increasing length and runs in:

$$
\Theta(n^2)
$$

For an actual cut plan, store the first cut length for each rod length, then repeatedly output that cut and reduce the remaining length.

## Matrix-Chain Multiplication Reference

Matrix-chain multiplication optimizes parenthesization cost, not the numerical multiplication itself. If the matrices are numbered starting at one and the dimensions array starts at zero, matrix number i has dimensions:

$$
p_{i-1}\times p_i
$$

Define the interval value as the minimum scalar multiplication cost for the subchain below.

$$
A_i\cdots A_j
$$

$$
m[i,i]=0
$$

For an interval with at least two matrices, split between the adjacent matrices below.

$$
A_k\text{ and }A_{k+1}
$$

$$
m[i,j]=\min_{i\le k<j}\left(m[i,k]+m[k+1,j]+p_{i-1}p_kp_j\right)
$$

Store the minimizing split:

$$
s[i,j]=\operatorname*{argmin}_{i\le k<j}\left(m[i,k]+m[k+1,j]+p_{i-1}p_kp_j\right)
$$

Fill by increasing chain length. There are quadratically many intervals and linearly many split candidates per interval, so the running time is:

$$
\Theta(n^3)
$$

The value and split tables take:

$$
\Theta(n^2)
$$

## LCS Reference

For two sequences, use prefixes. The prefix below means the first i elements of the first sequence, and the second prefix is analogous.

$$
X_i
$$

The LCS table stores the length of a longest common subsequence of the two prefixes.

$$
c[i,0]=0
$$

$$
c[0,j]=0
$$

If the last symbols match, they can be appended to an LCS of the two shorter prefixes.

$$
c[i,j]=c[i-1,j-1]+1
$$

If the last symbols differ, at least one of them is not used.

$$
c[i,j]=\max(c[i-1,j],c[i,j-1])
$$

The CLRS theorem behind this recurrence is a suffix choice theorem: matching last symbols belong to some LCS of the full prefixes, while differing last symbols justify dropping one side. Fill the table over prefix lengths in row-major or column-major dependency order.

For reconstruction, store arrows for diagonal, up, and left moves, or reconstruct from the value table: on a match output that symbol after recursively moving diagonally; otherwise move to a neighbor with the same optimal value.

The standard table runs in:

$$
\Theta(mn)
$$

Length alone can be stored with two rows or one rolling row, but full reconstruction needs arrows, a retained table, or a divide-and-conquer reconstruction technique.

## Optimal BST Reference

The optimal binary-search-tree problem includes both successful searches for sorted keys and unsuccessful searches ending at dummy keys. Do not drop the dummy probabilities.

Keys are sorted:

$$
k_1<k_2<\cdots<k_n
$$

Successful probabilities are:

$$
p_1,p_2,\ldots,p_n
$$

Dummy probabilities are:

$$
q_0,q_1,\ldots,q_n
$$

An empty subtree between positions contains exactly one dummy key, so the base case is:

$$
e[i,i-1]=q_{i-1}
$$

Maintain interval weights:

$$
w[i,i-1]=q_{i-1}
$$

$$
w[i,j]=w[i,j-1]+p_j+q_j
$$

For a nonempty interval, choose the root key and pay one extra level of depth for every item in the interval, represented by the weight term.

$$
e[i,j]=\min_{i\le r\le j}\left(e[i,r-1]+e[r+1,j]+w[i,j]\right)
$$

Store the minimizing root:

$$
root[i,j]=\operatorname*{argmin}_{i\le r\le j}\left(e[i,r-1]+e[r+1,j]+w[i,j]\right)
$$

Fill by increasing interval length. The direct CLRS algorithm runs in:

$$
\Theta(n^3)
$$

and uses:

$$
\Theta(n^2)
$$

A later optimization can reduce the running time when root choices are monotone:

$$
root[i,j-1]\le root[i,j]\le root[i+1,j]
$$

## Worked Pattern: Deriving a DP Recurrence

Use this answer pattern for new Chapter 14 problems:

1. **State the object and state.** "Let the table entry mean the optimal value for this exact subproblem." Include index ranges and empty cases.
2. **Name the last or first choice.** Split point, root, last matched symbol, first cut, predecessor state, or transition.
3. **Assume the optimal choice is known.** This reveals the subproblems without guessing the recurrence first.
4. **Prove subproblem optimality.** If replacing a chosen subproblem by a better legal solution would improve the whole solution, the chosen subproblem must be optimal.
5. **Check independence.** The replacement must not violate a shared constraint such as reused vertices, capacity already consumed, or future symbols already committed.
6. **Write the recurrence and base cases.** Only after the proof obligation is clear.
7. **Choose computation strategy.** Bottom-up for dense known tables; memoized top-down for sparse or demand-driven state spaces.
8. **Add reconstruction if needed.** Store the choice table or explain how the value table reconstructs the solution.

## Optimal Substructure Trap: Longest Simple Path

Do not transfer the shortest-path proof to longest simple paths in an unweighted graph.

Shortest paths have the cut-and-paste property: replacing a subpath by a shorter subpath preserves path legality and improves the whole path. Longest simple paths do not have the same independent subproblems because the simple-path constraint makes vertices a shared resource. A longest subpath from the start to an intermediate vertex may consume vertices needed after that intermediate vertex, so splicing independently optimal subpaths can repeat vertices or force a globally worse choice.

The correct response is not merely "longest path is hard." The CLRS reason is that optimal substructure requires independent subproblems, and the simple-path constraint couples them.

## Memoization, Bottom-Up Tables, and Production Judgment

Top-down memoization and bottom-up tabulation compute the same recurrence only when they cover the same state graph. Choose deliberately:

| Constraint | Prefer | Reason |
| --- | --- | --- |
| Dense finite state space and all states needed | Bottom-up | Better constants and predictable memory access. |
| Sparse reachable states | Memoized top-down | Avoids filling unreachable table entries. |
| Streaming or unknown horizon | Rolling, online, or memoized variant | Full table bounds may not be known. |
| Need actual decisions | Choice table, parent pointer, or root/split table | Value-only optimization loses the solution path. |
| Severe memory pressure | Rolling arrays, state compression, checkpointing, or approximation | Do not allocate a naive multidimensional table by reflex. |
| Latency or p99 constraints | Bound state expansions and measure table locality | Asymptotic table size can hide cache and allocation costs. |

When applying CLRS DP in a service, say what transfers: state design, recurrence proof, subproblem graph, and reconstruction. Also say what may not transfer: naive table size, offline availability of all input, exact optimization under unbounded streams, and hand-written implementation when a solver or domain library is safer.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Giving a correct matrix-chain recurrence but omitting that the algorithm optimizes parenthesization, not multiplication | State the optimized quantity before the recurrence. |
| Drifting on matrix-chain indices | Keep matrices one-indexed, dimensions zero-indexed, and split between adjacent matrices. |
| Reconstructing only values | Store first cuts, split points, arrows, roots, or parent choices when decisions are requested. |
| Treating longest simple path like shortest path | Explain the vertex-sharing independence failure, not just computational hardness. |
| Dropping optimal-BST dummy keys | Include empty-subtree base cases and weights using the dummy probabilities. |
| Reciting generic memoization advice | Tie memoization or tabulation to reachable states, streaming bounds, memory, and reconstruction. |
| Leaking scratch-work narration or inline formulas in CLRS answers | Start with the polished answer and put formal notation in display blocks. |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| "It has recursion, so use DP." | Require overlapping subproblems and a small reusable state space. |
| "Optimal substructure always holds for optimal problems." | Prove independent subproblems; shared resources can break the splice argument. |
| Prefix-only state for interval problems | Use both endpoints when choices split an interval. |
| Full bottom-up table by default | Check whether all states are reachable, bounded, and affordable. |
| Value table when solution path is requested | Store choices during computation or use a reconstruction method. |
| Omitting base cases for empty subproblems | Empty prefixes, zero rod length, one matrix, and dummy-only BST intervals are part of the recurrence. |
| Confusing greedy with DP | Greedy chooses locally first and solves one subproblem; DP evaluates candidate subproblems before choosing. |
| Hiding costs in table notation | Count states and choices per state; then state space and reconstruction storage separately. |

## Red Flags

Stop and repair the answer if it contains any of these:

- "Clearly DP applies" before proving optimal substructure and overlap.
- "Just memoize it" without defining the state key.
- "Use a two-dimensional table" without explaining what each axis means.
- An optimal value answer when the prompt asks for the chosen cuts, parenthesization, subsequence, roots, or policy.
- Inline recurrence algebra in prose for a CLRS answer that should use display math.
- Inline table entries, dimensions, prefixes, key names, probability symbols, or index ranges inside prose.
- Preambles such as "I'll read the files," "Let me recall," or "Using the skill" before the polished answer.
- Compliance checklists or self-reports before the mathematical answer; put any required checklist after the answer.
- Inline complexity claims such as saying the running time is Theta of a cubic or the interval is from one to n. Display the bound or interval instead.
- Longest-simple-path reasoning that mentions only hardness and not subproblem independence.
- Optimal-BST recurrence with no dummy-key probabilities or empty-subtree base case.

## Verification Pressure Tests

Use these prompts to check whether this skill is working:

1. "For matrix-chain multiplication with dimensions `p0..pn`, give the DP recurrence, split indexing, table-fill order, reconstruction table, and cost."
2. "A teammate says longest simple path has the same optimal substructure as shortest path. Explain exactly why the cut-and-paste proof fails."
3. "State the LCS recurrence using prefixes, including base rows and reconstruction, then give optimal-BST recurrence with dummy keys and weights."
4. "A service optimization problem has streaming input, sparse states, memory pressure, and must output decisions. Use CLRS DP without blindly allocating a full table."
5. "For a new interval optimization problem, derive the recurrence by identifying the choice and proving subproblem optimality before writing code."

Static checks for this skill:

- `SKILL.md` lives at `clrs/dynamic-programming/SKILL.md`.
- Frontmatter name is `dynamic-programming` and description starts with `Use when`.
- The parent `clrs` skill lists this chapter skill.
- Formal recurrences and bounds are displayed in LaTeX blocks.
- The text distinguishes CLRS mechanics from production table-design judgment.
