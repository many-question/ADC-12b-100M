# 工作环境与常用命令

## 1. 本地环境（一次性）

```bash
pip install -e ".[analysis,dev]"          # adcflow 工具包 + adctoolbox（上游提交 cd72061，需要 git）+ pytest
git config core.hooksPath tools/hooks     # 提交前检查（hygiene / ports / 生成文件）
```

* **RNL 命令行**：安装与 CI 相同的版本 `core-v0.5.2`（见 rnl 项目的 Release 页，下载后核对 SHA256），
  放到 `PATH` 中，`rnl --version` 应显示 0.5.2。
* **站点配置**：复制 `site.example.yaml` 为 `site.local.yaml`（已被 git 忽略）或 `~/.adcflow/site.yaml`，
  填写仿真服务器的 ssh 别名、服务器本地盘上的临时目录、Spectre 环境脚本、PDK 模型目录与文件名。
  这些信息**绝不提交**。ssh 需要免密（`ssh -o BatchMode=yes <alias> true` 能通过）。
* MATLAB 版 ADCToolbox 可选，用于 `analysis/` 中的交互分析；CI 与验收只用 Python 版。

## 2. 生成文件

以下文件由 `python -m adcflow gen` 从 `specs/` 生成，不要手改（CI 会检查是否同步）：

| 文件 | 来源 |
|---|---|
| `design/rnl/adc28_blocks.rnl`、`design/rnl/adc28_va.rnl` | 模块端口、Verilog-A 模块端口 → DEVICE 与符号 |
| `design/behav/veriloga/adc_arch*.vams` | `specs/arch.yaml` 的权重、单位电容等常数 |
| `design/behav/adc_cdac.scs` | 行为级 CDAC（26 个半电容 + 开关矩阵，含原理图） |
| `design/top/adc_top.scs` | 顶层结构网表与原理图（`tools/adcflow/gen_top.py` 中的连接表） |
| `tb/**/*.scs` | 验收测试台（`tools/adcflow/gen_tb.py`） |
| `docs/specs.md` | 模块规格表 |

## 3. 运行验收用例

```bash
python -m adcflow sim <test> [--corners typ|quick|all|<name,...>] [--view <block>=xtor ...] \
       [--param name=value ...] [--mode aps] [--jobs N] [--keep] [--no-record]
python -m adcflow report [--block adc_comp]     # 结果对照规格
python -m adcflow candidates [--block adc_comp] [--json]   # 晶体管级候选的排行榜（docs/proposals/open-candidates.md §3）
python -m adcflow verify <test> --block <block> --candidate <name> [--corners …] [--dry-run]   # 项目负责人在同一网表哈希上复跑候选的结果，写复核记录 verification/…（docs/verification.md §7）
python -m adcflow migrate-candidate <block> <name> --author <login>[=<显示名>] --description "…"   # 旧的单一 xtor 视图迁成候选（项目负责人）
python -m adcflow remeasure <test> --run build/runs/<run_id> [--dry-run]   # 不重仿真，用现行度量重算并重记该次运行的结果（只允许 SFDR 变化，#36）
python -m adcflow remeasure <test> --run build/runs/<run_id> --redraw     # 只重画证据图：任何指标变化即中止，结果中写 meta.redrawn（#47）
python -m adcflow rehash [--block <block>] [--test <test>] [--view xtor-<name>] [--dry-run] [-v]   # 不重仿真，把结果的记录换成其电路实际依赖的文件与 arch 取值（见下）
python -m adcflow corners all                   # 45 个工艺角名称
python -m adcflow clean-remote --older-than-h 12   # 清理服务器上本项目的遗留目录
```

每次 `sim`：

1. 在 `build/runs/<run_id>/` 生成仿真 deck（全局参数、工艺角模型段、各模块视图、Verilog-A、测试台）；
2. 打包上传到服务器本地盘的 `<remote_root>/<run_id>/`，并行运行 Spectre（共享 Verilog-A 编译缓存）；
3. 只取回小文件（监视器输出、日志、需要的波形，单文件默认 ≤ 50 MB），**随后删除服务器目录**；
4. 调用度量函数，把指标与判定写入 `results/<block>/<test>/<view>/<corner>.json`，
   其中 `meta.files` 记录电路实际依赖的文件（测试台、它可达的网表与 Verilog-A 及其 include、做 SOA 检查时的 `specs/soa.yaml`）的哈希，
   `meta.arch` 记录建作业与度量时读到的 `specs/arch.yaml` 键及其取值的哈希，`meta.views` 记录视图
   （何时过期见 [`verification.md`](verification.md) §2「结果过期」），`meta.git` 记录当时的提交，
   `meta.git_clean` 记录仿真时工作区是否干净（`git status --porcelain` 在 `results/` 之外没有任何改动、暂存或未跟踪的文件；
   被忽略的文件如 `site.local.yaml` 不算；`results/` 与 `verification/` 不算，因为成套重跑、复核时它们本身在变），不干净时
   `meta.git_dirty_paths` 列出这些路径（最多 20 个）。要提交的结果应先提交代码再仿真，使其为 `true`；度量函数同时用已读入的数据画证据图，
   写在 JSON 旁（`<corner>.<tag>.png`），清单记在 JSON 的 `figures`（见 [`verification.md`](verification.md) §4）。
   重跑同一结果会先删除它旧的图。

**旧结果迁到依赖集（`rehash`）。** 这次改动之前记录的结果列出了整个 deck 与整个 `arch.yaml`，任何一个模块或架构文件的改动
都使它们过期。`python -m adcflow rehash` 不重仿真地逐个检查，只有同时满足下列三条的结果才改记为其依赖集，其余保持过期、需要重跑：

