---
name: divide-and-conquer
description: Use when analyzing divide-and-conquer algorithms, solving recurrences, applying Master theorem or Akra-Bazzi, using recursion trees or substitution, comparing matrix multiplication with Strassen, or checking theorem applicability under misleading shortcuts.
license: MIT
---

# Solving Divide-and-Conquer Recurrences

## Overview

Use this skill when the hard part is choosing the correct recurrence tool, not merely simplifying algebra.

**Core principle:** identify the recurrence shape and theorem preconditions before applying a canned case. If the preconditions fail, switch methods instead of forcing the theorem.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style.

## When to Use

- An algorithm divides a problem of size $n$ into subproblems and combines their answers.
- You need a tight bound for $T(n)$ using substitution, a recursion tree, Master theorem, or Akra-Bazzi.
- A prompt suggests a shortcut such as “just use Master theorem” or “ignore the unequal split.”
- You need to compare standard recursive matrix multiplication with Strassen’s algorithm.

Do **not** use this skill for nonrecursive loop counting unless a recurrence is the central model.

## Method Selection

| Recurrence shape | First method to try | Watch for |
| --- | --- | --- |
| $T(n)=aT(n/b)+f(n)$ | Master theorem | Polynomial separation and regularity |
| Unequal subproblems, such as $T(n/3)+T(2n/3)+f(n)$ | Akra-Bazzi or recursion tree | Classical Master theorem does not apply |
| Nonstandard argument, such as $T(\sqrt n)$ | Change variables first | Apply Master theorem to the new variable |
| Bound proof requested | Substitution | Use explicit constants, not asymptotic notation in the inductive hypothesis |
| Matrix multiplication recurrence | Master theorem or recursion tree | Branching factor drives the exponent |

## Master Theorem Checklist

For $T(n)=aT(n/b)+f(n)$ with $a>0$ and $b>1$, compare $f(n)$ to the watershed $n^{\log_b a}$.

1. If $f(n)=O(n^{\log_b a-\epsilon})$ for some $\epsilon>0$, then $T(n)=\Theta(n^{\log_b a})$.
2. If $f(n)=\Theta(n^{\log_b a}\lg^k n)$ for constant $k\ge0$, then $T(n)=\Theta(n^{\log_b a}\lg^{k+1}n)$.
3. If $f(n)=\Omega(n^{\log_b a+\epsilon})$ for some $\epsilon>0$ and $af(n/b)\le cf(n)$ for some $c<1$ and sufficiently large $n$, then $T(n)=\Theta(f(n))$.

If none of these fits, say so. Example gap: $T(n)=2T(n/2)+n/\lg n$ is not standard Case $1$ or Case $2$; a recursion tree gives $T(n)=\Theta(n\lg\lg n)$.

## Recursion Trees

At each depth, compute both node count and subproblem size. Sum work per level, then sum levels. For unequal splits, never estimate leaves by pretending the deepest level is a full tree.

Example: $T(n)=T(n/3)+T(2n/3)+\Theta(n)$ has total internal work $\Theta(n)$ per active level and height $\Theta(\lg n)$, so $T(n)=\Theta(n\lg n)$. The leaf count is only $O(n)$, not $n^{\log_{3/2}2}$.

## Substitution Proofs

Use explicit constants in the inductive hypothesis.

Good: assume $T(m)\le cm\lg m$ for all $m<n$.

Bad: assume $T(m)=O(m\lg m)$ inside the proof.

If a tight guess almost closes but misses by a lower-order term, strengthen it. For example, try $T(n)\le cn-d$ instead of only $T(n)\le cn$ when constant work accumulates across branches.

## Akra-Bazzi

For recurrences of the form

$$
T(n)=f(n)+\sum_{i=1}^{k}a_iT(n/b_i),
$$

find $p$ such that

$$
\sum_{i=1}^{k}\frac{a_i}{b_i^p}=1.
$$

Then

$$
T(n)=\Theta\left(n^p\left(1+\int_1^n\frac{f(x)}{x^{p+1}}\,dx\right)\right).
$$

For $T(n)=T(n/5)+T(7n/10)+n$, the root $p$ lies between $0$ and $1$, and the integral yields $T(n)=\Theta(n)$.

## Worked Example: Change Variables

Solve $T(n)=2T(\sqrt n)+\Theta(\lg n)$.

Let $m=\lg n$ and $S(m)=T(2^m)$. Then $\sqrt n=2^{m/2}$, so

$$
S(m)=2S(m/2)+\Theta(m).
$$

Master theorem Case $2$ gives $S(m)=\Theta(m\lg m)$. Substitute back $m=\lg n$:

$$
T(n)=\Theta(\lg n\lg\lg n).
$$

## Matrix Multiplication Reference

Standard multiplication computes

$$
c_{ij}=\sum_{k=1}^{n}a_{ik}b_{kj}
$$

in $\Theta(n^3)$ time. The accumulator-style recursive version has recurrence $T(n)=8T(n/2)+\Theta(1)$ and solves to $\Theta(n^3)$; a block formula that explicitly adds submatrix products instead uses $T(n)=8T(n/2)+\Theta(n^2)$, which also solves to $\Theta(n^3)$.

Strassen reduces recursive multiplications from $8$ to $7$:

$$
T(n)=7T(n/2)+\Theta(n^2)=\Theta(n^{\lg 7}).
$$

Use these Strassen helper definitions:

$$
\begin{aligned}
S_1&=B_{12}-B_{22} & S_2&=A_{11}+A_{12} & S_3&=A_{21}+A_{22} & S_4&=B_{21}-B_{11} \\
S_5&=A_{11}+A_{22} & S_6&=B_{11}+B_{22} & S_7&=A_{12}-A_{22} & S_8&=B_{21}+B_{22} \\
S_9&=A_{11}-A_{21} & S_{10}&=B_{11}+B_{12}
\end{aligned}
$$

$$
\begin{aligned}
P_1&=A_{11}S_1 & P_2&=S_2B_{22} & P_3&=S_3B_{11} & P_4&=A_{22}S_4 \\
P_5&=S_5S_6 & P_6&=S_7S_8 & P_7&=S_9S_{10}
\end{aligned}
$$

$$
\begin{aligned}
C_{11}&=C_{11}+P_5+P_4-P_2+P_6 \\
C_{12}&=C_{12}+P_1+P_2 \\
C_{21}&=C_{21}+P_3+P_4 \\
C_{22}&=C_{22}+P_5+P_1-P_3-P_7
\end{aligned}
$$

Per non-base recursive call, there are $18$ submatrix additions/subtractions: $10$ for the $S_i$ matrices and $8$ for combining the $C_{ij}$ blocks.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Applying classical Master theorem to unequal splits | Use recursion trees or Akra-Bazzi |
| Treating $n/\lg n$ as Master Case $2$ with $k=-1$ | Standard Case $2$ requires $k\ge0$; use a recursion tree |
| Using $T(n)=O(g(n))$ as an inductive hypothesis | State $T(n)\le cg(n)$ and solve constants |
| Counting the deepest unequal-split level as full | Track which branches have already terminated |
| Assuming floors and ceilings change the asymptotic answer | Usually ignore them after confirming an algorithmic base case and polynomial-growth driving term |
| Thinking Strassen is faster because combining is cheaper | It is faster because the branching exponent drops from $3$ to $\lg 7$ |
