/*
 * gestionPWM.c
 *
 *  Created on: Mar 5, 2023
 *      Author: scant
 */


#include "gestionPWM.h"


#include "cmsis_os.h"
#include "main.h"

int tempete = 0;



enum stateCommandBatonome stateCommandBato;

Derive deriveToSet;
Derive deriveState;

Tirant tirantToSet;
Tirant tirantState;

int stateTempeteVal = 0;


void setCommandBato(enum stateCommandBatonome command)
{
	stateCommandBato = command;
}

void tempeteEnCours(int stateTempete)
{
	switch(stateTempete)
	{
	case 1:
		deriveToSet.directionDerive = BABORD;
		deriveToSet.forceDerive = POWER_4;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;

	case 2:
		deriveToSet.directionDerive = BABORD;
		deriveToSet.forceDerive = POWER_3;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;

	case 3:
		deriveToSet.directionDerive = BABORD;
		deriveToSet.forceDerive = POWER_2;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;

	case 4:
		deriveToSet.directionDerive = BABORD;
		deriveToSet.forceDerive = POWER_1;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;
	case 5:
		deriveToSet.directionDerive = BABORD;
		deriveToSet.forceDerive = POWER_0;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;
	case 6:
		deriveToSet.directionDerive = AVANT;
		deriveToSet.forceDerive = POWER_0;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;
	case 7:
		deriveToSet.directionDerive = TRIBORD;
		deriveToSet.forceDerive = POWER_0;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;
	case 8:
		deriveToSet.directionDerive = TRIBORD;
		deriveToSet.forceDerive = POWER_1;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;
	case 9:
		deriveToSet.directionDerive = TRIBORD;
		deriveToSet.forceDerive = POWER_2;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;
	case 10:
		deriveToSet.directionDerive = TRIBORD;
		deriveToSet.forceDerive = POWER_3;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;
	case 11:
		deriveToSet.directionDerive = TRIBORD;
		deriveToSet.forceDerive = POWER_4;
		stateCommandBato = REQUEST_COMMAND_DERIVE;
		break;


}
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
        	TIM1->CCR4 = valPWMTirant;
        	HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_1);
        	HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_4);
        	tirantToSet.tirantVoile = AVANT;
        	tirantToSet.forceTirant = POWER_0;

        	stateCommandBato = WAIT_FOR_COMMAND;
        	//logPWM("Initalisation de la commande PWM");
        	break;
        case WAIT_FOR_COMMAND:
        	//if (tempete == 1)
        	//{
        	//	tempeteEnCours((stateTempeteVal +1)%12);
        	//}
            /* code */
            break;
        
        case REQUEST_COMMAND_DERIVE:
        	//logPWM("Demande de commande de la dérive");
        	if (deriveToSet.directionDerive == TRIBORD)
        	{
        		//Direction Tribord
        		valPWMDerive = 160 + (10*deriveToSet.forceDerive) ;
        		//logPWM("Tribord, force : %d",deriveToSet.forceDerive);
        	}
        	else if (deriveToSet.directionDerive == BABORD)
        	{
        		//Direction Avant Toute !
        		valPWMDerive = 140 - (10*deriveToSet.forceDerive) ;
        		//logPWM("Babord, force : %d",deriveToSet.forceDerive);
        	}
        	else //Direction Avant Toute !
        	{
        		valPWMDerive = 150; //100 200;
        		//logPWM("Avant Toute !");
        	}
        	//MAJ Val Derive
        	TIM1->CCR1 = valPWMDerive;

        	//Copy
        	deriveState.directionDerive = deriveToSet.directionDerive;
        	deriveState.forceDerive = deriveToSet.forceDerive;
        	stateCommandBato = WAIT_FOR_COMMAND;

            break;

        case REQUEST_COMMAND_TIRANT:
        	//logPWM("Demande de commande de la dérive");
            /* code */
        	//logPWM("Demande de commande de la dérive");
			if (tirantToSet.tirantVoile == MOU)
			{
				//Direction Tribord
				valPWMTirant = 160 + (10*tirantToSet.forceTirant) ;
				//logPWM("Tribord, force : %d",deriveToSet.forceDerive);
			}
			else if (tirantToSet.tirantVoile == DUR)
			{
				//Direction Avant Toute !
				valPWMTirant = 140 - (10*tirantToSet.forceTirant) ;
				//logPWM("Babord, force : %d",deriveToSet.forceDerive);
			}
			else //Direction Avant Toute !
			{
				valPWMTirant = 150;
				//logPWM("Avant Toute !");
			}
			//MAJ Val Derive
			TIM1->CCR4 = valPWMTirant;

			//Copy
			tirantState.tirantVoile = tirantToSet.tirantVoile;
			tirantState.forceTirant = tirantToSet.forceTirant;
        	stateCommandBato = WAIT_FOR_COMMAND;
            break;
        
        default:
        	stateCommandBato = WAIT_FOR_COMMAND;
            break;
        }		//Code
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
	//logPWM("Initialisation de la tache PWM");
}
