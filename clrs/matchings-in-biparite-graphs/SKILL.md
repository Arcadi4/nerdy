---
name: matchings-in-biparite-graphs
description: Use when solving, proving, implementing, or reviewing bipartite matching, Hopcroft-Karp, stable marriage, Gale-Shapley, Hungarian assignment, feasible labels, equality subgraphs, or augmenting-path matching arguments.
license: MIT
---

# Matchings in Bipartite Graphs

## Overview

Matching answers are dual-structure answers: first decide whether the task is cardinality matching, stable preference matching, or weighted assignment, then use the certificate that belongs to that model. Augmenting paths certify maximum cardinality, no blocking pair certifies stability, and feasible labels plus equality edges certify optimal weighted assignments.

**Core principle:** do not collapse the chapter into a generic max-flow reduction. Preserve the matching-specific alternating-path, rejection, and labeling proof moves, then translate textbook pseudocode into implementation contracts only when the input model justifies it.

## Shared CLRS Conventions

- Follow the parent `clrs` skill for mathematical formatting: every formula, inequality, set expression, slack definition, or asymptotic bound belongs in a display LaTeX block, never in prose, headings, table cells, or inline code spans.
- Use `elementary-graph-algorithms` for ordinary graph representation, breadth-first search, depth-first search, and transpose traversal mechanics.
- Use `maximum-flow` when the requested deliverable is a flow-network reduction or an integrality proof. Use this skill when the requested deliverable is a matching algorithm, matching theorem, stable-matching proof, or assignment-labeling argument.
- Keep quick-reference tables verbal. Put all symbolic definitions and running times in display blocks near the table.
- State which side of the bipartition proposes, which side is optimized, and whether the matching is cardinality, stable, or weighted before naming an algorithm.
- Start directly with the polished answer. The first visible line must be a domain heading or a substantive matching sentence, not a process note. Do not include meta preambles such as “checking formatting,” “evaluating complexity,” “evaluating the skill,” “I’m thinking,” “displaying complexity,” “scenario answer,” or “finalizing the presentation,” because those are common places for forbidden inline formulas and session narration to leak. If a draft starts with one of those phrases, delete the preamble before answering.

## When to Use

Use this skill for:

- Maximum bipartite matching, augmenting paths, Berge-style optimality, symmetric-difference proofs, and Hopcroft-Karp.
- Stable marriage and Gale-Shapley, including blocking pairs, proposer-optimality, receiver-pessimality, and choice-order independence.
- Maximum-weight perfect matching in complete bipartite graphs, assignment problems, feasible labels, equality subgraphs, and the Hungarian algorithm.
- Questions about Hall's theorem, regular bipartite perfect matchings, hospital-resident variants, weak Pareto optimality, cycle covers by assignment reduction, and padding unequal assignment sides.
- Implementation reviews involving alternating directed graphs, layered augmenting-path searches, rank lookup tables, slack arrays, or relabeling invariants.

Do **not** use this as the main skill for non-bipartite matching, general stable roommates, or arbitrary weighted matching outside bipartite assignment. Mention the boundary explicitly: the stable-roommates problem can have no stable matching, and general graph matching needs different algorithms.

## First Decision

| Problem shape | Use | Required contract | Proof hook |
| --- | --- | --- | --- |
| Maximum cardinality in an unweighted bipartite graph | Hopcroft-Karp or augmenting paths | Bipartition is valid and edges cross sides only | No augmenting path iff maximum |
| One augmenting improvement or proof of nonoptimality | Symmetric difference | Current object is a matching | Alternating path increases size |
| Complete preference lists with equal sides | Gale-Shapley | Strict rankings over the other side | Men improve over time; first rejection proof |
| Proposer-side optimal stable matching | Gale-Shapley with chosen proposing side | Same proposing side fixed throughout | First rejected stable partner contradiction |
| Maximum-weight perfect assignment | Hungarian algorithm | Complete weighted bipartite graph with equal sides, or a justified padding/modification | Feasible labels and equality-perfect matching |
| Need only a matching reduction to flow | Maximum-flow skill | Unit-capacity flow network and integrality | Flow-to-matching extraction |

