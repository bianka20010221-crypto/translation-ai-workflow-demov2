from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import TranslationRequest
from .workflow import WorkflowService


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the fictional translation workflow demo")
    parser.add_argument("--request", required=True, help="Path to a JSON translation request")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()

    payload = json.loads(Path(args.request).read_text(encoding="utf-8"))
    result = WorkflowService().run(TranslationRequest(**payload))
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
