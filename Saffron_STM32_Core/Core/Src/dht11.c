#include "dht11.h"
#include "stm32l4xx_hal.h"

// 我们需要一个微秒级的延时函数，HAL库默认没有，这里我们自己实现一个
// 注意: 这个函数依赖于你在CubeMX中配置的系统时钟，对于NUCLEO-L476RG默认配置是准确的
static void delay_us(uint32_t us)
{
    uint32_t ticks = us * (HAL_RCC_GetHCLKFreq() / 1000000);
    uint32_t start = DWT->CYCCNT;
    while(DWT->CYCCNT - start < ticks);
}

// 设置GPIO引脚为输出模式
static void DHT11_Set_Pin_Output(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = DHT11_PIN_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP; // 推挽输出
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(DHT11_PIN_GPIO_Port, &GPIO_InitStruct);
}

// 设置GPIO引脚为输入模式
static void DHT11_Set_Pin_Input(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = DHT11_PIN_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP; // 上拉输入
    HAL_GPIO_Init(DHT11_PIN_GPIO_Port, &GPIO_InitStruct);
}

// DHT11 启动信号
static void DHT11_Start(void)
{
    DHT11_Set_Pin_Output();
    HAL_GPIO_WritePin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin, GPIO_PIN_RESET); // 拉低
    HAL_Delay(18); // 至少18ms
    HAL_GPIO_WritePin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin, GPIO_PIN_SET);   // 拉高
    delay_us(30); // 20-40us
    DHT11_Set_Pin_Input();
}

// 检查DHT11的响应
static uint8_t DHT11_Check_Response(void)
{
    uint8_t response = 0;
    delay_us(40);
    if (!(HAL_GPIO_ReadPin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin)))
    {
        delay_us(80);
        if ((HAL_GPIO_ReadPin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin)))
        {
            response = 1;
        }
        while ((HAL_GPIO_ReadPin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin))); // 等待信号变低
    }
    return response;
}

// 从DHT11读取一个字节
static uint8_t DHT11_Read_Byte(void)
{
    uint8_t i, result = 0;
    for (i = 0; i < 8; i++)
    {
        while (!(HAL_GPIO_ReadPin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin))); // 等待引脚变为高电平
        delay_us(40); // 延时40us
        if (HAL_GPIO_ReadPin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin)) // 如果40us后还是高电平，说明是数据'1'
        {
            result |= (1 << (7 - i));
            while ((HAL_GPIO_ReadPin(DHT11_PIN_GPIO_Port, DHT11_PIN_Pin))); // 等待引脚变低
        }
        else // 否则是数据'0'
        {
            result &= ~(1 << (7 - i));
        }
    }
    return result;
}

// 公开的读取函数
uint8_t DHT11_Read_Data(DHT11_Data_TypeDef *data)
{
    uint8_t Rh_byte1, Rh_byte2, Temp_byte1, Temp_byte2;
    uint16_t SUM;

    DHT11_Start();
    if (DHT11_Check_Response())
    {
        Rh_byte1 = DHT11_Read_Byte();
        Rh_byte2 = DHT11_Read_Byte();
        Temp_byte1 = DHT11_Read_Byte();
        Temp_byte2 = DHT11_Read_Byte();
        SUM = DHT11_Read_Byte();

        if (SUM == (Rh_byte1 + Rh_byte2 + Temp_byte1 + Temp_byte2))
        {
            data->temperature = Temp_byte1;
            data->humidity = Rh_byte1;
            return 1; // 读取成功
        }
    }
    return 0; // 读取失败
}
