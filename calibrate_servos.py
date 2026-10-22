#!/usr/bin/env python3
"""
Calibração interativa dos servos de direção (motores 1–6 / canais 0–5).

Grava três posições por motor em servo_calibration.json:
  frota 0°  → positions["0"]
  frota 90° → positions["90"]  (reto / neutro)
  frota 180° → positions["180"]

Uso na Raspberry:
  ./venv/bin/python calibrate_servos.py
  ./venv/bin/python calibrate_servos.py --motor 6
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import servo_config as sc
from servo_config import DEFAULT_CONFIG_PATH, SERVO_CHANNELS, motor_label

import servo_pca9685 as sp


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Calibração interativa dos servos")
    p.add_argument(
        "--motor",
        type=int,
        choices=range(1, 7),
        help="Começar direto no motor 1–6",
    )
    p.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Arquivo JSON de calibração",
    )
    p.add_argument("--bus", type=int, default=None)
    p.add_argument("--address", type=lambda x: int(x, 0), default=None)
    return p.parse_args()


def print_help() -> None:
    print(
        """
Comandos:
  + / -     ±1° no motor em calibração
  ++ / --   ±5°
  0 9 1     Mover este motor para 0°, 90° ou 180° (jog manual)
  v         Varredura lenta 0° → 180° → 0° (só este motor)

  GRAVAR posição atual para a frota (servo_pca9685.py 0 / 90 / 180):
  g0        Grava como frota 0°
  g9        Grava como frota 90° (reto)
  g1        Grava como frota 180°
  c         Atalho para g9 (neutro)

  TESTE:
  a         Frota 90° nos outros; este motor na posição atual
  t         Testar ângulo de frota (padrão 90)
  f0 f9 f1  Aplicar frota 0 / 90 / 180 em TODOS (com calibração)

  p         Mostrar posições 0/90/180 salvas de todos
  s         Salvar servo_calibration.json
  i         Alternar inversão deste motor
  m         Escolher outro motor
  h         Ajuda
  q         Sair (pergunta se salva)
