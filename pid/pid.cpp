#include <iostream.h>
#include <chrono.h>

class PID {
	public:
		// Coeficientes proporcional, integral e diferencial
		double	Kp;
		double	Ki;
		double	Kd;

		// Relógio do sintonizador
		// Utilizado para o cálculo dos termos integral e diferencial
		std::chrono::duration<double> time;

		// Erro acumulado para o termo integral
		double	err_I;

		// Construtor
		PID(double var, double Kp, double Ki, double Kd){
			// Inicializar variável de controle
			this.var = var;

			// Inicializar coeficientes
			this.Kp = Kp;
			this.Ki = Ki;
			this.Kd = Kd;

			// Inicializar relógio
			this.time = std::chrono::steady_clock::now()
		}

		// Computar
		double	compute(double target){
			// Termos proporcional, integral e diferencial
			double P;
			double I;
			double D;

			// Erro atual, da variável de controle até o alvo
			double err = target - this.var;

			// O termo proporcional é diretamente proporcional ao erro atual
			P = err * this.Kp;

			// Vamos calcular o intervalo de tempo
			const auto next_time = std::chrono:steady_clock::now()
			const auto diff_time = next_time - this.time

			// O termo integral é a soma de erros ao longo do tempo
			this.err_I = this.err_I + (err * diff_time)
			I = this.err_I * this.Ki

			// O termo diferencial é proporcional à taxa de variação do erro atual
			const double err_D = err / diff_time
			D = err_D * this.Kd

			// Por final, atualizar o tempo atual do sintonizador
			this.time = next_time

			// Retorna a soma dos três termos
			return P+I+D;
		};
}