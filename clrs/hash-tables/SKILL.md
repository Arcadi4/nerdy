---
name: hash-tables
description: Use when choosing, analyzing, or implementing hash tables, direct addressing, chaining, open addressing, universal hashing, load factors, probe bounds, deletion behavior, or cache-aware dictionary design under practical engineering constraints.
license: MIT
---

# Hash Tables

## Overview

Hash tables are not magic constant-time dictionaries. The core move is to separate the address calculation, collision policy, load-factor budget, and adversarial model, then choose the weakest mechanism that keeps expected probes, memory movement, deletion behavior, and cache locality within the real service constraints.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style.

## When to Use

- A prompt involves dictionaries, symbol tables, direct addressing, hash tables, hash functions, collision resolution, chaining, open addressing, double hashing, linear probing, tombstones, load factor, or universal hashing.
- You need to translate expected-time hashing assumptions into production capacity planning, p99 latency, adversarial-input defense, or memory-hierarchy behavior.
- A proposed design relies on expected constant time and you must state the hashing assumptions that make the claim meaningful.
- Keys are integers, byte strings, vectors, identifiers, request parameters, or user-controlled data whose distribution may matter.

Do **not** use this skill merely because a platform dictionary exists. Use the language or database default unless algorithm choice, attack resistance, resizing behavior, deletion semantics, or cache locality is the actual question.

## First Decision: What Problem Are You Really Solving?

| Need | Prefer | Why |
| --- | --- | --- |
| Dense small universe with no huge gaps | Direct addressing or bit vector | Worst-case constant lookup is paid for by allocating the whole universe |
| Sparse universe with dynamic inserts and deletes | Hash table | Compresses the address space to live keys while keeping expected constant operations |
| Frequent deletes and simple stable performance | Chaining, or open addressing with explicit cleanup policy | Deletion is straightforward for chaining; tombstones in open addressing accumulate |
| Cache-sensitive high-throughput table | Open addressing, often linear-probing-family designs at conservative load | Avoids pointers and probes contiguous cache blocks |
| Unknown or adversarial keys | Randomized or keyed hash family | Fixed static functions can be collision-targeted |
| Static set with only search | Consider sorted array, perfect hashing, or open addressing with extra capacity | Preprocessing can buy simpler worst-case lookup behavior |
| Variable-length byte strings | A string hash or keyed/cryptographic-inspired mixer plus a collision strategy | Division and word multiply-shift are integer-key building blocks, not complete string-table designs |

Before accepting a hash-table proposal, ask:

1. Are keys dense enough for direct addressing, or is the universe much larger than live keys?
2. Is the workload dominated by hits, misses, inserts, deletes, iteration, or resizing?
3. Is the input trusted, random-looking, structured, or adversarial?
4. Is p99 latency driven by probes, cache misses, pointer chasing, memory bandwidth, or hash computation?
5. Can the table rebuild or rehash, and what is the maximum live plus tombstone occupancy before it must do so?

## Direct Addressing Mindset

Direct addressing teaches the ideal dictionary: one key, one slot, worst-case constant operations. It is production-aligned only when the key universe is genuinely small or compact after remapping.

Use direct addressing when the allocation cost is proportional to the real domain you must cover anyway, such as small enum IDs, file descriptors within a fixed bound, bitsets for membership, or dense remapped IDs.

Do not allocate a huge direct-address table just because lookup would be constant. If initialization is the blocker, use the sparse-table trick: keep a compact stack/list of initialized keys and validate a slot by checking that its back-pointer/index agrees with the compact list. The deeper lesson is lazy validity, not huge zero-filled memory.

## Load Factor and Expected Cost Reference

The load factor is the average occupancy per table slot:

$$
\alpha = \frac{n}{m}
$$

For chaining, the value above may exceed one. For open addressing, at most one element occupies a slot, so it must stay below one for the standard bounds.

| Scheme | Assumptions | Cost label | Planning consequence |
| --- | --- | --- | --- |
| Chaining, unsuccessful search | Independent uniform hashing, constant hash computation | Expected chain scan | Misses scan one expected chain; high load grows roughly linearly |
| Chaining, successful search | Same, searched element uniformly among stored elements | Expected stored-element scan | Longer chains are sampled more often; still constant when load is bounded |
| Open addressing, unsuccessful search or insert | Simple uniform hashing for probe sequences, no deletions, load below full | Miss or insert probe bound | Misses and inserts explode as the table fills |
| Open addressing, successful search | Same, searched key uniformly among stored keys | Hit probe bound | Hits rise more slowly than misses, but still require headroom |

Reference bounds:

- Chaining unsuccessful search and successful search are expected constant time when the load factor is bounded. The cost form is:

$$
\Theta(1 + \alpha)
$$

- Open addressing unsuccessful search and insertion are bounded by:

$$
\frac{1}{1 - \alpha}
$$

- Open addressing successful search is bounded by:

$$
\frac{1}{\alpha}\ln\frac{1}{1 - \alpha}
$$

Use the miss or insert bound for capacity planning when misses, upserts, cache lookups, dedupe checks, or negative membership tests matter. Successful-search averages are not enough for p99 planning.

