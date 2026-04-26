---
name: machine-learning-algorithms
description: Use when answering CLRS-style machine-learning algorithm questions about k-means clustering, Lloyd's procedure, multiplicative weights, weighted majority, online experts, gradient descent, projected gradient descent, convex optimization, linear regression, or regularization.
license: MIT
---

# Machine-Learning Algorithms

## Overview

Machine-learning-algorithm answers must separate the textbook model from production machine-learning practice. Use the chapter mechanisms for their invariants, regret potentials, and convex-optimization proof moves; do not silently replace them with modern defaults such as k-means++ initialization, randomized exponential weights, or library-regression pipelines unless the prompt asks for production advice.

**Core principle:** first identify whether the task is clustering, online expert prediction, or convex optimization, then state the model assumptions that make the chapter theorem true before giving an algorithm, bound, or engineering recommendation.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, direct polished answers, theorem preconditions, and formula-free headings. Keep tables verbal and put objectives, updates, bounds, and potentials in display blocks adjacent to the table.

## Answer Formatting Guardrail

Machine-learning prompts often invite verification tables after theorem statements. A verification table is still a table: do not put parameter ranges, update factors, objective values, asymptotic bounds, theorem inequalities, or potential expressions in its cells.

Use this safe pattern instead:

1. In the table, use verbal labels such as "chapter penalty range," "prefix mistake theorem," "expert lower bound," or "projected-gradient guarantee."
2. Immediately before or after the table, put the exact expression in a display block.
3. If several expressions must be checked, use a numbered list with one display block per item instead of a table.

When reviewing your own answer, scan tables separately. If a table cell contains a symbol-heavy expression, move the expression out of the table before responding.

## When to Use

Use this skill for:

- k-means clustering, squared Euclidean dissimilarity, Lloyd's procedure, centroid updates, empty clusters, and vector quantization;
- online prediction from binary experts, deterministic weighted majority, multiplicative weights, mistake bounds, and regret-style potential arguments;
- convex gradient descent, projected gradient descent, average-iterate guarantees, line search, and amortized potential proofs;
- least-squares linear regression as convex optimization over weights, including norm-constrained regularization.

Do not use this skill for neural-network training, statistical learning theory, or production ML model selection unless the answer is explicitly connecting those topics back to these chapter mechanisms.

## First Decision

| Situation | First move | Watch for |
| --- | --- | --- |
| Unlabeled points and clusters | Check feature cleaning, scaling, dissimilarity, and whether the prompt wants Lloyd's local search or the global k-means objective | Treating Lloyd's result as globally optimal or changing the initialization without saying so |
| Binary expert predictions over time | Decide whether the deterministic weighted-majority theorem or the randomized exercise is being used | Importing the randomized bound into the deterministic theorem |
| Convex minimization over all space | Check convexity, differentiability, gradient norm bound, initial distance to an optimum, step size, and average-iterate return | Treating the gradient bound as a smoothness constant or reporting only the last iterate |
| Convex minimization with constraints | Add projection onto the feasible body and use the one-sided projection lemma | Replacing the chapter proof with a generic nonexpansiveness slogan |
| Linear regression | Name the weights as the optimization variables and the examples as data | Optimizing over feature vectors or forgetting the intercept and gradient cost |
| Regularization | Treat the norm bound as a constraint and project onto the ball | Saying regularization is only a penalty term or omitting the complexity-control purpose |

## K-Means and Lloyd's Procedure

Before computing clusters, check the feature contract:

1. Every example should have all attributes; either drop incomplete examples or impute missing values, with median imputation as the chapter's named example.
2. Scale comparable attributes so a large numeric range does not dominate distance; min-max scaling and mean-zero unit-variance scaling are both chapter-compatible choices.
3. Use squared Euclidean dissimilarity unless the prompt explicitly changes the model.

The chapter's dissimilarity is:

$$
\Delta(x, y) = \lVert x - y \rVert^2 = \sum_a (x_a - y_a)^2
$$

A clustering is an ordered collection of disjoint subsets, and empty clusters are allowed. Centers need not be input points. The objective is:

$$
f(S, C) = \sum_{x \in S} \min_j \Delta(x, c^{(j)})
$$

Equivalently, for the current assigned clusters:

$$
f(S, C) = \sum_{\ell=1}^{k} \sum_{x \in S^{(\ell)}} \Delta(x, c^{(\ell)})
$$

Use these theorem hooks precisely:

- **Theorem 33.1:** for a nonempty assigned cluster, the unique center minimizing within-cluster squared distance is the centroid.
- **Theorem 33.2:** for fixed centers, an assignment minimizes the objective if and only if every point is assigned to a nearest center.

The centroid update is:

$$
c^{(\ell)} = \frac{1}{\lvert S^{(\ell)} \rvert} \sum_{x \in S^{(\ell)}} x
$$

### Lloyd Workflow

1. Initialize the centers by independently sampling input points at random.
2. Initially assign all points to the first cluster.
3. Reassign a point only when a new center is strictly closer than its current center. Ties may be arbitrary in the nearest-center property, but the strict-improvement rule protects the termination proof.
4. If no assignment changes, stop.
5. Recompute nonempty cluster centers as centroids; set an empty cluster center to the zero vector.
6. Repeat reassignment and recomputation.

