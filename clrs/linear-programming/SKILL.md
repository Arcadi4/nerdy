---
name: linear-programming
description: Use when formulating, solving, proving, or reviewing linear-programming models, including standard form, feasibility, boundedness, simplex intuition, graph and flow LPs, duality, weak or strong duality, Farkas certificates, complementary slackness, or integer-LP caveats.
license: MIT
---

# Linear Programming

## Overview

Linear-programming answers are modeling and certificate problems before they are solver problems. First identify decisions, linear constraints, objective direction, feasibility status, and the proof certificate that would convince a skeptical reader the optimum is correct.

**Core principle:** an LP formulation is useful only when every variable has a real-valued meaning, every constraint preserves the original feasible set, the objective direction matches the bound semantics, and optimality can be certified by duality or complementary slackness.

## Shared Parent Conventions

- Follow the parent `clrs` skill for mathematical formatting: every expression, inequality, matrix relation, objective value, and asymptotic bound belongs in a display LaTeX block.
- Keep tables verbal. Put standard forms, duals, graph constraints, and certificate equations in display blocks adjacent to the table instead of inside table cells.
- Use `shortest-paths` for ordinary shortest-path algorithms, `maximum-flow` for augmenting-path and cut mechanics, and this skill when the task asks for LP formulation, duality, feasibility, or solver-based modeling.
- Do not announce that you are using this skill. Deliver the polished formulation, proof, or review directly.

## When to Use

Use this skill for:

- turning a resource-allocation, graph, flow, matching, shortest-path, or scheduling-style problem into a linear program;
- converting between arbitrary LP descriptions and the chapter's maximization standard form;
- deciding whether a model is feasible, infeasible, bounded, unbounded, or missing constraints;
- explaining simplex geometry, vertex optimality, ellipsoid methods, interior-point methods, or solver choice;
- writing primal-dual pairs, weak-duality upper bounds, equality certificates, strong-duality arguments, or complementary-slackness checks;
- distinguishing continuous LP relaxations from integer linear programs and avoiding false polynomial-time claims.

Do not use this skill merely because a problem has linear algebra. If the task is solving a numeric linear system, route to `matrix-operations`; if it is shortest-path computation without LP modeling, route to `shortest-paths`; if it is maximum-flow algorithm mechanics without LP or duality, route to `maximum-flow`.

## First Decision

| Situation | First move | Watch for |
| --- | --- | --- |
| Real-world modeling prompt | Name decision variables, constraints, objective, and sign restrictions | Optimizing before defining what variables mean |
| Existing LP not in standard form | Normalize objective direction, constraint direction, equalities, and variable signs | Changing the feasible set while changing notation |
| Shortest path as LP | Use distance-potential variables and maximize the target potential | Minimizing a lower-bound variable or adding binary path variables |
| Maximum flow as LP | Use edge-flow variables, capacities, conservation, and source net-flow objective | Creating variables for absent edges without explaining zero capacity or size blowup |
| Minimum-cost flow | Keep flow feasibility and demand constraints; minimize edge costs | Forgetting exact demand or conservation at ordinary vertices |
| Multicommodity flow | Create one flow per commodity plus shared-capacity constraints | Treating commodities independently after they share edges |
| Need optimality proof | Produce a dual feasible solution or complementary-slackness certificate | Naming strong duality without feasibility and boundedness conditions |
| Integer requirements appear | Say this is integer linear programming or a special integral polytope | Claiming general integer LP is polynomial-time solvable |
| Production optimization task | Prefer a mature LP or mixed-integer solver with explicit model checks | Hand-rolling simplex because the chapter describes its intuition |

Use the standard maximization form below as the chapter's anchor.

$$
\max c^T x
$$

$$
A x \le b
$$

$$
x \ge 0
$$

## Output Contract Checklist

Before answering, check each item that applies:

1. **Variables:** define every decision variable, its unit, and whether it is continuous, nonnegative, free, or integer.
2. **Constraints:** tie every constraint to a problem requirement, resource limit, conservation law, demand, or sign restriction.
3. **Objective:** state whether the objective is maximizing a value, minimizing a cost, or using a null objective for feasibility.
4. **Equivalence:** explain how feasible original solutions map to feasible LP solutions and back when the model is a reduction.
5. **Status:** say whether the LP could be infeasible, unbounded, or merely have an unbounded feasible region with finite optimum.
6. **Certificate:** for optimality, use primal-dual equality, weak duality, strong duality, or complementary slackness as appropriate.
7. **Computation:** distinguish polynomial-time LP algorithms from simplex practice and from integer LP hardness.
8. **Formatting:** keep all mathematical expressions in display blocks and outside tables.

