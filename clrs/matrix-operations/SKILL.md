---
name: matrix-operations
description: Use when solving CLRS-style matrix-operation problems involving linear systems, LU or LUP decomposition, pivoting, matrix inversion, symmetric positive-definite matrices, Schur complements, least-squares approximation, normal equations, pseudoinverses, or tridiagonal systems.
license: MIT
---

# Matrix Operations

## Overview

This skill turns matrix-operation questions into method choices with visible hypotheses. The core habit is: factor once, solve with triangular systems, state the rank or definiteness condition before using a shortcut, and never treat explicit inversion as the default way to solve a linear system.

## Shared CLRS Conventions

Use the parent `clrs` skill for display-math-only formatting, theorem-precondition discipline, and CLRS answer tone. In this chapter skill, keep tables verbal; place every matrix equation, cost expression, or symbolic condition in display LaTeX blocks outside the table.

## When to Use

Use this skill for:

- solving square linear systems by Gaussian elimination, LU decomposition, or LUP decomposition;
- reusing a factorization for many right-hand sides;
- deciding whether to compute an explicit inverse;
- explaining pivoting, permutation arrays, forward substitution, or back substitution;
- proving facts about symmetric positive-definite matrices and Schur complements;
- deriving least-squares normal equations and the full-column-rank pseudoinverse;
- recognizing tridiagonal linear systems and spline-style systems from the chapter problems.

Do not use this skill as the main guide for Strassen-style matrix multiplication; route those questions to `divide-and-conquer` unless the prompt is about its equivalence with inversion.

## First Decision

| Situation | Choose | Why |
| --- | --- | --- |
| Square nonsingular system | LUP decomposition, then triangular solves | Pivoting avoids zero pivots and is the practical chapter default |
| Many right-hand sides for the same matrix | Reuse one LUP factorization | Each additional solve is quadratic; explicit inverse is not needed |
| User asks for the inverse itself | Solve one system per identity-column after LUP | The inverse is the deliverable, not a shortcut for solving |
| Matrix is known symmetric positive-definite | LU without pivoting is theoretically safe | Leading submatrices and Schur complements remain positive-definite |
| Least-squares with more observations than basis functions | Build normal equations if full column rank holds | The normal-equation matrix is symmetric positive-definite under that hypothesis |
| Rectangular, rank-deficient, or numerically delicate prompt | State the chapter limit first | Do not invent unprovided QR, SVD, or rank-revealing claims unless asked beyond the chapter |

## Linear-System Workflow

For a square system, route the answer through the factorization identity:

$$
P A = L U
$$

Use these roles:

- permutation matrix records row interchanges;
- lower-triangular factor has unit diagonal entries;
- upper-triangular factor carries the pivots;
- solve in two triangular phases after applying the permutation to the right-hand side.

For a right-hand side, solve the two displayed systems in this order:

$$
L y = P b
$$

$$
U x = y
$$

State the cost split verbally unless a display block is needed:

$$
\text{one factorization costs } \Theta(n^3)
$$

$$
\text{one triangular-solve pair costs } \Theta(n^2)
$$

### Permutation-array rule

If a permutation array is used instead of an explicit permutation matrix, the forward solve must read the permuted right-hand-side entry at each row. Use the pattern below, not an unpermuted right-hand side.

$$
y_i = b_{\pi_i} - \sum_{j=1}^{i-1} l_{ij} y_j
$$

Then back substitution proceeds downward through the upper-triangular factor:

$$
x_i = \frac{y_i - \sum_{j=i+1}^{n} u_{ij} x_j}{u_{ii}}
$$

### Pivoting rule

Plain LU decomposition is the Gaussian-elimination factorization without row swaps. It is not safe as a default because a pivot can be zero even when the full matrix is nonsingular.

LUP decomposition fixes the default failure mode by choosing a pivot of maximum absolute value in the active column and swapping that row into pivot position. If every candidate pivot in the active column is zero, the matrix is singular in the chapter algorithm.

## Explicit Inverse Decision

Do not recommend computing the inverse merely because many systems share the same coefficient matrix. The arithmetic order is not the deciding win; stability and avoiding needless inverse materialization are.

Use this rule:

- If the user asks for solutions, factor once and solve each right-hand side.
- If the user asks for the inverse matrix, compute it by solving against the columns of the identity matrix after factorization.
- If the user compares solving by inverse multiplication with LUP solves, say the chapter favors LUP solves in practice.

When the inverse is the actual deliverable, express the column solve as:

$$
A x_i = e_i
$$

The inverse columns are then assembled as:

$$
A^{-1} = \begin{bmatrix} x_1 & x_2 & \cdots & x_n \end{bmatrix}
$$