Common bounds for this chapter are below.

$$
O(\sqrt{|V|}\,|E|)
$$

$$
O(n^2)
$$

$$
O(n^4)
$$

$$
O(n^3)
$$

## Cardinality Matching and Augmenting Paths

A matching is a set of edges with no shared endpoints. A bipartite graph has a left side and a right side, and every edge crosses between the two sides.

Use the alternating-path vocabulary precisely:

- An alternating path alternates between edges already in the matching and edges outside the matching.
- An augmenting path starts and ends at unmatched vertices.
- The first and last edges of an augmenting path are outside the matching.
- The path has one more nonmatching edge than matching edge.

The symmetric-difference update is below.

$$
M' = M \oplus P
$$

The operation removes the matching edges on the augmenting path and adds the nonmatching edges on the path. Lemma 25.1 says the result is a matching whose cardinality increases by one.

For several vertex-disjoint augmenting paths, use the update below.

$$
M' = M \oplus (P_1 \cup P_2 \cup \cdots \cup P_k)
$$

Corollary 25.2 says the matching size increases by the number of paths because the paths are vertex-disjoint.

### Berge-Style Optimality

When proving maximum cardinality, do not say merely that the algorithm is stuck. Use Corollary 25.4: a matching is maximum exactly when no augmenting path exists.

The proof hook is Lemma 25.3. Given a current matching and a larger matching, their symmetric difference decomposes into vertex-disjoint simple paths, cycles, and isolated vertices with alternating edges. If the other matching is larger, enough of those components are augmenting paths for the current matching.

Use this theorem when asked to:

1. prove a specific matching is maximum;
2. explain why any nonmaximum matching admits an augmenting path;
3. justify batching vertex-disjoint augmenting paths;
4. compare a current matching against an unknown optimum.

## Hopcroft-Karp

Hopcroft-Karp repeatedly augments along a maximal set of vertex-disjoint shortest augmenting paths. The set must be maximal, not maximum. The algorithm does not need to solve a harder disjoint-path optimization subproblem inside each phase.

The repeat-loop shape is:

1. Start with the empty matching.
2. Find a maximal set of vertex-disjoint shortest augmenting paths.
3. Augment by symmetric difference along all of those paths.
4. Stop when the set is empty.

### Line-Three Construction

When asked for the chapter-specific implementation, give the three-phase construction rather than a generic forward depth-first search:

1. Build the directed alternating graph. Direct unmatched edges from the left side to the right side, and matched edges from the right side to the left side.
2. Run a multi-source breadth-first search from every unmatched left vertex. Keep only layers through the first layer containing an unmatched right vertex, and keep only edges between consecutive layers. This is the layered directed acyclic graph.
3. Form the transpose of that layered graph. Run depth-first searches from unmatched vertices in the final layer back toward layer zero, marking vertices as discovered, to recover a maximal set of vertex-disjoint shortest augmenting paths.

Use the symbols below when a formal answer needs the chapter names.

$$
G_M
$$

$$
H
$$

$$
H^T
$$

$$
q
$$

The transpose search matters. Searching backward from the unmatched right vertices avoids repeatedly exploring prefixes that another path has already claimed from many layer-zero roots. Each vertex in the layered graph is searched at most once in that phase.

Per iteration, the directed graph construction, layered breadth-first search, transpose construction, and depth-first searches together use linear time in the graph representation.

$$
O(E)
$$

The total running time is Theorem 25.8.

$$
O(\sqrt{V}\,E)
$$

### Hopcroft-Karp Proof Hooks

Use Lemma 25.5 when asked why shortest augmenting paths get longer. After augmenting along a maximal set of shortest augmenting paths of length named by the final layer, any new shortest augmenting path is longer. If the new path is disjoint from the chosen set, maximality would have been violated. If it shares vertices, use the symmetric-difference construction below and count shared edges with Lemma 25.3.