## Modeling Workflow

Use this sequence for any formulation prompt:

1. Name the decisions, not the algorithms. Choose variables that directly represent controllable quantities or graph quantities.
2. Write sign and domain restrictions before objective tuning. Continuous LP variables are real-valued unless integer restrictions are explicitly required.
3. Translate each requirement into a linear equality or non-strict inequality. Strict inequalities are not LP constraints in the chapter model.
4. Choose the objective direction by asking whether the variables are upper bounds, lower bounds, costs, profits, or feasibility placeholders.
5. Check size. A polynomial-sized LP gives a polynomial-time route through general LP algorithms; an exponential path-variable LP may be a valid formulation but not a polynomial-size one.
6. State any overmodeling. Extra constraints are allowed only if they do not remove an optimal solution or if the prompt asks for the stricter model.

For the political-advertising pattern, variables are spending amounts, constraints are vote requirements, and the objective is total spending. Negative coefficients are allowed in constraints; negative spending is not allowed.

## Standard-Form Conversions

Use these conversions when the prompt asks for standard form or duality.

An equality constraint becomes the pair of opposite inequalities below.

$$
a^T x = b
$$

$$
a^T x \le b
$$

$$
-a^T x \le -b
$$

A less-than-or-equal inequality can become an equality by adding a nonnegative slack variable.

$$
a^T x \le b
$$

$$
a^T x + s = b
$$

$$
s \ge 0
$$

A minimization objective becomes an equivalent maximization by negating the objective. Translate the optimal value back by negating again.

$$
\min c^T x
$$

$$
\max -c^T x
$$

A free variable can be represented as a difference of two nonnegative variables.

$$
x_j = x_j^+ - x_j^-
$$

$$
x_j^+ \ge 0
$$

$$
x_j^- \ge 0
$$

Common trap: conversion is not just cosmetic. After converting, verify that every feasible assignment in the original system maps to exactly one or at least one assignment in the transformed system, and that objectives agree after translating back.

## Feasibility, Boundedness, and Geometry

Use the vocabulary precisely:

- A feasible solution satisfies every constraint.
- An infeasible LP has no feasible solution.
- An optimal solution is a feasible solution with best objective value.
- An unbounded LP is feasible but has no finite optimal objective value in the objective direction.
- An unbounded feasible region does not by itself imply an unbounded LP.

Geometric proof recipe:

1. Constraints define half-spaces.
2. Their intersection is convex.
3. Objective level sets are parallel hyperplanes.
4. If a finite optimum exists, some vertex of the feasible region is optimal.
5. Simplex moves along edges between neighboring vertices until no improving neighbor exists.
6. Convexity and linearity turn that local vertex optimum into a global optimum.

Production judgment: do not implement simplex from scratch for ordinary applications. Use maintained LP solver libraries, inspect solver status, and validate scaling, units, tolerances, infeasibility reports, and unboundedness certificates. The chapter insight to preserve is the model and certificate, not a bespoke simplex implementation.

## Graph and Flow Formulations

### Shortest-path potentials

For a single-pair shortest-path LP, use one potential variable per relevant vertex and maximize the target potential. The edge constraints make the target potential a lower bound on every source-to-target path length, so maximizing is the correct direction.

$$
\max d_t
$$

$$
d_v \le d_u + w(u,v) \quad \text{for each edge } (u,v)
$$

$$
d_s = 0
$$

Do not minimize the target potential. The constraints above are upper-bound constraints on each potential relative to predecessor potentials, so minimization usually runs away from the shortest-path value.

State the negative-cycle condition if weights may be negative. The formulation is meaningful for a finite shortest-path value only when relevant negative cycles do not make the source-to-target distance unbounded below.

### Maximum flow

Use flow variables, capacity constraints, conservation at ordinary vertices, nonnegativity, and the net source-flow objective.

$$
\max \sum_{v \in V} f_{sv} - \sum_{v \in V} f_{vs}
$$

$$
0 \le f_{uv} \le c(u,v)
$$

$$
\sum_{v \in V} f_{uv} = \sum_{v \in V} f_{vu} \quad \text{for ordinary vertices } u
$$

For a compact model, create variables only for edges or explicitly set nonedge capacities to zero. If the prompt asks for size, prefer the edge-based formulation.

### Minimum-cost flow

