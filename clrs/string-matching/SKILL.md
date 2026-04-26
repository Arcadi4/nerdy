---
name: string-matching
description: Use when solving exact pattern search, rolling-hash matching, finite-automaton matching, KMP prefix-function problems, suffix-array queries, LCP-array tasks, longest repeated/common substring problems, cyclic rotation tests, or Burrows-Wheeler transform exercises.
license: MIT
---

# String Matching

## Overview

String matching is about preserving information from previous character comparisons. The right method depends on whether the text is scanned once, patterns repeat, hashes are acceptable as filters, a full automaton is affordable, or the corpus should be indexed for many later queries.

**Core principle:** choose the matcher by workload and model assumptions, then state the invariant that makes skipped comparisons safe.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style. Keep string indices, costs, recurrences, and asymptotic bounds in display LaTeX blocks rather than inline prose.

When a table needs a cost or formula, keep the cell verbal and place the expression in a display block nearby.

For pressure-test answers, treat concrete assignments and indexed values as formulas too. Do not write prefix-function updates, array entries, or length equalities inline; introduce them in prose and put the symbolic expression in a display block.

## When to Use

- A prompt asks for exact pattern occurrences, valid shifts, overlaps, string-matching automata, Rabin-Karp, KMP, suffix arrays, LCP arrays, cyclic rotations, or Burrows-Wheeler transforms.
- You need to compare naive matching, rolling hashes, finite automata, KMP, and suffix-array indexing under a workload constraint.
- A proof asks why a shift is safe after a mismatch, why automaton states mean longest matched prefixes, or why suffix-array matches form a consecutive block.
- A production question involves collision risk, adversarial text, large alphabets, static corpora, many pattern queries, or reuse of learned comparisons.

Do **not** use this skill for approximate matching, edit distance, regular-expression engines, suffix trees, tries, or general dynamic programming unless exact substring search is the core issue.

## String-Matching Model

Name the text, pattern, alphabet, and valid shift before choosing an algorithm.

$$
T[1:n]
$$

$$
P[1:m]
$$

A shift is valid exactly when the pattern equals the length-m substring beginning at the next text position after the shift.

$$
P[1:m] = T[s+1:s+m]
$$

Use these conventions consistently:

- The empty string is the string with length zero.
- A prefix or suffix may be the whole string unless the prompt says proper.
- The prefix-function value for a pattern prefix is the longest proper prefix of the whole pattern that is also a suffix of that prefix.
- Equality of strings is not free in an implementation. It can inspect characters until the first mismatch.

Proofs often rely on the overlapping-suffix move: if two strings are suffixes of the same string, the shorter one is a suffix of the longer one; if their lengths are equal, they are equal.

## Algorithm Selection Checklist

Start with the workload, not the algorithm name.

| Workload or constraint | Prefer | Watch for |
| --- | --- | --- |
| One short pattern and tiny text | Naive matching | Worst cases with repeated characters |
| Exact single-pattern search in a long text | KMP | Preserve overlaps after a full match |
| Many patterns or two-dimensional rolling windows | Rabin-Karp as a filter | Hash matches require verification |
| Fixed pattern and small alphabet with repeated scans | String-matching automaton | Transition table can be too large |
| Mostly static corpus and many later pattern queries | Suffix array, plus LCP array when structural substring queries are needed | Build cost and comparison cost during queries |
| Longest repeated substring or longest common substring | Suffix array plus required LCP array | Separator handling and document-origin checks |

Canonical chapter costs:

$$
\text{naive matching time} = O((n-m+1)m)
$$

$$
\text{Rabin-Karp preprocessing time} = \Theta(m)
$$

$$
\text{Rabin-Karp worst-case matching time} = O((n-m+1)m)
$$

$$
\text{finite-automaton preprocessing time} = O(m|\Sigma|)
$$

$$
\text{finite-automaton matching time} = \Theta(n)
$$

$$
\text{KMP preprocessing time} = \Theta(m)
$$

$$
\text{KMP matching time} = \Theta(n)
$$

