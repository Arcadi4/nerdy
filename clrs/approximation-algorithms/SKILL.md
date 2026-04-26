---
name: approximation-algorithms
description: Use when approximating NP-hard optimization problems, proving approximation ratios, checking PTAS or FPTAS claims, or reviewing CLRS vertex cover, metric TSP, set cover, randomized MAX-3-CNF, LP rounding, subset-sum trimming, bin packing, scheduling, clique, matching, spanning-tree, or knapsack approximation arguments.
license: MIT
---

# Approximation Algorithms

## Overview

Approximation answers are certificate audits, not heuristic endorsements. First decide whether the problem is minimization or maximization, identify a polynomial-time lower or upper bound on the optimum, then prove the returned feasible solution is within the promised factor under the chapter's exact preconditions.

**Core principle:** never claim an approximation ratio from a good-looking local rule. Name the optimum bound, prove feasibility, prove the ratio against that bound, and reject the claim if any precondition, encoding assumption, or shortcut inequality is missing.

## Shared CLRS Conventions

- Follow the parent `clrs` skill for mathematical formatting: every cost ratio, probability, recurrence, inequality, asymptotic bound, threshold, and approximation factor belongs in a display LaTeX block.
- Keep tables verbal. Put ratio definitions, LP constraints, probabilities, trimming guarantees, and running times in display blocks near the table instead of inside table cells.
- Use `np-completeness` for exact decision hardness and reductions; use this skill when the task asks for near-optimal algorithms, approximation ratios, inapproximability gaps, schemes, or approximation proof certificates.
- Use `linear-programming` for general LP modeling; use this skill when an LP relaxation is being rounded to certify an approximation algorithm.
- Do not announce that you are using this skill. Deliver the polished algorithm, proof, counterexample, or review directly.

## When to Use

Use this skill for:

- proving or refuting an approximation ratio for a polynomial-time algorithm;
- distinguishing exact, pseudo-polynomial, PTAS, and FPTAS claims;
- checking metric TSP, general TSP, vertex cover, set cover, MAX-3-CNF, weighted vertex cover, or subset-sum approximation arguments;
- turning a greedy, randomized, LP-rounding, or trimming proof into a certificate-style answer;
- reviewing chapter problem patterns such as bin packing, weighted set cover, maximal matching, list scheduling, maximum spanning tree, maximum clique, or knapsack approximations.

Do **not** use this skill merely because an algorithm is heuristic or fast. Use it when the answer must connect a feasible solution to a provable optimum bound or a hardness gap.

## First Decision

| Situation | First move | Watch for |
| --- | --- | --- |
| Approximation claim | Identify minimization or maximization and the optimum symbol | Reversing ratio direction |
| Greedy proof | Name the bound on optimum before the local rule | Intuition without certificate |
| Metric TSP | Check triangle inequality before shortcutting | Applying metric proof to general TSP |
| Vertex cover | Distinguish maximal matching from highest-degree greedy | False counterexamples where greedy actually succeeds |
| Weighted cover | Use LP relaxation or weighted-specific method | Reusing unweighted maximal-matching proof |
| Set cover | Use uncovered-set shrinkage or weighted density charging | Answering with vertex-cover matching proof |
| Randomized maximization | Prove expected value and convert to approximation ratio | Confusing fraction of optimum with ratio |
| Numeric DP | Compare runtime to encoded input length | Calling pseudo-polynomial time polynomial |
| FPTAS claim | Prove runtime polynomial in input size and accuracy parameter | Only proving dependence on numeric target |
| Inapproximability | Build a yes/no optimum-value gap | Reducing in the wrong direction |

For minimization, compare the returned cost to the optimum cost as below.

$$
\frac{C}{C^*} \le \rho(n)
$$

For maximization, compare the optimum value to the returned value as below.

$$
\frac{C^*}{C} \le \rho(n)
$$

An approximation scheme takes an instance and an accuracy parameter. A PTAS is polynomial in input size for every fixed accuracy parameter. An FPTAS is polynomial in both input size and the reciprocal of the accuracy parameter.

## Output Contract Checklist

Before answering, check each item that applies:

1. **Problem type:** say minimization or maximization before quoting a ratio.
2. **Feasibility:** prove the algorithm returns a legal solution, not just a cheap or high-value object.
3. **Certificate bound:** state the lower bound for minimization or upper bound for maximization.
4. **Ratio chain:** connect returned solution, certificate bound, and optimum in the correct direction.
5. **Preconditions:** check triangle inequality, nonnegative costs, complete graph, positive weights, distinct literals, positive integer subset-sum items, or encoding assumptions.
6. **Algorithm variant:** distinguish set cover from vertex cover, maximal from maximum matching, metric from general TSP, weighted from unweighted cover, and exact from approximate subset sum.
7. **Runtime model:** prove polynomial time under encoded input size; call pseudo-polynomial algorithms pseudo-polynomial.
8. **Formatting:** keep formulas in display blocks and outside headings, tables, and inline prose.

