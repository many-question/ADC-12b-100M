# 晶体管级设计分工包

架构 v0.3（噪声预算重新分配，[`docs/noise-budget.md`](noise-budget.md)）与各模块规格是当前基线。下列 6 个模块可以**并行**开展晶体管级设计，
彼此只通过规格中的端口和负载条件耦合。每个模块的完整规格在 [`docs/specs.md`](specs.md)，
流程见 [`CONTRIBUTING.md`](../CONTRIBUTING.md) 与 [`docs/workflow.md`](workflow.md)。

**认领与角色**：模块**负责人**（模块 owner）是认领该模块、其认领 PR 已被合并的 GitHub 用户，记在
`specs/blocks/<block>.yaml` 的 `owner:`（`TBD` 表示未认领）；认领方式是发标题为 `[<block>] claim` 的 PR，
只把 `owner:` 改成自己的登录名。**项目负责人**是 `many-question`，负责架构、规格、测试台、评审与合并。
模块负责人只改自己模块的晶体管级网表、RNL 和结果；接口、规格、测试台或其它模块的改动先开 issue 由项目负责人决定。

## 总览

| 模块 | 关键指标 | 主要风险 | 依赖 / 交互 | 建议人选侧重 |
|---|---|---|---|---|
| `adc_comp` | 噪声 TT ≤ 200 µV、全角 ≤ 240 µV，1 mV 时延 ≤ 80 ps，τ ≤ 15 ps，Cin ≤ 20 fF，CLKC 输入 ≤ 16 fF，回踢 ≤ 40 µV/周期 | 慢角延时、回踢电荷留在浮空上极板 | 负载与时钟来自 SAR 逻辑 | 动态比较器 / 噪声 |
| `adc_sarlogic` | 全角转换 ≤ 4.1 ns（70 ps 比较器），环路开销 ≤ 35/40 ps，两段 DAC 等待 | SS/0.81 V/−40 °C 慢 1.6× 以上 | 驱动 CDAC 控制（15 fF/线）；输入 CONV ≤ 40 fF、OUTP/OUTN ≤ 7 fF | 异步数字 / 定制逻辑 |
| `adc_cdac` | C_S = 2.057 pF（cu = 1 fF，权重 980 560 318 180 102 57 32 18 10 6 3 2 1），权重误差在冗余内可校准（DAC-03），τ ≤ 15 ps，跟踪 SFDR ≥ 85 dB | 0.5 fF 半电容、驱动器 PMOS 在 0.81 V 关断不彻底、底板结电容非线性 | 栅压来自 bootstrap，控制来自 SAR 逻辑；时钟输入 PHI_S/PHI_SB ≤ 40 fF、CONV ≤ 80 fF | 电容阵列 / 开关 |
| `adc_bootstrap` | VG−VIN ≥ 0.72 V 且波动 ≤ 40 mV，关断 ≤ 60 ps，跟踪 SFDR ≥ 82 dB | 器件耐压（≤ 1.0 V）、负载为整个输入开关栅电容 | 负载 = CDAC 输入开关（规格给出参考负载）；PHI_B/PHI_BB 输入 ≤ 16 fF | 采样开关 |
| `adc_clkgen` | PHI_S→PHI_B 20–80 ps，先断后合，PHI_S 下降沿 ≤ 20 ps、抖动 ≤ 60 fs，AVDD 总电流 ≤ 80 µA（含负载） | 抖动、占空比 45/55 % | 驱动所有相位负载（共 530 fF） | 时钟 |
| `adc_ref` | 电荷回放 ENOB 损失 ≤ 0.1 bit，判决 12~14 期间变化 ≤ 200 µV，噪声（10 kHz~100 GHz）≤ 120 µV，直流 ±5 mV；不设功耗上限 | 全部片内（不用 nF 电容），小去耦下的恢复速度；只能用 1.8 V 供电得到 0.9 V | 负载 ≈ 2 pC/转换（与码基本无关，平均 200 µA） | 模拟 / 驱动 |

## 共同要求

