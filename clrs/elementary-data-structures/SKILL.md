---
name: elementary-data-structures
description: Use when reasoning about elementary data structures, dynamic sets, arrays, matrices, stacks, queues, linked lists, sentinels, rooted trees, representation choices, invariants, locality, or pointer-based tradeoffs under practical engineering constraints.
license: MIT
---

# Elementary Data Structures

## Overview

Treat elementary data structures as representation contracts, not classroom containers. The core move is to name the operations, access pattern, ownership model, and boundary invariants before choosing arrays, lists, stacks, queues, or tree links.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style.

## When to Use

- A problem asks for arrays, matrices, stacks, queues, linked lists, sentinels, rooted trees, or left-child/right-sibling representation.
- You need to implement or review a dynamic set with `SEARCH`, `INSERT`, `DELETE`, `MINIMUM`, `MAXIMUM`, `SUCCESSOR`, or `PREDECESSOR`-like operations.
- A design hinges on contiguity, locality, pointer chasing, deletion by pointer, circular-buffer wraparound, sentinel nodes, or parent/child/sibling navigation.
- A production discussion needs the lesson behind an undergraduate structure rather than a literal reimplementation.

Do **not** use this skill merely because code contains an array or list. Use ordinary language/library conventions unless representation choice, invariants, asymptotic behavior, or access patterns are central.

## First Decision: What Contract Does the Structure Serve?

| Need | Prefer | Why |
| --- | --- | --- |
| Random indexed access and dense storage | Contiguous array or vector | Index arithmetic is constant time and cache-friendly |
| Append/pop at one end | Dynamic array or stack abstraction | Simpler and more local than pointer nodes |
| FIFO bounded buffer | Circular array queue | Constant-time operations with fixed memory and explicit full/empty policy |
| Frequent middle splice with existing node handles | Doubly linked list | Pointer rewiring is constant time once the node is known |
| Search by key in an unordered small set | Array or list if tiny; otherwise a real dictionary | Elementary structures expose the cost; later chapters provide better dictionaries |
| Ordered enumeration from elementary structures only | Sorted array/list if updates are rare | Maintaining order shifts update cost somewhere |
| Variable-arity rooted tree | Child vectors or left-child/right-sibling | Choose by child iteration, random child access, memory, and parent navigation |

Before choosing, ask:

1. Which operations are required by API, and which are merely convenient?
2. Does `DELETE` receive a key, an index, an iterator, or a direct node pointer?
3. Is order semantic, insertion-order, sorted-by-key, or irrelevant?
4. Are elements moved, copied, referenced, or owned by the structure?
5. Is performance dominated by asymptotic cost, cache locality, allocation, or simplicity?

## Dynamic-Set Operation Discipline

Dynamic-set APIs separate queries from modifying operations so the representation can be judged by the exact contract.

| Operation family | Ask first | Common elementary consequence |
| --- | --- | --- |
| Search by key | Is the structure sorted, indexed, or unordered? | Unsorted arrays/lists scan; sorted arrays can binary search; sorted lists still traverse |
| Insert | Must relative order be preserved? | Arrays may shift; head-list insertion is cheap but changes order |
| Delete | Is a direct object pointer available? | Doubly linked lists delete by pointer; singly linked lists usually need predecessor search |
| Minimum/maximum | Is sorted order maintained? | Cheap only if representation keeps the extreme at an accessible boundary |
| Successor/predecessor | Is there bidirectional navigation or searchable order? | Singly linked lists do not support predecessor cheaply |

Do not answer with a more advanced structure as if the elementary representation already solved the problem. It is fine to say: "This introductory lesson shows why this elementary representation is insufficient; in production use a library hash map, ordered map, deque, vector, or tree implementation once the contract requires it."

## Arrays and Matrices: Contiguity Is the Lesson

An array is a contiguous block of equal-sized slots. The transferable insight is that representation determines address calculation, locality, and movement cost.

