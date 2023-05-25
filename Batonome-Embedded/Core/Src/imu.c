/*
 * imu.c
 *
 *  Created on: 16 janv. 2023
 *      Author: Aubin PRUD'HOMME
 */


#include <imu.h>
#include "cmsis_os.h"
#include "main.h"
#include <math.h>


#define IMU_ADDRESS 0xC0
#define IMU_CALIBRATE_REGISTER 0x1E
#define IMU_ANGLE_REGISTER_1 0x01
#define IMU_1 0x02
#define IMU_2 0x03

void ImuManagementTask()
{
	//printf("IMU management task is launched\n");

	uint8_t i2c_receive_buffer[1];
	uint8_t high_byte[1], low_byte[1];
	uint16_t cap = 0;

	for(;;)
	  {
		HAL_I2C_Mem_Read(&hi2c1, IMU_ADDRESS, IMU_ANGLE_REGISTER_1, 1, &i2c_receive_buffer[0], 1, 100);

		HAL_I2C_Mem_Read(&hi2c1, IMU_ADDRESS, IMU_1, 1, high_byte, 1, HAL_MAX_DELAY);
		HAL_I2C_Mem_Read(&hi2c1, IMU_ADDRESS, IMU_2, 1, low_byte, 1, HAL_MAX_DELAY);

		cap = ((uint16_t)high_byte[0] << 8)| low_byte[0];
		cap = cap/10;
		if (cap > 360)
		{
			cap = 0;
		}


		if (batonomeData.acceleroCalib==1)
		{
			batonomeData.cap = fmod(cap-offset,360.0f);
		}
		else
		{
			batonomeData.cap = cap;
		}
		vTaskDelay(500);
	  }
}



void imu_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t imuHandle;
	const osThreadAttr_t imu_attributes = {
	  .name = "imu",
	  .stack_size = 128 * 4,
	  .priority = (osPriority_t) osPriorityHigh,
	};

	imuHandle = osThreadNew(ImuManagementTask, NULL, &imu_attributes);
}
