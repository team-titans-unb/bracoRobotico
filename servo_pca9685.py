#!/usr/bin/env python3
"""
Controle de servos via PCA9685 (Adafruit CircuitPython).

Motores do projeto: canais 0 a 5 (6 servos).

Ligação:
  Pi 3.3V -> VCC | SDA -> SDA | SCL -> SCL | GND -> GND
  Fonte 5V -> V+ e GND do terminal verde (servos)
  Servos nos canais PWM 0, 1, 2, 3, 4, 5

Uso:
  ./venv/bin/python servo_pca9685.py 90              # todos 0–5 em 90°
  ./venv/bin/python servo_pca9685.py --angles 0,45,90,90,45,0
  ./venv/bin/python servo_pca9685.py -c 2 45         # só canal 2
  ./venv/bin/python servo_pca9685.py --sweep         # varre todos 0–5 juntos
  ./venv/bin/python servo_pca9685.py --sweep -c 0    # varre só canal 0
"""

from __future__ import annotations

import argparse
import os
import sys
import time

PULSE_MIN_US = 500
PULSE_MAX_US = 2500
SERVO_PERIOD_US = 20_000
SERVO_HZ = 50
DEFAULT_I2C_BUS = 1
DEFAULT_ADDRESS = 0x40

# Motores do robô (PCA9685 canais 0–5)
SERVO_FIRST = 0
SERVO_LAST = 5
SERVO_CHANNELS = list(range(SERVO_FIRST, SERVO_LAST + 1))
STAGGER_S = 0.01  # atraso entre canais (reduz pico de corrente)
NEUTRAL_ANGLE = 90.0

# Montagem espelhada: mesmo ângulo no código ≠ mesma direção física.
# Canais 0–2 = esquerda | 3–5 = direita (ajuste se a fiação for outra).
# True → envia (180 - ângulo) ao servo para alinhar com o lado oposto.
CHANNEL_INVERT: dict[int, bool] = {
    0: False,
    1: False,
    2: False,
    3: True,
    4: True,
    5: True,
}

# Ajuste fino por canal (°). Sobrescrito por servo_calibration.json se existir.
CHANNEL_TRIM: dict[int, float] = {ch: 0.0 for ch in SERVO_CHANNELS}

# Neutro por motor quando a frota recebe fleet_neutral (90°). Calibre com calibrate_servos.py
CHANNEL_NEUTRAL: dict[int, float] = {ch: NEUTRAL_ANGLE for ch in SERVO_CHANNELS}
FLEET_NEUTRAL = NEUTRAL_ANGLE
_ACTIVE_CONFIG: dict | None = None


def load_calibration(config_path: str | None = None) -> None:
    """Carrega servo_calibration.json e aplica invert/trim/neutro."""
    import servo_config as sc

    path = config_path or sc.DEFAULT_CONFIG_PATH
    config = sc.load_config(path)
    sc.apply_runtime_globals(config)


def fleet_to_logical(channel: int, fleet_angle: float) -> float:
    """Converte comando da frota (ex. 90° reto) em ângulo lógico do canal."""
    if _ACTIVE_CONFIG is not None:
        import servo_config as sc

        return sc.fleet_to_logical(_ACTIVE_CONFIG, channel, fleet_angle)
    offset = CHANNEL_NEUTRAL.get(channel, FLEET_NEUTRAL) - FLEET_NEUTRAL
    return max(0.0, min(180.0, float(fleet_angle) + offset))


def map_steering_angle(channel: int, angle: float, raw: bool = False) -> float:
    """Ângulo lógico → ângulo no hardware (inversão L/R + trim)."""
    if _ACTIVE_CONFIG is not None and not raw:
        import servo_config as sc

        return sc.map_to_hardware(_ACTIVE_CONFIG, channel, angle, raw=False)
    angle = max(0.0, min(180.0, float(angle)))
    if not raw and CHANNEL_INVERT.get(channel, False):
        angle = 180.0 - angle
    angle += CHANNEL_TRIM.get(channel, 0.0)
    return max(0.0, min(180.0, angle))


