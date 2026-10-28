# 验证计划

各模块的端口、指标与用例清单见 [`docs/specs.md`](specs.md)（由规格生成）。本文说明验证的层次、
约定和行为级模型的现状。

## 1. 层次

| 层次 | 工具 | 作用 |
|---|---|---|
| 系统级模型 | `tools/adcflow/model.py` | 架构与预算；所有仿真结果的参照（`python -m adcflow budget`） |
| 行为级视图 | `design/behav/*.scs` + Verilog-A | 每个模块与晶体管级视图端口完全一致；验证测试台、度量与顶层时序 |
| 模块验收 | `tb/<block>/*.scs` + `measure/<block>.py` | 同一测试台测行为级或晶体管级；限值来自规格 |
| 顶层验收 | `tb/top/tb_top_sine.scs` | 任意视图组合，45 个工艺角回归 |
| CI | GitHub Actions | 端口契约、RNL、生成文件、结果判定、单元测试、站点信息检查 |

## 2. 约定

* **工艺角**：`<process>_<supply>_<temp>`，例如 `tt_nom_27`、`ss_low_m40`。集合 `typ`（TT）、
  `quick`（7 个极端角）、`all`（45 个）。电源 ±10 % 同时作用于 0.9 V 与 1.8 V；VREF_IN 恒为 0.900 V。
  规定的电源包络就是这三档：AVDD 0.81~0.99 V，AVDD18 1.62~1.98 V。扫描电源的测试也不超出它：REF-04（`tb_ref_dc`）
  在每个工艺角都把 AVDD18 扫过 1.62~1.98 V（`corners.supply_envelope`），与该角自己的电源无关，工艺与温度仍随工艺角变化。
  以前的 `vdd18*0.9 … vdd18*1.1` 会叠加在该角电源上，高压角扫到 2.178 V，超出包络（#46）。
* **指标的适用工艺角**：每项指标只在其 `corners:` 集合（按 `corner_set` 展开）内的工艺角上判定；蒙特卡洛指标（`mc:`）
  只判 MC 运行，其它指标 MC 与标称运行都判。判断由同一个函数 `Spec.applies` 给出，结果写入、终端摘要、`check results`、
  `report`、证据图的规格表和站点共用。同一用例中其它工艺角的结果照常保存全部原始 metrics，结果 JSON 的 `specs_na`
  列出不适用的指标（值与适用集合，无判定），报告与站点标为 n/a；它们不计入该指标的最坏值、失败数和覆盖率。
  覆盖率 = 已记录的适用工艺角（去重，同一角的多个变体只算一次）/ 适用集合。适用角缺失时该指标无结果（签核时报错），
  适用角不通过即不通过；仿真错误与过期结果在任何工艺角都照常报告。例如 CLK-10（`corners: typ`）只判 `tt_nom_27`，
  `ff_high_125` 的 AVDD 电流作为实测值保留，供系统评估（#29）。
* **瞬态数值设置**：每个结果的 `meta.numerics` 记录仿真器实际使用的设置，读自 `spectre.log` 的
  `Important parameter values`：`reltol`、`maxstep_ps`、`method`、`errpreset`、`lteratio`、`abstol_V`，全局 `vabstol`，
  接受的步数 `steps_accepted` 与平均步长 `step_mean_ps`；保存了整段波形（从 t = 0 到结束）的测试另记实际最大步长
  `step_max_ps`，否则为 null（例如跟踪测试 `save=none`、`outputstart=tstop`，步长以 `maxstep` 为上限）。
  需要固定设置的测试在规格中写 `numerics:`，由 `gen_tb.py` 写进测试台的 `options`、`tran` 语句（测试台计入结果哈希）。
  **跟踪线性度测试**（`tb_bootstrap_track`、`tb_cdac_track`，BST-05/06、DAC-09/10）用 `reltol=1e-7`、`vabstol=1e-8`、
  `maxstep=1p`、`method=traponly`（#28）：默认设置（`reltol=1e-5`，`maxstep` 为仿真长度的 1/50 = 52.1 ns）下晶体管级开关的
  SFDR / SNDR 为 66.7 / 63.3 dB，没有收敛（收敛后约 93.6 / 93.0 dB），且在 `maxstep` 20 ps~1 ps 之间不单调，
  因此不能挑选某个粗步长的结果作证据。激励、采样时刻、FFT、端口、负载和限值不变。
