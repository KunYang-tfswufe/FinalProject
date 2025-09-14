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

# MicroPython WeAct Core Board 使用教程
#
#     发布于: 2020-01-01 | 更新于: 2021-10-30 | 分类: STM32 | 阅读次数: 24663
#
# Micropython
#
# MicroPython，是Python3编程语言的一个完整软件实现，用C语言编写，被优化于运行在微控制器之上。MicroPython是运行在微控制器硬件之上的完全的Python编译器和运行时系统。提供给用户一个交互式提示符（REPL）来立即执行所支持的命令。除了包括选定的核心Python库，MicroPython还包括了给予编程者访问低层硬件的模块。
#
# 具体请参考：https://micropython.org/
# 核心板外设定义及使用
#
#     注意：核心板引脚丝印省略字母P，例如A0为PA0。MicroPython中使用的IO统一为PAx, PBx, PCx…
#
# GPIO
#
# Library: pyb.Pin
# 定义
#
#     可用引脚: PA0-PA15, PB0-PB10, PB12-PB15, PC13-PC15
#     模式 mode:
#         Pin.IN - 输入模式
#         Pin.OUT_PP - 推挽输出
#         Pin.OUT_OD - 开漏输出
#         Pin.AF_PP - 复用功能推挽
#         Pin.AF_OD - 复用功能开漏
#         Pin.ANALOG - 模拟输入
#     上下拉 pull:
#         Pin.PULL_NONE - 无上下拉
#         Pin.PULL_UP - 上拉
#         Pin.PULL_DOWN - 下拉
#
# 使用
#
# # GPIO
# from pyb import Pin
# C13 = Pin('PC13', Pin.OUT_PP, Pin.PULL_NONE) # PC13推挽输出 无上下拉
# print(C13) # REPL 打印PC13 配置
# C13.high() # 输出高电平
# C13.low()  # 输出低电平
# print(C13.value()) # 读取PC13电平
#
# External interrupts 外部中断
# 定义
#
#     触发方式:
#         ExtInt.IRQ_RISING
#         ExtInt.IRQ_FALLING
#         ExtInt.IRQ_RISING_FALLING
#     上下拉:
#         pyb.Pin.PULL_NONE
#         pyb.Pin.PULL_UP
#         pyb.Pin.PULL_DOWN
#
# 使用
#
# # GPIO 外部中断
# from pyb import Pin, ExtInt
#
# callback = lambda e: print("PA0 <KEY> intr")
# ext = ExtInt(Pin('PA0'), ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, callback)
# ext.swint() # 手动触发回调 运行一次callback()
#
# ADC
#
# Library: pyb.adc
# 定义
#
#     外部通道: PA0, PA1, PA2, PA3, PA4, PA5, PA6, PA7, PB0, PB1
#     内部通道: Temperature, VBAT, VFEF
#
# 使用
#
# # ADC 外部通道
# from pyb import Pin, ADC
# IN0 = ADC(Pin('PA0'))
# print(IN0.read())
#
# IN1 = ADC(Pin('PA1'))
# print(IN1.read())
# ``````python
# # ADC 内部通道
# import pyb
# adc_in = pyb.ADCAll(12, 0x70000) # 12 bit resolution, internal channels
# print(adc_in.read_core_temp()) # Temperature
# print(adc_in.read_core_vbat()) # VBAT
# print(adc_in.read_vref()) # VREF
#
# Timer 定时器
#
# Library: pyb.Timer
# 定义
#
# STM32F4x1C 定时器引脚分布
#
#     当使用USB时，PA11已被占用
#
# Timer 	Channel 1 	Channel 2 	Channel 3 	Channel 4
# TIM1 	PA8 	PA9 	PA10 	PA11
# TIM2 	PA0, PA5, PA15 	PA1, PB3 	PA2, PB10 	PA3
# TIM3 	PA6, PB4 	PA7, PB5 	PB0 	PB1
# TIM4 	PB6 	PB7 	PB8 	PB9
# TIM5 	PA0 	PA1 	PA2 	PA3
# TIM9 	PA2 	PA3 		
# TIM10 	PB8 			
# TIM11 	PB9 			
#
# 定时器输入时钟频率：
#
#     96Mhz(F411)/84Mhz(F401): TIM1, TIM9, TIM10, TIM11
#     48Mhz(F411)/42Mhz(F401): TIM2, TIM3, TIM4, TIM5
#
# 使用
#
# Timer 定时功能
#
# import pyb
# from pyb import Timer
# # 频率：2Hz
# TIM1 = Timer(1, freq=2)
# print(TIM1.counter()) # get counter value
# TIM1.callback(lambda t: pyb.LED(1).toggle())
# TIM1.freq(5) # 更改定时器频率 5 Hz
# TIM1.deinit() # 取消使用TIM1
#
# Timer PWM功能
#
# import pyb
# from pyb import Pin, Timer
# TIM2 = Timer(2, freq=1000) # 频率：1KHz
#
# # Timer.PWM ：占空比： 0%->低电平 100%->高电平
# # Timer.PWM_INVERTED：占空比： 0%->高电平 100%->低电平
# pin_a0 = Pin('PA0', Pin.OUT_PP)
# ch1 = TIM2.channel(1, Timer.PWM, pin=pin_a0)
#
# ch1.pulse_width_percent(50) # 50% 占空比, 0 - 100%
# # ch1.pulse_width(int(TIM2.period()/2)) # 直接设置比较值 50% 占空比
#
# Timer 输入捕获功能
#
#     polarity can be one of:
#         Timer.RISING - 上升沿捕获
#         Timer.FALLING - 下降沿捕获
#         Timer.BOTH - 上升/下降沿都捕获
#
# from pyb import Pin, Timer
# import pyb
#
# # 96分频：1Mhz, 重装载值(周期)：65535, 向上计数
# TIM1 = Timer(1, prescaler=96-1, period=65535-1)
# pin_a8 = Pin('PA8', Pin.IN)
# ch1 = TIM1.channel(1, Timer.IC, pin=pin_a8, polarity=Timer.BOTH)
#
# ch1.callback(lambda t: print(ch1.capture()))
# pyb.delay(5000)
# ch1.callback(None)
# TIM1.deinit()
# print('TIM over')
#
# RTC (Real Time Clock)
#
# Library: pyb.RTC
# 定义
#
# 无。
# 使用
#
# from pyb import RTC
#
# rtc = RTC()
# # 设置时间 2020.01.01 周三, 12:00:00
# rtc.datetime((2020, 1, 1, 3, 12, 0, 0, 0))
# print(rtc.datetime()) # 获取时间
#
# # 获取有关启动时间和重置源的信息
# print(hex(rtc.info()))
# callback = lambda e: print("RTC WekeUP")
# rtc.wakeup(2000, callback)
#
# # pyb.stop() # 停止模式，如果当前使用USB连接，USB CDC 会进入假死状态
# # rtc.wakeup(0) # 取消唤醒
# # pyb.standby() # 待机模式，USB会断开，恢复时会自动复位
#
# UART 串口
#
# Library: pyb.UART
# 定义
#
#     UART1: TX-PA9, RX-PA10
#     UART2: TX-PA2, RX-PA3
#     UART6: TX-PA11, RX-PA12 (USB占用)
#     UART_REPL: 默认使用 UART1
#
# 使用
#
# from pyb import UART
#
# uart2 = UART(2, 9600)
# uart2.write('hello')
# uart2.read(5) # 从数据流里读取5个字节，没有则返回None
# uart2.readline() # 读取一行，以换行符结尾
# uart2.any()   # 返回可以读取的字节数
#
# SPI 总线
#
# Library: pyb.SPI
# 定义
#
#     SPI2: NSS-PB12, SCK-PB13, MISO-PB14, MOSI-PB15
#     SPI4: NSS-PB12, SCK-PB13, MISO-PA1, MOSI-PA11 (USB占用)
#     SPI5: NSS-PB1, SCK-PA10, MISO-PA12, MOSI-PB0 (USB占用)
#
# 使用
#
# from pyb import SPI
#
# spi2 = SPI(2, SPI.MASTER, baudrate=200000, polarity=1, phase=0)
# spi2.send('hello')
# spi2.recv(5) # receive 5 bytes on the bus
# spi2.send_recv('hello') # send and receive 5 bytes
#
# I2C 总线
#
# Library: machine.I2C
# 定义
#
#     I2C1: SCL-PB6, SDA-PB7
#     I2C2: SCL-PB10, SDA-PB9
#     I2C3: SCL-PA8, SDA-PB8
#
# 使用
#
# from machine import I2C
#
# # 硬件I2C
# i2c = I2C(1, freq=400000) # create hardware I2c object: I2C1
# # 软件I2C
# # i2c = I2C(scl='PB6', sda='PB7', freq=100000)
#
# i2c.scan() # returns list of slave addresses
# i2c.writeto(0x42, 'hello') # write 5 bytes to slave with address 0x42
# i2c.readfrom(0x42, 5) # read 5 bytes from slave
#
# i2c.readfrom_mem(0x42, 0x10, 2) # read 2 bytes from slave 0x42, slave memory 0x10
# i2c.writeto_mem(0x42, 0x10, 'xy') # write 2 bytes to slave 0x42, slave memory 0x10
#
# Servo Control 舵机控制
#
# Library: pyb.Servo
# 定义
#
#     注意: Servo模块使用了TIM5, 故两者不能同时使用。
#     舵机ID(1-4)对应引脚：PA0, PA1, PA2, PA3
#
# 使用
#
# from pyb import Servo
# s1 = Servo(1) # servo on position 1 (PA0)
# s1.angle(45) # move to 45 degrees
# s1.angle(-60, 1500) # move to -60 degrees in 1500ms
# s1.speed(50) # for continuous rotation servos
#
# Switch 按键
#
# Library: pyb.Switch
# 定义
#
#     核心板按键为(KEY): PA0
#
# 使用
#
# from pyb import Switch
#
# sw = Switch()
# print(sw.value()) # returns True or False
# sw.callback(lambda: pyb.LED(1).toggle())
#
# LED
#
# Library: pyb.LED
# 定义
#
#     核心板蓝色LED (C13): PC13
#
# 使用
#
# from pyb import LED
#
# led = LED(1) # 1=blue
# led.toggle()
# led.on()
# led.off()

