#ifndef INC_DHT11_H_
#define INC_DHT11_H_

#include "main.h"

// 定义一个结构体来存储温湿度数据
typedef struct
{
    uint8_t temperature;
    uint8_t humidity;
} DHT11_Data_TypeDef;

// 函数声明
uint8_t DHT11_Read_Data(DHT11_Data_TypeDef *data);

#endif /* INC_DHT11_H_ */