* **收敛交叉检查**：`python -m adcflow sim <test> --crosscheck` 让每个 job 再用规格 `crosscheck:` 的设置跑一次
  （跟踪测试：`maxstep=0.5p`、`method=gear2only`，其余同 `numerics`），只记录原设置的结果，差值写进它的 `meta.crosscheck`：
  两次的设置（要求的与实际的）、各指标的两个值与差、原始样本（`samples.txt`）的个数、采样时刻的最大差、逐样本差的 rms 与最大值；
  有逐管 SOA 时还有各对峰值的最大变化（§5）。**必须重做的时机**：跟踪测试在有代表性的最坏工艺角（对开关导通电阻与边沿最敏感的
  角，例如 `ss_low_m40`、`ss_low_125`、`ff_high_125`）以及模块设计有实质改动（拓扑、开关或自举电容尺寸、负载、时钟边沿）之后
  至少各做一次；正式验收在同步后的 `main` 与最终候选电路上重做。差值与指标到限值的余量相比必须可以忽略（#28 中晶体管级
  TT 的参照：两种方法差 0.05 dB SFDR、0.01 dB SNDR，样本差 2.8 µV rms），否则结果不能作证据，先查明原因。
  行为级 TT 的交叉检查见 §3 后的表。
* **频谱指标**：ENOB、SNDR、SNR、THD 由 ADCToolbox 0.6.4（`pyproject.toml` 固定版本）计算；SFDR 由 `tools/adcflow/spectrum.py`
  按 MATLAB `plotspec` 的定义计算（基波峰值频点 / 信号频点与 DC 之外最大的单个频点，含 Nyquist），因为 0.6.4 的 SFDR
  在杂散紧挨信号频点时出错（#36）。比较与依据见 [`docs/sfdr-estimator.md`](sfdr-estimator.md)；结果的
  `meta.provenance.spectrum` 记录所用的估计器。注意：ADCToolbox 0.6.4 `compute_spectrum` 返回的 `plot_data.is_coherent`
  实际是参数 `coherent_averaging`（是否做了多次记录的相干平均），不是按频点偏差判断的相干性。不能用它判断输入频率是否相干，
  相干性看实际的 fin、N 与 k（#47）。
* **噪声**：`noise_en=1` 时行为级模型注入比较器噪声、采样 kT/C 与时钟抖动；有晶体管级视图时
  （`devnoise=1`）打开 Spectre 瞬态噪声（`noisefmax`）。
* **正弦测试频率**：`fin_target=49.9 MHz` 取不超过 Nyquist−3 个频点的最大相干奇数频点
  （1024 点：49.71 MHz；256 点：48.83 MHz），避免窗函数主瓣碰到 Nyquist 频点。测试台模板里的 `fin` 只是占位值，
  不一定相干：用例的 `prepare`（`measure.top:prepare`、`measure.ref:replay_prepare`）按 `npts` 换成相干频率，
  所以要经 `python -m adcflow sim` 运行，不要直接拿模板仿真（模板中有注释说明，#47）。
* **ENOB**：按 −1 dBFS 输入测得的 SNDR 计算（不归一化到满量程），即 `(SNDR − 1.76)/6.02`。
  **验收用校准权重**（架构 v0.3 起；ADC 输出原始位，后端用每颗芯片的校准权重重建）：测试台连续采
  `ncal + npts` 次转换（各 1024），前 `ncal` 次是**校准记录**，用 `adctoolbox.calibrate_weight_sine`（wcalsin
  方法）拟合各位权重并缩放到标称权重之和；后 `npts` 次是**判定记录**（同一相干正弦的另一段：独立噪声、不同相位），
  用这组权重解码后算 ENOB / SNDR / SFDR（`enob`、`sndr_dBc`、`sfdr_dBc`，TOP-01/02/03/08/09 用它们）。
  权重不在被判定的记录上拟合，因此不会过拟合。同一记录按标称权重解码的结果报告为 `enob_nom`、`sfdr_nom_dBc` 等，
  不设限。实现见 `tools/adcflow/calib.py`、`measure/top.py`；系统模型用同一方法（`model.sine_test_cal`）。
* **比较器噪声**（`tb_comp_noise`）：17 个差分输入电平（±800 µV）× 每电平 512 次判决，用二项分布最大似然的
  probit 模型 `P(OUTP) = Φ((vd − μ)/σ)` 拟合计数，σ 为输入等效噪声、μ 为失调；同时报告 σ 的 95 % 剖面似然区间
  `noise_ci95_uV`。120~300 µV 时 σ 的 1σ 统计误差 ≤ 2.7 %（蒙特卡洛，无可测偏差）。验收仍按点估计对限值判定；
  区间说明结果离限值有多近（点估计在限值附近、区间跨过限值时，结论应附上区间）。
  无偏检查（行为级比较器 σ = 200 µV，`seed0` = 11 / 1 / 2 / 3 / 4 / 5，TT，`aps`）：201.5 / 201.4 / 202.8 / 200.2 / 198.4 /
  200.1 µV，平均 200.7 µV（+0.4 %），每个 95 % 区间（约 ±4 %）都包含 200 µV。旧方法（对比例最小二乘、13 × 64 或 17 × 128）
  在同一模型上得到 75.9 µV（σ = 80 µV）和 179.7 µV（σ = 200 µV），偏低是单次的统计起伏而不是方法偏差，但 ±6 % 的起伏
  与离限值的余量同量级，因此改为最大似然并加到每电平 512 次。仿真时间：行为级每次约 2.6 min（17 × 128 时约 2.1 min），
  瞬态长度 3.5 µs（原来的 4 倍）；晶体管级按比例增加。
