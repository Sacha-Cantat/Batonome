/*
 * gps.h
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */

#ifndef INC_GPS_H_
#define INC_GPS_H_

void gps_Init();

void GPS_RxCpltCallback();

enum enumstatecommandGPS{
	INITGPS, //140 //160
 	RUNNING//130 //170

};




#endif /* INC_GPS_H_ */
