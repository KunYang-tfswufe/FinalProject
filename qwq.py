# WeAct Studio STM32F4x1Cx v2.0+ — 完整修正后的引脚文档 (Corrected Full Pinout)
#
#     来源图片: STM32F4x1_PinoutDiagram_RichardBalint.png (更新: 2020-03-16) 说明: 已修正底部 SWD 焊盘的编号误标（PA13/PA14 不是主排针 32/33）并整理为完整的 Markdown 文件，便于在编辑器或工具中使用。
#
# 图例 (Legend)
#
#     POWER (红色): 电源
#     GROUND (黑色): 地
#     CPU PIN (绿色): 芯片引脚名 (如 PA0)
#     PIN NAME / 物理脚位 (青色): 物理排针编号 (如 Pin 1, Pin 2...)
#     CONTROL (橙色): 控制类引脚 (例如 BOOT0, NRST)
#     ANALOG (浅绿色): ADC / 模拟功能
#     TIMER & CHANNEL (浅紫色): TIMx / PWM
#     USART (浅蓝色): 串口复用
#     SPI / I2S (中紫色): SPI / I2S 复用
#     SDIO (棕色): SDIO (仅F411部分支持)
#     I2C (浅棕色): I2C / SMBUS
#     CAN BUS (粉色), USB (淡青色), MISC (浅橙色), BOARD HARDWARE (黄色) 等按原图颜色分组
#     标记:
#         ← 5V ← Tolerant：该引脚对5V电平具有容忍性（视芯片型号和板子设计）
#         ~：支持 PWM / 定时器输出
#          (F411) / (F401)：功能仅在该芯片型号上可用（请参考芯片数据手册）
#
# 板载核心组件 (Board components)
#
#     USB-C Connector (顶部)
#     BOOT0 按钮 (顶部左侧)
#     NRST 按钮 (顶部右侧)
#     STM32F4x1Cx 芯片 (中央)
#     KEY 用户按键：连接到 PA0（也标为 WKUP）
#     PWR LED (电源指示灯)
#     Blue LED (用户 LED)：连接到 PC13
#     底部 SWD 编程/调试焊盘（位于板底，不是主排针编号）:
#         3V3, SWDIO (JTMS / PA13), SWCLK (JTCK / PA14), GND
#
# 主引脚完整列表（按图片左侧 / 右侧 / 底部区域组织）
#
#     说明：以下以“Pin N (芯片引脚)” 的格式列出，并在括号中给出主要复用（摘录自图片）。注：部分功能以 (F411) 标记仅在 F411 系列可用。
#
# 左侧引脚（从上到下，靠近 USB-C 左侧）
#
#     Pin 44 (BOOT0): 控制引脚 BOOT0
#     Pin 25 (PB12): I2C2_SMBA, SPI2_NSS, I2S2_WS, TIM1_BKIN
#     Pin 26 (PB13): ~SPI2_SCK, ~I2S2_CK, (F411) TIM1_CH1N, (F411) I2S2_SCK4
#     Pin 27 (PB14): ~SPI2_MISO, (F411) I2S2_ext_SD, (F411) SDIO_D6
#     Pin 28 (PB15): ~SPI2_MOSI, I2S2_SD, RTC_REFIN, TIM1_CH3N, (F411) SDIO_CK
#     Pin 29 (PA8): ~MCO1, ~I2C3_SCL, ~TIM1_CH1, USB_FS_SOF
#     Pin 30 (PA9): ~I2C3_SMBA, ~TIM1_CH2, USART1_TX, USB_FS_VBUS
#     Pin 31 (PA10): ~TIM1_CH3, USART1_RX, USB_FS_ID
#     Pin 32 (PA11): ~TIM1_CH4, USART1_CTS, (F411) USART6_TX, USB_FS_DM(-)
#     Pin 33 (PA12): ~TIM1_ETR, USART1_RTS, (F411) USART6_RX, USB_FS_DP(+)
#     Pin 38 (PA15): JTDI, ~TIM2_CH1, ~TIM2_ETR, SPI1_NSS, SPI3_NSS
#     Pin 39 (PB3): JTDO-SWO, ~TIM2_CH2, SPI1_SCK, SPI3_SCK, (F411) I2S2_SDA2
#     Pin 40 (PB4): JTRST, ~TIM3_CH1, SPI1_MISO, SPI3_MISO, (F411) SDIO_D0
#     Pin 41 (PB5): ~TIM3_CH2, I2C1_SMBA, SPI1_MOSI, SPI3_MOSI, (F411) I2C2_SDA3
#     Pin 42 (PB6): ~TIM4_CH1, I2C1_SCL, USART1_TX (也常用作 I2C SCL)
#     Pin 43 (PB7): ~TIM4_CH2, I2C1_SDA, USART1_RX (也常用作 I2C SDA)
#     Pin 45 (PB8): ~TIM4_CH3, ~TIM10_CH1, I2C1_SCL, (F411) SDIO_D4
#     Pin 46 (PB9): ~TIM4_CH4, ~TIM11_CH1, I2C1_SDA, (F411) SDIO_D5
#
# 右侧引脚（从上到下，靠近 USB-C 右侧）
#
#     电源区 (顶部): 5V, GND (Pin 23), 3V3, 3V3 (Pin 24) — （板上有多处 3.3V 与 GND）
#     Pin 21 (PB10): ~TIM2_CH3, I2C2_SCL, SPI2_SCK, (F411) SDIO_D7
#     Pin 20 (PB2): BOOT1 (控制引脚)
#     Pin 19 (PB1): ADC9, TIM1_CH3N, TIM3_CH4
#     Pin 18 (PB0): ADC8, TIM1_CH2N, TIM3_CH3
#     Pin 17 (PA7): ADC7, TIM1_CH1N, TIM3_CH2, SPI1_MOSI
#     Pin 16 (PA6): ADC6, TIM1_BKIN, TIM3_CH1, SPI1_MISO, (F411) SDIO_CMD
#     Pin 15 (PA5): ADC5, TIM2_CH1, TIM2_ET, SPI1_SCK
#     Pin 14 (PA4): ADC4, SPI1_NSS, SPI3_NSS, I2S3_WS, (F411) SDIO_CK
#     Pin 13 (PA3): ADC3, TIM2_CH4, TIM5_CH4, TIM9_CH2, USART2_RX
#     Pin 12 (PA2): ADC2, TIM2_CH3, TIM5_CH3, TIM9_CH1, USART2_TX
#     Pin 11 (PA1): ADC1, TIM2_CH2, TIM5_CH2, USART2_RTS
#     Pin 10 (PA0): ADC0, TIM2_CH1, TIM2_ET, TIM5_CH1, USART2_CTS, WKUP1 (KEY) — 板上的用户按键连至此
#     Pin 7 (NRST): 复位 (NRST)
#     Pin 4 (PC15): OSC32_OUT (外部 32kHz 晶振输出)
#     Pin 3 (PC14): OSC32_IN, RTC_AMP1, RTC_OUT, RTC_TS
#     Pin 2 (PC13): Blue LED
#     Pin 1 (VBAT): 电池备份电源
#
# 中央 / 其它（中部两个排针和底部）
#
#     中心排针与板底（部分列举）:
#         Pin 29 (PA8): MCO1, TIM1_CH1, I2C3_SCL, USB_FS_SOF
#         Pin 30 (PA9): USART1_TX, I2C3_SMBA, TIM1_CH2, USB_FS_VBUS
#         Pin 31 (PA10): USART1_RX, TIM1_CH3, USB_FS_ID
#         Pin 32 (PA11): TIM1_CH4, USART1_CTS, USB_FS_DM(-) （注意：这是 PA11，对应主排针 32）
#         Pin 33 (PA12): TIM1_ETR, USART1_RTS, USB_FS_DP(+) （注意：这是 PA12，对应主排针 33）
#         Pin 34: 3V3 (板上第三排/底部 3.3V 输出)
#         Pin 37: GND (底部接地)
#         Pin 47: GND
#         Pin 48: 3V3
#
#     重要纠正：原始转换文件里错误地把 PA13 / PA14 标注为“Pin 32 / Pin 33”。这不正确：
#
#         PA11 / PA12 对应主排针 Pin 32 / Pin 33（如上所列）。
#         PA13 / PA14 是板底的 SWD 调试焊盘 (JTMS / SWDIO, JTCK / SWCLK)，不应被标记为主排针 32/33。
#
# 底部 SWD 与底部接点（单独列出，避免编号混淆）
#
#     这些焊盘位于板底或底部排针区，通常用于编程/调试，不等同于主排针编号。
#
#     SWD（底部 pad）:
#         3V3 (供电/测量参考)
#         SWDIO / JTMS = PA13 (调试数据线，位于底部 pad)
#         SWCLK / JTCK = PA14 (调试时钟线，位于底部 pad)
#         GND
#     其它底部接点（常见）:
#         PA13, PA14 为调试 pad（请勿与主排针编号混淆）
#         3V3 与 GND 底部焊盘（Pin 34 / Pin 37 在主图中位置）
#
# 外设复用 & 快速参考（节选）
#
#     下列为图中标注的常见外设复用，供快速查看；具体完整复用请参考芯片手册或将我导出为 CSV/JSON 以便检索。
#
#     USART / UART
#         PA9 = USART1_TX
#         PA10 = USART1_RX
#         PA11/PA12 = 可用于其他 USART 控制线（CTS/RTS 等）
#         PB6/PB7 可作为 I2C 或 USART 复用
#     I2C
#         PB6 = I2C1_SCL
#         PB7 = I2C1_SDA
#         PB8/PB9 在某些复用下可作为 I2C
#     SPI / SDIO / I2S
#         SPI1: PA5 (SCK), PA6 (MISO), PA7 (MOSI), PA4 (NSS)（视板上布线）
#         SPI2: PB13/PB14/PB15/PB12（具体复用详见主表）
#         SDIO：在 F411 上部分 PBx/PCx 被复用为 SDIO 信号（SD_CMD, SD_D0..D3, SD_CK 等）
#     ADC
#         PA0..PA7, PB0..PB1, PC0..PC3 等作为 ADC 输入（在主表已标注）
#     TIM / PWM
#         标注 ~ 的引脚代表支持 PWM 输出 (TIMx_CHy)
#
# 重要备注 (Notes)
#
#     TIM6 & TIM7 仅被 DAC 使用，在芯片封装和该板设计中没有对应外部引脚（如图片右下注记）。
#     在 F401 系列上，图示的多数引脚对 5V 是容忍的（请以芯片数据手册和板上设计为准）。
#     在 F411 系列上，图中注明的 Pin 10 (PA0) 与 Pin 41 (PB5) 在某些封装/板子上不是 5V 容忍（仅 3.3V）；请以实际芯片/板子说明为准。