* **可校准性**：校准只能纠正没有缺口的传递函数。CDAC 的 DAC-03 要求实测权重的系统误差加 4σ 失配
  落在每次判决的冗余之内，DAC-14 要求按上述方法校准后的 ENOB 损失 ≤ 0.02 bit（`docs/noise-budget.md` §5.2）。
* **结果过期**：结果 JSON 中的文件哈希与当前文件不一致即为过期，签核模块的过期结果 CI 报错。证据图（§4）不单独计哈希：
  图与 JSON 来自同一次仿真，JSON 过期则其图一并过期。

## 3. 行为级基线（架构 v0.3，TT，`aps`，`results/*/behav/`）

行为级视图在 TT 下通过了全部已记录的指标（`python -m adcflow report`，`check results --strict` 无错误无警告），
证明测试台、度量与限值彼此一致；晶体管级视图将用同一批测试台验收。v0.3 的行为级比较器噪声 σ = 190 µV（略低于 TT 限值 200 µV，约等于 `mc12`；取在限值上时无偏测量有一半机会不通过）。

| 模块 | 关键结果 |
|---|---|
| 顶层 `tb_top_sine`（1024 点校准 + 1024 点判定，49.71 MHz，−1 dBFS，噪声开） | ENOB 10.91（校准权重，验收；标称权重 10.88），SNR 67.6 dB，THD −83.4 dBc，SFDR 84.0 dB（`adcflow.spectrum`，#36；ADCToolbox 0.6.4 报 83.3 dB），FS 0.994 V，t_conv 2.72 ns，无丢失 RDY，8.01 mW（AVDD18 7.52 mW） |
| 顶层低频 / 占空比 45 %、55 % | ENOB 10.94 / 10.95 / 10.95（标称 10.90 / 10.89 / 10.90） |
| `adc_comp` | 噪声 189.5 µV，95 % 区间 181.7~197.7 µV（行为级 σ = 190 µV；17 × 512 次判决，二项最大似然），1 mV 时延 76 ps，30 mV 49 ps，τ 8 ps，回踢 ≈ 0（行为级比较器无回踢），Cin 15 fF，CLKC 12 fF，能耗 112 fJ |
| `adc_sarlogic`（UP/DN 负载 15 fF） | 1000 次随机转换 0 错误，转换 2.57 ns（比较器 70 ps 时 2.90 ns），超时 285 ps，210 µW；输入电容 CONV 30 fF、OUTP/OUTN 5 fF |
| `adc_cdac` | C_S 2.057 pF，FS 0.993 V，可校准性裕量 0.465 LSB，校准后 ENOB 损失 ≈ 0（标称 0.07 bit，4 颗失配芯片）；RL12 建立 12.7 ps，τ 1.2 ps，起始建立 11.4 ps；VREFP 电荷 0.77 pC；跟踪 SFDR 132.7 dB / SNDR 130.6 dB（显式数值设置，已到数值底噪，> 130 dB；默认设置的 109.3 / 101.8 dB 是数值噪声，见下）；输入电容 DH/RL 4.5 fF、PHI_S/PHI_SB 30 fF、CONV 60 fF |
| `adc_bootstrap`（参考开关 96 µm + 2.057 pF） | VG−VIN 0.855 V，关断 18 ps，开启 68 ps；跟踪 SFDR 94.6 dB / SNDR 94.6 dB（显式数值设置；默认设置为 92.6 / 85.8，v0.2 为 97.2 / 89.6，均未收敛，见下）；SOA 仅外部节点（参考开关，§5）：最大 \|Vgs\| 0.900 V（VG 为 0、VIN = 0.9 V 时，负向），0 违例；PHI_B/PHI_BB 输入 12 fF |
| `adc_clkgen`（规格负载共 530 fF） | PHI_S 延时 46 ps，PHI_S→PHI_B 40 ps，抖动 46 fs，占空比 45/55 % 无错误，AVDD 70 µA（行为级占位，含负载，CLK-10 ≤ 80 µA）；SOA（CLK-11，§5）：行为级没有可检查的器件（`external`，0 对，`soa_note` 说明），不是晶体管级证据 |
| `adc_ref`（follower 4 mA + 3 pF） | 回放 ENOB 损失 0.018 bit，判决 12~14 变化 41 µV，记忆 ≈ 0，最大跌落 9.1 mV；噪声 43.9 µV（带 1.2 pF 与 200 µA）；直流 −2.0 mV（200 µA 负载）；上电（支持的顺序，`tb_ref_startup`）VREFP 0~0.900 V、VCM 0~0.450 V，电源已上、VREF_IN 为 0 的 5 µs 内两者都为 0，斜坡期间跟随误差 4 µV，就绪后 |VREFP − VREF_IN| ≈ 0、VCM 450.0 mV（行为级 follower 与电源无关，只体现 VREF_IN 斜坡；交叉检查 maxstep 0.1 ns / gear2only 差 < 0.1 µV） |