* 新建 `design/xtor/<block>/<block>.scs`，子电路名与端口顺序与规格一致（`python -m adcflow check ports`）。
* 只用 PDK 器件（`nch_*_mac`、`pch_*_mac`、`cfmom_2t`、`*moscap*` 等，见 `design/rnl/adc28.rnl`）。
  理想元件只允许用于：去耦电容的寄生模型、尚无 PDK 等效的 CDAC 单位电容（需负责人同意并附寄生/失配模型）。
* 每个网表带**完整**的 RNL 原理图（精确的 PLACE / ORIENT / WIRE，`rnl check` 0 错误 0 警告 0 提示）
  和**高层语义**（`$DIFFERENTIAL_PAIR`、`$CURRENT_MIRROR`、`$MATCHED`、`$BRANCH`、`@GROUP` 等），方便评审。
* 验收：本模块全部用例 `--view <block>=xtor --corners all`，再做顶层混合仿真（其余模块行为级）。
* 不得修改其它模块、测试台或规格；需要改接口时先在 issue 中与项目负责人（`many-question`）讨论。

## 接口负载与输入电容

驱动端的测试台负载（规格 `operating:`）与接收端的输入电容限值是同一份预算：
**接收端实例数 × 输入电容限值 + 约 20 % 负载的走线 ≤ 驱动端负载**（实例数按顶层网表数，
`tests/test_specs_and_checks.py` 检查）。输入电容在接收模块已有的测试中测：DUT 的输入经一个电荷计
（`tb_qmeter_va`，0 V 通路）接到驱动源，取每个上升沿流入该引脚的电荷除以电压阶跃（含整个摆幅上的栅电容变化与
Miller 耦合，即驱动端实际充放的电荷），各沿取平均；TT 角（[`verification.md`](verification.md) §6）。

| 网络（驱动端负载） | 接收端（限值） | 走线 |
|---|---|---|
| PHI_S、PHI_SB（`adc_clkgen`，各 100 fF） | 2 × `adc_cdac` DAC-15 / DAC-16（40 fF） | 20 fF |
| PHI_B、PHI_BB（`adc_clkgen`，各 40 fF） | 2 × `adc_bootstrap` BST-09 / BST-10（16 fF） | 8 fF |
| CONV（`adc_clkgen`，250 fF） | 2 × `adc_cdac` DAC-17（80 fF）+ `adc_sarlogic` LOG-14（40 fF） | 50 fF |
| UP/DN（`adc_sarlogic` `load_updn`，15 fF） | 2 × `adc_cdac` DAC-13（6 fF，DH/RL，100 MHz 交流测量） | 3 fF |
| CLKC（`adc_sarlogic` `load_clkc`，20 fF） | `adc_comp` CMP-14（16 fF） | 4 fF |
| OUTP、OUTN（`adc_comp` `load_per_output`，10 fF） | `adc_sarlogic` LOG-15（7 fF） | 3 fF |
| 上极板（`adc_cdac` `top_load`，20 fF） | `adc_comp` CMP-12（20 fF，100 MHz 交流测量） | 计入上极板寄生 |

CONV 的分配：CDAC 的 CONV 使能 22 个采样半电容的三态驱动器（每个驱动器的上、下拉两路），比 SAR 逻辑
（复位与启动，可先经一级缓冲）需要更多直接扇出，所以每个 CDAC 80 fF、SAR 逻辑 40 fF。
行为级视图各输入带一个明确的电容（参数 `cin_*`，约为限值的 75 %），所以这些指标在行为级也有意义。

## 各模块要点

### adc_comp
* 输入共模约 0.49 V（0.40–0.56 V），首次比较差分输入可达 0.75 V；NMOS 输入、ulvt。
* 建议双尾（double-tail）或带预放大的 StrongARM：预放大级隔离回踢；输出带反相器满足 RTZ。
* 噪声主要由输入对 gm 与积分电容决定；TT ≤ 200 µV，在 125 °C、ff/ss 等全部角 ≤ 240 µV（v0.3，见 `docs/noise-budget.md` §4）。
* 失调不影响线性（冗余），但 σ ≤ 5 mV（蒙特卡洛 50 次）以免吃掉量程。
* CLKC 输入 ≤ 16 fF（CMP-14，每个上升沿的电荷 / VDD）：SAR 逻辑的 CLKC 负载 20 fF 减 4 fF 走线。尾管与复位管若超出，
  可在比较器内加一级缓冲（其延时计入 CMP-04/05/06）。输出负载 10 fF = SAR 逻辑输入（LOG-15 ≤ 7 fF）+ 3 fF 走线。

