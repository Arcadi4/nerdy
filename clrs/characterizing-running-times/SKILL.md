---
name: characterizing-running-times
description: Use when analyzing algorithm running time, asymptotic notation, Big O, Omega, Theta, little-o, little-omega, growth-rate comparisons, loop bounds, recurrence terms, or CLRS-style asymptotic exercises.
license: MIT
---

# Characterizing Running Times

## Overview

Use asymptotic notation to state the simplest precise growth bound for an algorithm or function. Always name the quantity being bounded: worst case, best case, all inputs, space, recurrence term, or another explicit quantity.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style.

## When to Use

- Analyzing algorithms, loops, recurrences, or pseudocode running time.
- Comparing growth rates: logarithms, polynomials, exponentials, factorials, iterated logarithms, and Fibonacci numbers.
- Proving or checking asymptotic claims.
- Fixing sloppy statements such as saying a lower bound is "at least Big O" or claiming an unqualified running time when only the worst case is tight.

## Core Workflow

1. **Name the case.** Say "worst-case running time," "best-case running time," or "running time for all inputs." A worst-case tight bound does not imply every input has that running time.
2. **Drop detail only after bounding.** Constants and lower-order terms vanish asymptotically, but justify the step with constants, thresholds, or known growth rules.
3. **Choose notation by claim strength.** Use O for upper bound, Omega for lower bound, Theta for tight bound, little-o for non-tight upper bound, and little-omega for non-tight lower bound.
4. **For Theta, prove both sides.** Use Theorem 3.1:

$$
f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \text{ and } f(n) = \Omega(g(n)).
$$

5. **For algorithm lower bounds, construct hard inputs.** A worst-case lower bound means: for every sufficiently large input size, at least one input of that size takes that much time.
6. **Use the simplest precise expression.** Prefer:

$$
\Theta(n^2)
$$

over:

$$
\Theta(3n^2 + 20n).
$$

Prefer Theta over O when the bound is tight.

## Notation Reference

Assume functions are asymptotically nonnegative.

**O-notation: asymptotic upper bound.** There are positive constants and a threshold such that eventually:

$$
0 \le f(n) \le c g(n).
$$

**Omega-notation: asymptotic lower bound.** There are positive constants and a threshold such that eventually:

$$
0 \le c g(n) \le f(n).
$$

**Theta-notation: tight bound.** There are positive constants and a threshold such that eventually:

$$
0 \le c_1 g(n) \le f(n) \le c_2 g(n).
$$

**little-o notation: non-tight upper bound.** For every positive constant, eventually:

$$
0 \le f(n) < c g(n).
$$

When the limit exists, this is equivalent to:

$$
\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0.
$$

**little-omega notation: non-tight lower bound.** For every positive constant, eventually:

$$
0 \le c g(n) < f(n).
$$

When the limit exists, this is equivalent to:

$$
\lim_{n \to \infty} \frac{f(n)}{g(n)} = \infty.
$$

Do not say "at least O." Say Omega for a lower bound. Do not use O when you mean a tight bound; say Theta.

## Growth-Order Ladder

For common positive functions, from slower to faster:

$$
1 < \lg^* n < \lg\lg n < \lg n < (\lg n)^k < n^\epsilon < n < n\lg n < n^a < c^n < n! < n^n
$$

where the constants satisfy:

$$
k \ge 1, \quad \epsilon > 0, \quad a > 1, \quad c > 1.
$$

Key rules:

- Changing logarithm bases changes only a constant factor.
- Any positive polynomial beats any polylogarithm:

$$
(\lg n)^k = o(n^\epsilon).
$$

- Any exponential with base greater than one beats any polynomial:

$$
n^b = o(a^n) \quad \text{for } a > 1.
$$

- Factorials beat fixed-base exponentials but are below the self-power:

$$
n! = \omega(2^n)
$$

and

$$
n! = o(n^n).
$$

- Stirling's approximation gives:

$$
\lg(n!) = \Theta(n\lg n).
$$

- Fibonacci numbers grow exponentially:

$$
F_i = \Theta(\phi^i), \quad \phi = \frac{1 + \sqrt{5}}{2}.
$$

- Floors and ceilings usually do not change polynomial growth:

$$
\lceil n \rceil^k = \Theta(n^k)
$$

and