- Constant-time indexed access comes from fixed element size and arithmetic on the base address.
- Variable-sized objects are normally stored indirectly through fixed-size references; this buys indexing but adds pointer chasing.
- Row-major and column-major matrix layouts encode a traversal preference. Match layout to the dominant loop order or library ABI.
- Single-array matrices are usually more cache-friendly than arrays of row pointers; arrays of row pointers support ragged rows and separate allocation.
- Blocked layouts trade simple indexing for locality on tiled algorithms and cache-sized working sets.

Industrial warning: asymptotic constant time does not mean equal cost. Scanning a contiguous array can beat a theoretically similar pointer traversal because allocation, cache misses, branch prediction, and prefetching matter.

## Stacks and Queues: Boundary Invariants Are the Product

Stacks and queues are restricted dynamic sets: deletion policy is part of the type.

| Structure | Invariant | Review hazards |
| --- | --- | --- |
| Stack | `top` names the most recently pushed live element, or the empty boundary | Underflow, overflow, stale array contents mistaken for membership |
| Circular queue | `head` names next dequeue; `tail` usually names next enqueue slot | Empty/full ambiguity, wraparound off-by-one, capacity mismatch |
| Deque | Both ends are legal insertion and deletion boundaries | Head/tail updates must be symmetric and tested through wraparound |

For circular queues, choose exactly one full/empty policy and state it in code comments or type invariants:

1. Leave one slot empty, so usable capacity is one less than storage capacity.
2. Store an explicit count, so all slots are usable.
3. Store an explicit full flag, and update it on every enqueue/dequeue transition.

Never mix policies. Tests should fill to capacity, attempt one extra enqueue, drain to empty, attempt one extra dequeue, and cross the physical end of the array in both directions.

## Linked Lists: Handles Beat Search Only If You Already Have Them

Linked lists teach that update cost and discovery cost are different.

| Variant | Strength | Hidden cost |
| --- | --- | --- |
| Singly linked, unsorted | Constant-time head insertion and forward traversal | Deleting an arbitrary node usually needs predecessor search |
| Doubly linked, unsorted | Constant-time splice/delete when a node handle is known | Extra pointer, more mutation surfaces, poor locality |
| Sorted list | Boundary extrema and ordered traversal are simple | Insertion/search still traverse unless extra indexing exists |
| Circular list with sentinel | Uniform boundary cases and simpler splice/delete code | Extra dummy node and a value that must not be treated as user data |

Use the phrase "given a pointer to the element" precisely. In `DELETE(S, x)`, the operation removes a known object, but a singly linked list still cannot generally unlink `x` in constant time from `x` alone, because the predecessor's `next` field must change. Separate these cases explicitly:

- Delete by key: first search for the node and usually its predecessor.
- Delete by node plus predecessor handle: constant-time pointer rewrite in a singly linked list.
- Delete by node alone in a doubly linked list: constant-time splice using `prev` and `next`.
- Delete by node alone in a singly linked list: not generally constant time; special "copy successor into this node" tricks fail for tails and break identity/handle semantics.

Many production bugs come from quoting the update bound while hiding the search or predecessor handle needed to make the bound true.

Sentinels are an engineering pattern: replace special-case boundary checks with a dummy object that satisfies the same pointer protocol. Use them when they simplify hot, error-prone pointer code; avoid them when many tiny lists make dummy-node memory or sentinel misuse costly.

## Rooted Trees: Pick Links for Navigation, Not for the Picture

Tree representation is an API choice.

| Representation | Use when | Avoid or qualify when |
| --- | --- | --- |
| Binary tree links: parent, left, right | Each node has at most two named children | General trees or child lists are needed |
| Fixed child pointer array | Branching factor is small and bounded | Most nodes have far fewer children than the bound |
| Child vector/list per node | Random child iteration and simple APIs matter | Per-node allocation overhead dominates |
| Parent pointers only | Algorithms walk toward roots, as in disjoint-set forests | Downward traversal is needed |
| Left-child/right-sibling | Arbitrary child counts need fixed pointer budget and ordered sibling traversal | Frequent random child access or very wide nodes need faster child indexing |

Left-child/right-sibling stores the first child and next sibling, optionally plus parent. It gives linear-time child iteration in the number of children and fixed pointer fields per node. It does **not** give constant-time access to the kth child; it is a compact traversal representation, not a general replacement for child arrays.

