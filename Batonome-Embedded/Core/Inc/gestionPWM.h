/*
 * gestionPWM.h
 *
 *  Created on: 05 mars 2023
 *      Author: scant
 */

#ifndef INC_GESTIONPWM_H_
#define INC_GESTIONPWM_H_

//structure de données pour la gestion des PWM
enum stateCommandBatonome{
	INIT,
	WAIT_FOR_COMMAND,
	REQUEST_COMMAND_DERIVE,
	REQUEST_COMMAND_TIRANT,
};

void setCommandBato(enum stateCommandBatonome command);


void gestionPWM_Init();




#endif /* INC_GESTIONPWM_H_ */