$$
A = M \oplus M' \oplus P
$$

Use Lemma 25.6 when bounding remaining work after paths are long. If every shortest augmenting path has length at least the current layer length, the gap to a maximum matching is bounded by the number of vertices divided by the number of vertices consumed per vertex-disjoint augmenting path.

The iteration proof combines both facts: path lengths strictly increase across phases, and after the paths become long enough, only few augmenting phases remain.

## Stable Marriage and Gale-Shapley

Stable marriage uses a complete bipartite graph with equal sides and strict preference lists. A stable matching has no blocking pair: an unmatched cross-side pair in which both vertices prefer each other to their assigned partners.

For the woman-proposing version, the algorithm is:

1. Every woman and every man starts free.
2. While some woman is free, choose a free woman.
3. She proposes to the first man on her list who has not yet received a proposal from her.
4. A free man accepts.
5. An engaged man keeps whichever proposer he prefers, breaking his old engagement if necessary.
6. A rejected woman remains or becomes free.

### Termination and Stability

Theorem 25.9 has two reusable moves.

Termination:

1. A woman never proposes to the same man twice.
2. The number of proposals is finite.
3. If a woman had proposed to every man and were still free, every man would be engaged.
4. With equal side sizes, that contradicts any woman remaining free.

Stability:

1. Suppose a final woman prefers another man to her assigned partner.
2. She must have proposed to that man earlier.
3. He either rejected her immediately or later left her for someone he preferred.
4. Men only improve their held partner over time.
5. Therefore he cannot prefer her to his final partner, so the alleged pair is not blocking.

The standard implementation uses a next-proposal index for each proposer and a rank lookup table for each receiver. That gives the chapter bound below.

$$
O(n^2)
$$

### Proposer Optimality and Receiver Pessimality

Theorem 25.11 is stronger than termination or stability. For a fixed proposing side, Gale-Shapley returns the same stable matching regardless of which free proposer is selected next, and every proposer gets the best partner that proposer can have in any stable matching.

Use the exact proof move when challenged:

1. Assume there is a first time any receiver rejects a proposer who belongs with that receiver in some stable matching.
2. At that moment the receiver switches to a new proposer.
3. Show the new proposer cannot have any stable partner preferred to that receiver.
4. In the alleged stable matching, the new proposer and that receiver would block.
5. Therefore the rejection could not have been of a stable partner.

Consequences:

- Different stable matchings may exist.
- A fixed proposing side's Gale-Shapley run returns only the proposer-optimal one.
- In woman-proposing Gale-Shapley, each man receives the worst partner he can receive among all stable matchings.
- Reversing the proposing side reverses which side receives the optimality guarantee.

## Hungarian Algorithm and Assignment

The assignment problem in this chapter is maximum-weight perfect matching in a complete weighted bipartite graph with equal sides. If the prompt has a minimization objective, unequal side sizes, or missing edges, first state the transformation: negate or shift weights for minimization when appropriate, pad sides with dummy vertices, or modify the graph so the perfect-matching model preserves the desired feasible assignments.

### Feasible Labels and Equality Edges

A feasible vertex labeling assigns labels so every edge weight is bounded above by the sum of the endpoint labels.

$$
h(l) + h(r) \ge w(l,r)
$$

A standard initial feasible labeling is below.

$$
h(l) = \max_{r \in R} w(l,r)
$$

$$
h(r)=0
$$

The equality subgraph keeps exactly the edges whose label sum equals the edge weight.

$$
h(l) + h(r) = w(l,r)
$$

Theorem 25.14 is the optimality certificate: any perfect matching in the equality subgraph under feasible labels is an optimal assignment. The proof compares the weight of any perfect matching to the sum of all labels. Equality edges make the chosen perfect matching achieve that upper bound.

### Search and Relabeling

The directed equality graph uses unmatched equality edges from left to right and matched equality edges from right to left. Breadth-first search starts from all unmatched left vertices and maintains the forest sides below.

$$
F_L = L \cap V_F
$$