## Hash Function Mindset

Independent uniform hashing is the ideal model for chaining, and simple uniform hashing is the ideal model for open-address probe sequences. Real implementations approximate these models. Always say where the randomness comes from.

| Hashing approach | Use when | Trap |
| --- | --- | --- |
| Division method | Educational integer examples or carefully chosen non-patterned table sizes | A fixed modulus can preserve key patterns; prime sizing may fight practical resizing |
| Multiplication or multiply-shift | Fast fixed-width integer mixing, especially with power-of-two table sizes | A fixed constant gives no adversarial guarantee by itself |
| Universal hashing | You need a theorem against any fixed key set | The guarantee is over a randomly chosen function family, not any one static function |
| Random odd multiply-shift | Fast practical integer hashing with bounded collision probability | The chapter's bound is approximate-universal, not a full random oracle |
| Cryptographic or keyed hashing | User-controlled keys, hash-flooding risk, or variable-length strings needing robust mixing | It may cost more CPU; on modern hardware this can still be cheaper than random memory misses |
| String or vector hashing | Variable-length byte strings or identifiers | First reduce the byte sequence with a sound mixer; do not treat a long string as a single machine word |

Industrial rule: a fast weak hash can make the table's asymptotics irrelevant under structured or hostile input. A slower robust hash can win when measurements or threat models show that it prevents long probe chains, cache misses, or attack-driven collision storms.

## Randomization and Universality

Universal hashing prevents a fixed adversarial key set from forcing the same bad collisions every run. The family matters more than the individual textbook formula.

| Property | Meaning for answers |
| --- | --- |
| Uniform | A fixed key is equally likely to land in any slot over the random choice of hash function |
| Universal | Any two distinct keys collide with probability at most the reciprocal of the table size |
| Approximately universal | Collision probability is within a constant factor of the universal target |
| Independent | Several keys jointly behave like independent random slot choices |

Do not say universal hashing means a static function can be chosen once and forgotten under adversarial workloads. In a long-running service, the practical analogue is a secret per-process or per-table seed, monitored collision behavior, and rehashing if the distribution becomes pathological.

## Collision Strategy Decision Table

| Strategy | Strength | Weakness | Production translation |
| --- | --- | --- | --- |
| Chaining | Simple deletion, load may exceed one, robust under growing buckets | Pointer chasing and allocation hurt cache locality; worst chain can be long | Good baseline for frequent deletes or external storage, but use compact buckets or tree/fallback defenses in hostile settings |
| Open addressing | Stores elements in the table, avoids pointers, often cache-friendly | Cannot exceed full occupancy; deletion and clustering are delicate | Use low load thresholds, resizing, tombstone cleanup, and measured probe distributions |
| Double hashing | Many probe sequences and less primary clustering than linear probing | More random memory access and step-size constraints | Good theoretical open-addressing default when cache locality is not the only concern |
| Linear probing | Excellent locality; deletion can be done by shifting within clusters | Primary clustering; needs stronger hash independence and conservative load | Often fastest in memory hierarchies when paired with a strong keyed hash and rebuild policy |

Treat collision strategy and hash function as separate axes. A cache-friendly probing strategy cannot rescue a hash that maps many real keys to the same neighborhood; a strong hash cannot rescue an overfull table with unbounded tombstones.

## Static Sets and Perfect Hashing

Perfect hashing is the right answer when the key set is fixed and lookups dominate. The mindset is different from a dynamic dictionary: spend randomized preprocessing to remove collision work from future searches.

Use this idea when all of these are true:

1. the set of keys is known before queries begin,
2. insertions and deletions are absent or handled by rebuilding,
3. lookup latency predictability matters more than update flexibility,
4. the implementation can afford build-time retries and extra metadata.

The two-level construction uses a first-level universal hash to place keys into buckets, then gives each bucket its own second-level table and randomly chosen hash function. The first level controls the sum of squared bucket sizes; the second level retries until that bucket has no collisions. The operational lesson is to isolate collision risk locally instead of overbuilding the entire table for the worst bucket.

In production, do not hand-roll textbook perfect hashing just because a set is static. Compare it with a sorted array, generated minimal-perfect-hash library, trie/FST, database index, or ordinary hash table. Choose perfect hashing when the build pipeline is controlled and the saved lookup variance or memory layout justifies the preprocessing complexity.

## Deletion Discipline

Chaining deletion is conceptually simple when the deletion operation receives a pointer or handle to the stored object; doubly linked lists make that constant time. If deletion receives only a key, the search cost still applies.

Open addressing deletion is not simply setting a slot to empty. A search stops at an empty slot, so clearing a slot can make later keys unreachable. The textbook tombstone value preserves probe chains, but tombstones make the table act fuller over time. For frequent deletes, require at least one of these policies:

1. periodic rebuild when tombstone count crosses a threshold,
2. resize or rehash based on live plus deleted occupancy,
3. a probing scheme with valid backward-shift deletion, such as linear probing,
4. a different table design if delete-heavy p99 latency is the priority.

