WeAct Studio STM32F4x1Cx v2.0+ — 完整修正后的引脚文档 (Corrected Full Pinout)

    来源图片: STM32F4x1_PinoutDiagram_RichardBalint.png (更新: 2020-03-16) 说明: 已修正底部 SWD 焊盘的编号误标（PA13/PA14 不是主排针 32/33）并整理为完整的 Markdown 文件，便于在编辑器或工具中使用。

图例 (Legend)

    POWER (红色): 电源
    GROUND (黑色): 地
    CPU PIN (绿色): 芯片引脚名 (如 PA0)
    PIN NAME / 物理脚位 (青色): 物理排针编号 (如 Pin 1, Pin 2...)
    CONTROL (橙色): 控制类引脚 (例如 BOOT0, NRST)
    ANALOG (浅绿色): ADC / 模拟功能
    TIMER & CHANNEL (浅紫色): TIMx / PWM
    USART (浅蓝色): 串口复用
    SPI / I2S (中紫色): SPI / I2S 复用
    SDIO (棕色): SDIO (仅F411部分支持)
    I2C (浅棕色): I2C / SMBUS
    CAN BUS (粉色), USB (淡青色), MISC (浅橙色), BOARD HARDWARE (黄色) 等按原图颜色分组
    标记:
        ← 5V ← Tolerant：该引脚对5V电平具有容忍性（视芯片型号和板子设计）
        ~：支持 PWM / 定时器输出
         (F411) / (F401)：功能仅在该芯片型号上可用（请参考芯片数据手册）

板载核心组件 (Board components)

    USB-C Connector (顶部)
    BOOT0 按钮 (顶部左侧)
    NRST 按钮 (顶部右侧)
    STM32F4x1Cx 芯片 (中央)
    KEY 用户按键：连接到 PA0（也标为 WKUP）
    PWR LED (电源指示灯)
    Blue LED (用户 LED)：连接到 PC13
    底部 SWD 编程/调试焊盘（位于板底，不是主排针编号）:
        3V3, SWDIO (JTMS / PA13), SWCLK (JTCK / PA14), GND

主引脚完整列表（按图片左侧 / 右侧 / 底部区域组织）

    说明：以下以“Pin N (芯片引脚)” 的格式列出，并在括号中给出主要复用（摘录自图片）。注：部分功能以 (F411) 标记仅在 F411 系列可用。

左侧引脚（从上到下，靠近 USB-C 左侧）

    Pin 44 (BOOT0): 控制引脚 BOOT0
    Pin 25 (PB12): I2C2_SMBA, SPI2_NSS, I2S2_WS, TIM1_BKIN
    Pin 26 (PB13): ~SPI2_SCK, ~I2S2_CK, (F411) TIM1_CH1N, (F411) I2S2_SCK4
    Pin 27 (PB14): ~SPI2_MISO, (F411) I2S2_ext_SD, (F411) SDIO_D6
    Pin 28 (PB15): ~SPI2_MOSI, I2S2_SD, RTC_REFIN, TIM1_CH3N, (F411) SDIO_CK
    Pin 29 (PA8): ~MCO1, ~I2C3_SCL, ~TIM1_CH1, USB_FS_SOF
    Pin 30 (PA9): ~I2C3_SMBA, ~TIM1_CH2, USART1_TX, USB_FS_VBUS
    Pin 31 (PA10): ~TIM1_CH3, USART1_RX, USB_FS_ID
    Pin 32 (PA11): ~TIM1_CH4, USART1_CTS, (F411) USART6_TX, USB_FS_DM(-)
    Pin 33 (PA12): ~TIM1_ETR, USART1_RTS, (F411) USART6_RX, USB_FS_DP(+)
    Pin 38 (PA15): JTDI, ~TIM2_CH1, ~TIM2_ETR, SPI1_NSS, SPI3_NSS
    Pin 39 (PB3): JTDO-SWO, ~TIM2_CH2, SPI1_SCK, SPI3_SCK, (F411) I2S2_SDA2
    Pin 40 (PB4): JTRST, ~TIM3_CH1, SPI1_MISO, SPI3_MISO, (F411) SDIO_D0
    Pin 41 (PB5): ~TIM3_CH2, I2C1_SMBA, SPI1_MOSI, SPI3_MOSI, (F411) I2C2_SDA3
    Pin 42 (PB6): ~TIM4_CH1, I2C1_SCL, USART1_TX (也常用作 I2C SCL)
    Pin 43 (PB7): ~TIM4_CH2, I2C1_SDA, USART1_RX (也常用作 I2C SDA)
    Pin 45 (PB8): ~TIM4_CH3, ~TIM10_CH1, I2C1_SCL, (F411) SDIO_D4
    Pin 46 (PB9): ~TIM4_CH4, ~TIM11_CH1, I2C1_SDA, (F411) SDIO_D5

