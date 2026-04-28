"""IOI 2025 JSONL prompt generator for CLRS skill benchmarks.

The generator intentionally uses only the Python standard library so prompts can be
copied into any agent framework without adapter code.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
from pathlib import Path
import re
from typing import Any, Literal, cast


PromptGroup = Literal["skills", "control", "reviewer"]
ANSWER_FILE_PATH = "answer.cpp"
PROMPT_TEMPLATES_PATH = Path(__file__).resolve().parents[1] / "ioi2025" / "prompt_templates.json"
_PROMPT_TEMPLATES: dict[str, Any] | None = None


@dataclass(frozen=True)
class IoiProblem:
    task: int
    name: str
    pdf_path: Path


@dataclass(frozen=True)
class IoiProblemSet:
    benchmark: str
    description: str
    problems: tuple[IoiProblem, ...]


@dataclass(frozen=True)
class PromptContext:
    problem_name: str
    raw_pdf_path: Path
    prompt_pdf_path: Path
    task: int
    scenario_id: str


@dataclass(frozen=True)
class PromptDraft:
    lines: tuple[str, ...]


@dataclass(frozen=True)
class PressureScenario:
    problem_name: str
    raw_pdf_path: Path
    task: int
    prompt: str


def load_ioi2025_problems(root: Path) -> IoiProblemSet:
    problems_path = root / "tests" / "ioi2025" / "problems.json"
    raw = json.loads(problems_path.read_text(encoding="utf-8"))
    problems = tuple(
        IoiProblem(
            task=int(problem["task"]),
            name=str(problem["name"]),
            pdf_path=Path(problem["pdf_path"]),
        )
        for problem in raw["problems"]
    )
    return IoiProblemSet(
        benchmark=str(raw["benchmark"]),
        description=str(raw["description"]),
        problems=problems,
    )


def build_prompt_contexts(root: Path) -> list[PromptContext]:
    problem_set = load_ioi2025_problems(root)
    return [_prompt_context(root, problem) for problem in problem_set.problems]


def build_pressure_scenarios(root: Path) -> list[PressureScenario]:
    return [
        PressureScenario(
            problem_name=context.problem_name,
            raw_pdf_path=context.raw_pdf_path,
            task=context.task,
            prompt=_render_prompt(_build_prompt_draft(context, "skills")),
        )
        for context in build_prompt_contexts(root)
    ]


def export_pressure_prompts_jsonl(root: Path, *, problem: int | None = None) -> str:
    return _export_jsonl(_prompt_records(root, "skills", problem=problem))


def export_control_prompts_jsonl(root: Path, *, problem: int | None = None) -> str:
    return _export_jsonl(_prompt_records(root, "control", problem=problem))


def export_reviewer_prompts_jsonl(root: Path, *, problem: int | None = None) -> str:
    return _export_jsonl(_prompt_records(root, "reviewer", problem=problem))


def _prompt_context(root: Path, problem: IoiProblem) -> PromptContext:
    return PromptContext(
        problem_name=problem.name,
        raw_pdf_path=root / problem.pdf_path,
        prompt_pdf_path=problem.pdf_path,
        task=problem.task,
        scenario_id=_problem_id(problem.task, problem.name),
    )


def _prompt_records(
    root: Path,
    group: PromptGroup,
    *,
    problem: int | None = None,
) -> list[dict[str, str]]:
    contexts = _select_contexts(build_prompt_contexts(root), problem)
    return [_prompt_record(context, group) for context in contexts]


def _prompt_record(context: PromptContext, group: PromptGroup) -> dict[str, str]:
    return {
        "id": _record_id(context, group),
        "prompt": _render_prompt(_build_prompt_draft(context, group)),
    }


def _record_id(context: PromptContext, group: PromptGroup) -> str:
    if group == "control":
        return f"control-{context.scenario_id}"
    if group == "reviewer":
        return f"reviewer-{context.scenario_id}"
    return context.scenario_id


def _export_jsonl(records: list[dict[str, str]]) -> str:
    return "\n".join(json.dumps(record, sort_keys=False) for record in records)


def _select_contexts(contexts: list[PromptContext], problem: int | None) -> list[PromptContext]:
    if problem is None:
        return contexts
    if problem < 1 or problem > 6:
        raise ValueError(f"expected IOI 2025 problem task between 1 and 6, found {problem}")
    selected = [context for context in contexts if context.task == problem]
    if not selected:
        raise ValueError(f"no IOI 2025 problem found for task {problem}")
    return selected


def _select_problem(scenarios: list[PressureScenario], problem: int | None) -> list[PressureScenario]:
    if problem is None:
        return scenarios
    if problem < 1 or problem > 6:
        raise ValueError(f"expected IOI 2025 problem task between 1 and 6, found {problem}")
    selected = [scenario for scenario in scenarios if scenario.task == problem]
    if not selected:
        raise ValueError(f"no IOI 2025 problem found for task {problem}")
    return selected


def _scenario_id(scenario: PressureScenario) -> str:
    return _problem_id(scenario.task, scenario.problem_name)


def _problem_id(task: int, problem_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", problem_name.lower()).strip("-")
    return f"ioi2025-{task}-{slug}"


def _build_prompt_draft(context: PromptContext, group: PromptGroup) -> PromptDraft:
    if group == "control":
        return _control_prompt_draft(context)
    if group == "reviewer":
        return _reviewer_prompt_draft(context)
    return _skills_prompt_draft(context)


def _skills_prompt_draft(context: PromptContext) -> PromptDraft:
    return PromptDraft(
        lines=(
            *_skills_opening(),
            *_problem_source(context),
            *_skills_setup(),
            *_solver_pre_assembly(uses_skills=True),
            *_skills_requirements(),
        )
    )


def _control_prompt_draft(context: PromptContext) -> PromptDraft:
    return PromptDraft(
        lines=(
            *_control_opening(),
            *_problem_source(context),
            *_control_setup(),
            *_solver_pre_assembly(uses_skills=False),
            *_control_requirements(),
        )
    )


def _reviewer_prompt_draft(context: PromptContext) -> PromptDraft:
    return PromptDraft(
        lines=(
            *_reviewer_opening(),
            *_reviewer_source(context),
            *_reviewer_policy(),
            *_reviewer_expected_output(),
        )
    )


def _render_prompt(draft: PromptDraft) -> str:
    return "".join(draft.lines)


def _prompt_templates() -> dict[str, Any]:
    global _PROMPT_TEMPLATES
    if _PROMPT_TEMPLATES is None:
        _PROMPT_TEMPLATES = json.loads(PROMPT_TEMPLATES_PATH.read_text(encoding="utf-8"))
    return cast(dict[str, Any], _PROMPT_TEMPLATES)


def _template_lines(key: str, **values: str) -> tuple[str, ...]:
    raw = cast(list[str], _prompt_templates()[key])
    return tuple(line.format(**values) for line in raw)


def _template_group_lines(section: str, group: str) -> tuple[str, ...]:
    raw = cast(list[str], _prompt_templates()[section][group])
    return tuple(raw)


def _template_string(key: str) -> str:
    return str(_prompt_templates()[key])


def _skills_opening() -> tuple[str, ...]:
    return _template_group_lines("openings", "skills")


def _control_opening() -> tuple[str, ...]:
    return _template_group_lines("openings", "control")


def _reviewer_opening() -> tuple[str, ...]:
    return _template_group_lines("openings", "reviewer")


def _problem_source(context: PromptContext) -> tuple[str, ...]:
    return (
        f"Raw problem PDF: {context.prompt_pdf_path}.\n",
        _pdf_extraction_guidance(),
        f"Problem: {context.problem_name} (task {context.task}).\n",
    )


def _reviewer_source(context: PromptContext) -> tuple[str, ...]:
    return (
        f"Problem: {context.problem_name} (task {context.task}).\n",
        f"Raw problem PDF: {context.prompt_pdf_path}.\n",
        _pdf_extraction_guidance(),
    )


def _skills_setup() -> tuple[str, ...]:
    return _template_group_lines("setups", "skills")


def _control_setup() -> tuple[str, ...]:
    return _template_group_lines("setups", "control")


def _solver_pre_assembly(*, uses_skills: bool) -> tuple[str, ...]:
    return (
        *_solver_file_policy(),
        *_solver_attempt_policy(),
        *_solver_metadata_policy(),
        *_solver_expected_output(uses_skills=uses_skills),
    )


def _solver_file_policy() -> tuple[str, ...]:
    return _template_lines("solver_file_policy", answer_file_path=ANSWER_FILE_PATH)


def _solver_attempt_policy() -> tuple[str, ...]:
    return _template_lines("solver_attempt_policy")


def _solver_metadata_policy() -> tuple[str, ...]:
    return _template_lines("solver_metadata_policy")


def _solver_expected_output(*, uses_skills: bool) -> tuple[str, ...]:
    group = "skills" if uses_skills else "control"
    expected_output = _prompt_templates()["solver_expected_output"]
    return (
        str(expected_output["header"]),
        str(expected_output["first_section"][group]),
        *cast(list[str], expected_output["middle_sections"]),
        str(expected_output["strategy_section"][group]),
        *cast(list[str], expected_output["tail_sections"]),
    )


def _first_solver_output_section(*, uses_skills: bool) -> str:
    group = "skills" if uses_skills else "control"
    return str(_prompt_templates()["solver_expected_output"]["first_section"][group])


def _strategy_output_section(*, uses_skills: bool) -> str:
    group = "skills" if uses_skills else "control"
    return str(_prompt_templates()["solver_expected_output"]["strategy_section"][group])


def _skills_requirements() -> tuple[str, ...]:
    return _template_group_lines("requirements", "skills")


def _control_requirements() -> tuple[str, ...]:
    return _template_group_lines("requirements", "control")


def _reviewer_policy() -> tuple[str, ...]:
    return _template_lines("reviewer_policy", answer_file_path=ANSWER_FILE_PATH)


def _reviewer_expected_output() -> tuple[str, ...]:
    return _template_lines("reviewer_expected_output")


def _pdf_extraction_guidance() -> str:
    return _template_string("pdf_extraction_guidance")


def build_copy_paste_guide() -> str:
    return _template_string("copy_paste_guide")


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit IOI 2025 CLRS benchmark prompts as JSONL.")
    parser.add_argument(
        "--group",
        choices=("skills", "control", "reviewer"),
        default="skills",
        help="Prompt group to export. Use 'control' for no-skill baseline prompts or 'reviewer' for cross-check prompts.",
    )
    parser.add_argument(
        "--problem",
        choices=range(1, 7),
        metavar="1-6",
        type=int,
        help="Emit only one IOI 2025 problem prompt so it can be given to a fresh agent.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    jsonl = _export_group(root, args.group, problem=args.problem)

    print(build_copy_paste_guide().rstrip())
    print("\nJSONL prompts:\n")
    print(jsonl)


def _export_group(root: Path, group: PromptGroup, *, problem: int | None = None) -> str:
    if group == "control":
        return export_control_prompts_jsonl(root, problem=problem)
    if group == "reviewer":
        return export_reviewer_prompts_jsonl(root, problem=problem)
    return export_pressure_prompts_jsonl(root, problem=problem)


if __name__ == "__main__":
    main()
