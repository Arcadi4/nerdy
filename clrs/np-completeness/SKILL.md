---
name: np-completeness
description: Use when classifying decision problems as P, NP, NP-hard, NP-complete, or co-NP; proving polynomial-time reductions; reviewing SAT, 3-CNF-SAT, CLIQUE, VERTEX-COVER, HAM-CYCLE, TSP, SUBSET-SUM, encoding, or pseudo-polynomial complexity arguments.
license: MIT
---

# NP-Completeness

## Overview

NP-completeness answers whether an exact polynomial-time algorithm is plausible under the chapter model. Treat every proof as a certificate-and-reduction audit: define the decision language, prove verifiability, reduce from a known hard source in the correct direction, and prove both answer preservation and polynomial construction size.

**Core principle:** an NP-completeness proof is incomplete unless it separately proves membership in NP, maps arbitrary source instances to target instances without solving them, proves both directions of equivalence, and accounts for encoding length.

## Shared CLRS Conventions

- Follow the parent `clrs` skill for mathematical formatting: every language definition, reduction relation, asymptotic bound, threshold, and symbolic assignment belongs in display LaTeX blocks.
- Keep tables verbal. Put reduction relations, targets, and construction formulas in display blocks near the table instead of inside table cells.
- Use `elementary-graph-algorithms` for ordinary graph traversal, `shortest-paths` for shortest-path algorithms, `linear-programming` for LP modeling, and this skill when the task asks for NP membership, NP-hardness, reductions, encoding, or exact hardness evidence.
- Do not announce that you are using this skill. Deliver the polished classification, reduction, or review directly.

## When to Use

Use this skill when a task involves:

- proving a decision problem is in P, in NP, NP-hard, NP-complete, or related to co-NP;
- converting optimization hardness into a bound decision version;
- building or reviewing a polynomial-time reduction;
- choosing among CIRCUIT-SAT, SAT, 3-CNF-SAT, CLIQUE, VERTEX-COVER, HAM-CYCLE, TSP, or SUBSET-SUM as a source problem;
- checking whether a numeric algorithm is pseudo-polynomial rather than polynomial in the input length;
- explaining why an exact polynomial algorithm for one NP-complete problem would imply the standard collapse.

Do **not** use this skill merely because an algorithm is slow. Use it when the answer must reason about formal decision languages, certificates, reductions, or encoding-sensitive polynomial time.

## First Decision

| Situation | First move | Watch for |
| --- | --- | --- |
| Candidate NP-complete proof | Prove membership in NP before hardness | Reduction alone proves only hardness |
| Hardness proof | Reduce a known NP-complete source to the candidate | Reversing the direction |
| Optimization prompt | Define a related decision version with a threshold | Claiming NP-completeness of an optimization problem directly |
| Numeric input with dynamic programming | Compare runtime to bit length, not numeric value | Calling pseudo-polynomial time polynomial |
| Circuit or formula conversion | Introduce variables for wires or subformulas | Exponential truth tables or duplicated fan-out |
| Gadget reduction | State local traversal or choice properties first | Drawing gadgets without proving forced behavior |
| Special-case relationship | Show the hard problem is a restricted instance of the target | Reducing the target to the hard special case |

Reduction direction rule:

$$
L_{\text{known hard}} \le_P L_{\text{candidate}}
$$

If the candidate then had a polynomial-time decision algorithm, the known hard source would also have one.

## Output Contract Checklist

Before giving a final NP-completeness answer, check each item that applies:

1. **Decision language:** name the yes/no problem and the encoded input.
2. **Certificate:** for NP membership, state the certificate, prove its length is polynomial in the encoded input length, and explain how to verify it in polynomial time.
3. **Source problem:** choose a known NP-complete source that structurally resembles the candidate.
4. **Mapping:** describe the construction from an arbitrary source instance to a target instance.
5. **No oracle:** ensure the construction does not require knowing whether the source instance is satisfiable or otherwise solved.
6. **Forward direction:** prove a yes source instance creates a yes target instance.
7. **Reverse direction:** prove a yes target instance yields a yes source instance.
8. **Size bound:** count the constructed objects and prove polynomial construction time.
9. **Encoding:** for numeric problems, compare runtime and instance size under the actual encoding.
10. **Conclusion:** distinguish NP-hard from NP-complete and state any conditional implication for polynomial algorithms.