## One Industrial Example: Bounded Work Queue Review

When reviewing an array-backed bounded FIFO queue, write the contract first:

```text
storage length: capacity + 1
usable capacity: capacity
empty: head == tail
full: next(tail) == head
enqueue: require not full; write at tail; advance tail
dequeue: require not empty; read at head; advance head
membership: only slots on the circular interval from head to tail are live
```

Then test the state machine, not just one happy path:

1. Empty queue rejects dequeue.
2. Enqueue exactly usable capacity items.
3. One more enqueue rejects overflow.
4. Dequeue some items, enqueue enough to wrap `tail`.
5. Drain through wraparound and verify FIFO order.
6. One more dequeue rejects underflow.

This example captures the chapter's deeper lesson: simple structures are safe only when boundary invariants are explicit and repeatedly exercised.

## Invariant and Proof Recipes

- **Array representation:** State the live range separately from allocated storage. Stale values outside the live range are not members.
- **Stack:** Prove push/pop by showing how `top` moves the live prefix boundary by one slot.
- **Circular queue:** Prove FIFO by tracking the circular interval from `head` to `tail` under the chosen full/empty policy.
- **Linked-list splice:** Name the two neighboring nodes before mutation; after mutation, every forward link's reverse link must agree in a doubly linked list.
- **Sentinel list:** Treat the sentinel as the permanent boundary object; prove no operation deletes it or returns it as a real element.
- **Left-child/right-sibling tree:** Prove child iteration by following `left-child` once and then `right-sibling` until the sibling boundary.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Jumping from elementary arrays/lists directly to hash tables or red-black trees without extracting the introductory representation lesson | Explain the operation/access-pattern mismatch first, then mention production library structures as alternatives |
| Calling an in-memory red-black tree "cache-friendly" because it is logarithmic | Separate asymptotic depth from locality; pointer-heavy trees often lose locality to arrays or B-tree-like layouts |
| Saying singly linked lists delete in constant time from a node pointer alone | Distinguish delete-by-key, delete-by-node-plus-predecessor, doubly linked delete-by-node, and invalid singly linked delete-by-node-alone claims |
| Treating circular queues as just modulo arithmetic | State head/tail meanings and the full/empty policy before code |
| Describing sentinels as only a micro-optimization | Emphasize boundary-condition simplification and the risk of returning/deleting dummy nodes |
| Treating left-child/right-sibling as a binary-tree trick with free child access | State fixed pointer budget, sibling traversal cost, and parent-pointer tradeoff |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Choosing a linked list for "fast insertion" while search dominates | Count the cost to find the insertion or deletion position |
| Treating a node pointer as enough to unlink from a singly linked list | Require a predecessor handle, use a doubly linked list, or state the narrow unsafe successor-copy exception and its identity/tail limits |
| Maintaining sorted order without pricing updates | Sorted arrays/lists move or traverse on insert/delete |
| Forgetting satellite data | Decide whether nodes own records, point to records, or carry payload directly |
| Confusing allocated slots with live elements | Track live ranges, `top`, `head`, `tail`, or node reachability |
| Mixing zero-origin and one-origin formulas | Convert all index arithmetic to the implementation language before coding |
| Using sentinels in public APIs | Hide sentinels behind iterators or methods so callers cannot persist or delete them |
| Assuming textbook pointer structures are production defaults | Prefer mature library containers unless the representation contract is special |

## Verification Pressure Tests

Use these to check future answers:

1. **Industrial dictionary:** For millions of request IDs with membership, update, and occasional ordering, the answer should explain the introductory representation tradeoffs before recommending a production map or ordered container.
2. **Circular queue wraparound:** The answer should name head/tail meanings, full/empty policy, usable capacity, and overflow/underflow tests.
3. **Singly linked deletion:** The answer should reject arbitrary constant-time deletion unless the predecessor or a special handle protocol is available.
4. **Sentinel list:** The answer should simplify splice/delete while warning that the sentinel is not a user element.
5. **Variable-arity tree:** The answer should compare left-child/right-sibling against child vectors or arrays based on child iteration, kth-child access, memory, and parent traversal.