# STM32F4x1 MiniF4 / WeAct Studio 微行工作室 出品
#
#     中文版本
#
#     STM32F401CCU6 / STM32F401CEU6 / STM32F411CEU6 Core Board
#
# "STM32F411 Immersion Gold Board 3D View"
# Where to buy
#
#     TaoBao WeAct Studio official store
#     AliExpress WeAct Studio Official Store
#
#     None of the boards received without Logo WeAct Studio && version number are produced by us. If there are any quality problems or technical problems, please find the seller to solve them by yourself. It is best to report them and comment on them, so as not to deceive others!!
#
# "Description of Logo and version number"
#
# We do not produce the boards that we received without the Logo WeAct Studio && version number.
# Our Boards
#
#     411 adopts lead-free gold-sinking process, 401 adopts lead-free process, and the needles are gold-plated. All materials conform to ROHS standard, and lead is harmful to health, while piracy USES lead for profit
#
#     All use the latest batch of chips to give customers the best product experience
#
#     25MHZ high speed crystal vibration & 32.768khz low speed crystal vibration adopt high quality metal shell crystal vibration, the starting effect is better
#
#     Flash disk is reserved to meet the needs of big data storage and microPython. USBDisk&&FATFFS routine is provided
#
#     Support for MicroPython programming with available MicroPython firmware
#
#     Support for Arduino programming, see detailsGithub
#
#     Version V3.1, there are three keys, reset key, BOOT0 key, user key
#
# "Chip batch introduction"
#
#     We are committed to always use the best raw material, using the latest chips, users get the best user experience, improve the efficiency of development.
#
# Our Board Packaging
#
# ""
# The parameters of the board chip we produced are compared
# 	STM32F401CCU6 	STM32F401CEU6 	STM32F411CEU6
# Freq. 	84Mhz 	84Mhz 	100Mhz
# ROM 	256KB 	512KB 	512KB
# RAM 	64KB 	96KB 	128KB
# Sale situation 	discontinued 	discontinued 	In the sale
# Pin distribution diagram
#
#     Thanks, Richard·Balint !!
#
# With the pin allocation diagram, it's easier to work with MicroPython and Arduino!
#
# "/General document/STM32F4x1 v2.0+ Pin Layout"
# MicroPython
#
#     version: V1.12-35
#
#     STM32F401CEU6 Supported
#     STM32F411CEU6 Supported.
#
# Board Definition
#
# STM32F401CE: /SDK/STM32F401CEU6/MicroPython/WeAct_F411CE
# STM32F411CE: /SDK/STM32F411CEU6/MicroPython/WeAct_F411CE
# HID Flash
#
#     supported in English and Chinese
#
# Enter the HID bootloader method:
#
#     Hold down the <KEY>, power on or reset again, and the C13 LED will blink to release
#     APP enters the bootloader reference stm32f401_test_APP 0x8004000.zip project
#     More instructions
#
# WeAct HID Flash
# How to enter ISP mode
#
#     Method 1: When the power is on, press the BOOT0 key and the reset key, then release the reset key, and release the BOOT0 key after 0.5 seconds
#     Method 2: When the power is off, hold down the BOOT0 key, and release the BOOT0 at 0.5s after the power is on
#     DFU Mode: Use the data line to connect to the computer. If there is an unrecognized problem, you can heat the chip appropriately (25°C) and then re-enter the ISP mode
#     Serial Port Mode: Connect PA9 and PA10 of core board with USB serial port
#     Soft: STM32CubeProg。
#
# Chip information
# MCU 	Freq. 	RAM 	ROM
# STM32F401CC 	84Mhz 	64KB 	256KB
# STM32F401CE 	84Mhz 	96KB 	512KB
# STM32F411CE 	100Mhz 	128KB 	512KB
#
# STM32F411 Info
# STM32F411CE 	STM32F401CC 	STM32F401CE
# STM32F411 Info 	STM32F401CC Info 	STM32F401CE Info
# Date Code 	Date Code 	Date Code
# 014 (2020.06) 	End Of Life 	934&935 (2020.06)
# 947&002 (2020.03) 	609&608 	
# 946&947 (2020.01) 	723 (2020.01) 	
# 19+ (2019) 	16+ (2019) 	
# All chips are functional and original
# Board Shape
#
# STM32F4X1 V2.0+
#
# 下载烧录问题汇总
# ISP下载
#
# 按住BOOT0键和NRST键，然后松开NRST键，0.5秒后松开BOOT0键，即可进入串口下载或DFU下载。USB连接MCU的TYPE-C接口或者串口连接PA9、PA10，下载软件推荐STM32CubeProg。
# 串口下载
#
# 使用USB转串口（例如：CH340）时，将TX连接到PA10，RX连接到PA9。同时不要将MCU的Type-C连接到电脑，必须使用外部供电，不然会影响MCU下载。