## Language and Class Vocabulary

A decision problem is represented by a language over binary strings. Use standard concise encodings unless the prompt explicitly changes the encoding.

$$
L = \{x \in \{0,1\}^* : Q(x)=1\}
$$

Class P contains languages decided in polynomial time. Class NP contains languages verifiable in polynomial time by a polynomial-length certificate.

$$
L = \{x : \exists y \text{ such that } A(x,y)=1\}
$$

P is contained in NP by ignoring the certificate. co-NP contains complements of NP languages; whether NP is closed under complement is unknown.

Use the implication below only after proving NP-completeness.

$$
L \in NPC \text{ and } L \in P \quad\Longrightarrow\quad P = NP
$$

## Reduction Proof Workflow

Use this sequence for every candidate problem.

1. Define the decision version. For an optimization problem, introduce a bound and ask whether some feasible solution meets it.
2. Prove membership in NP with an explicit certificate. Examples include a vertex subset, a Hamiltonian vertex sequence, a satisfying assignment, a subset of numbers, or a tour.
3. Pick a known NP-complete source whose constraints resemble the candidate's objects.
4. Construct the target instance in polynomial time from arbitrary source input.
5. Prove source yes implies target yes by transforming a source witness into a target witness.
6. Prove target yes implies source yes by extracting a source witness from any target witness.
7. Count vertices, clauses, numbers, digits, gates, or gadgets to prove polynomial size.
8. Conclude NP-hardness, then combine with membership in NP for NP-completeness.

Common direction trap:

$$
L_{\text{candidate}} \le_P L_{\text{known in P}}
$$

The relation above can support an upper bound for the candidate. It does not prove hardness.

Optimization-to-decision pattern:

1. Identify the optimization output, such as minimum cost, maximum length, largest subset, or best tour.
2. Introduce a threshold as part of the encoded input.
3. Ask whether some feasible solution meets the threshold in the correct direction.
4. Prove the optimization algorithm would answer the decision version by comparing its optimum with the threshold.
5. Prove hardness for the decision version; then explain the consequence for exact optimization.

## Encoding and Pseudo-Polynomial Time

Polynomial time is measured in the length of the encoded input, not in the magnitude of a numeric value. Reasonable concise encodings that are polynomially related preserve polynomial solvability, but unary and binary encodings can change whether a numeric dynamic program is polynomial in the input length.

If a dynamic program for SUBSET-SUM runs in time proportional to the target value, compare that value with the number of bits used to write it. With binary encoding, the table can be exponential in the input length. The algorithm is pseudo-polynomial; it does not prove a binary-encoded NP-complete problem is in P.

Safe conclusion pattern:

1. State the runtime in terms of the numeric target.
2. State the target can be exponentially larger than its bit representation.
3. Call the algorithm pseudo-polynomial under binary encoding.
4. If unary encoding is imposed, explain that the input length changes and the same dynamic program may become polynomial in that altered encoding.

## Canonical Source Problems and Reductions

Use CIRCUIT-SAT when proving NP-hardness from the definition of NP or when the source is an arbitrary polynomial-time verifier. Use SAT or 3-CNF-SAT for ordinary problem-to-problem reductions after the initial NP-complete problem is established, especially when the target naturally encodes Boolean choices, local consistency, clauses, or selected witnesses.

### CIRCUIT-SAT

CIRCUIT-SAT asks whether an acyclic Boolean circuit has an input assignment that makes its single output true. It is in NP by using an assignment to input wires, or all wires, as the certificate and checking each gate.