$$
F_R = R \cap V_F
$$

If the search reaches an unmatched right vertex, trace predecessors to get an augmenting path and update the matching by symmetric difference.

If the queue empties first, compute the minimum slack from reached left vertices to unreached right vertices.

$$
\delta = \min\{h(l)+h(r)-w(l,r): l \in F_L \text{ and } r \in R-F_R\}
$$

Relabel with the rule below.

$$
h(l) \leftarrow h(l)-\delta \quad \text{for } l \in F_L
$$

$$
h(r) \leftarrow h(r)+\delta \quad \text{for } r \in F_R
$$

All other labels stay unchanged.

Lemma 25.15 supplies the relabeling checklist:

1. Feasibility remains true by considering the four cases for membership in the reached sets.
2. Forest edges remain equality edges.
3. Matched edges remain in the directed equality graph.
4. At least one new equality edge enters from a reached left vertex to an unreached right vertex.

Do not omit the matched-edge preservation claim. For every matched edge at relabel time, its left endpoint is reached exactly when its right endpoint is reached.

$$
l \in F_L \quad\Longleftrightarrow\quad r \in F_R
$$

That equivalence is what prevents relabeling from breaking the current matching or forest.

The straightforward implementation reconstructs equality structure often enough to get the chapter bound below.

$$
O(n^4)
$$

The slack-array improvement avoids explicit reconstruction. Maintain, for each unreached right vertex, the minimum slack from the reached left set.

$$
\sigma(r)=\min_{l \in F_L}\{h(l)+h(r)-w(l,r)\}
$$

Then each relabel uses the minimum slack value, updates all unreached-right slacks, and refreshes slacks when the reached-left set grows. The improved bound is below.

$$
O(n^3)
$$

## Worked Answer Pattern

When solving a matching problem, use this structure:

1. **Classify the model:** cardinality matching, stable matching, or weighted perfect assignment.
2. **State preconditions:** bipartition, completeness, equal side sizes, strict preferences, weight objective, or required graph modification.
3. **Name the certificate:** no augmenting path, no blocking pair, or feasible labels plus equality-perfect matching.
4. **Choose the algorithm:** Hopcroft-Karp, Gale-Shapley, Hungarian, or a flow reduction only when the prompt asks for a flow model.
5. **Give the local proof move:** symmetric-difference decomposition, first rejection, or relabel feasibility.
6. **State implementation contract:** transpose-layered DFS, proposal indices and receiver ranks, or slack arrays.
7. **Separate textbook and production judgment:** prefer mature libraries for large matching or assignment workloads unless the task is educational, auditable, or needs a custom constraint adaptation.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Described Hopcroft-Karp with generic forward DFS from free left vertices | Use the chapter construction: directed alternating graph, layered DAG through the first unmatched-right layer, transpose search from that final layer back to layer zero |
| Said shortest augmenting paths get longer without proof hooks | Cite maximality for disjoint paths and the symmetric-difference construction for intersecting paths |
| Stated Gale-Shapley proposer optimality but skipped the stronger theorem | Include choice-order independence and the first rejected stable partner proof move |
| Claimed woman-proposing Gale-Shapley is good for both sides | State proposer-optimality and receiver-pessimality separately |
| Explained Hungarian relabeling with generic searched sets | Use the chapter names for reached left and reached right forest sets |
| Said matched edges stay equality edges without the reason | Include the endpoint-reachability equivalence for matched edges |
| Put formulas or bounds inside prose, table cells, headings, or inline code | Move symbolic content into display LaTeX blocks |
| Added meta preambles before the answer | Delete the preamble; the first visible line must be a substantive answer line |
| Used the maximum-flow bipartite matching reduction as the whole answer | Use flow only for flow-reduction prompts; otherwise preserve matching-specific algorithms and certificates |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Confusing maximal matching with maximum matching | Maximal only means no single edge can be added; maximum needs the augmenting-path certificate |
| Forgetting augmenting paths must start and end unmatched | Alternating paths that do not increase cardinality are not augmenting paths |
| Searching all shortest paths in Hopcroft-Karp | A maximal vertex-disjoint set is enough for each phase |
| Running Hopcroft-Karp phase three forward through the layered graph | Use the transpose search from unmatched vertices in the final layer back to the sources |
| Saying Gale-Shapley output depends on which free proposer is chosen | For a fixed proposing side, the stable matching is the same |
| Hiding receiver rankings in a linear scan | Precompute rank lookup tables for the quadratic implementation bound |
| Calling every complete weighted bipartite problem Hungarian-ready | Check perfect-matching feasibility, side sizes, missing edges, and minimization transformations |
| Relabeling Hungarian labels without preserving matched edges | Prove the matched-endpoint reachability equivalence before claiming the current matching survives |
| Treating textbook implementations as default production code | Extract the certificate and invariant; use libraries or specialized solvers for large or constrained workloads |
| Beginning with “I am checking,” “evaluating complexity,” “displaying complexity,” or “scenario answer” | Remove the preamble and start with the stable matching, augmenting-path, or assignment answer |

