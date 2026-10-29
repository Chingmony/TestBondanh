"""Requirement traceability check (DEC-039, TS-31, TS-32).

Collects requirement IDs from the approved documents and @pytest.mark.req(...)
tags from test files. Test files are parsed, never imported, so a broken test
file is reported instead of breaking the check.

Usage (from the repository root):
    .venv\\Scripts\\python.exe scripts\\trace.py --check    fail on untagged tests or bad IDs
    .venv\\Scripts\\python.exe scripts\\trace.py --report   print requirement ID -> tests
"""

from __future__ import annotations

import argparse
import ast
import io
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Only requirements can be test tags; decisions, risks, and questions cannot.
_ID = r"(?:TR-SEC-\d{2}|(?:BR|PR|FR|NFR|TR|TS)-\d{2,3})"
_ID_IN_TEXT = re.compile(rf"\b{_ID}\b")
_ID_EXACT = re.compile(_ID)

_TestNode = ast.FunctionDef | ast.AsyncFunctionDef


@dataclass(frozen=True)
class Problem:
    kind: str  # untagged_test | invalid_id | unknown_id | syntax_error
    location: str
    detail: str


def known_ids(docs_dir: Path) -> set[str]:
    """Every requirement ID that appears anywhere in the documents."""
    ids: set[str] = set()
    for doc in sorted(docs_dir.rglob("*.md")):
        ids.update(_ID_IN_TEXT.findall(doc.read_text(encoding="utf-8")))
    return ids


def _test_nodes(tree: ast.Module) -> Iterator[tuple[str, _TestNode]]:
    for node in tree.body:
        if isinstance(node, _TestNode) and node.name.startswith("test"):
            yield node.name, node
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for item in node.body:
                if isinstance(item, _TestNode) and item.name.startswith("test"):
                    yield f"{node.name}::{item.name}", item


def _req_arguments(node: _TestNode) -> list[ast.expr]:
    args: list[ast.expr] = []
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call) and ast.unparse(decorator.func) == "pytest.mark.req":
            args.extend(decorator.args)
    return args


def _tagged_tests(tests_dir: Path) -> Iterator[tuple[str, list[ast.expr] | SyntaxError]]:
    for path in sorted(tests_dir.rglob("test_*.py")):
        relative = path.relative_to(tests_dir).as_posix()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        except SyntaxError as error:
            yield relative, error
            continue
        for name, node in _test_nodes(tree):
            yield f"{relative}::{name}", _req_arguments(node)


def check(docs_dir: Path, tests_dir: Path) -> list[Problem]:
    known = known_ids(docs_dir)
    problems: list[Problem] = []
    for location, args in _tagged_tests(tests_dir):
        if isinstance(args, SyntaxError):
            problems.append(Problem("syntax_error", location, str(args)))
            continue
        if not args:
            problems.append(Problem("untagged_test", location, ""))
            continue
        for arg in args:
            if not (isinstance(arg, ast.Constant) and isinstance(arg.value, str)):
                problems.append(Problem("invalid_id", location, ast.unparse(arg)))
            elif not _ID_EXACT.fullmatch(arg.value):
                problems.append(Problem("invalid_id", location, arg.value))
            elif arg.value not in known:
                problems.append(Problem("unknown_id", location, arg.value))
    return problems


def report(docs_dir: Path, tests_dir: Path) -> dict[str, list[str]]:
    """Map each valid, known requirement ID to the tests tagged with it."""
    known = known_ids(docs_dir)
    mapping: dict[str, list[str]] = {}
    for location, args in _tagged_tests(tests_dir):
        if isinstance(args, SyntaxError):
            continue
        for arg in args:
            if isinstance(arg, ast.Constant) and arg.value in known:
                mapping.setdefault(arg.value, []).append(location)
    return {req_id: sorted(tests) for req_id, tests in sorted(mapping.items())}


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Check requirement traceability of tests.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail on untagged tests or bad IDs")
    mode.add_argument("--report", action="store_true", help="print requirement ID -> tests")
    parser.add_argument("--docs", type=Path, default=REPO / "docs")
    parser.add_argument("--tests", type=Path, default=REPO / "tests")
    options = parser.parse_args(argv)

    if options.report:
        for req_id, tests in report(options.docs, options.tests).items():
            print(req_id)
            for test in tests:
                print(f"    {test}")
        return 0

    problems = check(options.docs, options.tests)
    for problem in problems:
        print(f"{problem.kind:14} {problem.location}  {problem.detail}".rstrip())
    covered = report(options.docs, options.tests)
    print(f"{len(problems)} problem(s); {len(covered)} requirement ID(s) covered by tests")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