* TT 顶层 ENOB 10.91 比模型的行为级条件（比较器 200 µV 时 10.97，8192 点）低约 0.06 bit：一部分是行为级的
  THD（−83.4 dBc，模型未计），其余是 1024 点记录的统计起伏（SNR 估计约 ±3 %）。比较器取 200 µV 时实测为 10.84，
  TOP-02 因此取 10.75（用户决定，验收仍用 1024 点记录）；结果接近限值时可用更长记录
  （`--param npts=4096 --param ncal=4096`）复核。
* 接口负载 PR（各输入加了明确的输入电容）之后，几个行为级数值有变化，都是数值精度而不是电路变化：顶层 DVDD
  0.195 → 0.211 mW，即占位值本身（14 × 150 fJ × 100 MHz + 漏电 = 0.211 mW）；CDAC 跟踪 SFDR 97.9 → 109.3 dB
  （行为级采样网络是线性的）。推测原因是时钟沿处的电容迫使仿真器在这些沿上取更细的步长。
* 噪声关闭时顶层 ENOB 约 11.85（量化极限 12.0；v0.1 测得，v0.2/v0.3 未重测）；`ax` 模式下行为级 ADC 精度不足，因此验收一律用 `aps`。
* 行为级参考的 AVDD18 电流即 follower 偏置（4 mA）加 CDAC 平均电流；其余模块的功耗为预算值
  （固定电流 + 每次判决的电荷），不代表电路实际功耗。
* 参考电压的规格只约束判决时刻的行为（`tb_ref_replay`），回放方法见 `docs/reference.md` §6。

**跟踪测试的数值设置与收敛交叉检查**（行为级，TT，`aps`，`sim --crosscheck`，§2，#28）。“默认”是改动前 `main` 上的结果
（#32 之后，`reltol=1e-5`，`maxstep` 52.1 ns）；“显式”是 `numerics` 设置（记录的结果）；“交叉检查”只改 `maxstep=0.5p`、`gear2only`。
样本差是 256 个原始样本的逐点差，两次的采样时刻相同。显式与交叉检查的 SFDR 按 `adcflow.spectrum`（#36）计算，默认一行是旧值。

| 测试 | 设置 | SFDR (dBc) | SNDR (dB) | 接受步数 | 仿真时间 |
|---|---|---:|---:|---:|---:|
| `tb_bootstrap_track` | 默认 | 92.60 | 85.76 | 108 888 | 27 s |
| | 显式（1 ps，traponly） | 94.57 | 94.56 | 2 880 232 | 158 s |
| | 交叉检查（0.5 ps，gear2only） | 94.92 | 94.92 | 5 520 721 | 276 s |
| | 差（交叉检查 − 显式） | +0.35 | +0.36 | 样本差 1.6 µV rms，最大 2.1 µV | |
| `tb_cdac_track` | 默认 | 109.26 | 101.78 | 99 729 | 43 s |
| | 显式（1 ps，traponly） | 132.67 | 130.65 | 2 841 646 | 257 s |
| | 交叉检查（0.5 ps，gear2only） | 147.70 | 142.73 | 5 476 398 | 406 s |
| | 差（交叉检查 − 显式） | +15.0 | +12.1 | 样本差 0.16 µV rms，最大 0.38 µV | |

* `tb_bootstrap_track`：SFDR、SNDR 与 −THD 几乎相等，频谱由一个约 −95 dBc 的谐波主导（约 16 µV），µV 级的数值差就使它变化
  零点几 dB；+0.36 dB 比到限值的余量（BST-05/06：12.6 / 16.6 dB）小得多，结果可以作证据。默认设置下 SNDR 低 8.8 dB，
  是没有收敛的数值噪声，不是电路的性质。