$$
\text{suffix-array preprocessing time} = O(n\lg n)
$$

$$
\text{suffix-array query time for k occurrences} = O(m\lg n + km)
$$

## Naive Matching

Use naive matching as the baseline: slide the pattern over every possible shift and compare characters until mismatch or full match.

It is acceptable when the text is small, the pattern is tiny, or implementation simplicity matters more than worst-case guarantees. It is not a good explanation for long adversarial texts because it forgets every comparison made at the previous shift.

Worst-case tightness example:

$$
T = a^n
$$

$$
P = a^m
$$

Every shift compares the whole pattern.

Pressure traps:

- If all pattern characters are distinct, a mismatch after several characters allows a larger safe shift; do not blindly report the generic worst-case bound as inevitable.
- For random strings, expected comparisons can be small; state the random model before claiming it.
- Patterns with gap characters are not ordinary exact strings; use dynamic programming or automaton-style state expansion rather than plain naive matching.

## Rabin-Karp Rolling Hashes

Rabin-Karp treats each pattern-length window as a radix-number fingerprint and updates the text-window hash by removing the outgoing character and adding the incoming character.

Precompute the high-order radix power used by the rolling recurrence.

$$
h = d^{m-1} \bmod q
$$

Use Horner's rule to hash the pattern and first text window, then roll the text hash with the recurrence below.

$$
t_{s+1} = (d(t_s - T[s+1]h) + T[s+m+1]) \bmod q
$$

Correctness rule:

1. If the hashes differ, reject the shift.
2. If the hashes match, verify the substring character by character.
3. Report a match only after exact verification.

Do not let a production answer say that rare collisions make verification unnecessary. A hash match is a candidate, not a proof. Skipping verification turns exact matching into a probabilistic false-positive algorithm.

Parameter and model assumptions:

- Choose a modulus that keeps arithmetic in a machine word while reducing spurious hits.
- A prime modulus supports the standard random-modulo analysis and avoids many systematic collision patterns.
- The radix should represent the alphabet encoding used by the windows.
- The good expected behavior assumes relatively few valid shifts and spurious hits; adversarial collisions can return the method to the naive worst case.

Use Rabin-Karp when the rolling hash is the reusable idea: many patterns, two-dimensional matching, plagiarism-style filtering, or randomized file equality via polynomial evaluation. For a single exact pattern under adversarial input, prefer KMP or a library matcher with worst-case protection.

## String-Matching Automata

A string-matching automaton encodes, after each scanned character, the length of the longest prefix of the pattern that is a suffix of the text seen so far.

The suffix function maps any scanned string to that length.

$$
\sigma(x) = \max\{k : P[1:k] \text{ is a suffix of } x\}
$$

The transition from state `q` on character `a` is defined by appending that character to the matched prefix and applying the suffix function.

$$
\delta(q,a) = \sigma(P[1:q]a)
$$

Matching invariant:

$$
q = \sigma(T[1:i])
$$

This means the current state is exactly the amount of pattern prefix matched by a suffix of the text prefix already read.

Proof moves to cite:

- Appending one character can increase the suffix-function value by at most one.
- If the current state is already the suffix-function value for the scanned text, the next state can be computed from the matched prefix plus the new character.
- Induct over scanned text positions to prove the automaton state equals the suffix-function value.

Production warning: a dense transition table is attractive for small alphabets but expensive for byte-heavy, Unicode, token, or sparse alphabets. Do not build a full table merely to get linear scanning if KMP gives the same scan bound with linear pattern storage.

The straightforward transition computation is pedagogical and can be too slow.

$$
O(m^3|\Sigma|)
$$

With the prefix-function idea, the transition table can be constructed within the smaller preprocessing bound below.

$$
O(m|\Sigma|)
$$

## KMP Prefix Function

KMP is the default exact matcher for one pattern in one long text when worst-case linear time matters and building a full alphabet table is unnecessary.

The prefix-function value for a prefix ending at position `q` is the length of the longest proper prefix of the pattern that is also a suffix of that prefix.

