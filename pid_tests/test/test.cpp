#include <iostream>
#include <fstream>
#include <string>
#include "pid.h"

int main(){
	//criar um controlador
	PID control = PID(0.0, 1.0, 1.0, 1.0);

	//abrir arquivo de plotagem
	std::ofstream plotdata("pidplot.dat");

	//verifica se deu certo
	if (!plotdata.is_open()){
		std::cerr << "Erro ao abrir 'pidplot.dat'." << std::endl;
	}

	//escrever dados
	for (double x = 0; x<10; x++){
		double y = x*2;
		plotdata << std::to_string(x) + " " + std::to_string(y) << std::endl;
	}

	plotdata.close();

	return 0;
}