## Red Flags

Delete and rewrite the opening if the answer starts with any of these instead of matching content:

- A statement about checking formatting or complexity presentation.
- A statement about thinking, finalizing, evaluating, or planning the answer.
- A statement that the answer will come next.
- A heading whose only purpose is “Scenario answer” or “Evaluation” before the substantive answer.

The answer may include an evaluation section only after the substantive response and only when the prompt explicitly asks for it.

## Verification Pressure Tests

Use these prompts to test whether the skill changes behavior:

1. A Hopcroft-Karp explanation says to run depth-first search from free left vertices after breadth-first search. Ask for the chapter's line-three implementation and reject any answer that omits the transpose layered graph search from the first unmatched-right layer.
2. A proof claims a matching is maximum because no local edge can be added. Ask for the symmetric-difference theorem that separates maximal from maximum.
3. A Gale-Shapley prompt claims the output can change depending on which free woman is chosen next. Ask for the theorem that refutes this and require the first rejected stable partner proof move.
4. A stable matching answer says woman-proposing Gale-Shapley is fair to both sides. Ask which side is optimal and which side is pessimal among all stable matchings.
5. A Hungarian relabeling proof says tree edges and matched edges remain equality edges. Ask for the exact reached-set names, the relabel rule, the new-edge guarantee, and the matched-edge endpoint equivalence.
6. A weighted assignment implementation repeatedly rebuilds equality graphs. Ask for the slack-array improvement and the improved running time.
7. A response must include a quick-reference table and complexity bounds under parent CLRS formatting rules. Reject any formula in a table cell, heading, inline code span, or prose sentence.
8. A prompt asks for maximum bipartite matching and mentions maximum flow. Ask when the answer should use the flow reduction and when it should use Hopcroft-Karp directly.

## Static Checks

Before declaring the skill complete:

- Confirm this file lives at `clrs/matchings-in-biparite-graphs/SKILL.md` and preserves the requested `biparite` slug spelling.
- Confirm frontmatter has `name`, `description`, and `license`, with the name matching the directory slug.
- Confirm the parent `clrs/SKILL.md` routes to `matchings-in-biparite-graphs`.
- Inspect headings and tables for formulas; formulas must appear only in display LaTeX blocks.
- Check that Hopcroft-Karp includes the directed graph, layered graph, first unmatched-right layer, transpose graph, and backward depth-first searches.
- Check that Gale-Shapley includes choice-order independence, proposer-optimality, receiver-pessimality, and the first-rejection proof move.
- Check that Hungarian includes feasible labels, equality subgraph, forest sets, relabeling, matched-edge preservation, and slack-array improvement.
- Check that RED failures are represented in `## RED Pressure Failures This Skill Prevents`.
- Check that the skill distinguishes matching-specific algorithms from the `maximum-flow` bipartite matching reduction.
- Check that no session narrative, conversion story, authoring log, or meta-answer preamble appears in the skill or in GREEN pressure-test answers.