def set_servo_from_config(
    pca,
    channel: int,
    logical_angle: float,
    config: dict,
    raw: bool = False,
    min_us: int = PULSE_MIN_US,
    max_us: int = PULSE_MAX_US,
) -> None:
    import servo_config as sc

    if raw:
        hw = max(0.0, min(180.0, float(logical_angle)))
    else:
        hw = sc.map_to_hardware(config, channel, logical_angle, raw=False)
    pca.channels[channel].duty_cycle = angle_to_duty(hw, min_us, max_us)


def parse_trim_overrides(items: list[str] | None) -> dict[int, float]:
    """Ex.: ['5:-20', '2:5'] → {5: -20.0, 2: 5.0}"""
    overrides: dict[int, float] = {}
    if not items:
        return overrides
    for item in items:
        part = item.strip()
        if ":" not in part:
            raise ValueError(f"--trim inválido: {part!r} (use canal:graus, ex. 5:-20)")
        ch_s, delta_s = part.split(":", 1)
        overrides[int(ch_s)] = float(delta_s)
    return overrides


def angle_to_duty(
    angle: float,
    min_us: int = PULSE_MIN_US,
    max_us: int = PULSE_MAX_US,
) -> int:
    angle = max(0.0, min(180.0, float(angle)))
    pulse_us = min_us + (angle / 180.0) * (max_us - min_us)
    return int((pulse_us / SERVO_PERIOD_US) * 65535)


def setup_blinka_i2c_bus(bus: int) -> None:
    os.environ["BLINKA_I2C_ADAPTER"] = str(bus)


def create_pca9685(bus: int, address: int):
    setup_blinka_i2c_bus(bus)
    import board  # noqa: WPS433
    from adafruit_pca9685 import PCA9685  # noqa: WPS433

    i2c = board.I2C()
    pca = PCA9685(i2c, address=address)
    pca.frequency = SERVO_HZ
    return pca


def set_servo(
    pca,
    channel: int,
    angle: float,
    min_us: int = PULSE_MIN_US,
    max_us: int = PULSE_MAX_US,
    raw: bool = False,
) -> None:
    if channel < 0 or channel > 15:
        raise ValueError(f"Canal inválido: {channel} (use 0–15)")
    hw_angle = map_steering_angle(channel, angle, raw=raw)
    pca.channels[channel].duty_cycle = angle_to_duty(hw_angle, min_us, max_us)


def set_servos(
    pca,
    angles_by_channel: dict[int, float],
    min_us: int = PULSE_MIN_US,
    max_us: int = PULSE_MAX_US,
    stagger: bool = True,
    raw: bool = False,
) -> None:
    channels = sorted(angles_by_channel.keys())
    for i, channel in enumerate(channels):
        set_servo(pca, channel, angles_by_channel[channel], min_us, max_us, raw=raw)
        if stagger and i < len(channels) - 1:
            time.sleep(STAGGER_S)


def set_all_same_angle(
    pca,
    angle: float,
    channels: list[int] | None = None,
    min_us: int = PULSE_MIN_US,
    max_us: int = PULSE_MAX_US,
    raw: bool = False,
    fleet: bool = True,
) -> None:
    """Comando de frota (ex. 90°): aplica neutro calibrado por motor."""
    chans = channels if channels is not None else SERVO_CHANNELS
    if raw or not fleet:
        angles = {ch: angle for ch in chans}
    else:
        angles = {ch: fleet_to_logical(ch, angle) for ch in chans}
    set_servos(
        pca,
        angles,
        min_us=min_us,
        max_us=max_us,
        raw=raw,
    )


def parse_angles_list(text: str) -> dict[int, float]:
    """Ex.: '0,45,90,90,45,0' -> {0:0, 1:45, ...} para canais 0–5."""
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != len(SERVO_CHANNELS):
        raise ValueError(
            f"--angles precisa de {len(SERVO_CHANNELS)} valores "
            f"(canais {SERVO_FIRST}–{SERVO_LAST}), recebeu {len(parts)}",
        )
    return {ch: float(parts[i]) for i, ch in enumerate(SERVO_CHANNELS)}


def sweep_channel(
    pca,
    channel: int,
    step: int = 10,
    delay_s: float = 0.05,
    min_us: int = PULSE_MIN_US,
    max_us: int = PULSE_MAX_US,
    raw: bool = False,
) -> None:
    for angle in range(0, 181, step):
        set_servo(pca, channel, angle, min_us, max_us, raw=raw)
        time.sleep(delay_s)
    for angle in range(180, -1, -step):
        set_servo(pca, channel, angle, min_us, max_us, raw=raw)
        time.sleep(delay_s)


