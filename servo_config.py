"""Configuração e calibração por motor (salva em servo_calibration.json)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_VERSION = 2
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "servo_calibration.json"
FLEET_NEUTRAL = 90.0
FLEET_MIN = 0.0
FLEET_MAX = 180.0

SERVO_FIRST = 0
SERVO_LAST = 5
SERVO_CHANNELS = list(range(SERVO_FIRST, SERVO_LAST + 1))

FLEET_KEYS = ("0", "90", "180")

DEFAULT_CHANNEL_INVERT: dict[int, bool] = {
    0: False,
    1: False,
    2: False,
    3: True,
    4: True,
    5: True,
}

DEFAULT_CHANNEL_TRIM: dict[int, float] = {ch: 0.0 for ch in SERVO_CHANNELS}


def default_positions(channel: int | None = None) -> dict[str, float]:
    """Posições lógicas quando a frota pede 0°, 90° e 180°."""
    base = float(FLEET_NEUTRAL)
    return {"0": FLEET_MIN, "90": base, "180": FLEET_MAX}


def default_channel_entry(channel: int) -> dict[str, Any]:
    positions = default_positions(channel)
    return {
        "positions": positions,
        "neutral": positions["90"],
        "invert": DEFAULT_CHANNEL_INVERT.get(channel, False),
        "trim": DEFAULT_CHANNEL_TRIM.get(channel, 0.0),
        "min_limit": 0.0,
        "max_limit": 180.0,
    }


def default_config() -> dict[str, Any]:
    return {
        "version": CONFIG_VERSION,
        "fleet_neutral": FLEET_NEUTRAL,
        "i2c_bus": 1,
        "i2c_address": 0x40,
        "channels": {
            str(ch): default_channel_entry(ch) for ch in SERVO_CHANNELS
        },
    }


def normalize_positions(entry: dict[str, Any]) -> dict[str, float]:
    """Garante positions {0,90,180}; migra 'neutral' legado se necessário."""
    raw = entry.get("positions")
    if isinstance(raw, dict) and all(k in raw for k in FLEET_KEYS):
        return {k: float(raw[k]) for k in FLEET_KEYS}

    neutral = float(entry.get("neutral", FLEET_NEUTRAL))
    offset = neutral - FLEET_NEUTRAL
    return {
        "0": max(0.0, min(180.0, FLEET_MIN + offset)),
        "90": neutral,
        "180": max(0.0, min(180.0, FLEET_MAX + offset)),
    }


def sync_neutral_from_positions(entry: dict[str, Any]) -> None:
    entry["positions"] = normalize_positions(entry)
    entry["neutral"] = entry["positions"]["90"]


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    path = Path(path or DEFAULT_CONFIG_PATH)
    if not path.is_file():
        return default_config()
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return merge_with_defaults(data)


def merge_with_defaults(data: dict[str, Any]) -> dict[str, Any]:
    base = default_config()
    base["version"] = CONFIG_VERSION
    base["fleet_neutral"] = float(data.get("fleet_neutral", FLEET_NEUTRAL))
    base["i2c_bus"] = int(data.get("i2c_bus", 1))
    base["i2c_address"] = int(data.get("i2c_address", 0x40))
    channels_in = data.get("channels", {})
    for ch in SERVO_CHANNELS:
        key = str(ch)
        merged = default_channel_entry(ch)
        if key in channels_in:
            merged.update(channels_in[key])
        sync_neutral_from_positions(merged)
        merged["invert"] = bool(merged["invert"])
        merged["trim"] = float(merged["trim"])
        merged["min_limit"] = float(merged["min_limit"])
        merged["max_limit"] = float(merged["max_limit"])
        base["channels"][key] = merged
    return base


def save_config(config: dict[str, Any], path: Path | str | None = None) -> Path:
    path = Path(path or DEFAULT_CONFIG_PATH)
    config = merge_with_defaults(config)
    for ch in SERVO_CHANNELS:
        sync_neutral_from_positions(config["channels"][str(ch)])
    with path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return path


def get_channel(config: dict[str, Any], channel: int) -> dict[str, Any]:
    return config["channels"][str(channel)]


def get_positions(config: dict[str, Any], channel: int) -> dict[str, float]:
    entry = get_channel(config, channel)
    return {k: float(entry["positions"][k]) for k in FLEET_KEYS}


def set_fleet_position(
    config: dict[str, Any],
    channel: int,
    fleet_key: str,
    logical_angle: float,
) -> None:
    if fleet_key not in FLEET_KEYS:
        raise ValueError(f"Posição de frota inválida: {fleet_key}")
    entry = get_channel(config, channel)
    entry["positions"][fleet_key] = round(max(0.0, min(180.0, float(logical_angle))), 1)
    sync_neutral_from_positions(entry)


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def fleet_to_logical(config: dict[str, Any], channel: int, fleet_angle: float) -> float:
    """
    Mapeia comando de frota (0 / 90 / 180 ou interpolação) → ângulo lógico do canal.
    Três pontos calibrados por motor: positions['0'], ['90'], ['180'].
    """
    pos = get_positions(config, channel)
    fleet = max(FLEET_MIN, min(FLEET_MAX, float(fleet_angle)))
    mid = float(config["fleet_neutral"])

    if fleet <= mid:
        t = fleet / mid if mid > 0 else 0.0
        logical = _lerp(pos["0"], pos["90"], t)
    else:
        span = FLEET_MAX - mid
        t = (fleet - mid) / span if span > 0 else 0.0
        logical = _lerp(pos["90"], pos["180"], t)

    return max(0.0, min(180.0, logical))


def map_to_hardware(
    config: dict[str, Any],
    channel: int,
    logical_angle: float,
    raw: bool = False,
) -> float:
    angle = max(0.0, min(180.0, float(logical_angle)))
    entry = get_channel(config, channel)
    if not raw and entry["invert"]:
        angle = 180.0 - angle
    angle += float(entry["trim"])
    angle = max(float(entry["min_limit"]), min(float(entry["max_limit"]), angle))
    return max(0.0, min(180.0, angle))


def apply_runtime_globals(config: dict[str, Any]) -> None:
    """Atualiza constantes usadas por servo_pca9685.py."""
    import servo_pca9685 as sp

    sp.CHANNEL_INVERT = {ch: get_channel(config, ch)["invert"] for ch in SERVO_CHANNELS}
    sp.CHANNEL_TRIM = {ch: float(get_channel(config, ch)["trim"]) for ch in SERVO_CHANNELS}
    sp.CHANNEL_NEUTRAL = {
        ch: float(get_positions(config, ch)["90"]) for ch in SERVO_CHANNELS
    }
    sp.FLEET_NEUTRAL = float(config["fleet_neutral"])
    sp._ACTIVE_CONFIG = config  # noqa: SLF001


def motor_label(channel: int) -> str:
    return f"Motor {channel + 1} (canal {channel})"
