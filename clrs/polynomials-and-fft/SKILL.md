---
name: polynomials-and-fft
description: Use when multiplying polynomials, using coefficient or point-value representations, applying DFT or FFT, reasoning about roots of unity, convolution, FFT circuits, or exact modular Fourier transforms.
license: MIT
---

# Polynomials and the FFT

## Overview

The FFT chapter is about changing representation at the right points. Polynomial multiplication is expensive in coefficient form, cheap in point-value form, and fast overall only when the evaluation and interpolation points have roots-of-unity structure.

**Core principle:** never treat FFT as a magic multiplication primitive. State the representation, degree-bound, evaluation length, root system, inverse transform, and exactness model before giving an algorithm or bound.

## Shared CLRS Conventions

Follow the parent `clrs` skill for mathematical formatting, formula-free headings, direct polished answers, and CLRS-wide answer style. Keep formulas in display blocks, including degree-bounds, roots of unity, DFT definitions, recurrence equations, and convolution identities.

## When to Use

- A prompt asks for polynomial multiplication, convolution, coefficient representation, point-value representation, interpolation, or evaluation at many points.
- A prompt mentions DFT, inverse DFT, FFT, roots of unity, twiddle factors, butterflies, bit reversal, or FFT circuits.
- A prompt tries to multiply degree-bounded polynomials using too few point-value pairs.
- A prompt asks whether textbook complex FFT is safe for exact integer answers.
- A prompt asks for proof moves involving cancellation, halving, summation over roots of unity, or Vandermonde uniqueness.

Do **not** use this skill for general signal-processing design unless the algorithmic question is the discrete transform, convolution, or roots-of-unity structure.

## First Decision: Which Representation Is the Work In?

| Workload | Representation to prefer | Watch for |
| --- | --- | --- |
| Add two polynomials already in coefficient form | Coefficients | Add coordinatewise; multiplication is the hard operation |
| Evaluate one polynomial at one point | Coefficients with Horner's rule | This is linear, not FFT-worthy |
| Multiply many coefficients directly | Convert through point values | Degree-bound must grow before interpolation |
| Add or multiply values at the same evaluation points | Point values | The points must match between inputs |
| Recover coefficients from arbitrary points | Interpolation | General interpolation is slower and numerically fragile |
| Recover coefficients from roots of unity | Inverse DFT | Divide by the transform length after using inverse roots |

Use the chapter's two representations as an API contract:

$$
A(x)=\sum_{j=0}^{n-1}a_jx^j
$$

The coefficient vector is the stored form above. A point-value form stores distinct points and their values:

$$
\{(x_0,y_0),(x_1,y_1),\ldots,(x_{n-1},y_{n-1})\}
$$

where each value satisfies the relation below.

$$
y_k=A(x_k)
$$

## Degree-Bound Discipline

The most common FFT mistake is forgetting that multiplication changes the degree-bound. If two inputs have the same degree-bound, the product can require almost twice as many coefficients.

For two coefficient vectors with the degree-bound below:

$$
\operatorname{degree}(A)<n
$$

$$
\operatorname{degree}(B)<n
$$

the product satisfies the bound below.

$$
\operatorname{degree}(AB)<2n-1
$$

CLRS often pads to a simpler bound for FFT work:

$$
\operatorname{degree\mbox{-}bound}(AB)=2n
$$

Operational rule: evaluate both inputs at enough common points to interpolate the product, not merely enough points to represent each input. For radix-two FFT, pad to an FFT length that is a power of two and at least the output coefficient count.

If a teammate says that the original number of point-value pairs is enough, answer with the degree-bound failure first, then the fix. With too few points, interpolation is underdetermined and practical FFT-style multiplication produces aliasing or a circular convolution rather than the desired coefficient product.

## Polynomial Multiplication Pipeline

Use this checklist for coefficient-form multiplication:

1. **Double the degree-bound.** Add high-order zero coefficients so each input has room for the product representation.
2. **Evaluate using roots of unity.** Compute the DFT of each padded vector at the selected transform length.
3. **Pointwise multiply.** Multiply corresponding transformed values.
4. **Interpolate with the inverse transform.** Apply the inverse DFT and scale by the transform length.
5. **Trim or report the meaningful coefficients.** Keep the coefficients supported by the product degree-bound.

The coefficient formula for direct multiplication is convolution:

$$
c_j=\sum_{k=0}^{j}a_kb_{j-k}
$$

The FFT pipeline computes the same convolution through transform space:

$$
a\otimes b=\operatorname{DFT}^{-1}_{2n}\left(\operatorname{DFT}_{2n}(a)\cdot\operatorname{DFT}_{2n}(b)\right)
$$

where the dot in the expression above is componentwise multiplication and the inputs are padded before the transforms.

State the running time as dominated by the forward and inverse transforms:

$$
T(n)=\Theta(n\lg n)
$$

