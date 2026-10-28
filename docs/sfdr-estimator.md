# SFDR 估计器（#36）

本项目所有正弦测试的 SFDR（顶层 `tb_top_*`、`tb_bootstrap_track`、`tb_cdac_track`、`tb_ref_replay`，以及系统模型
`model.sine_test_cal` 和 `adcflow budget` 的失配表）都经过同一个辅助函数。#36 发现它报出的 SFDR 可能完全错误。
本文说明 Python 与 MATLAB 两个版本的 ADCToolbox 各错在哪里、我们现在采用的定义、测试结果，以及对已记录结果的影响。

## 1. 结论

* **Python ADCToolbox 0.6.4 的 SFDR 有两个错误。**
  1. 最大杂散的搜索排除了信号频点，但计算杂散功率时又在**未屏蔽**的频谱上，以杂散频点为中心对 ±side_bin 个频点求和。
     杂散紧挨着信号频点时，求和窗口会伸进信号频点。#36 的记录里，一个 −80 dBc 的杂散因此报成 SFDR 7.78 dBc；
     离基波 2 个频点、真实的 −60 dBc 单音也报成 7.78 dBc。
  2. 搜索与总功率都只用到频点 0 … N/2 − 1，看不到 Nyquist 频点。Nyquist 上 −80 dBc 的杂散报成 84.8 dBc，
     SNDR 同样漏掉它（报 84.8 dB，应为 80.0 dB）。
* **MATLAB ADCToolbox `plotspec`（v1.32）的 SFDR 定义是对的**，§4 的全部杂散用例都给出准确值。它的缺陷在别处：
  频谱几乎没有噪声时，自动 `sideBin` 会取 0，于是一个干净正弦的 SFDR 报 6.02 dB、SNDR 报 3.01 dB。
  真实的 ADC 记录都有噪声底，碰不到这种情形。