$$
\pi[q] = \max\{k : k < q \text{ and } P[1:k] \text{ is a suffix of } P[1:q]\}
$$

What a fallback preserves:

- If `q` pattern characters matched and the next character mismatches, the first reusable candidate is the longest border of the matched pattern prefix.
- Shifting by the difference between the matched length and that border keeps a known suffix aligned with the same prefix.
- Repeated fallback through prefix-function links enumerates all border lengths in decreasing order.

The safe shift after a mismatch is governed by the expression below.

$$
q - \pi[q]
$$

Computing the prefix function is linear by aggregate analysis: the candidate border length increases only by successful character matches and decreases only by following prefix links.

KMP matching invariant:

$$
q = \text{length of the longest prefix of } P \text{ that is a suffix of } T[1:i]
$$

After reporting a full match, do not reset to zero unless the prefix function says zero. Set the matched length to the prefix-function value of the full pattern so overlapping matches are preserved and the algorithm does not attempt to read beyond the end of the pattern.

$$
q = \pi[m]
$$

Common indexing hazard: many programming explanations use zero-based arrays and write the value after a match as the prefix value at the last array index. In a CLRS-style answer, state the convention first and keep the update above for the one-based pattern-length convention.

Reusable exercises and patterns:

- Cyclic rotation: search one string inside the other string doubled, after checking equal lengths.
- Improved prefix values: skip fallback states that would compare the same mismatching character again.
- Automaton from prefix function: when the direct next character fails, reuse the transition of the prefix-link state.

## Suffix Arrays and LCP Arrays

Use a suffix array when the text is mostly static and many later queries or substring-structure tasks justify indexing the text rather than preprocessing each pattern. Add the LCP array when the workload includes longest repeated substring, longest common substring, or other adjacent-suffix common-prefix queries; the suffix array orders the suffixes, while the LCP array supplies the common-prefix lengths that make those tasks direct.

The suffix array lists suffix start positions in lexicographic order. The rank array is its inverse. The LCP array stores the longest common prefix length between adjacent suffixes in suffix-array order.

Pattern-search rule:

1. Binary-search the suffix array for the first suffix whose prefix is not lexicographically less than the pattern.
2. Binary-search for the first suffix after the matching block.
3. Report the start positions in that consecutive block.

All occurrences are consecutive because every suffix beginning with the pattern lies in the lexicographic interval whose strings share that prefix. A suffix outside that interval is either smaller before the pattern is exhausted or larger before the pattern is exhausted.

The basic query bound includes both binary-search comparisons and output verification or extraction for each occurrence.

$$
O(m\lg n + km)
$$

LCP uses:

- Longest repeated substring: take the largest adjacent LCP value.
- Longest common substring of two texts: build one suffix array for the two texts separated by a sentinel not appearing in either text, then take the largest adjacent LCP whose two suffixes originate in different documents.
- Linear LCP construction: scan suffixes in text order using the rank array and reuse the fact that dropping the first character reduces the next relevant common-prefix length by at most one.

Doubling construction pattern:

1. Rank suffixes by the first character.
2. Repeatedly sort suffixes by the pair consisting of the current left-rank and the current right-rank.
3. Double the represented prefix length after each ranking pass.
4. Use counting or radix sort when ranks are integer keys.

The standard doubling construction gives the bound below.

$$
\Theta(n\lg n)
$$

Burrows-Wheeler transform tasks are suffix-array-adjacent. The transform records the character preceding each sorted rotation or suffix-style row; inversion relies on stable ranks of equal characters to map last-column positions back to first-column positions.

## Proof Recipes

### Suffix-function or automaton correctness

1. State what the current state means as a longest pattern prefix that is also a suffix of the scanned text.
2. Use the overlapping-suffix lemma to show that shorter candidates are nested inside longer suffixes.
3. Show that appending one character changes the candidate set exactly as the transition definition says.
4. Induct over scanned text positions.
5. Report exactly when the state reaches the accepting state.

### KMP correctness