NP-hardness proof move: for any NP language with polynomial-time verifier, build a circuit that simulates the verifier on fixed input and unknown certificate bits for the polynomial number of steps. The circuit is satisfiable exactly when a valid certificate exists.

### SAT from CIRCUIT-SAT

Create one formula variable per circuit wire and add a small equivalence constraint for each gate. Conjoin the output wire variable with all gate constraints.

Proof obligations:

- A satisfying circuit assignment extends to all wire variables and satisfies every gate clause.
- Any satisfying formula assignment makes each wire variable consistent with its gate, so the output wire is true.
- The construction has one constant-size formula block per gate.

Trap: do not recursively expand shared circuit outputs into a formula tree. Fan-out can duplicate subcircuits exponentially.

### 3-CNF-SAT from SAT

Use a local construction rather than a truth table for the whole formula.

1. Parse the formula and introduce a fresh variable for each internal node.
2. Add constraints that make each node variable equivalent to the operation applied to its children, and require the root variable to be true.
3. Convert each constant-size constraint to CNF by enumerating only the falsifying rows for that small relation.
4. Pad short clauses to exactly three distinct literals with fresh auxiliary variables.

For a two-literal clause, use the pair below.

$$
(\ell_1 \vee \ell_2 \vee p) \wedge (\ell_1 \vee \ell_2 \vee \neg p)
$$

For a one-literal clause, use four clauses over fresh variables.

$$
(\ell \vee p \vee q)
\wedge (\ell \vee p \vee \neg q)
\wedge (\ell \vee \neg p \vee q)
\wedge (\ell \vee \neg p \vee \neg q)
$$

Traps:

- A truth table for the entire formula is exponential in the number of variables.
- Repeated expansion of shared subformulas can be exponential.
- Reusing padding variables where freshness is required can couple independent clauses.

### CLIQUE from 3-CNF-SAT

Given a formula with one three-literal clause per row, create one vertex for each literal occurrence. Add edges only between vertices from different clauses whose literals are consistent, meaning they are not complements.

Set the clique size to the number of clauses.

Forward direction: choose one true literal from each clause. The chosen vertices are pairwise adjacent because they come from different clauses and no satisfying assignment makes complementary literals both true.

Reverse direction: a clique of the target size must choose one vertex from each clause, and all chosen literals are mutually consistent. Set those literals true and extend arbitrarily.

### VERTEX-COVER from CLIQUE

Use the complement graph. A clique of the original graph corresponds to leaving those vertices out of a cover in the complement graph.

Target cover size:

$$
|V| - k
$$

Proof move: a set is a clique in the original graph exactly when its complement covers every edge in the complement graph.

### HAM-CYCLE from VERTEX-COVER

For the CLRS gadget reduction, emphasize proof obligations over memorized drawings.

Checklist:

- Normalize away isolated vertices or state the construction's assumption.
- Encode the cover bound with selector structure so at most the requested number of original vertices are chosen.
- Use one edge gadget per original edge and designated traversal ports.
- Prove a selected endpoint gives a traversal that visits the corresponding edge gadget exactly once.
- Prove an unselected-unselected edge cannot be fully traversed in a Hamiltonian cycle.
- Prove choices are consistent across all gadgets incident to the same original vertex.
- Count the selectors, edge gadgets, internal vertices, and edges.

Forward direction: from a vertex cover, route the Hamiltonian cycle through gadget paths associated with selected cover vertices and stitch them through selector vertices.

Reverse direction: from a Hamiltonian cycle, extract the original vertices whose selector paths were used and prove every original edge has at least one extracted endpoint.

### TSP from HAM-CYCLE

Decision TSP asks whether a complete graph with nonnegative integer costs has a tour no more expensive than a threshold.

Given a graph for HAM-CYCLE, build a complete graph on the same vertices. Assign zero cost to original edges and unit cost to nonedges. Use threshold zero.

$$
c(i,j)=0 \text{ for original edges}
$$

$$
c(i,j)=1 \text{ for nonedges}
$$

$$
k=0
$$