The global k-means problem is NP-hard, so Lloyd's procedure is a local-search heuristic, not an exact optimizer. Its proof of termination relies on monotonic objective decrease and finitely many assignments: centroid recomputation cannot increase the objective, strict reassignment decreases it, and there are only finitely many clusterings.

The per-iteration assignment work is:

$$
O(dkn)
$$

The per-iteration centroid recomputation work is:

$$
O(dn)
$$

The total running time for the chapter's iteration count is:

$$
O(Tdkn)
$$

Production translation: run several random initializations and keep the best objective, monitor percentage decrease as a practical stopping rule, and treat modern initialization, validation metrics, and non-Euclidean alternatives as engineering additions rather than chapter defaults.

## Weighted Majority and Multiplicative Weights

Use the deterministic online-experts model when experts predict binary outcomes before each event and the learner sees the true outcome afterward. The learner is compared against every fixed expert on every prefix, especially the best expert in hindsight.

The warm-up perfect-expert argument maintains only experts that have never erred. If a perfect expert exists, every learner mistake removes at least half the surviving experts, so the learner makes at most:

$$
\lceil \lg n \rceil
$$

For general experts, the deterministic weighted-majority algorithm is:

1. Initialize every expert weight to one.
2. On each round, sum weights on prediction one and prediction zero.
3. Predict one on a tie or when the one-weight is larger.
4. After the outcome, multiply the weights of mistaken experts by the penalty factor below and leave correct experts unchanged.

$$
1 - \gamma
$$

The chapter assumes:

$$
0 < \gamma \le \frac{1}{2}
$$

### Deterministic Mistake Bound

For every expert and every prefix, Theorem 33.4 gives the learner's mistake bound:

$$
m^{(T')} \le 2(1 + \gamma)m_i^{(T')} + \frac{2 \ln n}{\gamma}
$$

The corollary against the best expert at the final horizon is:

$$
m^{(T)} \le 2(1 + \gamma)m^* + \frac{2 \ln n}{\gamma}
$$

Do not substitute the randomized exponential-weights regret expression for the deterministic theorem. If the prompt asks for the randomized exercise, say so explicitly and switch models.

The chapter's tuned choice, when it satisfies the penalty precondition, is:

$$
\gamma = \sqrt{\frac{\ln n}{m^*}}
$$

This yields:

$$
m \le 2m^* + 4\sqrt{m^* \ln n}
$$

### Potential Proof Move

Track total weight:

$$
W(t) = \sum_i w_i^{(t)}
$$

Initially the total weight is the number of experts. When the learner makes a mistake, at least half the weight was on the wrong prediction, so the next total weight is at most:

$$
W(t)\left(1 - \frac{\gamma}{2}\right)
$$

After a prefix, expert weight gives the lower bound:

$$
W(T') \ge (1 - \gamma)^{m_i^{(T')}}
$$

The learner's mistakes give the upper bound:

$$
W(T') \le n\left(1 - \frac{\gamma}{2}\right)^{m^{(T')}}
$$

Combine the two bounds and use the chapter's logarithm inequalities:

$$
\ln(1 - x) \le -x
$$

$$
\ln(1 - x) \ge -x - x^2
$$

The second inequality is used only under the small-parameter condition:

$$
0 < x \le \frac{1}{2}
$$

The Hedge exercise uses randomized prediction proportional to weights and a different update. Its expected mistake guarantee is not the deterministic theorem:

$$
m^* + \frac{\ln n}{\epsilon} + \epsilon T
$$

## Gradient Descent and Convex Optimization

For the chapter theorem, the function is differentiable and convex, the gradient norm is bounded over the iterates, and the returned point is the average of the iterates before the final update.

The gradient descent update is:

$$
x^{(t+1)} = x^{(t)} - \gamma \nabla f(x^{(t)})
$$

The returned point is:

$$
\bar{x} = \frac{1}{T}\sum_{t=0}^{T-1} x^{(t)}
$$

The convexity proof uses the tangent inequality:

$$
f(y) \ge f(x) + \langle \nabla f(x), y - x \rangle
$$

It also uses Jensen's inequality for the average iterate:

$$
f(\bar{x}) \le \frac{1}{T}\sum_{t=0}^{T-1} f(x^{(t)})
$$

Let the initial distance to an optimum be:

$$
R = \lVert x^{(0)} - x^* \rVert
$$

Let the gradient norm bound over the iterates be:

$$
\lVert \nabla f(x^{(t)}) \rVert \le L
$$

The chapter's step size is:

$$
\gamma = \frac{R}{L\sqrt{T}}
$$

Theorem 33.8 gives:

$$
f(\bar{x}) - f(x^*) \le \frac{RL}{\sqrt{T}}
$$

For target error, the required iteration count is:

$$
T = \frac{R^2L^2}{\epsilon^2}
$$

### Amortized Potential Proof Move

Use the distance-to-optimum potential:

$$
\Phi(t) = \frac{\lVert x^{(t)} - x^* \rVert^2}{2\gamma}
$$

Define amortized progress for one step as:

$$
p(t) = f(x^{(t)}) - f(x^*) + \Phi(t+1) - \Phi(t)
$$

Expanding the squared distance after the gradient step and applying the tangent inequality bounds progress by:

$$
p(t) \le \frac{\gamma L^2}{2}
$$

Sum the bound, telescope the potential terms, drop the nonnegative final potential, and apply Jensen to move from average objective value to the objective at the average point.

If the distance and gradient bounds are unknown, line search is a step-size selection heuristic: start with a small trial step that improves the objective, double while improvement continues, then binary-search the bracket. Preserve the idea rather than overfitting to the chapter's terse notation.

## Projected Gradient Descent

For constrained optimization, the feasible set must be closed and convex, and the initial point must already be feasible. Take the ordinary gradient step, then project back to the feasible set.

The tentative update is:

$$
x'^{(t+1)} = x^{(t)} - \gamma \nabla f(x^{(t)})
$$

The projected update is:

$$
x^{(t+1)} = \Pi_K(x'^{(t+1)})
$$

The projection operator chooses a closest feasible point:

$$
\Pi_K(b') = \arg\min_{b \in K} \lVert b - b' \rVert
$$

Use the chapter's one-sided projection lemma. For any feasible comparison point, projection does not increase squared distance to that point:

$$
\lVert b - a \rVert^2 \le \lVert b' - a \rVert^2
$$

With the optimum as the feasible comparison point, this is exactly what the unconstrained potential proof needs. Theorem 33.11 therefore gives the same average-iterate guarantee as the unconstrained theorem.

## Linear Regression and Regularization

In linear regression, the data points and labels are fixed; the optimization variables are the model weights. The chapter's model includes an intercept:

$$
f(x) = w_0 + \sum_{j=1}^{n} w_j x_j
$$

The least-squares loss is:

$$
\sum_i (f(x^{(i)}) - y^{(i)})^2
$$

This loss is convex because it is a sum of squared linear functions of the weights. A gradient computation over all examples and features costs:

$$
O(nm)
$$

For approximate least squares, gradient descent may be preferable to exact matrix inversion when the iteration count and gradient cost are favorable. Route numerical-stability and normal-equation details to `matrix-operations` when the task is about solving the linear system exactly.

The chapter's regularization example constrains the weight norm:

$$
\lVert w \rVert \le B
$$

Projection onto that ball leaves an inside point unchanged. For an outside tentative weight vector, project by radial scaling:

$$
w = \frac{B}{\lVert w' \rVert}w'
$$

The norm constraint controls model complexity and overfitting. With both the initial weights and optimum inside the ball, the initial distance is on the order of the radius:

$$
R = O(B)
$$

Using the chapter exercise's gradient bound for this setting gives:

$$
L = O(B)
$$

The projected-gradient guarantee becomes:

$$
O\left(\frac{B^2}{\sqrt{T}}\right)
$$

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Calling Lloyd's procedure a global k-means solver | Say the global problem is NP-hard and Lloyd's procedure reaches a local optimum under its monotonic-decrease proof. |
| Using k-means++ or silhouette scores as if they were the chapter algorithm | Name them as production additions, not chapter defaults. |
| Reassigning tied points freely during Lloyd termination reasoning | Use the strict-improvement reassignment rule to make objective decrease well founded. |
| Giving the randomized multiplicative-weights bound for deterministic weighted majority | Use Theorem 33.4 and Corollary 33.5 unless the prompt explicitly asks for the randomized exercise or Hedge. |
| Treating the gradient norm bound as a smoothness constant | The chapter theorem uses a bound on gradient norms over iterates, plus initial distance to an optimum. |
| Returning the last gradient-descent iterate in the theorem statement | Return and analyze the average iterate. |
| Proving projected gradient descent only by citing generic nonexpansiveness | Use Lemma 33.10: projection does not increase distance to any feasible comparison point. |
| Optimizing over examples in linear regression | Optimize over weights; examples and labels define the loss. |

## Pressure Tests

Use these checks after loading this skill:

1. **Lloyd fidelity:** answer a k-means prompt and verify it mentions scaling, squared Euclidean dissimilarity, centroid optimality, nearest-center assignment, strict reassignment for termination, empty-cluster zero centers, local optimum only, and the chapter running time.
2. **Weighted-majority constants:** answer an online-experts prompt and verify the deterministic theorem uses the chapter penalty parameter, tie rule, prefix guarantee, potential, and constants rather than the randomized regret bound.
3. **Projected-gradient proof:** answer a constrained convex optimization prompt and verify the returned point is the average iterate, the proof uses the distance potential and one-sided projection lemma, and the bound depends on initial distance and gradient norm.
4. **Linear-regression regularization:** answer a least-squares prompt and verify weights are variables, the intercept appears, gradient cost is stated, and norm-ball projection plus complexity control are included.
5. **Formatting:** scan the answer for formulas in prose, headings, table cells, or inline code spans; move every expression into display blocks.
