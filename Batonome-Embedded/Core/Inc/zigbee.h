/*
 * zigbee.h
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */



#ifndef ZIGBEE_ZIGBEE_H_
#define ZIGBEE_ZIGBEE_H_

void zigbee_Init();

void zigbeeTxCpltCallback();

enum key_pressed{
	UP, //140 //160
 	DOWN, //130 //170
	RIGHT, //120 //180
	LEFT, //110 //190
	SPACE
};




#endif /* ZIGBEE_ZIGBEE_H_ */