## Proof Patterns

### Lower-bound charging

Use this for deterministic minimization algorithms such as vertex cover, metric TSP, bin packing, and list scheduling.

1. Produce a feasible solution.
2. Exhibit a quantity any optimum must pay for, such as one endpoint per matching edge, a spanning tree no more expensive than a tour, total item size, average machine load, or largest job.
3. Show the algorithm pays at most a constant multiple of that bound.

### Upper-bound expectation

Use this for randomized maximization algorithms such as MAX-3-CNF and MAX-CUT.

1. Define an indicator for each satisfied constraint.
2. Compute its success probability under independent random choices.
3. Sum expectations by linearity.
4. Compare the optimum to an obvious upper bound such as the number of clauses or cuts.

For MAX-3-CNF with exactly three distinct literals per clause and no clause containing both a variable and its negation, a random assignment satisfies each clause with probability below.

$$
1 - \left(\frac{1}{2}\right)^3 = \frac{7}{8}
$$

If there are clauses as counted below, the expected satisfied count is below.

$$
\mathbf{E}[Y] = \frac{7m}{8}
$$

Since no assignment satisfies more clauses than the total number of clauses, the randomized approximation ratio is below.

$$
\frac{m}{7m/8} = \frac{8}{7}
$$

### Relaxation and rounding

Use this when an LP relaxation gives a lower bound for a minimization problem.

1. Write the integer program or name the integral feasible set.
2. Relax integrality and solve the LP.
3. Explain why the LP optimum is no worse than the integral optimum.
4. Round fractional values using the threshold or rule that preserves feasibility.
5. Charge the rounded cost to the LP objective.

For minimum-weight vertex cover, the LP relaxation has the edge constraints below.

$$
x(u) + x(v) \ge 1 \quad \text{for every edge } (u,v)
$$

The rounding rule includes every vertex satisfying the threshold below.

$$
x(v) \ge \frac{1}{2}
$$

The edge constraint guarantees at least one endpoint is rounded in. The weight chain is below.

$$
z^* = \sum_{v \in V} w(v)x(v)
\ge \sum_{v \in C} w(v)x(v)
\ge \frac{1}{2}\sum_{v \in C} w(v)
$$

Therefore the rounded cover has weight bounded as below.

$$
w(C) \le 2z^* \le 2w(C^*)
$$

### Trimming for approximation schemes

Use this for subset-sum approximation. Exact list merging is exponential in the worst case, and pseudo-polynomial when bounded by the numeric target. The approximation scheme stays polynomial by trimming nearby sums while retaining slightly smaller representatives.

With trimming parameter below, every removed value must have a retained representative satisfying the display guarantee below.

$$
\delta = \frac{\epsilon}{2n}
$$

$$
\frac{y}{1+\delta} \le z \le y
$$

After processing the first items, every feasible exact sum has a retained representative with the accumulated guarantee below.

$$
\frac{y}{(1+\epsilon/(2n))^i} \le z \le y
$$

For an optimal feasible sum, the returned largest retained sum satisfies the approximation bound below.

$$
\frac{y^\*}{z^\*} \le \left(1+\frac{\epsilon}{2n}\right)^n \le 1+\epsilon
$$

The algorithm is an FPTAS only after proving both the approximation guarantee above and a list-length bound polynomial in input size and the reciprocal accuracy parameter. The exact dynamic program alone is not polynomial under binary encoding.

## Core Algorithms and Claims

### Vertex cover by maximal matching

Algorithm: repeatedly choose any remaining edge, add both endpoints to the cover, and delete all incident edges.

Proof move:

1. The selected edges form a matching because incident edges are deleted.
2. Every vertex cover must include at least one endpoint of every selected edge.
3. No one vertex can cover two selected matching edges.
4. The selected edge count is a lower bound on optimum cover size.
5. The algorithm adds two vertices per selected edge.

The ratio chain is below.

$$
|C| = 2|A| \le 2|C^*|
$$

Trap: highest-degree greedy is a different heuristic and does not inherit this proof. Do not use a star graph as a counterexample against highest-degree greedy; highest-degree picks the center and is optimal there. If asked for the chapter exercise trap, build a bipartite instance where left degrees are uniform and right degrees vary so the heuristic's local degree order is misleading.

### Metric TSP by doubled MST and shortcutting

Use this only for complete graphs with nonnegative costs satisfying the triangle inequality. Compute an MST, traverse its edges twice, and shortcut repeated vertices in preorder.

The proof chain is below.