For linear probing, the deletion lesson is an invariant: after removing a slot, shift forward keys backward only when the vacated slot lies earlier in that key's probe sequence than its current location. Preserve reachability, not merely compactness.

## Memory-Hierarchy Guidance

The RAM-model probe count is only a proxy. In real systems, a random cache miss can dominate several arithmetic or mixing operations.

- Chaining may have good expected comparison counts but poor locality because nodes and buckets can live in different cache lines.
- Open addressing uses contiguous table storage and often wins despite theoretical clustering concerns.
- Linear probing's primary clustering is bad in the RAM model but can be beneficial for cache-block locality when load is controlled.
- Complex hash functions may be acceptable if they run in registers and prevent expensive random-memory probe chains.

When p99 matters, monitor probe lengths, cluster lengths, rebuild frequency, resize latency, and hash-flooding indicators. Do not plan only from average successful lookup cost.

## One Practical Design Pattern

For a high-throughput in-memory dictionary with fixed-width keys, common deletes, and p99 latency constraints:

1. Start from a mature platform hash map unless measurements require a custom table.
2. Use a seeded, high-quality mixer for the key type; for hostile keys use keyed hashing.
3. Choose collision strategy from deletion and locality constraints: chaining for simple stable deletes, or open addressing with explicit tombstone/back-shift/rebuild policy for cache locality.
4. Set separate thresholds for live load and effective occupancy.
5. Measure hit, miss, insert, delete, resize, and rebuild tails separately.
6. Rehash with a new seed if collision distribution becomes suspicious.

This pattern extracts the hashing mindset without hand-rolling the educational pseudocode unless the implementation constraints justify it.

## Invariant and Proof Recipes

- **Chaining expected search:** Define indicator variables for whether another key collides with the searched key. Sum collision probabilities using linearity of expectation; independence can be weakened to universal pairwise collision bounds for many results.
- **Universal hashing proof:** Fix two distinct keys, show the random parameters make their intermediate values distinct and uniformly distributed, then count how many reductions collide modulo the table size.
- **Open addressing unsuccessful search:** Bound the chance that the first several probes all hit occupied slots. Sum tail probabilities to get the geometric-style bound.
- **Open addressing successful search:** A successful search repeats the insertion probe sequence. Average the insertion cost over the load factor at the time each key was inserted.
- **Double hashing correctness:** Show the step size is relatively prime to the table size so the probe sequence visits every slot before repeating.
- **Linear-probing deletion:** Maintain the invariant that every live key is reachable from its home slot before encountering an empty slot.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Picking chaining as the only answer for delete-heavy p99 workloads | Discuss chaining's deletion simplicity and open addressing's cache-locality advantage; make the tradeoff explicit |
| Treating universal hashing as a fixed static function that remains safe against adversaries | State that the expectation is over a random choice from a family and use seeding or rehashing in production |
| Ignoring tombstone accumulation in open addressing | Plan with effective occupancy and require rebuild, cleanup, or backward-shift deletion |
| Giving hit-only averages for capacity planning | Use miss and insert probe bounds when negative lookups, inserts, or p99 latency matter |
| Recommending division or raw multiply-shift for variable-length strings | Distinguish integer-key building blocks from byte-string hashing pipelines |
| Reciting textbook algorithms without industrial translation | Name cache locality, pointer chasing, load thresholds, adversarial input, and measurement hooks |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Saying hash tables are constant time without assumptions | State average or expected time and the hashing model |
| Confusing load factor meanings | Chaining permits average chain length above one; open addressing must stay below full occupancy |
| Deleting an open-addressed slot by writing empty | This can break reachability; use tombstones, rebuilds, or valid shift deletion |
| Counting only live entries after many deletes | Track live entries and tombstones or occupied-ever slots |
| Choosing table size by theorem aesthetics alone | Production resizing, power-of-two masking, cache layout, and hash mixing interact |
| Treating primary clustering as always bad | It hurts RAM-model probe counts but can improve locality when controlled |
| Using cryptographic hashing reflexively | Use it when adversarial risk or robust variable-length mixing justifies the CPU cost |
| Trusting average-case claims for p99 latency | Measure tail probe counts and rebuild before clusters dominate |

## Verification Pressure Tests

Use these to check future answers:

1. **Delete-heavy dictionary:** For 64-bit keys, common deletes, and p99 latency, the answer should compare chaining deletion simplicity with open-address cache locality and require load/tombstone policies.
2. **Adversarial static hash trap:** For a fixed static function and user-controlled keys, the answer should reject unconditional expected constant time and explain randomized universal or keyed hashing.
3. **Capacity planning formulas:** For a workload with misses and inserts, the answer should use load factor and open-address miss or insert bounds, not only successful-search averages.
4. **Variable-length strings:** For byte-string keys in a cache-sensitive table, the answer should separate the string hash/mixer from the collision strategy and mention robust seeding or cryptographic-inspired hashing when appropriate.
5. **Linear-probing deletion:** For deletion without tombstones, the answer should preserve probe-sequence reachability rather than merely shifting every later key backward.
