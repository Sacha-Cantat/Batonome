/*
 * navig.c
 *
 *  Created on: May 11, 2023
 *      Author: scant
 */


/*
 * imu.c
 *
 *  Created on: 16 janv. 2023
 *      Author: Aubin PRUD'HOMME
 */


#include <navig.h>
#include "cmsis_os.h"
#include "gestionPWM.h"

#include "main.h"

void navigManagementTask()
{
	printf("NAVIG management task is launched\n");
	for(;;)
	  {
		printf("Hey");
	  }
}



void navig_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t navigHandle;
	const osThreadAttr_t navig_attributes = {
	  .name = "navig",
	  .stack_size = 128 * 4,
	  .priority = (osPriority_t) osPriorityHigh
	};

	navigHandle = osThreadNew(navigManagementTask, NULL, &navig_attributes);
}
