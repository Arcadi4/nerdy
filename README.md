# Nerdy Skills ☝️🤓

> "PhD-level intelligence."

Empower your agents with the famous (or infamous) computer science textbooks:

- *Introduction to Algorithms* (`clrs`)
- *Structure and Interpretation of Computer Programs* (`sicp`)
- *Types and Programming Languages* (`tapl`)
- *Computer Systems: A Programmer’s Perspective* (`csapp`)
- More coming... Recommendations are welcome!

## Get started

Install all books

```bash
npx skills add arcadi4/nerdy
```

Install one specific book

```bash
npx skills add arcadi4/nerdy@bookname
```

Example: installing only *Introduction to algorithms* (`clrs`)

```bash
npx skills add arcadi4/nerdy@clrs
```

## How to Use

I haven't received enough feedback nor performed enough real-world testing on these skills. Here are how these skills are intended to be used:

- `clrs`: For small models, provide solid algorithmic knowledge to prevent hallucinations. For larger ones, provide a comprehensive framework of analysis to prevent premature conclusions or skipping important details.
- `sicp`: Helpful at design and refactoring stages. Help models identify problematic patterns, and discover potentially beneficial but unconventional refactorings that are less common in the language's training data.

## File structure

```plaintext
nerdy/
|-- book-name              # The book name
    |-- SKILL.md           # The index skill. Agents start from here.
    |-- sub-skill/SKILL.md # After calling the index skill, agents may pick skills relevant to their problem.
```

## Progress

- [x] CLRS: Complete. With 28 specialized skills + 1 indexing skill.
- [ ] SICP: Planned. This will be the next book that I work on.
- [ ] TaPL: Not yet started.
- [ ] CSAPP: Not yet started.