## Roots of Unity Proof Moves

The roots-of-unity lemmas are not decorative. They are the reason divide-and-conquer evaluation and inverse interpolation work.

The principal root is:

$$
\omega_n=e^{2\pi i/n}
$$

All roots are powers of the principal root:

$$
1,\omega_n,\omega_n^2,\ldots,\omega_n^{n-1}
$$

Use these proof moves:

| Move | Use it when | What it buys |
| --- | --- | --- |
| Cancellation | Changing root order or relating roots at different lengths | Powers of a larger root become powers of a smaller root |
| Halving | Splitting even and odd coefficients in FFT | Squared roots collapse to the half-size root set |
| Summation | Proving inverse DFT matrix entries | Off-diagonal geometric sums vanish |
| Half-turn sign | Combining the second half of FFT outputs | The second half differs by a sign on the odd part |

Display the key identities when proving them:

$$
\omega_{dn}^{dk}=\omega_n^k
$$

For even transform length, the half-turn relation is:

$$
\omega_n^{n/2}=-1
$$

The summation lemma says the root powers cancel unless the exponent is divisible by the transform length:

$$
\sum_{j=0}^{n-1}\left(\omega_n^k\right)^j=0
$$

Use the expression above only under its precondition: the exponent is nonzero modulo the transform length.

## DFT and FFT Reference

The DFT evaluates a coefficient vector at all roots of unity for the chosen transform length:

$$
y_k=A\left(\omega_n^k\right)=\sum_{j=0}^{n-1}a_j\omega_n^{kj}
$$

The FFT is the divide-and-conquer algorithm for this evaluation when the transform length is an exact power of two. Split the coefficients into even-indexed and odd-indexed polynomials:

$$
A(x)=A^{\mathrm{even}}(x^2)+xA^{\mathrm{odd}}(x^2)
$$

Then recursively evaluate the even and odd parts at the half-size roots and combine them with twiddle factors.

For each index in the first half, the combine equations are:

$$
y_k=y_k^{\mathrm{even}}+\omega_n^k y_k^{\mathrm{odd}}
$$

$$
y_{k+n/2}=y_k^{\mathrm{even}}-\omega_n^k y_k^{\mathrm{odd}}
$$

The recurrence is:

$$
T(n)=2T(n/2)+\Theta(n)
$$

Therefore the transform time is:

$$
T(n)=\Theta(n\lg n)
$$

When writing pseudocode, include these obligations:

1. base case returns the single input value,
2. recursive calls receive even and odd coefficient subvectors,
3. the running twiddle factor starts at one,
4. the twiddle factor is multiplied by the principal root each loop,
5. the two outputs per loop are a sum and a difference.

## Inverse DFT and Interpolation

Interpolation at roots of unity is the inverse DFT, not arbitrary Vandermonde solving. The inverse matrix has conjugate root powers and a scaling factor.

Recover coefficients with:

$$
a_j=\frac{1}{n}\sum_{k=0}^{n-1}y_k\omega_n^{-jk}
$$

Implementation rule: run the same FFT structure with inverse roots, then divide every output by the transform length. Missing the final division is a correctness bug, not a constant-factor detail.

When proving inverse correctness, multiply the DFT matrix by the claimed inverse and use the summation lemma. The diagonal entries survive; off-diagonal entries vanish because their exponent difference is not divisible by the transform length.

## FFT Circuits and Iterative Implementations

The circuit view translates recursive FFT into a staged parallel computation.

Use these terms precisely:

- **Butterfly:** one twiddle multiplication followed by one sum and one difference.
- **Twiddle factor:** the root power multiplying the odd-side value before the sum and difference.
- **Bit-reversal permutation:** the input order produced by repeatedly splitting on low-order index bits.
- **Stage:** a layer of independent butterflies that can run in parallel.

For an input length that is a power of two, the circuit has logarithmically many stages and a linear number of butterflies per stage:

$$
\Theta(\lg n)
$$

stages and

$$
\Theta(n\lg n)
$$

butterfly operations in total.

Use the bit-reversal lesson when moving from recursive pseudocode to iterative code: either permute inputs first and run bottom-up stages, or keep an equivalent indexing scheme. Do not claim the recursive split disappears; it becomes the input permutation and stage layout.

## Exactness and Production Use

Textbook complex FFT is mathematically exact over complex numbers, but real implementations use finite-precision arithmetic. For exact integer polynomial products, do not promise correctness from a plain floating-point FFT unless coefficient and length bounds justify safe rounding.

Production checklist:

1. Bound the largest possible output coefficient before choosing an exact method.
2. If using floating-point FFT, prove the error margin stays below the rounding threshold or use a library with documented guarantees for the input range.
3. If exactness is required, prefer number-theoretic transforms over suitable modular rings or fields.
4. Choose a modulus and root so the needed transform length has a principal root of unity and inverse scaling is valid.
5. Use enough moduli and CRT reconstruction when one modulus cannot cover the coefficient range.