* **PyPI 上的 ADCToolbox 0.9.1 修好了 0.6.4 的两个错误**（重叠与 Nyquist），但杂散功率仍对 ±side_bin 的窗口求和，
  只是改在已屏蔽的副本上求和：窗口碰到被屏蔽的频点（信号频点或 DC）时，那部分泄漏被丢掉，SFDR 偏乐观
  （本文用例中 0.64 ~ 1.58 dB，窗口只剩一个频点时最多 10·log10(1.5) = 1.76 dB，§3）。所以我们不升级，保留自己的
  `plotspec` 式估计器。上游已报告为 [Arcadia-1/ADCToolbox#100](https://github.com/Arcadia-1/ADCToolbox/issues/100)。
* **我们采用 `plotspec` 的 SFDR 定义**，在项目自己的 Python 度量路径里实现（`tools/adcflow/spectrum.py`），
  因为 CI 和贡献者没有 MATLAB。信号频点和 side_bin 取自 0.6.4 的 `compute_spectrum`，相干 Hann 窗下为 1，
  也就避开了 MATLAB 自动 sideBin 的问题。ENOB、SNDR、SNR、THD 仍由 adctoolbox 0.6.4 计算，数值不变。
  §4 的 13 个用例全部正确，并与 MATLAB 逐一一致（干净正弦除外，原因见上）。
* **对已记录结果的影响**（§6）：7 个结果、11 个 SFDR 值都没有落入 #36 的重叠情形。变化只来自定义的差别：
  0.6.4 把杂散频点两侧频点里的噪声也算进了杂散。变化为 −0.03 ~ +1.30 dB，判定都不变。
  新值与 MATLAB `plotspec` 在相同记录上的结果相差 < 1e-8 dB。

## 2. Python ADCToolbox 0.6.4 错在哪里

文件指已安装的 `adctoolbox/spectrum/`，`compute_spectrum.py` 的 SHA-256 为
`07679ca1ec88de07ec54b1f4e7404e2314d7250b0dcee0c928e7b207e54d6804`，与 #36 一致。

* `compute_spectrum.py:75`：`n_inband = N // 2 // osr`。N = 1024 时搜索和求和都用 `[:512]`，即频点 0 … 511；
  Nyquist（频点 512）不在其中。信号功率（第 132 行）、总功率（第 137 行，从而 SNDR）、杂散搜索（第 166 行）都受影响。
* `compute_spectrum.py:118-128`：相干 Hann 窗下 `side_bin = 1`，信号频点为 `[f − 1, f + 1]`。
* `_harmonics.py:152-198` `_extract_highest_spur`：在副本里把信号频点置零后取最大值（第 184-191 行），这一步是对的；
  但随后在**原始**频谱 `spectrum_power` 上对 `[spur − side_bin, spur + side_bin]` 求和（第 194-196 行）。
  杂散紧挨着信号频点时（`spur = f ± 2`），这个窗口包含信号频点 `f ± 1`。Hann 窗下该频点比基波峰值低 6.02 dB，
  于是“杂散功率”约为信号功率的 1/6，SFDR ≈ 10·log10(1.5 / 0.25) = 7.78 dB。#36 的记录中，频点 508 占这个和的 99.99999833 %。
* 同一窗口也说明，离基波 2 个频点的真实单音不会被忽略，但会被报成 7.78 dBc；离基波 3 个频点以上时窗口不再重叠，结果正确。

## 3. MATLAB ADCToolbox `plotspec` 的定义

本地 `ADCToolbox` 仓库提交 `0e83f80`（“Update MATLAB v1.32 release docs”），`matlab/src/plotspec.m`，在 MATLAB R2025a 中运行。

* 第 270、277 行：带内范围 `1 … floor(N/2/OSR)+1`（1 起计），**包含 Nyquist**；第 383-385 行把偶数 N 的 Nyquist 频点减半，
  因为它在单边谱里只出现一次，减半后它与其它频点一样表示功率。
* 第 513-528 行：`sigs = spec(bin)`，即基波的**单个峰值频点**；把信号频点 `bin ± sideBin` 与 `spec(1:sideBin)`（DC）置零后，
  `spur = max(spec_inband)` 取剩余的**单个最大频点**；`SFDR = 10·log10(sigs/spur)`。两个峰值频点带着相同的窗增益，
  所以对相干记录这就是两个单音的功率比；杂散不按窗口求和，不会碰到信号频点。
* 缺陷（不影响我们）：第 414-464 行的 `sideBin = 'auto'` 用中位数估噪声底时，先剔除了 ≤ 1e-20 的频点。干净正弦只剩
  信号自己的 3 个频点，中位数就是 −6 dB 的旁瓣，于是 `sideBin = 0`，旁瓣被当成杂散（SFDR 6.02 dB、SNDR 3.01 dB）。

另外，本地仓库里较新的 Python 源码（0.8.3，`python/src/adctoolbox/spectrum/_harmonics.py:179-220`）已经改用
`plotspec` 的单频点定义并包含 Nyquist。但它把频点 `0 … side_bin`（比 MATLAB 多一个）置零，频点 1 上的真实单音因此被忽略
（报 86.0 dB，应为 80.0 dB）。

PyPI 上的最新版本 **0.9.1**（项目负责人在隔离的 venv 中用 §4 的同一组用例测试）：

* 0.6.4 的两个错误都已修正：#36 的记录报 80.79 dB（不再是 7.78 dB），Nyquist 用例报 80.00 dB。
* 剩下的问题：`_extract_highest_spur` 在**已屏蔽**的副本上对杂散频点 ±side_bin 求和。窗口碰到被屏蔽的频点（信号频点、DC）时，
  杂散落在那些频点上的泄漏被当成 0，杂散功率偏小，SFDR 偏乐观。紧挨信号频点或 DC 的相干单音少了一个 −6 dB 旁瓣，
  读数高 10·log10(1.5 / 1.25) = 0.79 dB；只剩中心频点时高 1.76 dB。§4 中的 `issue36`、两个边界用例、`near2`、`bin1` 都高 0.79 dB，
  `upper_edge_509` 高 1.58 dB，`bin511` 高 0.64 dB。
* 无注入杂散的 `quantized` 用例仍报 88.42 dB（与 0.6.4 相同；`plotspec` 为 88.08 dB），因为它仍按窗口求和再除以 ENBW，
  在真实记录上与 `plotspec` 的差别和 0.6.4 一样（§6）。

所以升级到 0.9.1 并不能得到 `plotspec` 的定义，我们保留自己的估计器（§5），测试套件仍固定 0.6.4。上游已报告为 [Arcadia-1/ADCToolbox#100](https://github.com/Arcadia-1/ADCToolbox/issues/100)。

## 4. 测试用例与结果

相干记录，N = 1024，单位幅度正弦加一个注入的杂散；真值是基波与杂散的功率比。用例定义在 `tests/sfdr_cases.py`，
MATLAB 用 `tests/matlab/sfdr_plotspec.m` 运行（`plotspec(x, 100e6, 2, 5, 'disp', false)`）；回归测试在 `tests/test_spectrum.py`。
表中为 SFDR（dBc）。

| 用例 | 内容 | 真值 | Python 0.6.4 | MATLAB plotspec | Python 0.8.3（上游源码） | Python 0.9.1（PyPI） | **adcflow** |
|---|---|---:|---:|---:|---:|---:|---:|
| `issue36` | 基波 509，−80 dBc @ 507，紧挨信号频点 508…510 | 80.00 | **7.78** | 80.00 | 80.00 | **80.79** | 80.00 |
| `lower_edge` | 基波 301，−80 dBc @ 299（紧挨下边界） | 80.00 | **7.78** | 80.00 | 80.00 | **80.79** | 80.00 |
| `upper_edge` | 基波 301，−80 dBc @ 303（紧挨上边界） | 80.00 | **7.78** | 80.00 | 80.00 | **80.79** | 80.00 |
| `upper_edge_509` | 基波 509，−80 dBc @ 511（上边界，紧挨 Nyquist） | 80.00 | **7.78** | 80.00 | 80.00 | **81.58** | 80.00 |
| `nonoverlap` | −80 dBc @ 305（相距 4 个频点，窗口不重叠） | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 | 80.00 |
| `near2` | 真实的 −60 dBc 单音，离基波 2 个频点 | 60.00 | **7.78** | 60.00 | 60.00 | **60.79** | 60.00 |
| `near3` | 真实的 −60 dBc 单音，离基波 3 个频点 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 | 60.00 |
| `dc_offset` | DC 偏置 0.01（不是杂散）与 −90 dBc @ 150 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 | 90.00 |
| `bin1` | −80 dBc @ 频点 1 | 80.00 | **80.64** | 80.00 | **86.02** | **80.79** | 80.00 |
| `nyquist` | −80 dBc（功率）余弦 @ Nyquist（频点 512） | 80.00 | **84.77** | 80.00 | 80.00 | 80.00 | 80.00 |
| `bin511` | −80 dBc @ 频点 511 | 80.00 | **80.79** | 80.00 | 80.00 | **80.64** | 80.00 |
| `clean` | 干净正弦（双精度） | ∞ | 274.0 | **6.02** | 276.0 | 274.0 | 276.0 |
| `quantized` | 12 bit 量化、−1 dBFS @ 509（无注入杂散） | — | 88.42 | 88.08 | 88.08 | 88.42 | 88.08 |

粗体：与真值相差超过 0.5 dB（干净正弦：明显错误）。0.9.1 一列由项目负责人在隔离的 venv 中测得，其余各列由本 PR 测得。

* SNDR：0.6.4 与 MATLAB 在全部杂散用例上相差 ≤ 0.2 dB，只有 `nyquist` 例外（0.6.4 报 84.77 dB，MATLAB 与真值都是 80.00 dB）。
  干净正弦上 MATLAB 报 3.01 dB。离基波 1~2 个频点的单音有一部分泄漏进信号频点，被算作信号，所以 `issue36` 等用例的 SNDR
  在两个版本中都是 80.79 dB。这是按频点划分信号的方法本身的局限，不是这个缺陷。
* `quantized`：没有注入杂散，0.6.4 把最大杂散频点 ±1 求和后除以 ENBW，其余版本取单个频点，两种定义相差 0.34 dB。
  真实记录（§6）的变化就属于这一类。

## 5. 我们采用的定义（`tools/adcflow/spectrum.py`）

```
x ← x − mean(x)；w ← 周期 Hann 窗；P[k] ← |rfft(x·w)[k]|²，k = 0 … N/2；P[N/2] ← P[N/2] / 2（偶数 N）
f、side_bin ← compute_spectrum 的基波频点与信号频点（相干 Hann：side_bin = 1）
把 P[f − side_bin … f + side_bin] 与 P[0 … max(side_bin, 1) − 1]（DC）置零，得 Q
SFDR = 10·log10( P[f] / max(Q) )，杂散频点 = argmax(Q)
```

* 与 `plotspec` 相同：单频点比、DC 不算杂散、包含 Nyquist 并减半。与上游 Python 0.8.3 不同：频点 1 仍参与搜索；
  与 0.9.1 不同：杂散取单个频点，不对（会被屏蔽截断的）窗口求和。
* 信号频点与 ENOB / SNDR / THD 用的是同一组，三者描述同一个信号。适用于相干记录（项目所有正弦测试都相干取频）；
  非相干记录上两个峰值频点的扇贝损失不同，单频点比会有偏差。
* `measure.common.spectrum` 与 `model.spectrum_metrics` 都调用它。度量调用它时，结果的 `meta.provenance.spectrum` 记下
  估计器名称与版本（`adcflow.spectrum v1`）、`adctoolbox 0.6.4` 以及各指标的来源。`pyproject.toml` 固定 `adctoolbox==0.6.4`，
  `tests/test_spectrum.py` 检查固定的版本、实际安装的版本与 `spectrum.ADCTOOLBOX` 三者一致，并检查 0.6.4 仍复现 #36
  （7.78 dBc）。升级 adctoolbox 时这些测试会提醒重新审查这里的处理。
* **未改动**：0.6.4 的 SNDR、SNR 也不含 Nyquist 频点（§2）。Nyquist 上若有杂散，SNDR 会偏乐观；
  项目的记录中 Nyquist 频点只有噪声，计入后 SNDR 降低 ≤ 0.025 dB（§6）。是否一并改为包含 Nyquist 由项目负责人决定；
  若改，ENOB 会随之变化，需要另开 PR 并重跑全部正弦结果。

## 6. 对已记录结果的影响

全部 7 个结果用修正后的代码重跑（行为级，TT，`aps`，提交 `7b5fcd8`，工作区干净）。跟踪测试带 `--crosscheck` 重跑，
保留 #28 的收敛交叉检查。除 SFDR 外，每个指标都与之前的结果逐位相同，说明两次仿真的数据一致，SFDR 的变化只来自估计器。
原来的仿真数据已不在本地，因此是重跑，没有用 `remeasure`。每个结果的 `meta.provenance.spectrum` 记录新的估计器。

| 结果 | 指标 | 原值（0.6.4） | 新值 | MATLAB plotspec | 基波 / 信号频点 | 最大杂散频点（0.6.4 / 新） | 0.6.4 窗口重叠信号频点 | 计入 Nyquist 后 SNDR 变化（dB） |
|---|---|---:|---:|---:|---|---|---|---:|
| `tb_top_sine` | `sfdr_dBc`（TOP-03 ≥ 75） | 83.33 | 83.98 | 83.98 | 509 / 508…510 | 239 / 239 | 否 | −0.006 |
| `tb_top_sine` | `sfdr_nom_dBc` | 83.67 | 84.13 | 84.13 | 509 / 508…510 | 503 / 503 | 否 | −0.008 |
| `tb_top_sine_lf` | `sfdr_dBc` | 84.40 | 85.37 | 85.37 | 11 / 10…12 | 503 / 503 | 否 | −0.014 |
| `tb_top_sine_lf` | `sfdr_nom_dBc` | 84.05 | 84.95 | 84.95 | 11 / 10…12 | 503 / 503 | 否 | −0.014 |
| `tb_top_duty` 45 % | `sfdr_dBc` | 84.76 | 85.63 | 85.63 | 509 / 508…510 | 109 / 109 | 否 | −0.011 |
| `tb_top_duty` 45 % | `sfdr_nom_dBc` | 84.17 | 85.28 | 85.28 | 509 / 508…510 | 109 / 109 | 否 | −0.012 |
| `tb_top_duty` 55 % | `sfdr_dBc` | 83.34 | 84.64 | 84.64 | 509 / 508…510 | 339 / 339 | 否 | −0.020 |
| `tb_top_duty` 55 % | `sfdr_nom_dBc` | 83.21 | 84.41 | 84.41 | 509 / 508…510 | 339 / 339 | 否 | −0.025 |
| `tb_ref_replay` | `sfdr_ref_dBc` | 84.56 | 85.08 | 85.08 | 509 / 508…510 | 280 / 280 | 否 | −0.000 |
| `tb_bootstrap_track` | `sfdr_dBc`（BST-05 ≥ 82） | 94.565 | 94.567 | 94.567 | 125 / 124…126 | 119 / 119 | 否 | 0.000 |
| `tb_cdac_track` | `sfdr_dBc`（DAC-09 ≥ 85） | 132.70 | 132.67 | 132.67 | 125 / 124…126 | 119 / 119 | 否 | −0.001 |

* 两个估计器找到的杂散频点都相同，没有一个与信号频点相邻，所以 #36 的 7.78 dBc 错误在已记录的结果中没有出现过。
  差别在杂散功率的取法：0.6.4 对杂散频点及其两侧共 3 个频点求和再除以 ENBW（1.5）。对一个相干单音，这与单频点比相同；
  顶层记录的最大杂散（约 −84 dBc）只比每频点噪声（SNDR 67.5 dB 分到 511 个频点，约 −95 dBc）高约 10 dB，
  两侧频点的噪声被算进杂散，SFDR 因此偏低 0.5~1.3 dB。新定义只取峰值频点。
* 跟踪测试的最大杂散是频点 119 的三次谐波（125 × 3 = 375，折叠到 119），是一个相干单音，远高于两侧，所以两种定义
  几乎一样（bootstrap 差 0.003 dB；CDAC 的频谱在数值底噪上，差 0.04 dB）。
* 系统模型：`adcflow budget` 的失配表（`docs/architecture.md`）中“标称权重 SFDR（最小）”一列，0.25 % 一行由 88.3 变为 89.1 dB，
  0.50 % 一行由 84.0 变为 84.3 dB，其余两行不变；ENOB 各列不变。
* 不在 `results/` 中的记录（例如 #36 中晶体管级混合顶层的私有运行）需由模块负责人用 `remeasure` 按新定义重算。
  #36 报告的 7.78 dBc 属于重叠情形。按 #36 的诊断，选中的杂散频点 507 比基波峰值低 84.546 dB；
  若它仍是最大的单个频点，新定义下该记录的 SFDR 即为 84.55 dBc。

## 7. 复现

```bash
python -m pytest tests/test_spectrum.py                    # 回归：真值、MATLAB 值、0.6.4 的 #36 复现、固定版本、remeasure
python tests/sfdr_cases.py <dir>                           # 写出用例，供 MATLAB 运行
matlab -batch "addpath('tests/matlab'); sfdr_plotspec('<dir>', '<ADCToolbox>/matlab/src')"
python -m adcflow remeasure <test> --run build/runs/<run_id> [--dry-run]
```

`remeasure` 不重新仿真，用现行度量对一次已取回的运行逐个 job 重算，并重写对应的结果：只允许名称含 `sfdr` 的指标变化，
其它任何指标与记录不同即中止（说明不是同一次仿真的数据），不写任何文件。仿真的 `meta`（日期、提交、文件哈希）保留，
`meta.remeasured` 记下重算的日期、提交、所用运行，以及每个变化指标的旧值与新值。保存了原始捕获的结果（例如 #36 中
晶体管级混合顶层的记录）可以用它按新定义重算，并留下明确的新旧出处。