# STM32F411xC/xE 微控制器架构框图（基于 MSv34920V2） — 修正版
#
# 本文档基于你从图片转换而来的文本进行校对与补充，修正了若干 OCR/语义错误并补充了缺失的注记（尤其是电源、定时器与调试信号相关的说明）。目标是产生一份完整、精确并且对 Cursor 等 AI 代码编辑器友好的 Markdown 上下文文件。
# 总体说明
#
# 该文档描述 STM32F411xC/xE 系列微控制器的内部架构框图要点，包括 Cortex-M4 内核、总线矩阵、闪存/SRAM、DMA、外设（GPIO、USART、SPI、I2C、ADC、TIM、USB、SDIO 等）、电源管理与时钟源、备份域与 RTC、调试与追踪接口等。
#
# 重要的纠正与补充（须知）：
#
#     APB 总线频率限制与定时器时钟（TIMxCLK）行为已明确区分（见“时钟与定时器”部分）。
#     补充并明确列出了电源引脚（VDD、VDDA、VSSA、VCAP、VBAT 等）及其电压范围与注记（PDR ON/OFF 状态）。
#     统一并纠正了调试/追踪引脚名称（JTAG/SWD、ETM、TRACECLK、TRACED[3:0] 等）。
#     补充了 AHB 总线矩阵（masters/slaves）与 DMA 流数、FIFO 说明、CRC 所在总线层次的明确注记。
#
# 结构化内容（逐项详述）
# CPU 与 Debug / Trace
#
#     CPU: ARM Cortex-M4，含 FPU，最高 100 MHz。
#     内部模块：MPU（内存保护单元）、NVIC（中断控制器）、ETM（嵌入式跟踪模块）、JTAG & SW。
#     总线接口：I-BUS (指令总线)、D-BUS (数据总线) 与 S-BUS (系统总线) 连接到 AHB 总线矩阵。
#     调试 / 追踪信号（建议使用原图精确命名）:
#         NJTRST, JTDI, JTCK/SWCLK, JTDO/SWDIO（或 TDO/SWO 取决具体封装），
#         TRACECLK, TRACED[3:0]（跟踪数据线 D0..D3），ETM。
#         注意：OCR 可能把 JTDO/SWDIO 写成 JTDO/SWD，请以原图为准。
#
# 存储器
#
#     512 KB Flash（含加速/指令 cache 注记）
#     128 KB SRAM
#     备份寄存器（Backup registers，位于备份域并由 VBAT 供电）
#
# 总线矩阵（AHB bus matrix）
#
#     图中标注为多主机 / 多从机的 AHB 矩阵（常见为若干 masters (CPU、DMA1、DMA2、AHB masters) 与 slaves (Flash, SRAM, 外设寄存器等)）。
#     CRC 模块位于 AHB/外设侧（按原图位置可视为靠近 Reset & Clock 控制域的一部分）。
#
# DMA
#
#     DMA1 与 DMA2：均支持多 Streams（例如图上标注 8 Streams）并带 FIFO 功能（各 stream 有 FIFO 支持以优化内存/外设传输效率）。
#     DMA 与 AHB/ APB 总线连接以实现内存与外设间的数据传输。
#
# 外设汇总（按总线分组）
#
#     GPIO PORT A..E, H（PA[15:0], PB[15:0], PC[15:0], PD[15:0], PE[15:0], PH[1:0]）
#     定时器：TIM1（高级 16-bit）、TIM2（32-bit）、TIM3（16-bit）、TIM4（16-bit）、TIM5（32-bit）、TIM9/10/11（16-bit）等。
#         TIM1: 先进的定时器，支持互补输出、死区、BKIN 等。
#         TIM2/5: 32-bit 定时器（更多计数范围）。
#     通用同步串口与外设：USART1/2/6, SPI1/2/3/4/5, I2C1/2/3, SDIO/MMC, ADC1, USB OTG FS, RTC, WWDG, IWDG（看图为 WDG 32K 驱动）等。
#     ADC: ADC1，16 个模拟输入，内部温度传感器，参考电压/ADC 引脚注记（VDDREF_ADC / VREF）
#     SDIO/MMC：支持外接 SD 卡 / MMC
#     USB OTG FS：含 PHY / FIFO，相关电平与引脚（DP, DM, ID, VBUS, SOF 等）
#     CRC: 硬件 CRC 加速器，用于外设和数据校验
#
# RTC 与备份域
#
#     LSE (外部 32.768 kHz 晶振) 输入：OSC32_IN / OSC32_OUT，VBAT 为 RTC 供电，VBAT 范围图上标注 1.65 to 3.6 V。
#     备份寄存器、RTC alarm/Stamp 输出（ALARM_OUT, STAMP1）
#
# 电源与复位（补充并修正）
#
#     主要引脚：VDD（主供电），VDDA（模拟供电），VSSA（模拟地），VBAT（备用电池供电给备份域/RTC），VCAP（内核电容引脚）等。
#     电压范围注记（请以原图精确数值为准，示例）：
#         VDD = 1.7 to 3.6 V (PDR OFF), 1.8 to 3.6 V (PDR ON) —— 原图分别在不同 PDR 状态下给出不同允许范围，务必以图中标注为最终参考。
#         VBAT = 1.65 to 3.6 V（用于 RTC/备份域）
#     电源管理模块：电压调节器、POR/PDR/BOR、PVD（电压检测）、Power interface 等（详见原图）
#     VCAP：内核电容连接引脚（通常用于内部稳压器的电容）。
#     VREF_ADC/VDDREF_ADC：ADC 参考/采样电压相关引脚或注记。
#
# 时钟、复位与 PLL
#
#     系统时钟由 HSE/HSI/PLL/LSI 组合生成，原图有 RC_HS、RC_LS、PLL1&2、XTAL 等模块。
#     Reset & Clock Control（RCC）位于靠近电源子系统的区域，负责时钟分配、总线 prescaler、外设时钟使能。
#
# 时钟与定时器（重要纠正）
#
#     APB2 总线：最大运行频率 100 MHz（外设 PCLK2 ≤ 100 MHz）。
#     APB1 总线：最大运行频率 50 MHz（外设 PCLK1 ≤ 50 MHz）。
#     定时器时钟（TIMxCLK）：当 APB prescaler ≠ 1 时（即 APB 分频器使 PCLK 发生分频），定时器时钟会是 PCLK 的两倍（这是 ARM 总线/定时器常见行为）。因此 TIMxCLK 最多能达到 100 MHz（适用于 APB1 的定时器在 APB1 被分频时亦可得到 2×PCLK1，从而计数速率可达 100 MHz）。
#         简单总结：APB1 外设（PCLK1）上限 50 MHz，但 APB1 上的 定时器（例如 TIM2/3/4/5）可以被时钟到 100 MHz（在 prescaler ≠ 1 的情况下）。APB2 外设及定时器的上限为 100 MHz。
#
# 外设复用（AF）与引脚复用说明
#
#     文档原图中对每个外设旁边标记了可复用的 AF 函数（例如 SPI 的 MOSI/MISO/SCK、USART 的 TX/RX/CTS/RTS、I2C 的 SCL/SDA 等）。OCR 过程中常丢失一些 AF 标签或把 AF 缩写错写，已在本文档中尽量保留关键 AF 注记，例如“RX, TX, CK, CTS, RTS as AF”、“MOSI/SD, MISO/SCK/CK, NSS/WS as AF”等。请在需要精确引脚表时参考芯片参考手册（RM）与封装引脚分配表。
#
# 外设通道与位宽（示例）
#
#     TIM1：3 个互补通道 + 4 个通道 + BKIN as AF（图中有“3 compl. channels TIM1_CH1[1:3]N, 4 channels TIM1_CH1[4]ETR, BKIN as AF”之类注记）
#     TIM2/TIM5：32-bit，TIM3/TIM4/TIM9/TIM10/TIM11：16-bit（以原图标注为准）
#     ADC：16 个模拟输入（ADC1）