Minimum-cost flow keeps ordinary flow feasibility but adds exact source demand, exact sink demand, ordinary vertex conservation, and minimizes total edge cost.

$$
\min \sum_{(u,v) \in E} a(u,v) f_{uv}
$$

$$
\sum_{v \in V} f_{sv} - \sum_{v \in V} f_{vs} = d
$$

$$
\sum_{v \in V} f_{vt} - \sum_{v \in V} f_{tv} = d
$$

$$
\sum_{v \in V} f_{uv} = \sum_{v \in V} f_{vu} \quad \text{for every ordinary vertex } u
$$

Use this model when the amount shipped is fixed and the optimization is cost, not flow value.

### Multicommodity flow

Create one flow for each commodity and bind them through shared edge capacities. There may be no objective if the question is feasibility.

$$
\sum_{i=1}^{k} f^i_{uv} \le c(u,v)
$$

Each commodity has its own conservation and demand constraints. Do not solve each commodity independently unless capacities are not shared.

### Bipartite matching as LP

The natural edge-variable relaxation for bipartite matching is a legitimate LP formulation, but explain why integrality is available if the answer needs an actual matching. The chapter also supports the maximum-flow reduction; use that route when the prompt expects CLRS flow integrality rather than total-unimodularity vocabulary.

$$
\max \sum_{e \in E} x_e
$$

$$
\sum_{e \ni v} x_e \le 1 \quad \text{for each vertex } v
$$

$$
x_e \ge 0
$$

If you add binary constraints, say you have changed the problem into an integer linear program unless you are explicitly proving the LP relaxation has an integral optimum.

## Duality and Certificates

For the chapter standard primal, the dual is below.

$$
\max c^T x
$$

$$
A x \le b
$$

$$
x \ge 0
$$

$$
\min b^T y
$$

$$
A^T y \ge c
$$

$$
y \ge 0
$$

Mechanical rule:

1. Change maximization to minimization.
2. Exchange objective coefficients and right-hand-side coefficients.
3. Transpose the constraint matrix.
4. Reverse the inequality direction for the main constraints.
5. Preserve nonnegativity for the dual variables in this standard form.

Interpretation rule: nonnegative dual variables are multipliers for primal constraints. A feasible dual solution is a valid upper bound on every primal feasible objective value. Minimizing the dual searches for the best such upper bound.

Weak duality says every primal feasible objective value is at most every dual feasible objective value.

$$
c^T x \le b^T y
$$

Use the equality certificate below when candidate feasible solutions are given.

$$
c^T \bar{x} = b^T \bar{y}
$$

If both candidates are feasible and the displayed equality holds, both are optimal.

Strong duality needs the right preconditions. In the chapter standard setting, if primal and dual are feasible and bounded, their optimal objective values are equal. Do not use strong duality to prove feasibility; establish feasibility first or cite the appropriate theorem status.

## Complementary Slackness Checklist

Use complementary slackness when you have candidate primal and dual solutions or need to construct one certificate from the other.

First verify feasibility on both sides. Then check the two zero-product conditions.

For every primal constraint, either the dual variable is zero or the primal constraint is tight.

$$
y_i\left(b_i - A_i x\right) = 0
$$

For every primal variable, either the primal variable is zero or the corresponding dual constraint is tight.

$$
x_j\left((A^T y)_j - c_j\right) = 0
$$

Operational proof recipe:

1. List the positive primal variables and force their dual constraints tight.
2. List the positive dual variables and force their primal constraints tight.
3. Solve the resulting equalities for the missing certificate values.
4. Verify all remaining inequalities and nonnegativity conditions.
5. Conclude optimality by weak duality through equal objective values.

Do not skip feasibility. Complementary slackness equations alone do not certify optimality if either side violates its constraints.

## Farkas Certificates and Fundamental Status

Farkas's lemma is a certificate of exactly one of two alternatives: a linear inequality system has a solution, or a nonnegative separating multiplier proves it cannot have one.

Use it as a proof move, not as a computational recipe:

1. Put the target feasibility question into matrix inequality form.
2. Assume the feasible alternative fails.
3. Invoke the separating multiplier alternative.
4. Translate the multiplier equations into a contradiction with the alleged optimum or with feasibility.

The fundamental theorem status list is exhaustive for a standard-form LP:

1. finite optimum;
2. infeasible;
3. unbounded in the objective direction.

When reviewing solver output, require one of these statuses plus a certificate or witness: primal solution for finite optimum, infeasibility certificate, or improving ray for unboundedness.

## Integer Linear Programming