* `tb_cdac_track`：行为级 CDAC 的采样网络是理想的线性模型，显式设置下剩下的只有积分的数值误差（样本差 0.16 µV rms，
  约为 0.72 V 幅度的 −133 dB）。SFDR / SNDR 因此停在 130~150 dB 的数值底噪上，随设置跳动十几 dB，不是一个稳定的 dB 值；
  收敛的结论是“> 130 dB，受数值精度限制”，两次都比 DAC-09/10 的限值（85 / 80 dB）高 45 dB 以上，判定不受影响。
  默认设置下的值同样是数值噪声：#32 前 97.9 / 91.2 dB，#32 只在 CDAC 的时钟输入上加了电容（与线性度无关）后变成
  109.3 / 101.8 dB。这一行为级数值只说明测试台与度量已收敛，不代表电路；晶体管级开关接入后，收敛判断以 dB 差相对余量和
  样本差为准。
* 运行时间：显式设置约为默认的 6 倍（158 s 对 27 s，257 s 对 43 s），交叉检查再约 1.6~1.7 倍；一次 `--crosscheck` 的总耗时
  bootstrap 9 min、CDAC 13 min（两个 job 并行，排队时更长）。晶体管级视图按电路规模增加。

## 4. 证据图

每个结果 JSON 都带可读的证据图：度量函数用已读入的数据画图，写在结果旁，
`results/<block>/<test>/<view>/<stem>.<tag>.png`（`<stem>` 是 JSON 文件名去掉扩展名，例如
`tt_nom_27.spectrum.png`、`tt_nom_27__duty0.45.codes.png`），JSON 里的

```json
"figures": [{"file": "tt_nom_27.spectrum.png", "caption": "一句话说明这张图。"}]
```

列出文件与说明。约定：matplotlib（Agg）、固定样式与字体、图中文字一律英文；坐标轴带单位；
有规格的地方画出规格线（限值取自 `specs/blocks/*.yaml`，由 `figures.limits` 读取）；
每张图顶部一行 `测试 | 视图 | 工艺角`；每个 PNG ≤ 200 KB（超出时自动降低分辨率）；输出不含时间戳，同一数据画出的图逐字节相同。
频谱图（`figures.plot_spectrum`）用与正式度量相同的周期 Hann 窗（`spectrum.hann`），相干单音只占 k−1 … k+1 三个频点；
图中写出窗类型与实际的 N、fs、fin 和频点 k。以前用对称 Hann 窗（`numpy.hanning`），载波两侧多出 −58 dBc（N = 256）或
−70 dBc（N = 1024）的窗口旁瓣，看上去像杂散或非相干输入（#47）。只改图时用 `python -m adcflow remeasure <test> --run <dir> --redraw`：
用原来的运行数据重画，任何指标与记录不同即中止，结果中写 `meta.redrawn`。
重跑一个结果会先删掉它旧的图，再写新图。