### adc_sarlogic
* 行为级模型 `design/behav/veriloga/adc_sarlogic_va.va` 是功能与时序的参考实现。
* 关键路径：比较器 VALID → 位锁存 → UP/DN → DAC 等待 → CLKC。前 6 步等待 40 ps，之后 75 ps（TT），
  等待延时应与 CDAC 驱动器同向随工艺变化（同类器件的延时链）。
* 超时（≈ 250 ps）强制判 1；CONV 下降时未完成也要装载输出寄存器并给出 RDY。
* D 输出驱动 50 fF；RDY 在 D 稳定后 ≥ 100 ps 上升，在下一个 CONV 上升时下降。
* UP/DN 每线负载 15 fF（v0.1 为 12 fF）：两个 CDAC 控制输入（DAC-13 各 ≤ 6 fF）+ 3 fF 走线。CLKC 负载 20 fF。
  按 ΣC·V·f 估算，这些输出负载（UP/DN 13 × 15 fF、CLKC 14 × 20 fF、RDY 与 D 各 50 fF，D 每位 0.25~0.5 次上升）约 63~79 µA、57~71 µW，LOG-13（≤ 300 µW）仍有余量。
* 输入：CONV ≤ 40 fF（LOG-14），OUTP/OUTN 各 ≤ 7 fF（LOG-15，比较器输出负载 10 fF 减 3 fF 走线），每个上升沿的电荷 / VDD。

### adc_cdac
* 26 个半电容（`cu = 1.0 fF`，LSB 半电容 0.5 fF），j = 9（180）和 j = 6（32）不采样（满量程 > VREF 的关键）。
* 输入开关：栅极接 VG 的 NMOS，按电容大小缩放（时间常数相同），并联总电阻 ≤ 15 Ω。
* 权重不必精确，但必须可校准：系统误差 + 4σ 失配（1 fF 单位 σ = 0.5 %）在冗余之内（DAC-03），校准后 ENOB 损失 ≤ 0.02 bit（DAC-14）。
* 驱动器：VREFP/VREFN 之间的反相器，CONV = 0 时采样半电容的驱动器三态；`DH` 拉低 H 半，`RL` 抬高 L 半。
  在 VDD = 0.81 V、VREFP = 0.9 V 时 PMOS 关断栅压只有 0.09 V，需用 svt/hvt 或从 VREFP 取预驱动电源。
* 上极板寄生 ≤ 10 % C_DAC（含比较器输入），上极板复位开关在 PHI_S 下降时断开（采样时刻）。
* 时钟输入（每个上升沿的电荷 / VDD）：PHI_S、PHI_SB 各 ≤ 40 fF（DAC-15/16），CONV ≤ 80 fF（DAC-17）；
  DH/RL 控制输入仍 ≤ 6 fF（DAC-13）。PHI_S/PHI_SB 直接驱动上极板复位开关时，40 fF 栅电容约对应每管 35~40 µm；
  在 VCM = 0.45 V（Vgs ≈ 0.45 V）下这样的传输门导通电阻估计在 70~100 Ω，远大于行为级的 ron_top = 10 Ω。
  跟踪时间常数 (50 + 12.5 + 100) Ω × 2.057 pF ≈ 0.33 ns，4.1 ns 跟踪窗口内约 12 τ，建立不受影响；
  上极板电压只在 VCM 附近小幅变化，电阻近似恒定。DAC-09/10 在晶体管级确认；若开关必须更大，可在 CDAC 内
  用本地缓冲驱动它，但缓冲的延时与抖动会进入采样时刻（CLK-09 只计 adc_clkgen），需事先在 issue 中讨论。