$$
c(T) \le c(H^*)
$$

$$
c(W) = 2c(T) \le 2c(H^*)
$$

Triangle inequality is the only reason shortcutting cannot increase the walk cost.

$$
c(H) \le c(W)
$$

Thus the returned tour is bounded as below.

$$
c(H) \le 2c(H^*)
$$

Do not shortcut a doubled walk for general TSP without proving triangle inequality. Without it, the direct edge used by the shortcut can be more expensive than the path it replaces.

For general TSP, the chapter's inapproximability proof uses a Hamiltonian-cycle gap. Original edges get cheap cost, nonedges get expensive cost.

$$
c(u,v)=1 \quad \text{for original edges}
$$

$$
c(u,v)=\rho |V| + 1 \quad \text{for nonedges}
$$

If the original graph has a Hamiltonian cycle, the optimum tour cost is below.

$$
|V|
$$

If it does not, every tour uses an expensive edge and has cost greater than the gap below.

$$
\rho |V|
$$

A polynomial-time constant-ratio approximation would distinguish the two cases and solve Hamiltonian cycle.

### Greedy set cover

Set cover is not vertex cover. If the prompt says set cover, the objects are universe elements and sets, not graph edges and endpoint choices. Do not answer a set-cover question with the vertex-cover maximal-matching proof.

For unweighted set cover, repeatedly choose the set covering the largest number of currently uncovered elements. The chapter proof compares the uncovered set to an optimum cover of size below.

$$
k = |C^*|
$$

At every iteration, some optimum set covers at least the average number of current uncovered elements. Greedy does at least as well, so uncovered elements shrink as below.

$$
|U_{i+1}| \le |U_i|\left(1-\frac{1}{k}\right)
$$

After enough iterations, the bound is below one uncovered element.

$$
|U_i| \le |X|\left(1-\frac{1}{k}\right)^i \le |X|e^{-i/k}
$$

Choosing the iteration count below proves the logarithmic approximation.

$$
i = k\lceil \ln |X| \rceil
$$

$$
|C| \le |C^*|\lceil \ln |X| \rceil
$$

Trap: do not replace this proof with the weighted set-cover harmonic proof unless the prompt is weighted, and do not replace it with the vertex-cover matching proof. For weighted set cover, the natural greedy choice is minimum cost per newly covered element, and the ratio is harmonic in the maximum set size.

For weighted set cover, define the largest set size as below before quoting the harmonic bound.

$$
d = \max_{S \in \mathcal{F}} |S|
$$

The weighted greedy ratio is bounded by the harmonic quantity below.

$$
H(d)
$$

### Exact and approximate subset sum

Exact subset-sum list merging keeps all achievable sums not exceeding the target. It is exponential in the worst case and pseudo-polynomial when the numeric target bounds the list. The approximate version trims after every merge, deletes values above the target, and returns the largest retained value.

Example checkpoint: with items and target below, the chapter's approximate run with the stated accuracy parameter returns the displayed value, while the optimum is displayed after it.

$$
S=\langle 104,102,201,101\rangle
$$

$$
t=308
$$

$$
\epsilon=0.40
$$

$$
302
$$

$$
307=104+102+101
$$

If asked to return the subset, carry predecessor pointers or retained-item witnesses through merge, trim, and deletion; do not return only the numeric value.

## Chapter Problem Patterns

| Problem pattern | Certificate idea | Trap |
| --- | --- | --- |
| Bin packing first-fit | Total item size lower-bounds optimum; at most one used bin can remain at most half full under the simple proof | Importing stronger first-fit decreasing bounds not used by the chapter prompt |
| Weighted set cover | Greedy cost per newly covered element and harmonic charging by maximum set size | Using unweighted largest-new-coverage rule after weights appear |
| Maximum matching | A maximal matching is not maximum, but a maximum matching bounds the greedy maximal matching through a vertex-cover endpoint argument | Confusing maximal and maximum |
| Parallel-machine scheduling | Average load and largest job are lower bounds on optimum makespan | Forgetting to identify the last job on the most-loaded machine |
| Maximum spanning tree | Maximum incident edges provide a certificate whose total weight is within a factor of a maximum spanning tree | Treating local maximum edges as automatically a tree |
| Knapsack approximation | Fractional restricted instance has at most one fractional item; dropping it loses at most half | Reusing density greedy as exact indivisible knapsack |
| Maximum clique | Graph power turns a constant approximation into a stronger approximation scheme consequence | Assuming vertex-cover approximability transfers through complement |

When a prompt asks for external improvements such as Christofides for metric TSP, first state that the chapter's doubled-MST method gives the displayed factor below, then clearly label stronger algorithms as outside this chapter skill rather than silently replacing the chapter result.

$$
2
$$

