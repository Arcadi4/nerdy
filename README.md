# Nerdy Skills ☝️🤓

> "PhD-level intelligence."

Empower your agents with the famous (or infamous) computer science textbooks:

- *The Art of Computer Programming* series (`taocp`)
- *Introduction to Algorithms* (`clrs`)
- *Structure and Interpretation of Computer Programs* (`sicp`)
- *The C Programming Language* (`knr`)
- More coming... Recommendations are welcome!

## Get started

Install all books

```bash
npx skills add arcadi4/nerdy
```

Install one specific book

```
npx skill add arcadi4/nerdy.git@bookname
```

Example: installing only *Introduction to algorithms*

```
npx skill add arcadi4/nerdy.git@clrs
```

## File structure

```plaintext
nerdy/
|-- book-name         # The book name
    |-- SKILL.md      # The index skill. Agents start from here.
    |-- ...sub-skills # After calling the index skill, agents may pick skills relevant to their problem.
```

## Progress

- [x] CLRS: Complete. With 28 specialized skills + 1 indexing skill.
- [ ] K&R: Not yet started.
- [ ] SICP: Planned. This will be the next book that I work on.
- [ ] TAOCP: Not yet started.
