#pragma once

#include <chrono>

class PID {
	public:
		// Coeficientes proporcional, integral e diferencial
		double	Kp;
		double	Ki;
		double	Kd;

		// Variável de controle
		double var;

		// Relógio do sintonizador
		// Utilizado para o cálculo dos termos integral e diferencial
		std::chrono::steady_clock::time_point time;

		// Erro acumulado para o termo integral
		double	err_I;

		// Construtor
		PID(double var, double Kp, double Ki, double Kd);

		// Obter ômega
		double	compute(double target);
};