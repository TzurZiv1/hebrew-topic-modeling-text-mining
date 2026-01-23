from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from project_paths import get_paths


NOTEBOOKS = [
    "notebooks/hebrew_topic_stage1_datasets_prep final.ipynb",
    "notebooks/hebrew_topic_stage2_preprocessing final.ipynb",
    "notebooks/hebrew_topic_stage3_baselines_cpu final.ipynb",
    "notebooks/hebrew_topic_stage3_top2vec_gpu final.ipynb",
    "notebooks/hebrew_topic_stage-4-advanced-topic-models-final.ipynb",
    "notebooks/hebrew_topic_stage5_comparison_notebook_fixed.ipynb",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Hebrew topic modeling pipeline notebooks in order."
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually execute notebooks (default: dry-run).",
    )
    parser.add_argument(
        "--from-stage",
        type=int,
        default=1,
        choices=range(1, 6),
        help="Start from stage number (1-5).",
    )
    parser.add_argument(
        "--to-stage",
        type=int,
        default=5,
        choices=range(1, 6),
        help="End at stage number (1-5).",
    )
    parser.add_argument(
        "--skip-top2vec",
        action="store_true",
        help="Skip the GPU Top2Vec notebook (stage 3b).",
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=None,
        help="Override project root (also sets HTM_ROOT).",
    )
    parser.add_argument(
        "--data-root",
        type=str,
        default=None,
        help="Override data directory (sets HTM_DATA_DIR).",
    )
    parser.add_argument(
        "--models-root",
        type=str,
        default=None,
        help="Override models directory (sets HTM_MODELS_DIR).",
    )
    parser.add_argument(
        "--results-root",
        type=str,
        default=None,
        help="Override results directory (sets HTM_RESULTS_DIR).",
    )
    return parser.parse_args()


def stage_filter(paths: list[str], from_stage: int, to_stage: int, skip_top2vec: bool) -> list[str]:
    stage_map = {
        1: [paths[0]],
        2: [paths[1]],
        3: [paths[2], paths[3]],
        4: [paths[4]],
        5: [paths[5]],
    }
    selected = []
    for stage in range(from_stage, to_stage + 1):
        selected.extend(stage_map[stage])
    if skip_top2vec:
        selected = [p for p in selected if "stage3_top2vec" not in p]
    return selected


def build_env(args: argparse.Namespace) -> dict[str, str]:
    env = os.environ.copy()
    if args.project_root:
        env["HTM_ROOT"] = args.project_root
    if args.data_root:
        env["HTM_DATA_DIR"] = args.data_root
    if args.models_root:
        env["HTM_MODELS_DIR"] = args.models_root
    if args.results_root:
        env["HTM_RESULTS_DIR"] = args.results_root
    return env


def run_notebook(nb_path: Path, execute: bool, env: dict[str, str]) -> None:
    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        str(nb_path),
    ]
    if execute:
        subprocess.run(cmd, check=True, env=env)
    else:
        print("DRY-RUN:", " ".join(cmd))


def main() -> int:
    args = parse_args()
    selected = stage_filter(NOTEBOOKS, args.from_stage, args.to_stage, args.skip_top2vec)

    paths = get_paths(args.project_root).ensure()
    env = build_env(args)

    print("Using project root :", paths.root)
    print("Using data dir     :", paths.data_dir)
    print("Using models dir   :", paths.models_dir)
    print("Using results dir  :", paths.results_dir)
    print("Execute notebooks  :", args.execute)

    for nb in selected:
        nb_path = Path(nb)
        if not nb_path.exists():
            print("Missing notebook:", nb_path)
            return 1
        run_notebook(nb_path, args.execute, env)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
