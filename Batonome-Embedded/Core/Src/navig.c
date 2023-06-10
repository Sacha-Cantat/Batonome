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

#include <stdio.h>
#include <math.h>
#include <stdbool.h>

#define EARTH_RADIUS 6371000  // Rayon moyen de la Terre en mètres

// retourne l'angle entre le Nord et entre le premier et deuxieme point
//   0 = Nord
//  90 = Est
// 180 = Sud
// 270 = Ouest
double angleWithNorth(CordoGPS bat,CordoGPS bouee) {
    double dLon = bouee.longitude - bat.longitude;
    double y = sin(dLon) * cos(bouee.latitude);
    double x = cos(bat.latitude) * sin(bouee.latitude) - sin(bat.latitude) * cos(bouee.latitude) * cos(dLon);
    double brng = atan2(y, x);
    brng = fmod((brng + 2 * M_PI), (2 * M_PI));
    double angle = brng * 180 / M_PI;
    return angle;
}

double positive(double nb) {
    if (nb < 0) {
        nb = -nb;
    }
    return nb;
}

bool isAngleNearAngle(double angle1,double angle2, double interval) {
    return ( positive(angle2-angle1)<interval || positive(angle2-angle1) > (360-interval) );
}

double toRadians(double degrees) {
    return degrees * M_PI / 180.0;
}

bool arePointsClose(CordoGPS point1, CordoGPS point2, double threshold) {
    double lat1 = toRadians(point1.latitude);
    double lon1 = toRadians(point1.longitude);
    double lat2 = toRadians(point2.latitude);
    double lon2 = toRadians(point2.longitude);

    double dLat = lat2 - lat1;
    double dLon = lon2 - lon1;

    double a = sin(dLat / 2) * sin(dLat / 2) + cos(lat1) * cos(lat2) * sin(dLon / 2) * sin(dLon / 2);
    double c = 2 * atan2(sqrt(a), sqrt(1 - a));

    double distance = EARTH_RADIUS * c;

    return (distance <= threshold);
}

/*****
 * Entrees
 *  Angle 0->360 entre le vent par rapport a l'avant du bateau
 *  Angle 0->360 entre l'avant du bateau et le nord
 *  Point GPS du bateau
 *  Point GPS de la bouee a contourner
 *
 * Sorties
 *  Angle 0->360 Entre le nord et la direction a prendre
*****/
double algoNavigation(double direction_vent, double direction_bateau, CordoGPS position_bateau, CordoGPS position_bouee ) {
    double direction_vent_nord  = 0;
    double direction_recherchee = 0;
    double direction_bouee      = 0;


    // Vent par rapport au nord
    direction_vent_nord = fmod(direction_bateau+direction_vent, 360);

    // Calcul de la direction de la bouee en fonction position bateau et bouee
    direction_bouee = angleWithNorth(position_bateau,position_bouee);

    // Verif si vent de face , vent arrière
    bool vent_face_avant = isAngleNearAngle(direction_bouee,direction_vent_nord,40);
    bool vent_face_arriere = isAngleNearAngle(fmod(direction_bouee+180, 360),direction_vent_nord,40);


    // Si vent de face ou de dos, direction a 45° par rapport au bateau
    if (vent_face_avant) {
        direction_recherchee = fmod(direction_vent_nord+45,360);
    }
    else if (vent_face_arriere) {
        direction_recherchee = fmod(direction_vent_nord+45+180,360);
    }
    // Si c'est bon alors l'angle de la direction_recherchee = direction_bouee
    else {
        direction_recherchee = direction_bouee;
    }
    //printf("%f, %f, %f / %f, %d\n",direction_bouee,direction_vent_nord,direction_bateau,direction_recherchee ,vent_face_avant) ;
    return direction_recherchee;
}

/******
 * Entrees
 *  Angle 0->360 entre direction actuelle du bateau et le nord
 *  Angle 0->360 entre direction voulue du bateau et le nord
 * Sorties
 *  Rien : tourne le safran dans le bon sens avec +/- de force
 ******/
