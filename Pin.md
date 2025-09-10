好的，这是为您提供的 "WeAct Studio STM32F4x1Cx v2.0+" 引脚图的纯文本描述，方便您复制粘贴给Cursor作为上下文。

---

### **WeAct Studio STM32F4x1Cx v2.0+ 引脚图文本描述**

#### **文档信息**

- **标题**: WeAct Studio STM32F4x1Cx v2.0+ Pinout Diagram
- **更新日期**: 2020-03-16

#### **图例 (Legend)**

- **红色**: POWER (电源)
- **黑色**: GROUND (地)
- **绿色**: PIN NAME (引脚名称, 如PA0, PB1)
- **橙色**: CONTROL (控制引脚, 如BOOT0, NRST)
- **浅绿色**: ANALOG (模拟引脚, 如ADC)
- **浅紫色**: TIMER & CHANNEL (定时器和通道)
- **浅蓝色**: USART (串口)
- **中紫色**: SPI / I2S (SPI总线 / I2S音频)
- **棕色**: SDIO (SD卡接口, 仅F411可用)
- **浅棕色**: I2C (I2C总线)
- **青色**: USB (USB接口)
- **浅橙色**: MISC (杂项功能)
- **黄色**: BOARD HARDWARE (板载硬件相关, 如LED, SWD)
- **标识**:
  - `← 5V ← Tolerant`: 表示引脚为5V容忍。
  - `← 3.3V ← (F411)`: 表示在F411芯片上此引脚为3.3V电压。
  - `~`: 表示该引脚支持PWM功能。

---

#### **板载核心组件**

- **顶部**: USB-C Connector, BOOT0 Button, NRST (Reset) Button.
- **中央**: STM32F4x1Cx 芯片.
- **按钮**:
  - **BOOT0**: 用于选择启动模式。
  - **NRST**: 复位按钮。
  - **KEY**: 用户按键 (连接到 PA0, WKUP1)。
- **LED**:
  - **PWR**: 电源指示灯。
  - **Blue LED**: 用户可控蓝色LED (连接到 PC13)。
- **底部编程接口**:
  - 3V3
  - SWDIO (JTMS) / **PA13**
  - SWCLK (JTCK) / **PA14**
  - GND

---

#### **左侧引脚 (从上到下)**

- Pin 44 (**BOOT0**) - 控制引脚
- Pin 25 (**PB12**): I2C2_SMBA, SPI2_NSS, I2S2_WS, TIM1_BKIN
- Pin 26 (**PB13**): (F411) SCK2, SPI2_SCK, I2S2_CK
- Pin 27 (**PB14**): (F411) NSS2, (F411) I2S2_ext_SD, SPI2_MISO
- Pin 28 (**PB15**): (F411) SD_CK, (F411) I2S2_SD, SPI2_MOSI, RTC_REFIN
- Pin 29 (**PA8**): MCO1, I2C3_SCL, T1_CH1
- Pin 30 (**PA9**): I2C3_SMBA, T1_CH2, USB_OTG_FS_VBUS
- Pin 31 (**PA10**): T1_CH3, (F411) T1_ETR, OTG_FS_ID, RX1
- Pin 32 (**PA11**): T1_CH4, OTG_FS_DM, CTS1, (F411) TX6
- Pin 33 (**PA12**): T1_ETR, OTG_FS_DP, RTS1, (F411) RX6
- Pin 38 (**PA15**): NSS1, NSS3, JTDI, T2_CH1, T2_ETR
- Pin 39 (**PB3**): SCK1, SCK3, T2_CH2, JTDO-SWO
- Pin 40 (**PB4**): MISO1, MISO3, T3_CH1, JTRST
- Pin 41 (**PB5**): MOSI1, MOSI3, I2C1_SMBA, T3_CH2
- Pin 42 (**PB6**): SCL1, I2C1_SCL, T4_CH1, TX1
- Pin 43 (**PB7**): SDA1, I2C1_SDA, T4_CH2, RX1
- Pin 45 (**PB8**): SCL1 (SDA3), I2C1_SCL, T4_CH3, T10_CH2, (F411) T10_CH1, SD_D4
- Pin 46 (**PB9**): SDA1 (SDA2), I2C1_SDA, T4_CH4, T11_CH1, (F411) SD_D5

---

#### **右侧引脚 (从上到下)**

- **电源**:
  - **5V**
  - **GND** (引脚23)
  - **3V3** (引脚24)
- Pin 21 (**PB10**): SCL2, I2C2_SCL, T2_CH3, (F411) SD_D7
- Pin 20 (**PB2**): **BOOT1** - 控制引脚
- Pin 19 (**PB1**): ADC9
- Pin 18 (**PB0**): ADC8
- Pin 17 (**PA7**): ADC7, T1_CH1N, T3_CH2
- Pin 16 (**PA6**): ADC6, SDO, CMD, MISO1, T1_BKIN, T3_CH1
- Pin 15 (**PA5**): ADC5, SCK1, T2_CH1, T2_ET
- Pin 14 (**PA4**): ADC4, CK2, NSS1, NSS3
- Pin 13 (**PA3**): ADC3, RX2, T2_CH4, T5_CH4, T9_CH4
- Pin 12 (**PA2**): ADC2, TX2, T2_CH3, T5_CH3, T9_CH2
- Pin 11 (**PA1**): ADC1, RTS2, T2_CH2, T5_CH2
- Pin 10 (**PA0**): ADC0, CTS2, WKUP1, T2_CH1, T2_ET, T5_CH1 (**连接到 KEY 按键**)
- Pin 7 (**NRST**) - 控制引脚
- Pin 4 (**PC15**): OSC32_OUT
- Pin 3 (**PC14**): OSC32_IN, RTC_AMP1, RTC_OUT, RTC_TS
- Pin 2 (**PC13**): **LED BLUE** (连接到板载蓝色LED)
- Pin 1 (**VBAT**)

---

#### **其他引脚**

- **底部边缘**:
  - Pin 47 (**GND**)
  - Pin 48 (**3V3**)
- **右下角**:
  - Pin 29 (**MCO1**)

---

#### **重要备注 (Notes)**

- TIM6 和 TIM7 仅由 DAC 使用，并且没有外部引脚。
- 在 STM32F401 上，所有引脚都是 5V 容忍的。
- 在 STM32F411 上，引脚 10 (**PA0**) 和引脚 41 (**PB5**) 仅为 3.3V 电压，非 5V 容忍。