右侧引脚（从上到下，靠近 USB-C 右侧）

    电源区 (顶部): 5V, GND (Pin 23), 3V3, 3V3 (Pin 24) — （板上有多处 3.3V 与 GND）
    Pin 21 (PB10): ~TIM2_CH3, I2C2_SCL, SPI2_SCK, (F411) SDIO_D7
    Pin 20 (PB2): BOOT1 (控制引脚)
    Pin 19 (PB1): ADC9, TIM1_CH3N, TIM3_CH4
    Pin 18 (PB0): ADC8, TIM1_CH2N, TIM3_CH3
    Pin 17 (PA7): ADC7, TIM1_CH1N, TIM3_CH2, SPI1_MOSI
    Pin 16 (PA6): ADC6, TIM1_BKIN, TIM3_CH1, SPI1_MISO, (F411) SDIO_CMD
    Pin 15 (PA5): ADC5, TIM2_CH1, TIM2_ET, SPI1_SCK
    Pin 14 (PA4): ADC4, SPI1_NSS, SPI3_NSS, I2S3_WS, (F411) SDIO_CK
    Pin 13 (PA3): ADC3, TIM2_CH4, TIM5_CH4, TIM9_CH2, USART2_RX
    Pin 12 (PA2): ADC2, TIM2_CH3, TIM5_CH3, TIM9_CH1, USART2_TX
    Pin 11 (PA1): ADC1, TIM2_CH2, TIM5_CH2, USART2_RTS
    Pin 10 (PA0): ADC0, TIM2_CH1, TIM2_ET, TIM5_CH1, USART2_CTS, WKUP1 (KEY) — 板上的用户按键连至此
    Pin 7 (NRST): 复位 (NRST)
    Pin 4 (PC15): OSC32_OUT (外部 32kHz 晶振输出)
    Pin 3 (PC14): OSC32_IN, RTC_AMP1, RTC_OUT, RTC_TS
    Pin 2 (PC13): Blue LED
    Pin 1 (VBAT): 电池备份电源

中央 / 其它（中部两个排针和底部）

    中心排针与板底（部分列举）:
        Pin 29 (PA8): MCO1, TIM1_CH1, I2C3_SCL, USB_FS_SOF
        Pin 30 (PA9): USART1_TX, I2C3_SMBA, TIM1_CH2, USB_FS_VBUS
        Pin 31 (PA10): USART1_RX, TIM1_CH3, USB_FS_ID
        Pin 32 (PA11): TIM1_CH4, USART1_CTS, USB_FS_DM(-) （注意：这是 PA11，对应主排针 32）
        Pin 33 (PA12): TIM1_ETR, USART1_RTS, USB_FS_DP(+) （注意：这是 PA12，对应主排针 33）
        Pin 34: 3V3 (板上第三排/底部 3.3V 输出)
        Pin 37: GND (底部接地)
        Pin 47: GND
        Pin 48: 3V3

    重要纠正：原始转换文件里错误地把 PA13 / PA14 标注为“Pin 32 / Pin 33”。这不正确：

        PA11 / PA12 对应主排针 Pin 32 / Pin 33（如上所列）。
        PA13 / PA14 是板底的 SWD 调试焊盘 (JTMS / SWDIO, JTCK / SWCLK)，不应被标记为主排针 32/33。

底部 SWD 与底部接点（单独列出，避免编号混淆）

    这些焊盘位于板底或底部排针区，通常用于编程/调试，不等同于主排针编号。

    SWD（底部 pad）:
        3V3 (供电/测量参考)
        SWDIO / JTMS = PA13 (调试数据线，位于底部 pad)
        SWCLK / JTCK = PA14 (调试时钟线，位于底部 pad)
        GND
    其它底部接点（常见）:
        PA13, PA14 为调试 pad（请勿与主排针编号混淆）
        3V3 与 GND 底部焊盘（Pin 34 / Pin 37 在主图中位置）

外设复用 & 快速参考（节选）

    下列为图中标注的常见外设复用，供快速查看；具体完整复用请参考芯片手册或将我导出为 CSV/JSON 以便检索。

    USART / UART
        PA9 = USART1_TX
        PA10 = USART1_RX
        PA11/PA12 = 可用于其他 USART 控制线（CTS/RTS 等）
        PB6/PB7 可作为 I2C 或 USART 复用
    I2C
        PB6 = I2C1_SCL
        PB7 = I2C1_SDA
        PB8/PB9 在某些复用下可作为 I2C
    SPI / SDIO / I2S
        SPI1: PA5 (SCK), PA6 (MISO), PA7 (MOSI), PA4 (NSS)（视板上布线）
        SPI2: PB13/PB14/PB15/PB12（具体复用详见主表）
        SDIO：在 F411 上部分 PBx/PCx 被复用为 SDIO 信号（SD_CMD, SD_D0..D3, SD_CK 等）
    ADC
        PA0..PA7, PB0..PB1, PC0..PC3 等作为 ADC 输入（在主表已标注）
    TIM / PWM
        标注 ~ 的引脚代表支持 PWM 输出 (TIMx_CHy)

重要备注 (Notes)

    TIM6 & TIM7 仅被 DAC 使用，在芯片封装和该板设计中没有对应外部引脚（如图片右下注记）。
    在 F401 系列上，图示的多数引脚对 5V 是容忍的（请以芯片数据手册和板上设计为准）。
    在 F411 系列上，图中注明的 Pin 10 (PA0) 与 Pin 41 (PB5) 在某些封装/板子上不是 5V 容忍（仅 3.3V）；请以实际芯片/板子说明为准。