## Equivalence With Matrix Multiplication

The chapter connects matrix inversion and matrix multiplication by reductions. Preserve the message without turning inversion into a recommended solver.

Use these statements:

- A fast matrix-multiplication algorithm can speed matrix inversion asymptotically.
- A fast matrix-inversion algorithm can be used to multiply matrices asymptotically.
- This equivalence is theoretical and separate from the practical advice for solving linear systems.

If formulas are needed, put the block-matrix construction in display math and explain the reduction in prose.

## Symmetric Positive-Definite Matrices

Before using the positive-definite shortcut, state the condition:

$$
x^T A x > 0 \quad \text{for every nonzero vector } x
$$

For real matrices, a nonsingular square matrix has a symmetric positive-definite normal-equation matrix:

$$
x^T A^T A x = \lVert A x \rVert^2
$$

This is positive for every nonzero vector because nonsingularity prevents a nonzero vector from mapping to zero.

For rectangular least-squares matrices, replace nonsingularity with full column rank:

$$
\operatorname{rank}(A) = n
$$

### Schur-complement proof move

For a symmetric positive-definite matrix, leading principal submatrices are symmetric positive-definite. The Schur complement used by Gaussian elimination is also symmetric positive-definite.

Use this proof shape:

1. Partition the matrix so the first pivot is isolated.
2. Show the pivot is strictly positive from positive-definiteness.
3. Form the Schur complement after eliminating the first column.
4. Prove the Schur complement remains symmetric positive-definite by embedding a nonzero vector into the original quadratic form.
5. Induct to justify LU decomposition without pivoting.

The operational consequence is:

- all pivots are strictly positive;
- no row exchange is needed for the exact-arithmetic theorem;
- this is a theorem for symmetric positive-definite inputs, not a blanket replacement for LUP.

## Least-Squares Approximation

Start with the approximation model, then build the design matrix from basis-function evaluations.

For basis functions and coefficients, write the approximation as:

$$
F(x) = \sum_{j=1}^{n} c_j f_j(x)
$$

For data points, define the design matrix by:

$$
a_{ij} = f_j(x_i)
$$

The least-squares objective is:

$$
\min_c \lVert A c - b \rVert^2
$$

Derive the normal equations by differentiating the squared residual:

$$
A^T A c = A^T b
$$

If the columns of the design matrix are linearly independent, the normal-equation matrix is symmetric positive-definite and the full-column-rank pseudoinverse is:

$$
A^+ = (A^T A)^{-1} A^T
$$

The solution is:

$$
c = A^+ b
$$

### Least-squares method choice

For chapter-faithful answers, say this:

- form the normal equations under the full-column-rank hypothesis;
- solve the resulting symmetric positive-definite system using the chapter's LU reasoning;
- warn about overfitting when the number of basis functions matches the number of data points;
- mention only the chapter's numerical caveat unless the user asks for modern numerical-linear-algebra advice.

Do not introduce condition-number squaring, backward stability, QR decomposition, singular-value decomposition, regularization, or rank-revealing factorization as part of the default chapter answer. Those may be valid modern numerical-linear-algebra topics, but they are not the chapter-level correction this skill is meant to teach.

## Tridiagonal Systems and Splines

When a problem gives a tridiagonal system, do not default to general cubic-time elimination. The chapter problem asks for a linear-time solver that exploits the three nonzero diagonals.

Use this recognition rule:

- only the main diagonal and the adjacent diagonals are nonzero;
- elimination updates only neighboring coefficients;
- store and update the three diagonals rather than a dense matrix.

For spline-related prompts, identify the linear system generated by continuity and smoothness constraints before solving. The skill goal is the system setup and the specialized structure, not a generic polynomial-regression answer.

## Worked Pattern: Many Right-Hand Sides

When asked whether to invert once for many right-hand sides, answer in this shape:

1. State that the coefficient matrix is shared.
2. Compute one LUP decomposition.
3. For each right-hand side, include the displayed permutation-array forward-substitution equation.
4. Finish with back substitution.
5. Say explicit inversion is only for when the inverse matrix is requested.

Use the displayed systems:

$$
P A = L U
$$

$$
L y^{(k)} = P b^{(k)}
$$

$$
U x^{(k)} = y^{(k)}
$$

Include the permutation-array equation explicitly if the prompt mentions a permutation array or asks how the right-hand side is permuted:

$$
y_i^{(k)} = b_{\pi_i}^{(k)} - \sum_{j=1}^{i-1} l_{ij} y_j^{(k)}
$$

Then state the reusable-cost conclusion:

$$
\text{total cost for } m \text{ right-hand sides is } \Theta(n^3 + m n^2)
$$