def sweep_channels(
    pca,
    channels: list[int],
    step: int = 10,
    delay_s: float = 0.05,
    min_us: int = PULSE_MIN_US,
    max_us: int = PULSE_MAX_US,
    raw: bool = False,
    fleet: bool = True,
) -> None:
    """Varredura sincronizada (com calibração de frota se fleet=True)."""
    for angle in range(0, 181, step):
        if raw or not fleet:
            angles = {ch: float(angle) for ch in channels}
        else:
            angles = {ch: fleet_to_logical(ch, float(angle)) for ch in channels}
        set_servos(pca, angles, min_us=min_us, max_us=max_us, raw=raw)
        time.sleep(delay_s)
    for angle in range(180, -1, -step):
        if raw or not fleet:
            angles = {ch: float(angle) for ch in channels}
        else:
            angles = {ch: fleet_to_logical(ch, float(angle)) for ch in channels}
        set_servos(pca, angles, min_us=min_us, max_us=max_us, raw=raw)
        time.sleep(delay_s)


def format_angles(angles: dict[int, float], raw: bool = False) -> str:
    parts = []
    for ch in sorted(angles):
        hw = angles[ch] if raw else map_steering_angle(ch, angles[ch])
        parts.append(f"{ch}:{angles[ch]:.0f}°→{hw:.0f}°")
    return ", ".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Servos 0–5 na PCA9685 (adafruit_pca9685)",
    )
    parser.add_argument(
        "angle",
        nargs="?",
        type=float,
        help="Ângulo 0–180 para todos os motores 0–5 (ou um canal com -c)",
    )
    parser.add_argument(
        "--angles",
        type=str,
        metavar="LIST",
        help="Ângulos por canal: 6 valores para 0,1,2,3,4,5 (ex.: 0,45,90,90,45,0)",
    )
    parser.add_argument(
        "-c",
        "--channel",
        type=int,
        default=None,
        help="Controlar só este canal (0–15). Sem -c: motores 0–5",
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Varre 0°–180°–0° (todos 0–5, ou só -c se informado)",
    )
    parser.add_argument(
        "--bus",
        type=int,
        default=DEFAULT_I2C_BUS,
        help=f"Barramento I2C (padrão: {DEFAULT_I2C_BUS})",
    )
    parser.add_argument(
        "--address",
        type=lambda x: int(x, 0),
        default=DEFAULT_ADDRESS,
        help="Endereço I2C (padrão: 0x40)",
    )
    parser.add_argument("--min-us", type=int, default=PULSE_MIN_US)
    parser.add_argument("--max-us", type=int, default=PULSE_MAX_US)
    parser.add_argument(
        "--release",
        action="store_true",
        help="Para PWM ao sair (deinit)",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Sem inversão por lado (ângulo direto no servo; só calibração)",
    )
    parser.add_argument(
        "--trim",
        action="append",
        metavar="CH:DELTA",
        help="Trim por canal em graus (ex. 5:-20 para motor 6 / canal 5)",
    )
    parser.add_argument(
        "--nudge",
        metavar="CH:DELTA",
        help="Só um canal: parte de 0° lógico + delta (ex. 5:20 = motor 6 gira ~20°)",
    )
    parser.add_argument(
        "--no-calibration",
        action="store_true",
        help="Ignora servo_calibration.json",
    )
    parser.add_argument(
        "--no-fleet",
        action="store_true",
        help="Mesmo número em todos os canais (sem offset de neutro)",
    )
    return parser.parse_args()


def resolve_target_channels(args: argparse.Namespace) -> list[int]:
    if args.channel is not None:
        return [args.channel]
    return SERVO_CHANNELS.copy()


