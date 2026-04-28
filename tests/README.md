# Skill benchmark prompts

This directory contains raw IOI 2025 benchmark data and a standard-library JSONL prompt generator for manual CLRS skill testing.

## Manual smoke checks

```bash
python3 -m py_compile tests/prompts/ioi2025.py
```

Generate one prompt from each group and confirm each command prints a copy/paste guide followed by one JSONL object:

```bash
python3 -m tests.prompts.ioi2025 --group skills --problem 1
python3 -m tests.prompts.ioi2025 --group control --problem 1
python3 -m tests.prompts.ioi2025 --group reviewer --problem 1
```

## Data contract

- `tests/ioi2025/problems.json` lists the six raw IOI 2025 problem PDFs.
- The generator emits JSONL records with only `id` and `prompt`.
- Skills prompts contain no preset CLRS skill map. They tell the tested model to use the `clrs` indexing skill first, then choose applicable CLRS chapter skills by judgment.
- Control prompts forbid all skills.
- Reviewer prompts are for a separate reviewer model after the tested solver has produced a C++ answer file.

## Manual JSONL prompt export

Generate framework-agnostic skills prompts one problem at a time. The command prints the copy/paste guide first, then the JSONL prompt object:

```bash
python3 -m tests.prompts.ioi2025 --group skills --problem 1
```

Generate the matching no-skill control prompts for a separate fresh agent:

```bash
python3 -m tests.prompts.ioi2025 --group control --problem 1
```

After the tested agent produces its C++ `.cpp` file, generate reviewer prompts for a separate reviewer model:

```bash
python3 -m tests.prompts.ioi2025 --group reviewer --problem 1
```

Change `--problem 1` to `--problem 2` through `--problem 6` so each IOI problem is solved by a new agent. Run the skills and control commands separately for each problem you evaluate.

Each JSONL prompt object contains only:

```json
{"id": "ioi2025-1-souvenirs", "prompt": "..."}
```

### Copy/paste guide

1. Generate `skills prompts` or `control prompts` with the per-problem commands above.
2. Copy one JSONL object from the command output. Paste the prompt value into a new tested agent.
3. Skills prompts tell the tested solver to use the `clrs` indexing skill and choose CLRS chapter skills by judgment.
4. The tested solver discovers PDF text-extraction tools first, such as `pdftotext`, before trying direct PDF reading; extraction must print to stdout and must not create temporary text files.
5. The tested solver may only read the named raw problem PDF and write the fixed answer file `answer.cpp`; it must not choose another file name or path.
6. The tested solver appends metadata comments to the `.cpp` file instead of writing a separate result dump.
7. The tested solver must not use subagents, file search, directory listing, `grep`, `rg`, `ripgrep`, `find`, `ls`, `glob`, `ast_grep_search`, or read/list/search/open/visit `ioi2025solutions`; that directory is reserved for the separate reviewer model.
8. Generate `reviewer prompts` for a separate reviewer model after the `.cpp` exists. The reviewer cross-verifies the candidate `.cpp` file against `ioi2025solutions` and writes the final `Result dump`.

The prompt is self-contained: it tells the tested solver to start immediately, discover and use local PDF text-extraction tools like `pdftotext` before direct PDF reading, read only the raw IOI PDF, produce only `answer.cpp`, append metadata comments, use the `clrs` indexing skill for the skills group, avoid all skills for the control group, avoid subagents, web search, file search, directory listing, `ioi2025solutions`, and any file operation except reading the PDF and writing `answer.cpp`, run any answer file at most three times, and return the expected sections for skill testing. Human contestant performance statistics are not included in generated prompts.

The generator is intentionally standard-library only. Live RED/GREEN agent scoring stays manual and framework-independent through the generated prompts.