| 测试 | 图（`<tag>`） | 内容 |
|---|---|---|
| `tb_comp_delay` | `delay` | 延时随输入差的变化（含 ln 拟合与限值）、±1 mV 判决瞬态并标出延时、复位到 10 % VDD |
| `tb_comp_noise` | `noise` | 判决概率与二项分布最大似然 probit 拟合（及 σ 的 95 % 区间带、限值处的曲线）、拟合残差与二项分布误差带 |
| `tb_comp_kickback` | `kickback`、`cin` | 每个周期后的差分输入、每周期变化量对限值、Cin 与 CLKC 输入电容；CLKC 各上升沿的输入电容对限值（§6） |
| `tb_cdac_weights` | `weights` | 各位权重与标称、各位权重误差对 0.5 % 限值、上升/下降步长不对称 |
| `tb_cdac_settle` | `settle`、`cin` | 整个序列的顶板波形；起始与 RL12 / RL5 / RL0 之后的误差（对数坐标），标出容差线、建立时间与限值；规格表；PHI_S、PHI_SB、CONV 各上升沿的输入电容对限值（§6） |
| `tb_cdac_track` | `spectrum` | 顶板采样谱，SFDR / SNDR 对限值 |
| `tb_bootstrap_dc` | `switch`、`soa`、`cin` | VG−VIN 随输入、最坏关断 / 开启边沿（时延与限值）、参考开关三对端电压对 ±1.0 V、规格表；逐管 SOA（§5）：各器件各端电压的最大 \|V\| 对限值、最坏一对的全程波形与峰值附近的时间点；PHI_B、PHI_BB 各上升沿的输入电容对限值（§6） |
| `tb_bootstrap_track` | `spectrum` | 经自举开关采样的频谱，SFDR / SNDR 对限值 |
| `tb_clkgen_timing` | `timing`、`soa` | CLK 下降 / 上升沿处 PHI_S、PHI_B、CONV 时序、PHI_S 下降沿（80 %→20 %）、占空比 50 / 45 / 55 % 各周期的延时与间隔对限值、规格表与 CLK-11 的 SOA 范围；逐管 SOA（§5，有器件时）同 `tb_bootstrap_dc` |
| `tb_clkgen_jitter` | `jitter` | 采样相位沿的直方图与高斯、各沿残差、限值处曲线 |
| `tb_sarlogic_func` | `decisions`、`conversion`、`timing`、`cin` | 输出码对输入、各判决位置的错码数、转换时间直方图；一次异步转换的波形（14 个比较器时钟、DAC 控制沿、RDY）；各环路时间逐事件对限值；CONV、OUTP、OUTN 各上升沿的输入电容对限值（§6） |
| `tb_sarlogic_rand`、`_func_slow` | `decisions` | 同上（无波形） |
| `tb_sarlogic_timeout` | `decisions`、`timeout` | 同上；比较器不应答时 CLKC 被超时拉低的波形与每次超时时间对窗口 |
| `tb_ref_dc` | `dc` | VREFP 随负载、随 AVDD18、VCM 随负载（含窗口与斜率限值）、规格表 |
| `tb_ref_noise` | `psd` | VREFP / VCM 噪声谱密度与 10 kHz 积分起点、积分噪声对 120 µV 限值 |
| `tb_ref_startup` | `startup` | 支持的上电顺序下电源、VREF_IN、VREFP、VCM 的全程波形对 −0.1~1.0 V 窗口；斜坡期间对 VREF_IN 的跟随误差；斜坡后 VREFP 向终值的建立、±5 mV 带与就绪时刻；规格表 |
| `tb_ref_replay` | `replay` | 各判决时刻 VREFP 偏差对冗余容差包络与 12~14 判决限值、转换前 VREFP 的记忆、转换内跌落、ENOB 代价 |
| `tb_top_sine`、`_sine_lf`、`_duty` | `spectrum`、`codes` | 输出谱（标称与校准权重）标注 ENOB / SNDR / SFDR 与限值；码对正弦相位折叠及拟合、拟合误差、转换时间直方图 |

`python -m adcflow check results --strict` 检查：`figures` 中列出的文件必须存在、命名为 `<stem>.<tag>.png`
并 ≤ 200 KB；`--strict` 下每个有结果的 JSON 必须有图（失败的结果除外）；结果旁未列入清单的 PNG 报警告。
新增测试的度量函数从 `ctx["figs"]` 取得接收器并至少画一张图，见 `docs/workflow.md` §4。

## 5. 逐管 SOA 检查

规格中“每个薄栅器件 |Vgs|、|Vgd|、|Vds| ≤ 1.0 V，各工艺角”的要求由 `adcflow` 的通用 SOA 检查
（`tools/adcflow/soa.py`）验收，目前用于 `adc_bootstrap` 的 BST-08（`tb_bootstrap_dc`）和 `adc_clkgen` 的 CLK-11
（`tb_clkgen_timing`，#27）。

**启用**：在模块规格的用例下加 `soa:`。

```yaml
tests:
  tb_bootstrap_dc:
    soa: {dut: [XDUT], external: [MSWP]}
```

* `dut`：要检查其内部器件的测试台实例（缺省为本模块在测试台中的全部实例）。
* `external`：测试台自身位于 DUT 边界上的薄栅器件，例如参考输入开关；任何视图都检查（缺省为测试台顶层的全部薄栅 MOS）。

其它模块（例如由 VG 驱动的 CDAC 输入开关）启用时：在用例下加同样的 `soa:`；度量函数读入瞬态波形
`w = tran(job_dir)` 后调用 `soa.measure(ctx, w, m)`，画图时调用 `soa.figure(fg, ctx, m, w)`；
规格中加一条 `metric: soa_violations, max: 0, corners: all` 的指标。测试台不必改：要保存的节点由流程加进 deck。

**器件分类**：`specs/soa.yaml` 给出限值 `limit_V: 1.0` 与器件模型的分类。薄栅 MOS（端口 d g s b）检查 gs、gd、ds 三对，
薄栅 MOS 电容（p n）检查 pn；厚栅（1.8 V）器件不检查，列在结果的 `soa_skipped`。名称像 MOS 器件（`mos_pattern`）
却没有列出的模型使检查无法验证。该文件记入结果的 `meta.files`，改动会使相关结果过期。端电压取 PDK 宏模型
（`*_mac`）实例的端口，即网表中写出的节点。

