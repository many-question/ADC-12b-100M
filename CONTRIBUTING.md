# Contributing / 协作指南

**English summary.** This repository is a 12-bit-class, 100 MS/s asynchronous SAR ADC in 28 nm HPC+,
described entirely as plain Spectre netlists plus RNL schematic records (no schematic editor). The
architecture, block specifications, behavioral models, testbenches and the `adcflow` tool are done and pass
at the typical corner; the transistor-level design of the blocks is open to everyone. There is no claiming:
you (or your AI agent) may submit a transistor-level **candidate** for any block except `adc_top`, at any
time, with no limit on participants or candidates per block. A candidate is a directory
`design/xtor/<block>/<name>/` plus its results; a pull request titled `[<block>] candidate <name> …` may only
touch that one candidate. All candidates are scored by the same testbenches and specs and listed on a
per-block leaderboard on the project site; the project lead (GitHub `many-question`) reviews, re-runs the
best ones (`adcflow verify`; the records live in `verification/`, never in a candidate's own results) and selects
one per block (`selected:` in the block spec). Everything below is written in Chinese;
this file is meant to be read by an AI agent that has been pointed at its raw URL, and by people. Process
details and PDK access are not in this repository: contact `many-question` (see section 11).
Spec-change notices for a block are posted as GitHub issues titled `[<block>] …`; before each work session and
before opening or updating a PR, run `gh issue list --state open --search "[<block>] in:title"` and acknowledge
them in the issue and in `candidate.yaml` (section 4).

---

## 1. 项目是什么，去哪里看

12 bit 级、100 MS/s 异步 SAR ADC（28 nm HPC+，0.9 V / 1.8 V）。所有设计数据都是 **Spectre 网表 + RNL 原理图记录**，
不使用 Virtuoso 等图形化原理图工具。架构、规格、行为级模型、测试台和 `adcflow` 流程都已完成，行为级验证在 TT 角全部通过；
项目在晶体管级设计之前停下，晶体管级设计向所有人开放：每个模块可以有任意多个相互竞争的候选设计。

仓库：<https://github.com/many-question/ADC-12b-100M>（本文件原始地址：
<https://raw.githubusercontent.com/many-question/ADC-12b-100M/main/CONTRIBUTING.md>）。
项目网站（进度、验证结果、各模块原理图、候选排行榜）：<https://many-question.github.io/ADC-12b-100M/>。

| 想看什么 | 文件 |
|---|---|
| 架构、指标分配、误差预算 | [docs/architecture.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/architecture.md) |
| 各模块规格（端口、指标、用例、工艺角集合） | [docs/specs.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/specs.md)；机器可读版 `specs/blocks/<block>.yaml` |
| 模块交接包（要点、风险、建议顺序） | [docs/handoff.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/handoff.md) |
| 候选机制的完整设计（命名、评分、选定） | [docs/proposals/open-candidates.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/proposals/open-candidates.md) |
| 工具与流程（环境、`adcflow sim`、签核步骤） | [docs/workflow.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/workflow.md) |
| 验证策略与用例 | [docs/verification.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/verification.md) |
| 设计推导与被排除的方案 | [docs/reference.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/reference.md) |

## 2. 两种角色

* **项目负责人**：`many-question`。维护架构、规格、接口、测试台、顶层与流程；合并 PR；复核排在前面的候选；
  决定每个模块选定哪个候选和签核。
* **贡献者**：任何人（或其 AI agent）。提交候选、更新自己的候选、对规格变更通知作出确认。没有“模块负责人”，也不需要许可或认领。
  同一个 GitHub 账号可以提交多个候选；`candidate.yaml` 里可以给每位作者写一个显示名（例如某个 agent 的名字）以区分，
  显示名是自报的、不被验证，网站一律显示为 `显示名 (@登录名)`。

## 3. 选一个模块

模块有 6 个可提交候选：`adc_comp`（比较器）、`adc_sarlogic`（异步 SAR 逻辑）、`adc_cdac`（电容阵列与驱动）、
`adc_bootstrap`（栅压自举采样开关）、`adc_clkgen`（时钟相位）、`adc_ref`（参考驱动）。`adc_top` 由项目负责人维护。

1. 看项目网站的模块页（每个模块的“候选”排行榜：候选数、每个候选的当前指标），或运行
   `python -m adcflow candidates [--block <block>]`。已有很多候选的模块仍然欢迎新的：不同的拓扑、更低的功耗、更小的面积都有价值。
2. 读 `docs/handoff.md` 里该模块的要点，再读 `specs/blocks/<block>.yaml`（端口、指标、用例）。模块之间的依赖
   （例如 `adc_cdac` 与 `adc_bootstrap`）见 `docs/handoff.md`。
3. 不需要任何人批准，直接开始；先读本模块未关闭的 `[<block>]` issue（第 4 节第 6 步）。

## 4. 提交一个候选

**命名。** 候选名 `<name>` 只能含小写字母、数字和连字符（2~24 个字符），新候选的名字必须是你的 GitHub 登录名（小写），或以 `<登录名>-` 开头加变体：
`alice`、`alice-strongarm`。候选名在同一模块内唯一，合并后不改名。

**目录。** `design/xtor/<block>/<name>/`：

* `<block>.scs`：晶体管级网表，子电路名与端口顺序与规格完全一致，带完整的 RNL 原理图（第 6 节）。**不得含 `include` / `ahdl_include`**：
  模型库由运行器的 deck 提供；
* `candidate.yaml`：

  ```yaml
  name: alice-strongarm                  # 与目录名一致
  description: 一两句话：拓扑、特点、取舍。
  status: wip                            # wip | ready | withdrawn
  acknowledged: []                       # 已确认的规格变更通知（[<block>] issue 号），见第 6 步
  authors:
    - {github: alice, name: "Alice 的 agent 3"}   # name 可选，自由文本，不被验证；github 是身份
  ```

  `ready` 表示你认为它已完整、可以被评比；`withdrawn` 表示撤回（目录保留，排行榜不再显示）。

**步骤。**

1. Fork 本仓库，从最新 `main` 建分支（例如 `cand/<block>-<name>`）。
2. 创建候选目录，写网表和 `candidate.yaml`；用 `python -m adcflow sim … --view <block>=xtor:<name>` 跑验收（第 9 节），
   结果自动写入 `results/<block>/<test>/xtor-<name>/`。
3. 向 `main` 发 PR，**标题 `[<block>] candidate <name> <摘要>`**，例如 `[adc_comp] candidate alice-strongarm first netlist`。
   网站据此把 PR 链接到模块页，CI 通过的开放 PR 会在候选数里计为“未评审”。一个 PR 只含**一个**候选。
4. CI 通过后项目负责人合并（合并只是收录，不代表选定，设计评审在选定时进行）。之后你可以继续发 PR 更新同一个候选。
5. 排在前面的候选，项目负责人用 `python -m adcflow verify` 在同一网表哈希上复跑，复核记录写在项目负责人维护的
   `verification/<block>/<name>/<test>/<job>.json`（不在你的候选路径里）。记录与你的结果相符（各指标判定相同、数值在容差内，
   见 [docs/verification.md](https://github.com/many-question/ADC-12b-100M/blob/main/docs/verification.md) §7）且未过期时，
   排行榜把这个结果标为“已复核”；只有已复核的结果才能用于选定（第 10 节）。复跑前提是结果记录的网表哈希就是网表现在的哈希、结果未过期，
   所以改了网表就要重跑全部用例。不要在结果 JSON 里写 `meta.verified_by` 之类的复核标记，CI 会拒绝。
6. **关注本模块的 issue。** 规格变更、接口调整等通知由项目负责人发在标题以 `[<block>]` 开头的 GitHub issue 里。
   @提及不一定能到达实际干活的人（账号可能是共用的，agent 也不读通知），所以请主动查：每次开始工作前、
   以及每次发 PR 或更新 PR 前，运行

   ```bash
   gh issue list --state open --search "[<block>] in:title"
   ```

   （或在 GitHub / 项目网站的 issue 列表里看），读完每一个未关闭的 `[<block>]` issue。**每个活跃候选（`status` 为 `wip` 或 `ready`）
   都必须确认规格变更通知**：在 issue 里回复，并在下一个 PR 里把 issue 号加进该候选的 `acknowledged`。规格变更若改到了某个结果的电路实际依赖的输入
   （它的测试台、它用到的网表与 Verilog-A、它读到的 arch 取值），该结果显示为过期（stale），要重跑；没有确认通知的候选不会被选定，也不进入顶层混合回归。

## 5. 候选 PR 可以改什么，什么要先开 issue

候选 PR **只能新增或修改**：

* `design/xtor/<block>/<name>/**`（你的候选目录）；
* `results/<block>/*/xtor-<name>/**`（你的结果和图）。

候选 PR **不得改**其它候选（包括它们的结果）、`specs/`、`tb/`、`tools/`、`.github/`、`docs/`、`design/top/`、`design/behav/`、
`verification/`（项目负责人的复核记录）、其它模块，也不要放生成文件。更新一个已有候选，PR 作者的 GitHub 登录名必须在该候选 `candidate.yaml` 的 `authors[].github` 里
（大小写不敏感，以基准分支为准）。**候选 PR 不能改 `authors`**，改作者只有项目负责人在不含候选路径的单独 PR 里能做；
候选不能删除，要撤回就把 `status` 改成 `withdrawn`。新候选必须带 `candidate.yaml` 并列出 PR 作者。
没有例外：任何涉及候选路径的 PR（包括项目负责人账号提交的）都遵守这些规则；不涉及候选路径的 PR 是项目负责人的 PR，不受候选规则约束。
`adc_top` 没有候选。PR 标题不由 CI 检查，但网站按 `[<block>]` 前缀链接 PR，请按第 4 节命名。

本地先自查（先提交再运行，`check all` 里也包含内容规则）：

```bash
python -m adcflow check candidates                                       # 候选目录与网表的内容规则
python -m adcflow check candidates --base origin/main --author <你的登录名>   # 再加上 PR 的路径和作者规则
```

候选目录的限制：只能有 `<block>.scs`、`candidate.yaml` 和 `.md` / `.png` / `.svg` / `.txt` 文件，不能有子目录，总共 ≤ 2 MB，
每个 PNG ≤ 200 kB。网表里只能有子电路内部的实例，器件只能是 PDK 器件（`design/rnl/adc28.rnl` 里的模型，以及 SOA 配置里的 MOS）、
`resistor` / `capacitor` / `inductor` 或自己的子电路，不得含 `include` / `ahdl_include`。结果目录里只放 `.json`（≤ 1 MB，
`block` / `test` / `view` 与路径一致）和 `.png`（≤ 200 kB）；结果目录不能脱离它的候选目录单独存在。

端口、端口顺序、电源域、负载条件、规格指标、`specs/arch.yaml`、测试台、度量函数、工具和 CI 的任何改动都**先开 issue**
（用仓库的 issue 模板，说明哪个模块、要改什么、为什么、对其它模块的影响），由项目负责人决定后单独处理。
`docs/specs.md`、`design/rnl/adc28_blocks.rnl`、`tb/**` 等是生成文件，由 `python -m adcflow gen` 生成，不要手改。

## 6. 设计规则

* **只用网表 + RNL**：晶体管级设计写成 `design/xtor/<block>/<name>/<block>.scs`（Spectre 语法），带**完整**的 RNL 原理图
  （精确的 PLACE / ORIENT / WIRE）和高层语义（差分对、电流镜、`MATCHED`、`GROUP` 等）。不要提交 Virtuoso 原理图、
  版图或其它图形化工具的文件。RNL 语法与画法可参考仓库里已有的网表，以及 [RNL 项目](https://github.com/rich-netlist/rnl)。
* **子电路名和端口顺序与规格完全一致**（`python -m adcflow check ports` 检查）；不得修改端口。
* **只用 PDK 器件**（`design/rnl/adc28.rnl` 里列出的 MOS、`cfmom_2t`、MOS 电容等）。理想元件只在 `docs/handoff.md`
  允许的情形使用，并需事先在 issue 中得到同意。
* **PDK 数据与模型绝不进入 git**：不提交模型文件、从模型中提取的参数表、模型卡片片段。网表里只写实例参数。
* **不要写工艺厂商名**：全仓库只称 “28 nm HPC+”，也不要写 PDK 产品代号。
* **不要写任何机器、服务器、主机名、目录路径、环境脚本路径、许可证信息**，文件里和提交信息里都不行。
  这些只放在被 git 忽略的 `site.local.yaml`。`python -m adcflow check hygiene` 在本地和 CI 中检查。
* 不要提交原始仿真数据（PSF、波形、日志），只提交 `results/` 下的小体积 JSON 结论和图。

## 7. 开始之前：本地环境

```bash
git clone https://github.com/<你的账号>/ADC-12b-100M && cd ADC-12b-100M
pip install -e ".[analysis,dev]"          # adcflow 工具包 + pytest
git config core.hooksPath tools/hooks     # 提交前检查（hygiene / ports / 生成文件）
```

* 安装与 CI 相同版本的 RNL 命令行（`core-v0.5.2`，核对 SHA256），见 `docs/workflow.md`。
* 复制 `site.example.yaml` 为 `site.local.yaml`（已被 git 忽略，**绝不提交**），按注释填写**你自己的**仿真环境。
* 提交信息用 [Conventional Commits](https://www.conventionalcommits.org/)：`feat(comp): StrongARM with preamp`，
  `type` ∈ `feat fix docs refactor test ci chore perf`，`scope` 为模块名。禁止对 `main` 强推。

## 8. 你自己的仿真环境与 PDK

仿真需要 Cadence Spectre 和 28 nm HPC+ 的 PDK 模型，二者都**不在仓库中，也不由本项目提供**：

* 你需要自己的 Spectre 许可和 PDK 访问权限（通常来自你所在的公司、学校或项目的授权）。
* 工具通过 `site.local.yaml` 找到你的环境（说明见 `site.example.yaml` 与 `docs/workflow.md`）；这个文件只在你自己的机器上。
* 没有 PDK 访问，或不确定该用哪个工艺角库、哪些器件时：联系 `many-question`（第 11 节），不要猜测，也不要把任何 PDK 内容贴进 issue 或 PR。

## 9. 验收与提交结果

1. 逐个运行本模块的验收用例（用例名与工艺角集合见 `specs/blocks/<block>.yaml`），视图写 `xtor:<你的候选名>`：

   ```bash
   python -m adcflow sim <test> --view <block>=xtor:<name> --corners all     # 例如 tb_comp_delay
   python -m adcflow report --block <block>                                  # 结果对照规格
   python -m adcflow candidates --block <block>                              # 排行榜：你的候选与其它候选
   ```

   结果写入 `results/<block>/<test>/xtor-<name>/<corner>.json`。规格要求蒙特卡洛的用例（`tb_comp_offset_mc`）只在 `typ` 上运行，
   `sim` 按规格跑全部样本；验收用 `--mode aps`（默认）。
   单独写 `xtor`（不带候选名）表示该模块已选定的候选，不是你的候选。
2. 全部指标在其工艺角集合上通过后，可以自己做顶层混合仿真（其余模块行为级）作参考：
   `python -m adcflow sim tb_top_sine --view <block>=xtor:<name> --corners quick`。正式的顶层混合回归由项目负责人做。
3. 把结果 JSON（`adcflow sim` 自动写入，meta 里记录了电路实际依赖的网表与 Verilog-A 的哈希及读到的 arch 取值）和图连同网表一起提交；
   结果必须对应提交的那一版网表和当前规格，否则 CI 和排行榜判定过期（stale）。
4. 提交前本地运行 CI 的检查，必须全部通过：

   ```bash
   python -m adcflow check all
   python -m pytest -q -m "not slow"
   ```

CI 会检查：hygiene（无站点信息、模型卡片、工艺厂商名、大文件）、端口契约、RNL（0 错误 0 警告，网表必须画完整）、
生成文件同步、候选 PR 的路径和作者规则（结果里不得有 `meta.verified_by`，候选 PR 不得改 `verification/`）、`results/` 与当前规格一致且未过期、单元测试。

## 10. PR 流程、评比与选定

1. 从最新 `main` 分支工作，增量提交；可以先发草稿 PR。发 PR 或更新 PR 前先看本模块的未关闭 `[<block>]` issue（第 4 节第 6 步），
   并在 PR 里勾选 “checked open `[<block>]` issues”。规格变更合并后，基于旧 `main` 的分支要 rebase，并重新运行受影响的用例。
2. 向 `main` 发 PR，标题 `[<block>] candidate <name> <摘要>`，按 PR 模板填写：做了什么、候选状态、证据（`report` / `candidates` 摘要与运行的命令）、检查清单。
3. CI 全绿后项目负责人合并：端口与规格一致、只改了自己的候选、原理图完整、结果未过期。合并即收录到排行榜，不做设计评审。
4. **候选状态**（`candidate.yaml` 的 `status`）：`wip`（进行中）→ `ready`（认为完整，可评比）；`withdrawn`（撤回，不再显示）。
5. **评比。** 排行榜用同一套测试台和规格，列出规格通过数与工艺角覆盖、过期 / 未复核标记、关键裕量、功耗、面积代理和（有则）顶层 ENOB 裕量。
   你自己跑的结果是**自报**的。项目负责人用 `adcflow verify` 在同一网表哈希上复跑，每个结果一条复核记录，放在 `verification/`
   （只有不涉及候选路径的项目负责人 PR 改它）。排行榜只在记录存在、复核的就是网表现在的哈希、记录未过期、并且与你的自报值相符
   （判定相同、指标在容差内）时把结果算作**已复核**；复跑与自报不符的标为**复核不符**，该候选排在全部通过的候选之后。
   结果自己的 meta 不作数。**只有已复核的结果才能用于选定**。
6. **选定。** 资格：规格要求的全部指标在全部工艺角都通过且结果未过期、已复核，通过 SOA 检查，且换进顶层后的混合回归全部通过。
   排序依次为：顶层 ENOB 裕量（容差 0.05 bit）→ 功耗（5 %）→ 面积代理（5 %）→ 其余鲁棒性裕量（5 % 限值）；容差内相同则已选定的保持。
   项目负责人做最终决定，并在块规格里写 `selected: <候选名>`，网站显示其作者。**只有选定的候选进入顶层混合运行。**
7. **挑战。** 任何人可以提交严格更好的候选来替换已选定的候选：满足全部资格，且按上面的排序在容差之外更好；
   替换由项目负责人改 `selected:`，原候选保留在排行榜上。
8. 块状态：`behavioral`（未选定）→ `xtor-review`（已选定，待签核）→ `signoff`（45 角顶层回归通过，由项目负责人设置）。
9. 合并后网站自动更新排行榜、进度、结果和原理图。

## 11. 联系项目负责人

工艺细节、PDK 访问、规格疑问、不确定该不该改某个文件，或任何其它你需要的信息：联系 `many-question`。

* GitHub：[@many-question](https://github.com/many-question)（在 issue 或 PR 里 @ 即可）
* 邮件：jielu1995@outlook.com

## 12. 给 AI agent 的清单

1. 读第 1~6 节。看排行榜（网站或 `python -m adcflow candidates`），和用户确认做哪个模块；不需要认领或许可。
2. 运行 `gh issue list --state open --search "[<block>] in:title"`，读完所有未关闭的 `[<block>]` issue，对规格变更通知在 issue 里回复确认；
   每次开始工作前、发 PR 或更新 PR 前都重复这一步。
3. fork → 分支 → 在 `design/xtor/<block>/<name>/` 写 `<block>.scs`（无 `include`，带完整 RNL）和 `candidate.yaml`
   （`authors: [{github: <登录名>, name: <你的 agent 名>}]`，`acknowledged` 填已确认的 issue 号）。候选名是用户的 GitHub 登录名或以 `<登录名>-` 开头。
4. 用 `--view <block>=xtor:<name>` 跑本模块全部用例并提交 `results/<block>/*/xtor-<name>/`。
   端口、规格、测试台、其它模块、其它候选的改动一律先开 issue，不放进候选 PR。
5. 用户提供的仿真环境只写进被忽略的 `site.local.yaml`；在任何文件、提交信息、PR 和 issue 里都不要出现工艺厂商名、
   PDK 内容、机器、服务器或路径信息。
6. 规格变更后 rebase 到最新 `main`，运行 `python -m adcflow rehash --block <block> --view xtor-<name>`（不重仿真；依赖未变的结果改记、保持有效），
   再重新运行仍判为过期的用例。
7. `adcflow check all` 与 `pytest` 通过、结果已提交，再发标题为 `[<block>] candidate <name> …` 的 PR，一个 PR 只含一个候选。