"""
    )


def choose_motor() -> int:
    print("\nEscolha o motor (1–6):")
    for ch in SERVO_CHANNELS:
        print(f"  {ch + 1} → canal {ch}")
    while True:
        raw = input("Motor: ").strip()
        if raw.lower() in ("q", "sair"):
            raise SystemExit(0)
        try:
            num = int(raw)
            if 1 <= num <= 6:
                return num - 1
        except ValueError:
            pass
        print("Digite um número de 1 a 6.")


def sweep_one(pca, channel: int, config: dict, step: int = 5, delay: float = 0.06) -> None:
    print(f"Varredura {motor_label(channel)}...")
    for angle in range(0, 181, step):
        sp.set_servo_from_config(pca, channel, float(angle), config)
        time.sleep(delay)
    for angle in range(180, -1, -step):
        sp.set_servo_from_config(pca, channel, float(angle), config)
        time.sleep(delay)
    print("Varredura concluída.")


def apply_fleet_pose(
    pca,
    config: dict,
    fleet_angle: float,
    hold_channel: int | None = None,
    hold_logical: float | None = None,
) -> None:
    for ch in SERVO_CHANNELS:
        if hold_channel is not None and ch == hold_channel and hold_logical is not None:
            logical = hold_logical
        else:
            logical = sc.fleet_to_logical(config, ch, fleet_angle)
        sp.set_servo_from_config(pca, ch, logical, config)
        time.sleep(sp.STAGGER_S)


def apply_fleet_all(pca, config: dict, fleet_key: str) -> None:
    fleet_angle = float(fleet_key)
    apply_fleet_pose(pca, config, fleet_angle)


def save_fleet_position(
    config: dict,
    channel: int,
    fleet_key: str,
    logical: float,
) -> None:
    sc.set_fleet_position(config, channel, fleet_key, logical)
    label = {"0": "0°", "90": "90° (reto)", "180": "180°"}[fleet_key]
    print(
        f"Gravado {motor_label(channel)} → frota {label} = {logical:.1f}° lógico "
        f"(hw {sc.map_to_hardware(config, channel, logical):.1f}°)",
    )


def print_status(channel: int, logical: float, config: dict) -> None:
    entry = sc.get_channel(config, channel)
    pos = sc.get_positions(config, channel)
    hw = sc.map_to_hardware(config, channel, logical)
    print(
        f"\n{motor_label(channel)} | jog: {logical:5.1f}° | hw: {hw:5.1f}°",
    )
    print(
        f"  Salvo → frota 0°={pos['0']:.1f}° | 90°={pos['90']:.1f}° | 180°={pos['180']:.1f}° | "
        f"invert={entry['invert']}",
    )


def print_all_positions(config: dict) -> None:
    print("\nPosições calibradas (ângulo lógico por motor):")
    print(f"  {'Motor':<14} {'frota 0°':>8} {'frota 90°':>9} {'frota 180°':>10}  inv")
    for ch in SERVO_CHANNELS:
        pos = sc.get_positions(config, ch)
        inv = sc.get_channel(config, ch)["invert"]
        print(
            f"  {motor_label(ch):<14} {pos['0']:>8.1f} {pos['90']:>9.1f} "
            f"{pos['180']:>10.1f}  {inv}",
        )


def calibration_loop(
    pca,
    config: dict,
    config_path: Path,
    start_channel: int | None,
) -> None:
    channel = start_channel if start_channel is not None else choose_motor()
    entry = sc.get_channel(config, channel)
    logical = float(sc.get_positions(config, channel)["90"])
    dirty = False

    print_help()
    print(
        "\nCalibração em 3 pontos: alinhe cada motor e use g0 / g9 / g1 para gravar.\n"
        "Depois teste com f0, f9, f1 (frota inteira)."
    )
    print_status(channel, logical, config)

    while True:
        cmd = input("> ").strip().lower()
        if not cmd:
            continue

        if cmd in ("q", "quit", "sair"):
            if dirty:
                save = input("Salvar calibração antes de sair? [S/n]: ").strip().lower()
                if save in ("", "s", "sim", "y", "yes"):
                    sc.save_config(config, config_path)
                    print(f"Salvo em {config_path}")
            break

        if cmd == "m":
            channel = choose_motor()
            logical = float(sc.get_positions(config, channel)["90"])
            print_status(channel, logical, config)
            continue

        if cmd in ("h", "?"):
            print_help()
            continue

        if cmd in ("g0", "save0"):
            save_fleet_position(config, channel, "0", logical)
            dirty = True
            print_status(channel, logical, config)
            continue
        if cmd in ("g9", "g90", "save90", "c"):
            save_fleet_position(config, channel, "90", logical)
            dirty = True
            print_status(channel, logical, config)
            continue
        if cmd in ("g1", "g180", "save180"):
            save_fleet_position(config, channel, "180", logical)
            dirty = True
            print_status(channel, logical, config)
            continue

        if cmd == "f0":
            apply_fleet_all(pca, config, "0")
            print("Frota 0° aplicada em todos.")
            continue
        if cmd in ("f9", "f90"):
            apply_fleet_all(pca, config, "90")
            print("Frota 90° aplicada em todos.")
            continue
        if cmd in ("f1", "f180"):
            apply_fleet_all(pca, config, "180")
            print("Frota 180° aplicada em todos.")
            continue

        if cmd == "+":
            logical = min(180.0, logical + 1.0)
        elif cmd == "-":
            logical = max(0.0, logical - 1.0)
        elif cmd == "++":
            logical = min(180.0, logical + 5.0)
        elif cmd == "--":
            logical = max(0.0, logical - 5.0)
        elif cmd == "0":
            logical = 0.0
        elif cmd in ("9", "90"):
            logical = float(config["fleet_neutral"])
        elif cmd in ("1", "180"):
            logical = 180.0
        elif cmd == "v":
            sweep_one(pca, channel, config)
            continue
        elif cmd == "a":
            print("Frota 90° nos demais; este motor na posição atual.")
            apply_fleet_pose(
                pca,
                config,
                float(config["fleet_neutral"]),
                hold_channel=channel,
                hold_logical=logical,
            )
            print("Ajuste com +/- e grave com g0 / g9 / g1.")
            continue
        elif cmd == "t":
            raw = input("Ângulo de frota para testar [90]: ").strip()
            fleet = float(raw) if raw else float(config["fleet_neutral"])
            apply_fleet_pose(
                pca,
                config,
                fleet,
                hold_channel=channel,
                hold_logical=logical,
            )
            print(f"Frota em {fleet:.0f}° aplicada.")
            continue
        elif cmd == "p":
            print_all_positions(config)
            continue
        elif cmd == "s":
            sc.save_config(config, config_path)
            dirty = False
            print(f"Salvo em {config_path}")
            continue
        elif cmd == "i":
            raw = input("Inverter este motor? [s/N]: ").strip().lower()
            entry["invert"] = raw in ("s", "sim", "y", "yes")
            dirty = True
            print(f"Invert={entry['invert']}")
            continue
        else:
            print("Comando desconhecido. Use h para ajuda.")
            continue

        sp.set_servo_from_config(pca, channel, logical, config)
        print_status(channel, logical, config)


def main() -> None:
    args = parse_args()
    config_path = args.config
    config = sc.load_config(config_path)
    sc.apply_runtime_globals(config)

    bus = args.bus if args.bus is not None else int(config["i2c_bus"])
    address = args.address if args.address is not None else int(config["i2c_address"])

    try:
        pca = sp.create_pca9685(bus, address)
    except (ImportError, OSError, RuntimeError) as e:
        print(f"Erro ao abrir PCA9685: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Calibração roboBio | i2c-{bus} | 0x{address:02x}")
    print(f"Arquivo: {config_path}")

    start_ch = (args.motor - 1) if args.motor else None
    try:
        calibration_loop(pca, config, config_path, start_ch)
    finally:
        pca.deinit()
        print("PWM liberado.")


if __name__ == "__main__":
    main()