**机制**：建 deck 时（`runner.make_deck`）从 `dut` 实例往下展开所选视图的网表（包括子电路层次），列出每个器件及其
端口所接的节点：接到 DUT 端口的映射为测试台网络，内部节点写成层次名（`XDUT.net1`、`XDUT.X1.net2`）；deck 在测试台之后
追加一条只含这些节点的 `save`（测试台已保存的不重复）。Spectre 有显式 `save` 时只保存所列信号，数据量小。仿真后对每个器件、
每对端口计算 V(a) − V(b) 在**全部时间点**上的最大绝对值、发生时刻与正负号，超过 `limit_V` 即为违例；`soa_violations`
是违例的器件/端口对数，同一对多次超限只计一次。

选用“保存端电压后分析”而不用 Spectre 器件断言（`assert`）：断言只报告超限，给不出未超限器件的最大值与时刻，而验收要求每个器件、
每对端口都有可追溯的最大值；`*_mac` 是宏模型，断言须挂在其内部的基础器件或模型名上，这些名称随 PDK 而变；节点电压则由现有的
PSF 读入器解析，器件与节点的对应关系由流程自己写出，可复现。

时间分辨率就是仿真器接受的时间点：不抽样（无 strobe），也不允许 `outputstart`（波形不从 t = 0 开始即为无法验证）；Spectre 在
边沿与振荡处按局部截断误差自动缩小步长。用一个故意违例的晶体管级小网表（TT，`aps`；不入库，因含 PDK 路径）验证：

| 用例 | 器件 | 结果 |
|---|---|---|
| 负向 Vgs（栅 0 V，源 1.15 V） | `XDUT.MNEG` | gs = −1.150 V，违例 |
| Vds（漏 1.15 V） | `XDUT.MVDS` | ds = 1.150 V，违例 |
| 内部节点（嵌套子电路，栅接 RLC 振荡的内部节点） | `XDUT.XS.MI` | gs = 1.0934 V、gd = 1.0933 V，违例 |
| 正常 PMOS、边界器件 | `XDUT.MCLEAN`、`MEXT` | 通过 |
| 厚栅 `nch_18_mac`，Vds = 1.15 V | `XDUT.MTHICK` | 不检查，列入 `soa_skipped` |
| 删去一个节点的波形 | — | `SOA unverified` |

振荡过冲的峰值不落在激励断点上：默认步长得 1.09335 V（局部步长 4.2 ps），`maxstep=0.05p` 的参考为 1.09320 V，相差 0.15 mV。
8 ns 的瞬态只有 204 个时间点（40 kB）。

**结果**：`soa_scope`（`device`：DUT 内的器件加边界器件；`external`：只有边界器件）、`soa_devices`、`soa_devices_dut`（检查的器件数）、
`soa_pairs`、`soa_violations`、`soa_max_V`、`soa_worst`（器件、端口对、带符号的值、时刻、局部步长）、`soa_points`、
`soa_dt_max_ps`、`soa_skipped`、`soa_table`（每个器件每对端口的 `max_V`、`signed_V`、`t_ns`、`dt_ps`、`pass`）。
`t_ns` 是最大值首次出现的时间点（最大值是一段平台时取平台起点，容差 0.1 mV），`dt_ps` 是该点两侧较大的仿真步长，
`signed_V` 是该点带符号的端电压。
`t_over_ps` 是该对 |V| 超过限值的累计时间（相邻时间点之间按线性插值），**只作诊断**：判定只看最大值，
超限时间短不能作为豁免理由（#27）。`soa_worst` 也带这一项。
证据图 `<stem>.soa.png`：各对的最大 |V| 对限值（超限的标出超限时间）、最坏一对的全程波形、最坏峰值附近保存的时间点。

**无法验证**：没有 SOA 计划、晶体管级 DUT 下找不到薄栅器件、未分类的 MOS 模型、所需节点没有波形、波形不从 t = 0 开始时，
度量返回错误 `SOA unverified: …`，不写 `soa_violations`（相应指标判为不通过），绝不报 0。`dut`、`external` 写错则在仿真前报错。

**行为级视图**没有内部器件：`soa_scope = external`，只检查边界器件（bootstrap 为参考开关 MSWP 的 |VG−VIN|、|VG−BP|、|BP−VIN|，
两个方向）。行为级通过只说明测试台和外部波形没有超限，**不是晶体管级签核证据**；BST-08 的签核要用 `--view adc_bootstrap=xtor`
得到的 `device` 结果。