Do not add a table cell containing that expression; keep it in display math as above.

Do not verbalize symbolic costs in prose as a workaround. If the response needs an asymptotic expression, put it in display math even if the same idea was already described in words.

## RED Pressure Failures This Skill Prevents

| Failure | Correct behavior |
| --- | --- |
| Recommending inverse multiplication once there are many right-hand sides | Reuse one LUP factorization and triangular solves; compute inverse only if requested |
| Forgetting the permutation in forward substitution | Read the permuted right-hand-side entry when solving the lower-triangular system |
| Claiming the permutation was handled without showing the rule | Include the displayed permutation-array forward-substitution equation |
| Treating positive-definite normal equations as the best square-system method | Acknowledge the theorem, then keep LUP as the practical square-system default |
| Claiming rectangular or rank-deficient cases are handled by LUP from this chapter | State the full-column-rank hypothesis for least squares and avoid unsupported rank-revealing claims |
| Replacing the chapter method with QR, SVD, ridge regression, or Cholesky by default | Mention only as beyond-chapter modern advice when explicitly requested |
| Leaking formulas inside prose, headings, code spans, or tables | Put every equation and symbolic cost in display math blocks |
| Putting formulas in a final self-check after obeying the main answer | Apply the parent display-math rule to the entire response, including checklists and self-checks |
| Saying symmetric positive-definite inputs can still have zero LU pivots | Preserve the theorem: the pivots are strictly positive in exact arithmetic |
| Rejecting normal equations by importing condition-number or stability theory | Use the chapter's stated practical comparison: LUP uses fewer arithmetic operations by a constant factor and has somewhat better numerical properties |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Using plain LU for an arbitrary nonsingular matrix | Use LUP unless a safe-pivot hypothesis is given |
| Saying pivoting is unnecessary because the matrix is nonsingular | Nonsingularity does not prevent a zero pivot in the current row order |
| Computing the inverse to solve ordinary systems | Factor and solve; the inverse is a separate deliverable |
| Applying symmetric positive-definite reasoning to non-square data without rank conditions | Require full column rank for the design matrix |
| Forgetting the overfitting warning in least squares | Warn when the basis count reaches the data count |
| Treating matrix multiplication equivalence as implementation advice | Keep it as an asymptotic reduction result |
| Putting expressions such as costs or normal equations in table cells | Move expressions to display blocks outside the table |
| Using formulas in a self-check table | Write self-checks in words only, or move the expression to a display block before the table |
| Saying pivoting is needed for a symmetric positive-definite matrix because a zero pivot may appear | Do not contradict the positive-pivot theorem; pivoting remains the general default for arbitrary square systems, not because symmetric positive-definite pivots are zero |
| Writing symbolic costs in words to avoid display math | Either omit the symbolic cost or put it in display math |

## Verification Pressure Tests

Use these prompts to check whether the skill changes behavior:

1. A user has one nonsingular coefficient matrix and many right-hand sides. They propose computing the inverse once. The answer must choose LUP reuse, include the displayed permutation-array forward-substitution equation, give the reusable cost in display math, avoid verbalized symbolic costs in prose, and reject inverse materialization unless the inverse is requested.
2. A user claims that because a square real matrix is nonsingular, the normal-equation matrix is symmetric positive-definite, so factoring the normal-equation matrix without pivoting must be the best square-system method. The answer must separate the true theorem from the bad practical conclusion, preserve the positive-pivot theorem for symmetric positive-definite matrices, and reject the practical conclusion using the chapter's stated comparison rather than unsupported QR, SVD, rank-revealing, condition-number, or backward-stability claims.
3. A user asks for least-squares coefficients from basis functions and sample points. The answer must construct the design matrix, derive the normal equation, state the full-column-rank condition for the pseudoinverse, warn about overfitting, and keep all formulas out of prose and tables.
4. A user gives a tridiagonal system. The answer must exploit the three-diagonal structure rather than defaulting to dense cubic-time Gaussian elimination.

## Static Checks

Before deploying or revising this skill, check:

- frontmatter has `name`, trigger-focused `description`, and `license`;
- formulas appear only in display LaTeX blocks;
- Markdown tables contain words only, not equations or symbolic costs;
- self-check tables contain words only, not equations or symbolic costs;
- headings contain no formulas;
- the parent `clrs` skill routes `matrix-operations`;
- the skill covers linear systems, LU, LUP, inverse computation, matrix-multiplication equivalence, symmetric positive-definite matrices, Schur complements, least squares, pseudoinverses, tridiagonal systems, and splines;
- source-branded labels are absent except where routing to CLRS is necessary.