### adc_bootstrap
* 经典栅压自举（Abo/Gray 结构），升压电容在转换期间充电；负载为一侧全部输入开关的栅电容
  （测试台中用 96 µm/30 nm `nch_ulvt_mac` + 2.057 pF 作为参考负载）。
* 所有薄栅器件端电压 ≤ 1.0 V（各工艺角，BST-08 逐管检查 |Vgs|、|Vgd|、|Vds|，见 [`verification.md`](verification.md) §5）；PHI_B 下降后 VG 需在 60 ps 内降到 0.1 V 以下。
* PHI_B、PHI_BB 输入各 ≤ 16 fF（BST-09/10，每个上升沿的电荷 / VDD）：时钟负载 40 fF 由两个自举电路分担，另留 8 fF 走线。
  关断下拉管（约 110 fF × 1.8 V 在 40 ps 内放完，需数 mA）若由 PHI_BB 直接驱动会接近或超过该限值，可加一级本地缓冲，
  其延时计入 BST-03（≤ 60 ps，自 PHI_B 下降沿起）。

### adc_clkgen
* 输入为外部 CLK（高电平跟踪）。相位顺序：CLK↓ → PHI_S↓ → PHI_B↓（20–80 ps 后）→ CONV↑；
  CLK↑ → CONV↓ → PHI_B↑/PHI_S↑（先断后合）。
* PHI_S 下降沿决定采样时刻：边沿 ≤ 20 ps、抖动 ≤ 60 fs（瞬态噪声测量）。
* 输出负载（规格 `operating.loads`，测试台由此生成）：PHI_S/PHI_SB 各 100 fF，PHI_B/PHI_BB 各 40 fF，CONV 250 fF，
  共 530 fF。CLK-10 计 AVDD 的全部平均电流（TT ≤ 80 µA），含这些负载的充放电（ΣC·V·f = 47.7 µA），
  其余约 30 µA 留给反相器链内部节点与短路电流。接收端受输入电容限值约束（见上文“接口负载与输入电容”），
  这 530 fF 因此是有约束的上限，而不只是估计。

### adc_ref
* VREF_IN（0.900 V，高阻）→ VREFP，必须由 AVDD18 供电（可用 1.8 V 厚栅器件）。**全部片内**：
  nF 级去耦只能放片外（键合线寄生），不采用；pF 级去耦可以串电阻。拓扑、电流、去耦由设计者决定，不设功耗上限。
* 规格只约束 VREFP 在比较器使用它的时刻：`tb_ref_replay` 把系统级模型一次近 Nyquist 转换序列的 CDAC 电荷
  （v0.3：起始 0.93 pC + 13 次切换，含与信号相关的部分）灌入 VREFP，在每个判决时刻采样，再送回模型计算 ENOB 损失
  （REF-12 ≤ 0.1 bit）；判决 12~14 没有冗余，期间 VREFP 变化 ≤ 200 µV（REF-13）；无跨转换记忆（REF-14）；
  10 kHz~100 GHz 噪声 ≤ 120 µV（REF-08，约 0.12 bit；1~10 kHz 只是增益漂移，单独报告）。
* 行为级起点：开环 NMOS follower（EKV 模型）4 mA、去耦 3 pF（v0.3 电荷加倍；v0.2 的 2 mA + 1.5 pF 回放损失 0.027 bit，
  电流与电容同乘 2 时 VREFP 波形相同）。系统级模型给出的方向：
  节点电容越小越好，恢复时间常数 C/g_s ≲ 60~80 ps；几十 pF 的去耦配 mA 级驱动是最坏区域。
  研究过程与被排除的方案见 [`docs/reference.md`](reference.md)。
* 需要在晶体管级确认：器件 g_s/I 与源极电容、慢角大信号恢复、栅极复制偏置的精度与噪声、AVDD18 耦合。
* 直流测试（REF-01、`tb_ref_dc`）与噪声测试（`tb_ref_noise`）的 VREFP 负载为 v0.3 的 CDAC 平均电流 200 µA
  （规格 `operating.load_vrefp_dc`，测试台由此生成）：每次转换两侧共 0.93 pC（起始）+ 1.02 pC（13 次切换）= 1.95 pC，
  × 100 MHz = 195 µA（v0.2 为 100 µA），覆盖近 Nyquist 回放（`tb_ref_replay`，npts 1024，49.707 MHz）积分得到的
  平均 176 µA（与信号相关的部分使平均值略低）。REF-01、REF-04、REF-11 都在这个工作点上测；负载扫描 0~200 µA
  是特性表征（负载调整率，只报告，不设限值）。回放测试照旧只施加实际的电荷序列，不另加直流电流源。