def main() -> None:
    args = parse_args()
    targets = resolve_target_channels(args)

    if not args.no_calibration:
        load_calibration()

    global CHANNEL_TRIM
    trim_overrides = parse_trim_overrides(args.trim)
    if trim_overrides:
        CHANNEL_TRIM = {**CHANNEL_TRIM, **trim_overrides}

    use_fleet = not args.no_fleet

    if (
        not args.sweep
        and args.angle is None
        and args.angles is None
        and args.nudge is None
    ):
        print(
            "Informe um ângulo, --angles, --nudge ou --sweep.\n"
            "  Ex.: servo_pca9685.py 90\n"
            "  Ex.: servo_pca9685.py --nudge 5:20",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.angles is not None and args.channel is not None:
        print("Use --angles OU -c, não os dois.", file=sys.stderr)
        sys.exit(1)

    if args.nudge is not None and (
        args.angle is not None or args.angles is not None or args.sweep
    ):
        print("Use --nudge sozinho (sem ângulo posicional nem --sweep).", file=sys.stderr)
        sys.exit(1)

    try:
        pca = create_pca9685(args.bus, args.address)
    except ImportError:
        print(
            "Bibliotecas Adafruit não instaladas.\n"
            "  ./venv/bin/pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)
    except (OSError, ValueError, RuntimeError) as e:
        print(f"Erro ao abrir PCA9685: {e}", file=sys.stderr)
        sys.exit(1)

    label = (
        f"canal {args.channel}"
        if args.channel is not None
        else f"motores {SERVO_FIRST}–{SERVO_LAST}"
    )
    print(
        f"PCA9685 0x{args.address:02x} | i2c-{args.bus} | {label} | {SERVO_HZ} Hz",
    )

    try:
        if args.nudge is not None:
            nudge_map = parse_trim_overrides([args.nudge])
            if len(nudge_map) != 1:
                print("--nudge use um par canal:delta (ex. 5:20)", file=sys.stderr)
                sys.exit(1)
            ch, delta = next(iter(nudge_map.items()))
            logical = max(0.0, min(180.0, 0.0 + delta))
            set_servo(
                pca,
                ch,
                logical,
                min_us=args.min_us,
                max_us=args.max_us,
                raw=args.raw,
            )
            hw = map_steering_angle(ch, logical, raw=args.raw)
            motor_num = ch + 1
            print(
                f"Motor {motor_num} (canal {ch}): 0° + {delta:+.0f}° "
                f"→ lógico {logical:.0f}° → hardware {hw:.0f}°",
            )
            if not args.release:
                time.sleep(0.5)
            return

        if args.sweep:
            if args.channel is not None:
                print(f"Varredura canal {args.channel}...")
                sweep_channel(
                    pca,
                    args.channel,
                    min_us=args.min_us,
                    max_us=args.max_us,
                    raw=args.raw,
                )
            else:
                print(f"Varredura motores {SERVO_FIRST}–{SERVO_LAST} (sincronizado)...")
                sweep_channels(
                    pca,
                    SERVO_CHANNELS,
                    min_us=args.min_us,
                    max_us=args.max_us,
                    raw=args.raw,
                    fleet=use_fleet,
                )
            print("Pronto.")
            return

        if args.angles is not None:
            try:
                angles_map = parse_angles_list(args.angles)
            except ValueError as e:
                print(e, file=sys.stderr)
                sys.exit(1)
            set_servos(
                pca,
                angles_map,
                min_us=args.min_us,
                max_us=args.max_us,
                raw=args.raw,
            )
            print(format_angles(angles_map, raw=args.raw))
            return

        if args.channel is not None:
            set_servo(
                pca,
                args.channel,
                args.angle,
                min_us=args.min_us,
                max_us=args.max_us,
                raw=args.raw,
            )
            hw = map_steering_angle(args.channel, args.angle, raw=args.raw)
            print(f"Canal {args.channel} lógico {args.angle:.0f}° → hardware {hw:.0f}°")
        else:
            set_all_same_angle(
                pca,
                args.angle,
                channels=targets,
                min_us=args.min_us,
                max_us=args.max_us,
                raw=args.raw,
                fleet=use_fleet,
            )
            mode = "frota+calibração" if use_fleet and not args.raw else "direto"
            print(f"Motores {SERVO_FIRST}–{SERVO_LAST} -> {args.angle:.0f}° ({mode})")

        if not args.release:
            time.sleep(0.5)
    finally:
        if args.release:
            pca.deinit()
            print("PWM liberado (deinit).")


if __name__ == "__main__":
    main()
