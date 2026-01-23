from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Optional


def _find_repo_root(start: Path) -> Path:
    candidates = [start] + list(start.parents)
    for path in candidates:
        if (path / "README.md").exists() or (path / ".git").exists():
            return path
    return start


def _default_root() -> Path:
    env_root = os.environ.get("HTM_ROOT") or os.environ.get("HTM_BASE_DIR")
    if env_root:
        return Path(env_root).expanduser().resolve()

    colab_drive = Path("/content/drive/MyDrive")
    if colab_drive.exists():
        return colab_drive / "HebrewTopicModel"

    kaggle_working = Path("/kaggle/working")
    if kaggle_working.exists():
        return kaggle_working / "HebrewTopicModel"

    return _find_repo_root(Path.cwd())


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    data_dir: Path
    models_dir: Path
    results_dir: Path

    def ensure(self) -> "ProjectPaths":
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        return self


def get_paths(root: Optional[Path | str] = None) -> ProjectPaths:
    base = Path(root).expanduser().resolve() if root else _default_root()

    data_dir = Path(os.environ.get("HTM_DATA_DIR") or base / "data")
    models_dir = Path(os.environ.get("HTM_MODELS_DIR") or base / "models")
    results_dir = Path(os.environ.get("HTM_RESULTS_DIR") or base / "results_artifacts")

    return ProjectPaths(
        root=base,
        data_dir=data_dir,
        models_dir=models_dir,
        results_dir=results_dir,
    )
