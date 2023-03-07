/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32l4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <imu.h>
#include "gps.h"
#include "zigbee.h"
#include "gestionPWM.h"
/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

#define RX_BUFFER_SIZE 80
#define PWMLOG 1
#define ZIGBEELOG 1
#define GPSLOG 1
#define IMULOG 1


typedef struct CordoGPS {
    long double latitude;
    long double longitude;
}CordoGPS;

typedef struct batonomeStruct {
	CordoGPS positionGPS;
    float angle;
    int autreInformation;
}BatonomeStruct;

enum DirectionDerive{
	BABORD,
	TRIBORD,
	AVANT,
};

enum Force{
	FORCE_0, //140 //160
 	FORCE_1, //130 //170
	FORCE_2, //120 //180
	FORCE_3, //110 //190
	FORCE_4, //100 //200
};




typedef struct BatonomeStructConf {
	CordoGPS balise;
	CordoGPS perimetreNav[20];
}BatonomeStructConf;

typedef struct derive {
	enum DirectionDerive directionDerive;
	enum Force forceDerive;
	int test;
}Derive;

//TODO GERER le tirant
typedef struct tirant {
	enum DirectionDerive directionTirant;
	enum Force forceTirant ;
	int test;
}Tirant;


extern UART_HandleTypeDef huart1;
extern UART_HandleTypeDef huart2;
extern TIM_HandleTypeDef htim1;


extern I2C_HandleTypeDef hi2c1;
extern I2C_HandleTypeDef hi2c3;

extern uint8_t UART1_rxBuffer[RX_BUFFER_SIZE] ;
extern uint8_t UART1_txBuffer[RX_BUFFER_SIZE] ;
extern uint8_t rxData;


extern BatonomeStruct batonomeData;
extern BatonomeStructConf batonomeDataConf;

extern Derive deriveToSet;
extern Derive deriveState;

extern Tirant tirantToSet;
extern Tirant tirantSet;
/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */


/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */
void logPWM(const char *format, ...);
void logIMU(const char *format, ...);
void logGPS(const char *format, ...);
void logZIGBEE(const char *format, ...);





/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
