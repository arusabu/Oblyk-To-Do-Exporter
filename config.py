from dataclasses import dataclass
from pathlib import Path
import tomllib

@dataclass(frozen=True)
class Gym:
    id: int


@dataclass(frozen=True)
class GradeRange:
    grade_min: str
    grade_max: str


@dataclass(frozen=True)
class Config:
    gym: Gym
    top_rope: GradeRange
    lead: GradeRange


def load_config() -> Config:
    config_path = Path("config.toml")

    with config_path.open("rb") as file:
        data = tomllib.load(file)

    return Config(
        gym=Gym(**data["gym"]),
        top_rope=GradeRange(**data["top_rope"]),
        lead=GradeRange(**data["lead"]),
    )