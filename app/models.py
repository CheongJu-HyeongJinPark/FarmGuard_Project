# 모델 파일 경로
import pathlib
from typing import Any

import torch

# 모델 루트 경로
model_base_path = pathlib.Path(__file__).parent.parent

# 모델 경로
model_paths = {
    "파프리카": model_base_path / "model.pt",
    "포도": model_base_path / "model.pt",
    "토마토": model_base_path / "model.pt",
    "고추": model_base_path / "model.pt",
    "오이": model_base_path / "model.pt",
    "딸기": model_base_path / "model.pt",
}

# 실제 모델을 dict 형태로 변환합니다.
models = {key: torch.hub.load("ultralytics/yolov5", "custom", path=path) for key, path in model_paths.items()}


# 각각 모델을 evaluation 모드로 진입시킵니다
def eval() -> None:
    for model in models.values():
        model.eval()


def get(name: str) -> Any:
    """
    name 에 알맞는 모델을 불러옵니다
    """
    try:
        return models[name]
    except KeyError:
        return None