1. State the matched-length invariant before processing the next text character.
2. On mismatch, follow prefix links until the next candidate prefix can accept the character or no candidate remains.
3. Argue that skipped shifts cannot be valid because their required prefix length is not a border of the matched prefix.
4. On match, increase the matched length by one.
5. On a full match, report the shift and fall back to the full-pattern border to preserve overlaps.

### Suffix-array query correctness

1. Compare the pattern only against prefixes of sorted suffixes.
2. Identify the lexicographic lower and upper boundaries of suffixes beginning with the pattern.
3. Use the consecutive-interval property to justify reporting exactly that block.
4. Include the cost of comparing the pattern during binary search and the cost of returning every occurrence.

## RED Pressure Failures This Skill Prevents

- Treating Rabin-Karp hash equality as exact equality and skipping substring verification.
- Claiming Rabin-Karp has unconditional linear worst-case matching time.
- Writing cost expressions inline in tables or prose, violating the parent CLRS formatting rule.
- Resetting KMP to zero after a full match and missing overlaps.
- Mixing zero-based prefix-array conventions with the CLRS matched-length update without explaining the convention.
- Recommending a full finite-automaton transition table for a large alphabet without a memory warning.
- Saying suffix-array search is only logarithmic while omitting pattern comparison and output costs.
- Explaining LCP arrays as optional metadata but forgetting longest repeated substring and longest common substring uses.

## GREEN Behaviors This Skill Enables

- Selects the matcher from workload facts: one pattern, many patterns, fixed pattern, static corpus, structural substring query, alphabet size, and adversarial risk.
- Gives Rabin-Karp as a candidate filter, verifies every hash hit for exact search, and names the expected-hit assumption before using expected performance.
- Explains automaton matching through the suffix-function state invariant, then checks whether the transition table is affordable for the alphabet.
- Uses KMP prefix links to preserve the longest reusable border after a mismatch and falls back to the full-pattern border after reporting a match.
- Handles overlapping occurrences explicitly instead of relying on a reset or a library call.
- Chooses suffix arrays with required LCP support for static-corpus queries that include longest repeated substring or longest common substring.
- Includes output-sensitive suffix-array query cost and explains why all matching suffixes form one consecutive lexicographic interval.
- Keeps all costs, recurrences, prefix-function updates, and indexed examples in display math blocks under the parent CLRS style.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Choosing by favorite algorithm | Choose by workload: one pattern, many patterns, fixed pattern, or indexed corpus |
| Calling rolling hashes exact | Hashes filter candidates; exact search still verifies matching windows |
| Ignoring adversarial collisions | State the expected-hit model and worst-case fallback |
| Forgetting overlap handling | After a KMP report, fall back to the full-pattern border |
| Overbuilding automata | Dense transition tables need alphabet-size and memory justification |
| Treating suffix arrays as just search | Use LCP for repeated and common substring structure |
| Losing CLRS style | Put formulas and costs in display blocks, not inline prose or table cells |

## Verification Pressure Tests

Use these tests when validating an answer or revising this skill:

1. **KMP overlap test:** Given a pattern with a nonzero full-pattern border, require the report action and the next matched length under the CLRS convention. The answer must preserve overlaps.
2. **Rolling-hash safety test:** Ask whether verification can be skipped after a hash match. The answer must reject that for exact matching, explain spurious hits, state the expected model, and preserve the worst-case bound.
3. **Automaton memory test:** Ask for finite-automaton matching over a large alphabet. The answer must mention the state meaning, transition definition, and transition-table cost before recommending it.
4. **Suffix-array workload test:** Ask for many pattern queries plus longest repeated substring and longest common substring on a static corpus. The answer must choose suffix arrays with LCP, explain consecutive occurrence blocks, and include output-sensitive query cost.
5. **Parent-format test:** Ask for a comparison table. The answer must keep formulas out of table cells and place costs in display blocks.
6. **Inline-assignment test:** Ask for a KMP example with a concrete border length. The answer must put the concrete prefix-function value and the post-match update in display blocks rather than writing them inline.