The chapter's modular exercise highlights a modulus form where powers of two can serve as roots in modular arithmetic:

$$
m=2^{tn/2}+1
$$

and uses the candidate root below.

$$
\omega=2^t
$$

The later modular-FFT problem uses prime moduli whose multiplicative group contains an element of the required order. In either setting, verify that the transform and inverse transform are well-defined: the root has the required order, the transform length is invertible modulo the modulus, and the summation lemma analogue holds.

## Proof and Exercise Patterns

| Prompt type | Reusable move |
| --- | --- |
| Uniqueness of interpolation | Convert point-value constraints to a Vandermonde system and cite distinct evaluation points |
| Lagrange interpolation | Build basis polynomials that are one at their own point and zero at all others |
| Reverse polynomial values | Substitute reciprocal points and account for the degree-bound factor |
| Cartesian sums of integer sets | Encode membership as polynomial coefficients and use convolution counts |
| Power-of-three FFT | Split coefficients by index residue and recurse on cubed roots |
| Chirp transform | Rewrite the exponent to expose a convolution |
| Multidimensional DFT | Apply one-dimensional transforms along each axis; separability makes order irrelevant |
| Multipoint evaluation | Build a product tree of linear factors and pass remainders down the tree |

For exercises that ask for an algorithm, always state:

1. representation of inputs and outputs,
2. padding or degree-bound assumptions,
3. root or modulus preconditions,
4. whether the result is mathematical exactness or numerical computation,
5. the recurrence or summation that gives the running time.

## RED Pressure Failures This Skill Prevents

| Baseline failure | Required correction |
| --- | --- |
| Saying the original point count is enough for multiplying two degree-bounded inputs | State that the product has a larger degree-bound and needs enough common evaluation points for interpolation |
| Explaining FFT multiplication without padding | Add high-order zero coefficients before forward transforms |
| Giving inverse FFT without scaling | Use inverse roots and divide every output by the transform length |
| Treating roots-of-unity lemmas as optional facts | Use halving for recursive subproblems and summation for inverse correctness |
| Recommending complex FFT for exact integer products without qualification | Discuss roundoff, coefficient bounds, modular transforms, and CRT reconstruction |
| Drawing the circuit but ignoring the input permutation | Connect recursive even-odd splitting to bit reversal and staged butterflies |
| Calling any transform-space product a convolution without checking length | Distinguish linear convolution from circular aliasing caused by insufficient padding |

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Confusing degree with degree-bound | Degree is the highest nonzero term; degree-bound is any strict upper bound used for representation |
| Multiplying point-value forms evaluated at different points | Pointwise operations require the same evaluation points in the same order |
| Interpolating a product from too few values | Use enough values for the product degree-bound, usually a padded power-of-two transform length |
| Forgetting that FFT assumes a power-of-two length in the chapter | Pad or explicitly switch to a generalized transform outside the chapter scope |
| Using the forward root for inverse DFT | Use inverse powers and then scale |
| Treating floating-point FFT as exact algebra | State numerical error assumptions or switch to modular arithmetic |
| Hand-rolling FFT for production by default | Prefer mature numerical or NTT libraries unless the exercise asks for the textbook mechanism |
| Ignoring coefficient growth in integer convolution | Bound output coefficients before selecting moduli or rounding strategy |

## Verification Pressure Tests

Use these prompts to check future answers:

1. **Multiplication pipeline:** Given two coefficient vectors with the same degree-bound, the answer should pad to a product-safe transform length, run two forward DFTs, pointwise multiply, run an inverse DFT, scale, trim, and state the transform-dominated bound.
2. **Too-few-points trap:** If someone proposes multiplying two point-value forms with only the original number of values, the answer should diagnose the product degree-bound and explain underdetermination or aliasing.
3. **Inverse transform:** Given transformed values at roots of unity, the answer should use inverse root powers and divide by the transform length.
4. **Roots proof:** A proof of FFT correctness should invoke halving for squared roots and the half-turn sign for the second half of outputs.
5. **Exact integer service:** The answer should reject unconditional floating-point exactness and require coefficient bounds, modular roots, invertible transform length, enough moduli, and CRT if needed.
6. **Circuit mapping:** The answer should identify butterflies, twiddle factors, bit reversal, stage count, and total butterfly work.

## Static Checks

- `clrs/polynomials-and-fft/SKILL.md` exists and its frontmatter name matches the directory slug.
- `clrs/SKILL.md` routes FFT, DFT, convolution, and polynomial multiplication prompts to this skill.
- No heading contains a formula.
- No Markdown table cell contains display math delimiters.
- The skill includes RED failures for padding, point-count, inverse scaling, exactness, and circuit permutation traps.
- The skill distinguishes educational FFT mechanics from production exactness and library judgment.
