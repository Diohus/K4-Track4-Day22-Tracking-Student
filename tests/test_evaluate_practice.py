"""Kiểm tra cấu hình chấm của video luyện không cần ảnh lab."""

import json

from evaluate_practice import _load_eval_config, run_trackeval


def test_missing_config_uses_lab_defaults(tmp_path):
    assert _load_eval_config(tmp_path) == {"benchmark": "LAB21", "split": "train"}


def test_supplied_config_takes_priority(tmp_path):
    video_dir = tmp_path / "video_1"
    video_dir.mkdir()
    (video_dir / "eval_config.json").write_text(
        json.dumps({"benchmark": "CUSTOM", "split": "train"}), encoding="utf-8"
    )
    assert _load_eval_config(tmp_path)["benchmark"] == "CUSTOM"


def test_numpy_aliases_are_available_in_trackeval_process(tmp_path):
    script_dir = tmp_path / "scripts"
    script_dir.mkdir()
    (script_dir / "run_mot_challenge.py").write_text(
        "import numpy as np\nassert np.float is float\nassert np.int is int\n",
        encoding="utf-8",
    )
    run_trackeval(tmp_path, "luot_thu", "LAB21", "train")