$$
\lfloor n \rfloor^k = \Theta(n^k)
$$

for constant powers when the expressions are defined appropriately.

## Worked Pattern: Insertion Sort

Upper bound for all inputs:

- The outer loop runs:

$$
n - 1
$$

times.
- For outer index value:

$$
i,
$$

the inner loop runs at most:

$$
i - 1 \le n - 1
$$

times.
- Total inner-loop work is at most:

$$
(n - 1)(n - 1) < n^2,
$$

with constant work per iteration.
- Therefore insertion sort runs in:

$$
O(n^2)
$$

time on all inputs.

Worst-case lower bound:

- Put the largest third of the values in the first third of the array.
- After sorting, those values must move to the last third.
- Each of those values crosses at least the middle third of positions one step at a time.
- That forces:

$$
\Omega\left(\frac{n}{3} \cdot \frac{n}{3}\right) = \Omega(n^2)
$$

moves for such inputs.

Conclusion: insertion sort's worst-case running time is:

$$
\Theta(n^2),
$$

but its best-case running time is:


$$
\Theta(n).
$$

It is correct to say insertion sort runs in:

$$
O(n^2)
$$

time for all inputs, but incorrect to say its running time is:

$$
\Theta(n^2)
$$

without qualifying worst case.

## Equations and Anonymous Functions

Asymptotic notation denotes sets, but equations conventionally use equality.

Standalone right side means set membership:

$$
4n^2 + 100n + 500 = O(n^2).
$$

Inside formulas, asymptotic notation means an unnamed function in that set:

$$
2n^2 + 3n + 1 = 2n^2 + \Theta(n).
$$

Left-side notation is coarser on the right:

$$
2n^2 + \Theta(n) = \Theta(n^2).
$$

Each occurrence of asymptotic notation is a separate anonymous function unless the expression clearly binds it, for example:

$$
\sum_{i=1}^{n} O(i).
$$

## Common Mistakes

- **Mistake:** Putting quick scratch-work expressions in prose before switching to display blocks. **Fix:** Move every threshold, comparison, ratio, and bound into a display block, even if it appears only in setup or explanation.
- **Mistake:** Starting with planning paragraphs that mention formulas before the final answer. **Fix:** Start directly with the final response and put all scratch work that remains visible into display blocks.
- **Mistake:** Putting formulas in headings or inline dollar math. **Fix:** Use formula-free headings and put the expression in the next display block.
- **Mistake:** "Worst case is Theta of n squared, so the algorithm's running time is Theta of n squared." **Fix:** Say "worst-case running time" unless every input has that growth.
- **Mistake:** "An O of n log n algorithm is faster than an O of n squared algorithm." **Fix:** O is only an upper bound; compare tight Theta bounds when possible.
- **Mistake:** "At least O of n squared." **Fix:** Use Omega for lower bounds.
- **Mistake:** Ignoring negative lower-order terms too early. **Fix:** Use definitions. This expression is not bounded above by a constant multiple of n squared:

$$
\frac{n^3 - 100n^2}{n^2} = n - 100.
$$

- **Mistake:** Treating little-o like O. **Fix:** The first relation is true; the second is false:

$$
2n = o(n^2), \quad 2n^2 \ne o(n^2).
$$

- **Mistake:** Treating little-omega like Omega. **Fix:** This is tight, not little-omega:

$$
\frac{n^2/2}{n^2} = \frac{1}{2}.
$$

- **Mistake:** Misordering slow functions. **Fix:** The iterated logarithm grows slower:

$$
\lg^* n < \lg\lg n.
$$

## Quick Proof Recipes

- **Polynomial:** An asymptotically positive degree-d polynomial is:

$$
\Theta(n^d).
$$

- **O proof:** Bound every lower term by the highest-order term after a threshold, then choose one constant.
- **Omega proof:** Keep a positive fraction of the dominant term after lower-order subtractions become small enough.
- **little-o or little-omega proof:** Compute the limit of the ratio when possible; zero gives little-o and infinity gives little-omega.
- **Loop upper bound:** Bound maximum iterations per loop level and multiply or sum.
- **Loop lower bound:** Identify many operations that must happen for a family of inputs.
- **Recurrences:** Keep anonymous linear or constant terms as asymptotic blocks when exact lower-order details do not affect the asymptotic solution.
