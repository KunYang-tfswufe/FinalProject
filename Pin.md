### **修正后的最终版本 (Corrected and Final Version)**

#### **文档信息**

- **标题**: WeAct Studio STM32F4x1Cx v2.0+ Pinout Diagram
- **更新日期**: 2020-03-16

#### **图例 (Legend)**

- **红色**: POWER (电源)
- **黑色**: GROUND (地)
- **绿色**: PIN NAME (引脚名称)
- **橙色**: CONTROL (控制引脚)
- **浅绿色**: ANALOG (模拟功能)
- **浅紫色**: TIMER & CHANNEL (定时器)
- **浅蓝色**: USART (串口)
- **中紫色**: SPI / I2S
- **棕色**: SDIO (仅F411可用)
- **浅棕色**: I2C
- **粉色**: CAN BUS
- **青色**: USB
- **浅橙色**: MISC (杂项)
- **黄色**: BOARD HARDWARE (板载硬件)
- **标识**:
  - `← 5V ← Tolerant`: 表示引脚为5V容忍。
  - `← 3.3V ← (F411)`: 在F411芯片上，此引脚为3.3V。
  - `~`: 表示该引脚支持PWM功能。

#### **板载核心组件**

- **顶部**: USB-C Connector, BOOT0 Button, NRST (Reset) Button.
- **中央**: STM32F4x1Cx 芯片.
- **按钮**: BOOT0, NRST, **KEY** (用户按键, 连接到 **PA0**).
- **LED**: PWR (电源灯), **Blue LED** (用户LED, 连接到 **PC13**).
- **底部编程/调试接口 (SWD)**:
  - Pin 1: 3V3
  - Pin 2: SWDIO (JTMS / **PA13**)
  - Pin 3: SWCLK (JTCK / **PA14**)
  - Pin 4: GND

---

#### **左侧引脚 (从上到下)**

- **Pin 44 (BOOT0)**: 控制引脚
- **Pin 25 (PB12)**: I2C2_SMBA, SPI2_NSS, I2S2_WS, TIM1_BKIN
- **Pin 26 (PB13)**: ~SPI2_SCK, ~I2S2_CK, (F411) TIM1_CH1N, (F411) SCK2
- **Pin 27 (PB14)**: ~SPI2_MISO, (F411) I2S2_ext_SD, (F411) NSS2
- **Pin 28 (PB15)**: ~SPI2_MOSI, I2S2_SD, RTC_REFIN, TIM1_CH3N
- **Pin 29 (PA8)**: ~MCO1, ~I2C3_SCL, ~TIM1_CH1, USB_FS_SOF
- **Pin 30 (PA9)**: ~I2C3_SMBA, ~TIM1_CH2, USART1_TX, USB_FS_VBUS
- **Pin 31 (PA10)**: ~TIM1_CH3, (F411)TIM1_ETR, USART1_RX, USB_FS_ID
- **Pin 32 (PA11)**: ~TIM1_CH4, USART1_CTS, (F411)USART6_TX, USB_FS_DM
- **Pin 33 (PA12)**: ~TIM1_ETR, USART1_RTS, (F411)USART6_RX, USB_FS_DP
- **Pin 38 (PA15)**: ~JTDI, ~TIM2_CH1, ~TIM2_ETR, SPI1_NSS, SPI3_NSS
- **Pin 39 (PB3)**: ~JTDO-SWO, ~TIM2_CH2, SPI1_SCK, SPI3_SCK
- **Pin 40 (PB4)**: ~JTRST, ~TIM3_CH1, SPI1_MISO, SPI3_MISO
- **Pin 41 (PB5)**: ~TIM3_CH2, I2C1_SMBA, SPI1_MOSI, SPI3_MOSI
- **Pin 42 (PB6)**: ~TIM4_CH1, I2C1_SCL, USART1_TX
- **Pin 43 (PB7)**: ~TIM4_CH2, I2C1_SDA, USART1_RX
- **Pin 45 (PB8)**: ~TIM4_CH3, ~TIM10_CH1, I2C1_SCL, (F411)SDIO_D4
- **Pin 46 (PB9)**: ~TIM4_CH4, ~TIM11_CH1, I2C1_SDA, (F411)SDIO_D5

---

#### **右侧引脚 (从上到下)**

- **电源**: 5V, **GND (Pin 23)**, 3V3
- **Pin 21 (PB10)**: ~TIM2_CH3, I2C2_SCL, SPI2_SCK, (F411)SDIO_D7
- **Pin 20 (PB2)**: **BOOT1** - 控制引脚
- **Pin 19 (PB1)**: ADC9, TIM1_CH3N, TIM3_CH4
- **Pin 18 (PB0)**: ADC8, TIM1_CH2N, TIM3_CH3
- **Pin 17 (PA7)**: ~ADC7, ~TIM1_CH1N, ~TIM3_CH2, SPI1_MOSI
- **Pin 16 (PA6)**: ~ADC6, ~TIM1_BKIN, ~TIM3_CH1, SPI1_MISO, (F411)SDIO_CMD
- **Pin 15 (PA5)**: ~ADC5, ~TIM2_CH1, ~TIM2_ET, SPI1_SCK
- **Pin 14 (PA4)**: ~ADC4, SPI1_NSS, SPI3_NSS, I2S3_WS, (F411)SDIO_CK2
- **Pin 13 (PA3)**: ~ADC3, ~TIM2_CH4, ~TIM5_CH4, ~TIM9_CH2, USART2_RX
- **Pin 12 (PA2)**: ~ADC2, ~TIM2_CH3, ~TIM5_CH3, ~TIM9_CH1, USART2_TX
- **Pin 11 (PA1)**: ~ADC1, ~TIM2_CH2, ~TIM5_CH2, USART2_RTS
- **Pin 10 (PA0)**: ~ADC0, ~TIM2_CH1, ~TIM2_ETR, ~TIM5_CH1, USART2_CTS, **WKUP1 (KEY)**
- **Pin 7 (NRST)**: 控制引脚
- **Pin 4 (PC15)**: OSC32_OUT
- **Pin 3 (PC14)**: OSC32_IN, RTC_AMP1, RTC_OUT, RTC_TS
- **Pin 2 (PC13)**: **LED BLUE**
- **Pin 1 (VBAT)**: 电池备份引脚

---

#### **底部其他引脚**

- **Pin 34**: 3V3
- **Pin 37**: GND
- **Pin 47**: GND
- **Pin 48**: 3V3
- **MCO1**: (PA8的复用功能)
- **MCO2**: (PC9的复用功能，此板未引出)

---

#### **重要备注 (Notes)**

- `TIM6` 和 `TIM7` 仅由 DAC 使用，并且在这些芯片上没有引出外部引脚。
- 在 **F401** 上，所有引脚都是 5V 容忍的。
- 在 **F411** 上，引脚 **10 (PA0)** 和引脚 **41 (PB5)** **不是** 5V 容忍的，仅支持 3.3V 电压。