**没有可检查的器件**：DUT 只有行为级视图、测试台顶层也没有薄栅 MOS 时（`tb_clkgen_timing`），计划为 `external` 且没有器件。
结果明确写出这一点而不是静默报 0：`soa_scope: external`、`soa_devices: 0`、`soa_pairs: 0`、`soa_table: []`、
`soa_note: "nothing to check: XDUT uses behavioral views (no devices) and the testbench has no thin-oxide device at its top
level; not transistor-level evidence"`，`soa_violations` 为 0 个对中的 0 个；时序证据图的规格表下注明范围。仍要求波形从 t = 0
覆盖整段瞬态，否则无法验证。晶体管级视图下找不到薄栅器件仍是错误，不会落入这一情形；测试台顶层有未分类的 MOS 模型（缺省
`external` 时）同样无法验证。CLK-11 的签核要用 `--view adc_clkgen=xtor` 得到的 `device` 结果。

**时钟（CLK-11）**：规则与 bootstrap 相同（|Vgs|、|Vgd|、|Vds| ≤ `limit_V` = 1.0 V，绝对值、两个方向、`corners: all`），
`soa: {dut: [XDUT]}`。覆盖的窗口就是 `tb_clkgen_timing` 的整段瞬态：t = 0 起的启动、占空比 50 % 的 8 个周期、45 % 与 55 %
各 4 个周期，0~161 ns 的每个时间点，包括全部跳变沿；窗口之外（更长的运行、其它占空比或频率）不在 CLK-11 的范围内。
测试台 `maxstep=2p`，保存的点就是仿真器接受的全部时间点。晶体管级视图的时间分辨率按 #19 的做法核对：在有代表性的
最坏工艺角运行 `sim tb_clkgen_timing --view adc_clkgen=xtor --corners <角> --crosscheck`（规格 `crosscheck: {maxstep: 0.5p}`，§2），
结果的 `meta.crosscheck.soa` 给出各对峰值的最大差值与违例数的对比，记入设计 PR。
体端与结的正向偏置不设项目门槛，由设计按器件的合法使用条件保证（#27）。

## 6. 时钟与数字输入的输入电容

驱动端的测试台负载（`adc_clkgen` `loads`、`adc_sarlogic` `load_updn` / `load_clkc`、`adc_comp` `load_per_output`）
由接收端的输入电容限值约束：接收端实例数 × 限值 + 约 20 % 负载的走线 ≤ 驱动端负载（表见
[`handoff.md`](handoff.md)“接口负载与输入电容”，`tests/test_specs_and_checks.py` 按顶层网表检查）。

| 指标 | 引脚 | 限值 | 测试 |
|---|---|---|---|
| DAC-15 / 16 / 17 | `adc_cdac` PHI_S / PHI_SB / CONV | 40 / 40 / 80 fF | `tb_cdac_settle` |
| BST-09 / 10 | `adc_bootstrap` PHI_B / PHI_BB | 16 / 16 fF | `tb_bootstrap_dc` |
| LOG-14 / 15 | `adc_sarlogic` CONV / OUTP、OUTN（取较大者） | 40 / 7 fF | `tb_sarlogic_func` |
| CMP-14 | `adc_comp` CLKC | 16 fF | `tb_comp_kickback` |

**测量**：测试台中 DUT 的这些输入不直接接驱动源，而是经一个电荷计 `tb_qmeter_va`（`QM<tag>`，0 V 通路）；
`V(Q<tag>)` 是流入该引脚的累计电荷（fC），由仿真器用与电路相同的积分方法和步长积出。度量
（`adcflow.measure.common.edge_cin`）对引脚电压的每个上升沿，取 50 % 过零点前 50 ps 到后 200 ps（不超过与相邻下降沿的中点）
之间的电荷变化，除以同一窗口内的电压变化（不足 0.8 VDD 的沿不计），各沿取平均作为指标。这就是驱动端每个沿实际充的电荷：
包括栅电容在整个摆幅上的变化与 Miller 耦合，而在某一电平上的小信号交流值会漏掉这些。

为什么不对保存的电流波形求和：仿真器在断点（边沿的拐角）后用后向欧拉重启、其余步用梯形法，两者混用时，
对电流采样无论用梯形和还是矩形和都不精确（行为级电容上曾分别差 −7 % 与 +50 %）；
`idt` 与电容的 `ddt` 用同一公式，对容性负载得到的电荷是精确的。

控制输入 DH/RL（DAC-13）与比较器输入（CMP-12）仍用 100 MHz 交流电流（模拟输入在偏置点附近小信号工作）。
行为级视图在这些输入上有明确的电容（`cin_*` 参数，约为限值的 75 %），交流与电荷两种测量都得到该值。
