---
name: clrs
description: Use when working with CLRS, Introduction to Algorithms by Cormen, Leiserson, Rivest, and Stein, including algorithm design, data structures, asymptotic analysis, recurrences, proof style, or textbook-grounded algorithm explanations.
license: MIT
---

# Introduction to Algorithms

## When to Use

Use this skill when you need to understand, implement, or analyze an algorithm-intensive problem, choose an algorithmic technique, reason about a sophisticated data structure, or answer a CLRS-style exercise.

## CLRS Skill Selection

1. Identify the problem being solved and the CLRS concept it most closely matches.
2. If the user mentions a chapter topic directly, load the matching chapter skill.
3. If the topic is inferred rather than named, map the problem to likely CLRS techniques before choosing a chapter skill.
4. Use chapter skills for chapter-specific facts, examples, theorem details, and common traps.
5. Keep the index skill for shared CLRS answer style and routing; do not store chapter-specific algorithms or theorem catalogs here.

Current chapter skills:

- `characterizing-running-times`: asymptotic notation, running-time bounds, growth-rate comparisons, and loop-bound reasoning.
- `divide-and-conquer`: recurrences, recursion trees, substitution, Master theorem, Akra-Bazzi, and divide-and-conquer matrix multiplication.
- `probabilistic-analysis-and-randomized-algorithms`: probabilistic analysis, indicator random variables, randomized algorithms, random permutations, balls-and-bins, birthday paradox, streaks, and online hiring.
- `sorting-and-order-statistics`: heaps, priority queues, sorting choice, stability, linear-time sorting preconditions, selection, medians, quantiles, and top-k decisions.

## Mathematical Formatting

Always put mathematical expressions in display LaTeX blocks. Do not put formulas in inline code spans, inline math, or plain prose. Notation names such as O-notation, Theta-notation, or little-omega can appear in prose, but any expression, inequality, limit, recurrence, or growth comparison must be displayed as a block.

This applies to the entire response, including headings, scratch work, examples, thresholds, ratios, and explanatory narration. If a sentence would contain symbols such as variables, powers, inequalities, limits, or fractions, split the expression into a display block and refer to it from prose as "the expression above" or "the bound below." Do not leak scratch-work formulas in prose before the polished answer.

Start directly with the polished answer. Do not include planning paragraphs, scratch-work narration, or "I am checking" preambles; those are common places where formulas accidentally escape display blocks.

Never place formulas in Markdown headings. Use prose headings such as "First claim" or "Little-o check," then put the formula below the heading in a display block.

Forbidden patterns:

- A heading that embeds a formula.
- A prose sentence that embeds a ratio, limit, threshold, recurrence, or asymptotic relation.
- An inline code span that contains a formula or inequality.

Safe pattern:

```markdown
## First claim

The claim is true.

$$
\frac{f(n)}{g(n)} \to 0
$$

Therefore the first expression is little-o of the second expression.
```

## General CLRS Conventions

- State which case, model, or quantity is being analyzed before giving a bound or theorem result.
- Ground answers in CLRS terminology and theorem names when relevant; cite theorem numbers when the chapter skill provides them.
- Check theorem preconditions before applying a named result.
- Prefer precise tight bounds when justified, and say when only an upper or lower bound has been shown.
- Keep chapter-specific worked examples, algorithms, proof recipes, and common mistakes in the relevant chapter skill.
