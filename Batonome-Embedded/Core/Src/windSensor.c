/*
 * windSensor.c
 *
 *  Created on: Jan 12, 2023
 *  Author  : Thibault CAPEL
 *  Purpose : Ce script utilise les fonctions de la bibliothèque HAL
 *  pour configurer les broches du codeur incrémental en tant qu'entrées
 *  et utilise les interruptions pour détecter les changements de niveau.
 *  Il utilise également une boucle infinie pour afficher l'angle calculé
 *  en utilisant les impulsions comptées.
 */

#define ENCODER_RESOLUTION 4096


#include "windSensor.h"
//#include "stm32l4xx_hal.h" // Include header for STM32L4xx HAL library
#include "cmsis_os.h"
#include "main.h"

volatile uint32_t encoder_count = 0; // Global variable to store encoder count
int valPIN0  = 0;
int valPIN1  = 0;


void EXTI0_IRQHandler(void)
{
    // Interrupt handler for channel A
    if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) { // Check if A channel is low
        if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_1) == GPIO_PIN_SET) { // Check if B channel is high
            encoder_count++; // Increment encoder count
        }
        else {
            encoder_count--; // Decrement encoder count
        }
    }
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0); // Clear interrupt flag for pin 0
}

void EXTI1_IRQHandler(void)
{
    // Interrupt handler for channel B
    if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_SET) { // Check if A channel is high
        if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_1) == GPIO_PIN_RESET) { // Check if B channel is low
            encoder_count--; // Decrement encoder count
        }
        else {
            encoder_count++; // Increment encoder count
        }
    }
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_1); // Clear interrupt flag for pin 1
}

void windSensorTask()
{
    // Initialize GPIO pins
    __HAL_RCC_GPIOA_CLK_ENABLE(); // Enable clock for GPIOA peripheral
    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.Pin = GPIO_PIN_0 | GPIO_PIN_1; // Set pins 0 and 1
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING_FALLING; // Set as input with interrupt on rising and falling edge
    GPIO_InitStruct.Pull = GPIO_PULLUP; // Enable pull-up resistors
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // Enable and set external interrupt for encoder channel A
    HAL_NVIC_SetPriority(EXTI0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);

    // Enable and set external interrupt for encoder channel B
    HAL_NVIC_SetPriority(EXTI1_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI1_IRQn);

    for(;;)
    {
    	float angle = ((float)encoder_count / ENCODER_RESOLUTION) * 360.0; // Calculate angle
    	angle = fmodf(angle, 360.0f); // Wrap angle between 0 and 360
    	if(angle < 0.0f) angle += 360.0f; // Handle negative angles
    	batonomeData.angle = angle;
    	//printf("Angle: %.2f\n", angle); // Print angle to console
    	osDelay(500); // Delay for 500 milliseconds
    }
}

void windSensor_Init()
{
    /* Definitions for zigbee_com */
    osThreadId_t windSensorHandle;
    const osThreadAttr_t windSensor_attributes = {
      .name = "windSensor",
	  .stack_size = 128 * 4,
	        .priority = (osPriority_t) osPriorityHigh,
	      };

	      windSensorHandle = osThreadNew(windSensorTask, NULL, &windSensor_attributes);
	  }