Adding integrality constraints changes the computational problem. Weak duality-style bounds can still compare feasible integer primal and dual solutions, but strong LP duality does not generally survive integrality.

Use the comparison below when both integer versions are feasible and bounded.

$$
IP \le P = D \le ID
$$

Do not claim a general polynomial-time algorithm for integer linear programming. If an LP relaxation gives integer optima for a special problem, state the special structural reason, such as a flow integrality theorem or a totally unimodular constraint matrix.

## Worked Pattern: Model Then Certify

When asked to prove an LP solution optimal, answer in this shape:

1. **Primal model:** define the decision variables, objective, and constraints.
2. **Candidate:** state the proposed primal values and verify feasibility.
3. **Dual:** write the dual using the standard-form rule or explain any conversion first.
4. **Dual candidate:** give dual values and verify dual feasibility.
5. **Equality:** show the objective values match in a display block.
6. **Conclusion:** invoke weak duality or complementary slackness to certify optimality.

Use the equality certificate as the final displayed comparison.

$$
c^T \bar{x} = b^T \bar{y}
$$

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Gave correct isolated formulas but no chapter-wide modeling workflow | Start with variables, constraints, objective direction, equivalence, status, and certificate |
| Formulated shortest paths with path-selection or minimization habits | Use potential variables, edge upper-bound constraints, and maximize the target potential |
| Treated matching integrality as obvious or added binary variables silently | Explain flow integrality or relaxation integrality; otherwise call it integer programming |
| Stated weak duality but did not separate it from strong duality | Use weak duality for bounds and equality certificates; require feasibility and boundedness for strong duality |
| Mentioned complementary slackness without checking feasibility first | Verify primal and dual feasibility before zero-product conditions |
| Covered shortest path, matching, and duality but omitted minimum-cost and multicommodity flow | Include the graph-flow formulation decision rules from the chapter |
| Leaked formulas in table cells or prose | Put all symbolic expressions in display LaTeX blocks |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Choosing variables after writing constraints | Define decision variables and units first |
| Using strict inequalities | Replace the model with non-strict LP constraints or explain why ordinary LP does not apply |
| Minimizing a variable constrained only as a lower-bound certificate | Re-evaluate objective direction from the constraint semantics |
| Calling an unbounded feasible region an unbounded LP | Check whether the objective has a finite optimum |
| Converting to standard form but forgetting objective translation | Map the transformed optimum back to the original objective |
| Using simplex as a production default | Prefer maintained solvers; preserve simplex as geometry and certificate intuition |
| Reading dual variables without matching them to primal constraints | Pair each dual variable with the corresponding primal constraint |
| Applying integer-flow or matching extraction to arbitrary real LPs | Require an integrality theorem or add integer constraints and state the hardness consequence |

## Verification Pressure Tests

Use these prompts to test whether the skill changes behavior:

1. A shortest-path prompt asks for an LP and tempts binary path variables. The answer must use potentials, maximize the target potential, and explain the objective direction.
2. A bipartite-matching prompt asks whether binary constraints are necessary. The answer must distinguish the continuous relaxation, integrality justification, and integer programming.
3. A candidate primal-dual pair is given. The answer must verify both feasibilities, check complementary slackness, and conclude through weak duality.
4. A minimum-cost multicommodity-flow prompt names shared capacities and costs. The answer must keep commodity flows separate, aggregate capacity shared, and objective cost over aggregate edge flow.
5. A solver returns infeasible or unbounded. The answer must request or describe the appropriate certificate instead of giving an optimum.
6. A response must include a decision table and LP formulas under the parent CLRS formatting rules. Reject any formula in a table cell, heading, inline code span, or prose sentence.
7. A production team asks whether to implement simplex. The answer must recommend a solver unless the task is educational, while preserving the geometric and dual-certificate lesson.

## Skill Structure Validation

Use these checks when reviewing this skill:

- Confirm this file lives at `clrs/linear-programming/SKILL.md`.
- Confirm frontmatter has `name`, `description`, and `license`, with the name matching the directory slug.
- Confirm the parent `clrs/SKILL.md` routes to `linear-programming`.
- Inspect headings and tables for formulas; formulas must appear only in display LaTeX blocks.
- Check that the skill covers modeling, standard form, feasibility, simplex intuition, graph LPs, duality, complementary slackness, Farkas certificates, integer LP, and production solver judgment.
- Check that RED failures are represented in `## RED Pressure Failures This Skill Prevents`.
- Check that no session narrative, source-processing story, or authoring log appears in the skill.