* VCM = 0.45 V ± 10 mV，只给上极板复位，负载很小。**VCM 负载（2 × 2.5 pF，100 MHz 切换）没有任何 adc_ref 测试台施加，
  也没有模块级的 VCM 动态限值**：VCM 的验收是 REF-02（直流）加顶层混合回归（`tb_top_sine`，用晶体管级 `adc_ref`），
  后者施加真实的上极板切换。理由：
  * 跟踪期间 P、N 两个上极板一起复位到 VCM，它们退回的电荷一阶上大小相等、方向相反（差分输入的变化），在 VCM 节点抵消，
    平均电流 ≈ 0；
  * 剩下的是共模误差，只能经 P/N 失配进入差分结果，而比较器输入共模范围（0.40~0.56 V）给它留了余量；
  * 所以 VCM 建立误差主要移动共模，漏进结果的部分由顶层 ENOB 与满量程检查发现。
  需要时可另开 issue 加一个跟踪结束时 VCM 建立的表征测试台（不设限值）。
* **上电顺序（#34）**：只支持一种顺序（规格 `operating.power_up_sequence` / `power_up`，[`architecture.md`](architecture.md) §7.3）：

  1. AVDD 与 AVDD18 先上电，AVDD 不晚于 AVDD18，每个斜坡 ≥ 1 µs；此期间 VREF_IN 保持 0 V。
  2. 两个电源都稳定之后，VREF_IN 以 ≥ 10 µs 的斜坡从 0 升到 0.9 V。
  3. 就绪（ready）之前 CLK 保持静止（不转换）；就绪 = VREF_IN 到达 0.9 V 之后 5 µs，此后的转换才有效。

  其它任何顺序都不支持、不验证。`tb_ref_startup`（全部工艺角）按这个顺序施加电源与 VREF_IN（两个电源一起在 1 µs 内上升，
  VREF_IN 在 2~12 µs 斜坡，就绪 17 µs，运行到 20 µs），负载为 VREFP 1.2 pF、VCM 2 × 2.5 pF，没有直流负载（CLK 静止）：
  REF-15~18 要求整个过程中 VREFP、VCM 在 −0.1~1.0 V 之内，REF-19 要求从就绪起 VREFP 与其终值之差 ≤ 5 mV。
  报告（不设限值）：终值 VREFP − VREF_IN（启动失败会在这里显出约 −900 mV）、终值 VCM、斜坡期间最大 |VREFP − VREF_IN|、
  斜坡结束后进入 ±5 mV 的时间。逐管 SOA 检查不用于 `adc_ref`（厚栅器件）。负责人此前看到的 1.39 V / 1.085 V 峰值
  来自不支持的顺序（20 ns 的 VREF_IN 阶跃、VREF_IN 已存在时电源上升），不必再满足；在支持的顺序下需要确认的是：偏置与伺服
  从零电源正常启动、斜坡期间不饱和、5 µs 内进入 ±5 mV。行为级视图的 follower 与 VCM 驱动是与 AVDD18 / AVDD 无关的理想电流源，
  只能体现 VREF_IN 斜坡与建立，体现不了电源裕量与偏置启动。

## 建议顺序

1. 同时启动：`adc_comp`、`adc_sarlogic`（共同决定转换时间），`adc_cdac` + `adc_bootstrap`（共同决定线性度，
   两人需对齐输入开关的栅电容与导通电阻），`adc_ref`、`adc_clkgen`（相对独立）。
2. 每个模块通过自己的验收后，项目负责人逐个替换进顶层（`--view <block>=xtor`）跑 `tb_top_sine` quick 角。
3. 全部替换后跑 45 角顶层回归，签核（项目负责人）。