For general TSP, an algorithm can still output some Hamiltonian tour when the complete graph is provided, but the chapter gap proof says no polynomial-time constant-ratio guarantee exists under the standard assumption.

For bin packing first-fit, the simple chapter proof uses total size as a lower bound and the half-full property. If total item size is below, optimum uses at least its ceiling.

$$
S = \sum_i s_i
$$

$$
\mathrm{OPT} \ge \lceil S \rceil
$$

First-fit uses at most the displayed number of bins under this proof.

$$
\lceil 2S \rceil
$$

For list scheduling on identical parallel machines, use the average-load and largest-job lower bounds below.

$$
C^*_{\max} \ge \frac{1}{m}\sum_j p_j
$$

$$
C^*_{\max} \ge \max_j p_j
$$

The greedy makespan is at most their sum, hence the ratio below.

$$
C_{\max} \le 2C^*_{\max}
$$

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Claiming highest-degree vertex cover is justified by the maximal-matching proof | Separate the algorithms; the proof only applies to edges chosen as a matching, and the star graph is not a valid failure case for highest-degree greedy |
| Shortcutting doubled MST walks for nonmetric TSP | State triangle inequality as a hard precondition before the shortcut step |
| Replacing the chapter's unweighted set-cover proof with weighted dual-fitting folklore | Use uncovered-set shrinkage for unweighted set cover; reserve harmonic maximum-set-size charging for weighted set cover |
| Answering a set-cover prompt with the vertex-cover maximal-matching proof | Use universe elements, chosen sets, uncovered elements, and optimum set family size; matching edges belong only to vertex cover |
| Saying subset sum is an FPTAS because exact DP is pseudo-polynomial | Prove trimming accuracy and runtime polynomial in input size and reciprocal accuracy |
| Applying unweighted vertex-cover maximal matching to positive weights | Use LP relaxation and threshold rounding for weighted vertex cover |
| Mixing general TSP with metric TSP or importing Christofides | Metric doubled-MST gives factor two; general TSP has no constant approximation unless the standard collapse occurs |
| Importing stronger bin-packing or scheduling results not in the prompt | Answer the chapter's first-fit and list-scheduling lower-bound proofs unless the user asks for external refinements |
| Leaking formulas into prose, headings, code spans, or table cells | Move every ratio, threshold, probability, and bound into display math |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Treating a heuristic as an approximation algorithm without proof | Require a certificate bound and ratio chain |
| Forgetting ratio direction for maximization | Compare optimum value to returned value |
| Calling a pseudo-polynomial algorithm polynomial | Measure time against encoded input length |
| Saying an approximation scheme is fully polynomial because it is polynomial for fixed accuracy | Check dependence on reciprocal accuracy |
| Using LP rounding without proving feasibility after rounding | For every edge, show at least one endpoint crosses the threshold |
| Omitting the random variable definition in randomized proofs | Define indicators and sum expectations |
| Claiming complement of vertex cover yields clique approximation | The complement relation does not preserve constant-factor approximation |
| Treating set cover and vertex cover as interchangeable because both say cover | Set cover chooses subsets of a universe; vertex cover chooses graph vertices incident to edges |
| Using theorem labels without preconditions | Check metricity, positivity, completeness, distinct literals, and encoding first |

## Verification Pressure Tests

Use these prompts to check whether an answer follows the skill:

1. **Vertex cover and TSP trap:** Reject highest-degree vertex-cover proof reuse, explain maximal matching lower bound, reject nonmetric TSP shortcutting, and keep all formulas in display math.
2. **Set cover, LP, and subset sum:** Compare unweighted greedy set cover, minimum-weight vertex cover LP rounding, and subset-sum trimming by naming each certificate bound and precondition. The set-cover part must not mention matching edges or vertex endpoints.
3. **Randomized and lower-bound patterns:** Classify MAX-3-CNF, general TSP, first-fit bin packing, and list scheduling by expectation, gap, or deterministic lower-bound proof, with exact chapter constants.
4. **Formatting audit:** Ask for a decision table plus formulas and a post-answer self-evaluation table; formulas must appear outside table cells in both the answer and the evaluation.
5. **Coverage audit:** Ask which chapter section applies to PTAS versus FPTAS, weighted set cover, maximal matching, or knapsack approximation; the answer must not silently omit the section.

Static checks:

- Frontmatter has `name`, `description`, and `license`, and the name matches `approximation-algorithms`.
- No formulas appear in headings or Markdown table cells.
- Source-specific labels are used only for routing, theorem identity, or provenance.
- Every major chapter section appears as a decision rule, proof pattern, trap, or pressure test: approximation framework, vertex cover, TSP, set cover, randomization, LP rounding, subset-sum FPTAS, and chapter problem patterns.
