#!/bin/bash
# Rode na Raspberry: bash setup_pi.sh
cd "$(dirname "$0")"

echo "==> Pacotes do sistema (só o necessário)..."
sudo apt update
sudo apt install -y python3-venv python3-pip i2c-tools python3-smbus \
    python3-libgpiod libgpiod2 || {
    echo "Aviso: apt falhou. Se apareceu erro de libjs-mathjax, rode na Pi:"
    echo "  sudo dpkg --configure -a"
    echo "  sudo apt -f install"
    echo "Depois execute este script de novo."
    exit 1
}

echo "==> Ambiente virtual em ./venv ..."
rm -rf venv
python3 -m venv venv || {
    echo "Erro ao criar venv. Tente: sudo apt install -y python3-venv"
    exit 1
}

./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "==> Habilitar I2C (precisa reboot depois)..."
if command -v raspi-config >/dev/null; then
    sudo raspi-config nonint do_i2c 0 || true
fi
sudo modprobe i2c-dev 2>/dev/null || true
sudo usermod -aG i2c "$USER" 2>/dev/null || true

echo ""
echo "Teste a placa: sudo i2cdetect -y 1   (deve mostrar 40 na linha 40:)"
echo ""
echo "Pronto. Sempre use o Python do venv:"
echo "  ./venv/bin/python servo_pca9685.py 90"
echo "  ./venv/bin/python servo_pca9685.py --sweep"
