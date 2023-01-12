/*
 * gps.c
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */


#include "gps.h"


#include "cmsis_os.h"
#include "main.h"

void gpsTask()
{
	for(;;)
	{
			//Code
	}
}



void gps_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t gpsHandle;
	const osThreadAttr_t gps_attributes = {
	  .name = "gps",
	  .stack_size = 128 * 4,
	  .priority = (osPriority_t) osPriorityNormal,
	};

	gpsHandle = osThreadNew(gpsTask, NULL, &gps_attributes);
}