Then a tour of cost at most the threshold uses only original edges, exactly forming a Hamiltonian cycle.

### SUBSET-SUM from 3-CNF-SAT

Use digit positions to encode variable choices and clause satisfaction. Choose a base large enough to prevent carries; base seven is safe for the chapter construction.

For variables and clauses, create numbers with variable digits followed by clause digits.

Variable-choice numbers:

- For each variable, create one number for setting it true and one for setting it false.
- Both have a one in that variable's digit.
- A choice number has a one in a clause digit exactly when the corresponding literal appears in that clause.

Slack numbers:

- For each clause, create one slack number with a one in that clause digit.
- Create a second slack number with a two in that clause digit.

Target digits:

- Each variable digit target is one.
- Each clause digit target is four.

Forward direction: select exactly one choice number per variable according to a satisfying assignment. Each clause receives at least one and at most three literal contributions, and the slack numbers fill the clause digit to four.

Reverse direction: every variable digit target forces exactly one choice number for each variable, defining an assignment. Each clause digit must receive at least one literal contribution, because slack alone cannot reach four without exceeding available slack values. Therefore every clause has a true literal.

No-carry obligation: prove the largest possible digit sum stays below the base, so each digit enforces its own constraint independently.

## Choosing a Source Problem

| Target flavor | Good source | Why |
| --- | --- | --- |
| Boolean choices with local clauses | 3-CNF-SAT | Variables become choices; clauses become constraints |
| Pairwise consistency among chosen objects | CLIQUE or 3-CNF-SAT | Edges encode compatible choices |
| Covering all constraints with limited selected objects | VERTEX-COVER | The bound controls selected witnesses |
| Visiting every vertex exactly once | HAM-CYCLE | Hamiltonian structure is already exact traversal |
| Complete weighted tour with penalties | HAM-CYCLE | Zero-one costs enforce original adjacency |
| Exact numeric target | 3-CNF-SAT to SUBSET-SUM | Digits encode choices and satisfied clauses |
| Candidate contains a hard special case | That hard special case | Special-case containment proves hardness of the general target |

When the target is more general than a known hard problem, you may prove hardness by showing the known hard problem is a restricted version of the target. The direction is from the restricted hard problem into the general target.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Reducing the candidate to a known NP-complete problem | Reduce the known NP-complete problem to the candidate |
| Proving only NP-hardness | Add membership in NP to conclude NP-completeness |
| Solving the source instance during construction | The mapping must be computable without knowing the answer |
| Giving only one implication | Prove both source yes to target yes and target yes to source yes |
| Ignoring construction size | Count objects and argue polynomial time |
| Treating optimization problems as NP-complete directly | Define and prove hardness for the decision version |
| Using numeric value as input size | Measure against encoded length and identify pseudo-polynomial algorithms |
| Expanding formulas or circuits naively | Use one variable per node or wire and local constraints |
| Drawing a gadget without local proof | State ports, forced traversal, consistency, and extraction obligations |
| Claiming special target structure weakens the reduction | Restricted target instances are allowed; hardness transfers to the general problem |

## Pressure Tests

Use these checks when reviewing answers or revising this skill:

1. **Direction trap:** A proposed proof reduces LONGEST-SIMPLE-PATH to SHORTEST-PATH. The answer must reject the direction and give the full NP-completeness checklist.
2. **Formula blowup trap:** A SAT-to-3-CNF conversion proposes a full truth table or recursive expansion. The answer must use local auxiliary variables and prove polynomial size.
3. **Digit construction trap:** A SUBSET-SUM proof must specify literal clause digits, slack values, target digits, no-carry base, and both directions.
4. **Encoding trap:** A binary-encoded SUBSET-SUM dynamic program polynomial in the numeric target must be classified as pseudo-polynomial, not as proof of membership in P.
5. **Gadget proof trap:** A VERTEX-COVER to HAM-CYCLE proof must state selector, port, consistency, extraction, and polynomial-size obligations.
