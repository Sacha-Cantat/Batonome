/*
 * gestionPWM.c
 *
 *  Created on: Mar 5, 2023
 *      Author: scant
 */


#include "gestionPWM.h"


#include "cmsis_os.h"
#include "main.h"





enum stateCommandBatonome stateCommandBato;

Derive deriveToSet;
Derive deriveState;

Tirant tirantToSet;
Tirant tirantSet;




void setCommandBato(enum stateCommandBatonome command)
{
	stateCommandBato = command;
}


void gestionPWM_Task(void *argument)
{
	static int valPWMDerive=150;
	static int valPWMTirant= 150;
	for(;;)
	{
        switch (stateCommandBato)
        {
        case INIT:
        	//Démarrage de la PWM
        	TIM1->CCR1 = valPWMDerive;
        	HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_1);
        	stateCommandBato = WAIT_FOR_COMMAND;
        	logPWM("Initalisation de la commande PWM");
        	break;
        case WAIT_FOR_COMMAND:
            /* code */
            break;
        
        case REQUEST_COMMAND_DERIVE:
        	logPWM("Demande de commande de la dérive");
        	if (deriveToSet.directionDerive == TRIBORD)
        	{
        		//Direction Tribord
        		valPWMDerive = 160 + (10*deriveToSet.forceDerive) ;
        		logPWM("Tribord, force : %d",deriveToSet.forceDerive);
        	}
        	else if (deriveToSet.directionDerive == BABORD)
        	{
        		//Direction Avant Toute !
        		valPWMDerive = 140 - (10*deriveToSet.forceDerive) ;
        		logPWM("Babord, force : %d",deriveToSet.forceDerive);
        	}
        	else //Direction Avant Toute !
        	{
        		valPWMDerive = 150; //100 200;
        		logPWM("Avant Toute !");
        	}
        	//MAJ Val Derive
        	TIM1->CCR1 = valPWMDerive;
        	//Copy
        	deriveState.directionDerive = deriveToSet.directionDerive;
        	deriveState.forceDerive = deriveToSet.forceDerive;
        	stateCommandBato = WAIT_FOR_COMMAND;

            break;

        case REQUEST_COMMAND_TIRANT:
        	logPWM("Demande de commande de la dérive");
            /* code */
        	stateCommandBato = WAIT_FOR_COMMAND;
            break;
        
        default:
        	stateCommandBato = WAIT_FOR_COMMAND;
            break;
        }

			//Code
	}
}



void gestionPWM_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t pwmHandle;
	const osThreadAttr_t pwm_attributes = {
	  .name = "pwm",
	  .stack_size = 256 * 4,
	  .priority = (osPriority_t) osPriorityHigh,
	};

	pwmHandle = osThreadNew(gestionPWM_Task, NULL, &pwm_attributes);
	stateCommandBato = INIT;
	logPWM("Initialisation de la tache PWM");
}
