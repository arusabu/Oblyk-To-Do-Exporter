from __future__ import annotations

def blank() -> None:
    print()

def title(title: str) -> None:
    print("=" * len(title))
    print(title)
    print("=" * len(title))

def info(message: str) -> None:
    print(message)

def success(message: str) -> None:
    print(f"✓ {message}")

def warning(message: str) -> None:
    print(f"⚠ {message}")

def error(message: str) -> None:
    print(f"✗ {message}")

def item(label: str, value: object, label_width: int) -> None:
    print(f"{label:.<{label_width}} {value}")