1. 电路现在可达的每个文件，内容与仿真时相同：比对记录的哈希；旧记录没有计哈希的文件（`adc_arch*.vams` 这类 `` `include ``）
   取 `meta.git` 那次提交中的文件，只在 `meta.git_clean` 为 `true` 且本地有该提交时可行；
2. 内容变了（或只在新旧两个 deck 之一中）的文件，无论仿真时还是现在，都不定义电路现在可达的任何名称
   （仿真时的内容取自该提交，并须与记录的哈希一致）；
3. 它读到的 arch 取值不变：重建该作业（须得到记录的参数）时 `prepare` 读到的键，以及度量函数可能读 `arch.yaml` 时
   （静态检查 `deps.may_read_arch`）的整个文件，与仿真所用的 `arch.yaml`（按记录的哈希认定，取自当前文件或该提交）比较。

改记的结果保留仿真的 `meta.git`、`meta.date` 等，换上缩减后的 `meta.files`、`meta.arch`、`meta.views`，并在 `meta.rehashed`
写入改记的日期、提交与原来记录的文件数。已在依赖集上且未过期的结果不动。候选作者在自己的候选 PR 里运行
`python -m adcflow rehash --block <block> --view xtor-<name>`（只改动本候选的结果文件；候选名可能在别的模块也有，所以要带 `--block`），提交改记后的结果。

视图选择：默认全部行为级；`--view adc_comp=xtor` 使用 `design/xtor/adc_comp/adc_comp.scs`，
此时自动包含所选工艺角的 PDK 模型段并打开器件噪声（`devnoise=1`）。

`--jobs` 的默认值是站点配置的 `sim.jobs`（没有时为 6）。

仿真模式默认 `aps`。`cx` 忽略 `errpreset` 与 `relref`（SPECTRE-592），也不用于正式结果（[`verification.md`](verification.md) §2）。`ax` / `mx` 在本项目的 Verilog-A 行为级模型上精度不足
（行为级 ADC 的 ENOB 从 11.25 掉到 10.63），只能用于晶体管级的快速探索，验收必须用 `aps`。

## 4. 新增或修改测试台

* 测试台在 `tools/adcflow/gen_tb.py` 中描述（元件、网络、参数、分析），`gen` 生成网表和原理图。
* 第一行 `parameters` 中的参数可由规格 `params:` 或 `--param` 覆盖；`vdd vdd18 tempc noise_en devnoise
  beh_speed vref_in cdac_behav` 由 deck 提供，测试台中不要声明（`cdac_behav` = 1 表示 `adc_cdac` 用行为级视图）。
* 监视器写小文本文件（`tb/common/veriloga/`）；只在度量需要时保存波形（`save` 列出信号）。
* 要求逐管 SOA（每个薄栅器件 |Vgs|、|Vgd|、|Vds| ≤ 1.0 V）的用例在规格中加 `soa:`：流程在 deck 中保存 DUT 内各器件的端口节点，度量函数调用 `soa.measure` / `soa.figure`，见 [`verification.md`](verification.md) §5。
* 度量函数放在 `tools/adcflow/measure/<block>.py`，签名 `fn(job_dir, ctx) -> dict`，键名即规格中的 `metric`。
  `ctx["figs"]` 是图的接收器（`tools/adcflow/figures.py` 的 `FigureSink`）：新测试的度量函数用
  `sink_of(ctx)` 取得它，`fg.new(...)` 建图、`fg.save(fig, tag, caption)` 保存；规格线用
  `limits(ctx, metric)`（来自 `specs/blocks/*.yaml`），每个测试至少要有一张图，否则 `check results --strict` 报错。
* 规格中的 `prepare: module:fn` 在建 job 时改写参数（例如把 `fin_target` 换成相干频点）；返回的
  `_files: {文件名: 文本}` 会写进 job 目录，测试台用相对路径读取（`tb_ref_replay` 的 `iload.pwl` / `trig.pwl`）。

## 5. 晶体管级设计的签核

1. `design/xtor/<block>/<name>/<block>.scs`（候选目录，另有 `candidate.yaml`）：子电路名、端口与规格一致，完整 RNL 原理图与语义，不含 `include`。
2. 本模块全部用例：`--view <block>=xtor:<name> --corners all`；规格要求 `mc` 的蒙特卡洛用例（`tb_comp_offset_mc`）只在其工艺角
   （`typ`）上跑，`sim` 按规格自动跑全部样本（`docs/verification.md` §2）；结果在 `results/<block>/<test>/xtor-<name>/`。
3. 提交网表与 `results/`，PR 标题 `[<block>] candidate <name> …`，一个 PR 一个候选；贡献者发 PR，项目负责人（`many-question`）合并、
   对排在前面的候选用 `adcflow verify` 在同一网表哈希上复跑（记录在 `verification/`，相符且未过期即“已复核”，[`verification.md`](verification.md) §7），换进顶层做混合回归，选定一个候选（`selected:`），45 角顶层回归通过后把块状态改为 `signoff`。
4. 规格变更通知发在 `[<block>]` issue；每个活跃候选确认并重跑（`candidate.yaml` 的 `acknowledged`）。

## 6. 服务器使用规则

* 只在服务器本地盘的临时目录下仿真，不在 `/home` 下运行；
* 服务器上的数据随时可能被清除：有用的数据仿真结束就取回，大文件只取需要的部分；
* 每次运行结束自动删除服务器目录；异常退出后用 `clean-remote` 清理。