void setSafran(double direction_bateau, double direction_recherchee){
	direction_bateau = 360 - direction_bateau;
    double angleRelatif = fmod(direction_recherchee-direction_bateau+180,360)-180 ;
    bool directionSafran ;
    if ( angleRelatif > 0 ) {
      // On veut aller a droite -> 100
      directionSafran = false;
    } else {
      // On veut aller a gauche -> 200
      directionSafran = true;
    }

    switch((int) positive(angleRelatif)) {
    case 2 ... 5:
      // Tourner 148
      if (directionSafran) {/*Tourner 150-2*/
    	  TIM1->CCR1=148;}
      else {/*Tourner 150+2*/
    	  TIM1->CCR1=152;
      }
      break;
    case 6 ... 10:
      // Tourner 145
      if (directionSafran) {/*Tourner 150-5*/
    	  TIM1->CCR1=145;
      }
      else {/*Tourner 150+5*/
    	  TIM1->CCR1=155;
      }
      break;
    case 11 ... 20:
      // Tourner 140
      if (directionSafran) {/*Tourner 150-10*/
    	  TIM1->CCR1=140;
      }
      else {/*Tourner 150+10*/
    	  TIM1->CCR1=160;
      }
      break;
    case 21 ... 45:
      // Tourner 133
      if (directionSafran) {/*Tourner 150-17*/
    	  TIM1->CCR1=133;
      }
      else {/*Tourner 150+17*/
    	  TIM1->CCR1=167;}
      break;
    case 46 ... 90:
      // Tourner 125
      if (directionSafran) {/*Tourner 150-25*/
    	  TIM1->CCR1=125;
      }
      else {/*Tourner 150+25*/
    	  TIM1->CCR1=175;
      }
      break;
    case 91 ... 180:
      // Tourner 100
      if (directionSafran) {/*Tourner 150-50*/
    	  TIM1->CCR1=100;
      }
      else {/*Tourner 150+50*/
    	  TIM1->CCR1=200;
      }
      break;
    default:
      // Tourner 150
      break;
  }
}

/******
 * Entrees
 *  Angle 0->360 entre le vent et l'avant du bateau
 * Sorties
 *  Rien : Tendre plus ou moins la voile
 ******/
void setVoile(double direction_vent) {
  // 0 = face bateau et 90 = tribord
  switch((int) positive(direction_vent)) {
    case 0 ... 35 :
        // Vent debout : valeur largue
		TIM1->CCR4= 170;
      break;
    case 325 ... 360:
		TIM1->CCR4= 170;
      break;

    case 36 ... 61 :
        // Bon plein : 113voir un peu plus
		TIM1->CCR4= 180;// 114;
      break;
    case 299 ... 324 :
		TIM1->CCR4= 180;
      break;

    case 62 ...90 :
      	// Petit Largue 118
		TIM1->CCR4= 176;
      break;
    case 270 ... 298 :
		TIM1->CCR4= 176;
      break;

    case 91 ... 115 :
    	// Largue 125
		TIM1->CCR4= 169;
      break;
    case 245 ... 269 :
		TIM1->CCR4= 169;
      break;

    case 116 ... 158 :
      	// Grand Largue 140
		TIM1->CCR4= 154;
      break;
    case 202 ... 244 :
		TIM1->CCR4= 154;
      break;

    case 159 ... 201 :
    	// Vent arriere 160
		TIM1->CCR4= 140;
      break;
  }
}

void navigManagementTask()
{
	//batonomeData.angle = 150; //Vendt
	//batonomeData.cap = 150; //ANgle par raaport au nord
	//printf("NAVIG management task is launched\n");
	double direction_recherchee_task =0;
	int delayNav = 9;
	for(;;)
	  {
		if (batonomeDataConf.balise.latitude>0)
		{
			delayNav = delayNav+1;
			if (delayNav > 8)
			{
				direction_recherchee_task = algoNavigation((double) batonomeData.angle,(double) batonomeData.cap, batonomeData.positionGPS,  batonomeDataConf.balise );
				delayNav =0;
			}
			setSafran((double) batonomeData.cap, direction_recherchee_task);
			setVoile((double) batonomeData.angle);
			vTaskDelay(250);
			//osDelay(250);
		}
	  }

}



void navig_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t navigHandle;
	const osThreadAttr_t navig_attributes = {
	  .name = "navig",
	  .stack_size = 256 * 4,
	  .priority = (osPriority_t) osPriorityHigh
	};

	navigHandle = osThreadNew(navigManagementTask, NULL, &navig_attributes);

	TIM1->CCR1 = 150 ;
	TIM1->CCR4 = 180;

	HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&htim1,TIM_CHANNEL_4);

	/*batonomeData.positionGPS.latitude = 47.248803;
	batonomeData.positionGPS.longitude =-1.548719 ;

	batonomeDataConf.balise.latitude = 47.248945;
	batonomeDataConf.balise.longitude =  -1.548231;*/
}
