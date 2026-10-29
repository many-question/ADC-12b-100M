# 提案：用公开竞争的候选设计取代模块认领

> 状态：**用户已批准方向和第 8 节的各点，尚未实现。** 本文定规则和实施顺序；按第 7 节分 PR 实现。

**English summary.** Today a contributor *claims* one block (`owner:` in the block spec) and works alone.
This proposal drops claiming. Anyone may submit a transistor-level **candidate** for any block except
`adc_top` at any time, with no limit on participants or candidates. A candidate lives in
`design/xtor/<block>/<candidate>/`, is scored by the same testbenches and specs as every other one, and appears
on a per-block **leaderboard** on the website (number of candidates, current metrics). The project lead selects
one eligible candidate per block (`selected: <candidate>` replaces `owner:`) by a published tie-break order;
only the selected candidate is used in the mixed top-level runs, and it can be challenged by a strictly better
one. Spec-change notices stay as `[<block>]` issues. Contributors may declare a display name next to their GitHub login (shown as `name (@login)`, never verified). Sections 1–7 below define layout, PR rules and CI,
scoring, selection, notices, migration and the implementation plan.

## 0. 动机与已定的原则

认领把一个模块锁给一个人：认领后不干活的人占着位置，别人想试另一种拓扑要先争取许可，而且我们不知道哪种拓扑最好。
改为公开竞争：

* **没有认领。** 任何人随时可以为任何模块（`adc_top` 除外，由项目负责人维护）提交晶体管级候选。
* **人数和候选数不设上限。** 同一个人可以提交多个候选。
* 网站对所有人显示每个模块的候选数和每个候选的当前指标（模块排行榜）。
* 项目负责人（`many-question`）仍然负责规格、接口、测试台、评审、合并和最终选择。

## 1. 目录、命名与迁移

**候选名** `<name>`：`[a-z0-9-]{2,24}`，新候选必须以提交者的 GitHub 登录名（小写）开头，可再加 `-<变体>`：
`alice`、`alice-strongarm`。这样没人能占用别人名字的前缀；项目负责人不受此限。候选名在同一模块内唯一，合并后不改名。

| 内容 | 路径 |
|---|---|
| 候选目录 | `design/xtor/<block>/<candidate>/`，网表为 `<block>.scs`（子电路名、端口顺序与规格一致），可有 `candidate.yaml`、说明、图 |
| `candidate.yaml` | `authors: [{github: <登录名>, name: <显示名，可选>}, …]`、`description:`（一两句）、`status: wip \| ready \| withdrawn`、可选 `acknowledged: [<issue 号>]`（第 5 节） |
| 运行器视图键 | `--view adc_cdac=xtor:<candidate>`；单独的 `xtor` 表示该模块 `selected` 的候选（未选定则报错）。规格里不再列 `views.xtor` |
| 结果路径 | `results/<block>/<test>/xtor-<candidate>/<corner>.json`（`:` 在路径里换成 `-`，与现有 `behav`、`xtor` 并列） |
| 顶层混合运行 | `results/adc_top/<test>/xtor-<blk>@<candidate>[+<blk>@<candidate>…]`（`blk` 为去掉 `adc_` 的简称，如 `xtor-comp@alice`） |

目录里**只有 PDK 器件和模块内部子电路**：候选网表不得 `include` / `ahdl_include` 任何文件（CI 检查）。运行时的模型库由运行器的 deck 提供。
这既是端口契约的一部分，也防止别人的网表在项目负责人的环境里读取不该读的文件。

**现有内容怎么迁**（项目负责人做，各一个小 PR，见第 7 节）：

| 现状 | 迁成 |
|---|---|
| #25 bootstrap、#26 clkgen、#31 ref（草稿 PR，`design/xtor/<block>/<block>.scs`） | 改标题 `[<block>] candidate many-question …`（候选名与 `candidate.yaml` 的作者署名按提交者确认的为准）；目录移到 `design/xtor/<block>/many-question/`；结果目录 `xtor` → `xtor-many-question`；加 `candidate.yaml`。`adcflow migrate-candidate` 只改路径和 `meta.files` 的键，文件内容哈希不变，所以结果不会变过期 |
| `adc_comp` 的标签 `adc-comp-mc12` 等（历史版本，网表不在 `main`） | 标签保留作历史；`mc12`（`docs/noise-budget.md` 引用的版本）导入为候选 `many-question-mc12`；其它标签按需再导入，不自动迁 |
| `adc_cdac`、`adc_sarlogic`（尚无晶体管级工作） | 无需迁移。`adc_sarlogic` 的 `owner: Arcadia-1` 失去特殊地位，他/她可随时提交候选 `arcadia-1` |

## 2. PR 规则与 CI 检查

候选 PR 标题 `[<block>] candidate <name> <摘要>`（后续更新同一候选也用以 `[<block>]` 开头的标题），网站据此把它链到模块页。

**一个候选 PR 只能新增或修改：**

* `design/xtor/<block>/<name>/**`（自己的候选目录）；
* `results/<block>/*/xtor-<name>/**`（自己的结果和图）。

**不得改动**：其它候选、`specs/`、`tb/`、`tools/`、`.github/`、`docs/`、顶层、行为级模型、其它模块的任何文件。
不碰任何生成的跟踪文件：站点从目录树现算排行榜，**不存跟踪的候选索引**，所以无上限的候选 PR 不会互相冲突。
规格或接口要求仍然先开 `[<block>]` issue，由项目负责人决定（沿用 CONTRIBUTING §5）。

**谁可以更新一个候选**：`candidate.yaml` 的 `authors`。CI 检查 `check candidates --base --author`（取代 `check owners`）：

1. 变更路径必须落在上面的允许前缀内，且只涉及**一个**候选 `<name>`；
2. 新候选：`<name>` 在基准分支上不存在，且以 PR 作者的登录名开头；必须带合法的 `candidate.yaml`，PR 作者的登录名在 `authors[].github` 里（首个 PR 即由此设定）；
3. 已有候选：PR 作者的登录名必须在**基准分支上**该候选的 `authors[].github` 里（改 `authors` 本身也要这个条件，所以共同作者由现有作者加；改别人候选的 `authors` 只有项目负责人能做）；
4. 目录大小 ≤ 2 MB，PNG ≤ 200 kB（与结果的限制一致），不含二进制/大文件，不含 `include`；
5. `adcflow check hygiene`（工艺名、站点信息、模型卡）、端口契约、`rnl` 对该候选的网表照常；
6. 项目负责人的 PR 不受 1~4 限制（他要迁移、删候选、改规格）。

**显示名。** `authors[].name` 是可选的自由文本（例如某个 agent 的名字），用来区分同一个人的不同 agent。同一个 GitHub 账号可以在不同显示名下拥有多个候选；
候选名仍是模块内的唯一键。CI 只验证 `github` 部分；显示名是自报的、不被验证，但必须通过工艺名称检查和 hygiene。
排行榜和候选页一律显示 `显示名 (@登录名)`（没有显示名时只显示 `@登录名`），所以显示名无法冒充别的账号。
`withdrawn` 的候选不再显示在排行榜上（目录保留，作者或项目负责人可恢复）。

## 3. 打分与排行榜

**同一套测试台、同一套规格。** 每个候选在每个测试、每个规格要求的工艺角上跑 `adcflow sim … --view <block>=xtor:<name>`，结果提交到自己的结果目录。

每个候选的指标（`adcflow candidates` 从目录树和结果 JSON 计算，站点调用同一函数）：

| 列 | 含义 |
|---|---|
| 规格通过数 / 总数 | 以规格要求的工艺角集合判定（规格里的 `corners`），任一角不过即该项不过 |
| 工艺角覆盖 | 已有结果的（规格, 角）数 / 要求的数 |
| 作者 | `显示名 (@登录名)`，来自 `candidate.yaml` |
| 状态标记 | `stale`（输入哈希已变）、`unverified`（项目负责人尚未在同一网表哈希上复跑，见下）、`SOA 违例`、仿真/度量错误 |
| 关键裕量 | 各规格 (限值−值)/限值 的最小值及对应规格号 |
| 功耗 | 各测试台报告的供电电流 × 电源电压（没有该度量的模块由项目负责人经 issue 补充；缺失显示 “—”） |
| 面积代理 | 从网表算：器件数、Σ(W·L) 和电容单元数/总电容（脚本统一，不依赖版图） |
| 顶层 ENOB 裕量 | 项目负责人把该候选换进顶层混合运行后的结果（没有则 “—”） |

**页面**：模块页新增“候选”标签（按第 4 节顺序排序的排行榜，每行链到该候选的指标表、网表查看器和 PR）；首页的模块表新增“候选：N”列
（N = 未撤回的候选数，含已合并和有 CI 通过的开放 PR）。已选定的候选加标记。

**数据来源与安全**（沿用草稿预览的规则，`sitegen/preview.py`）：

* 已合并的候选用主分支数据；开放 PR 的候选只显示 CI “contracts, drawings, results” 通过的提交，标“未评审”，不进主分支的状态和统计；
* 用 `git fetch origin +refs/pull/<N>/head` 取提交，`git cat-file blob` 当数据读，**从不运行 PR 的任何代码**；
* 展示前过工艺名称检查和 hygiene 规则，不过就不显示内容、只留元数据；判定用主分支的规格重算（不信任 PR 里的规格副本，PR 也不能改规格）。

**可信度。** 仿真需要各人自己的 PDK 和 Spectre，CI 无法复现，所以提交的结果是**自报**的。排行榜把“自报”和“已复核”分开：
项目负责人在同一网表哈希上复跑后，结果加 `meta.verified_by`；只有已复核的结果才能用于选定（第 4 节），未复核的显示为灰色。
（实现时改为：复核记录放在候选路径之外的 `verification/`，由 `adcflow verify` 写入，候选结果里的 `meta.verified_by` 被 CI 拒绝、也不被采信，
见 [`docs/verification.md`](../verification.md) §7；放在结果里，作者在自己的 PR 里就能伪造。）
复跑只在候选排到前面时做，不是每个候选都复跑；在项目负责人的环境里运行前先审查网表（无 `include`、器件均为 PDK 器件）。

## 4. 选定

**资格**：规格要求的**全部指标在全部工艺角**都通过且结果未过期、已复核；SOA 检查通过；并且把它换进顶层后的**混合回归**（其余模块行为级，
`tb_top_sine`、`tb_top_duty` 等，工艺角集合与顶层规格一致）全部通过。

**排序**（公开，依次比较，前一项在容差内相同才看下一项）：

1. 顶层 ENOB 裕量（容差 0.05 bit）；
2. 功耗（容差 5 %）；
3. 面积代理（容差 5 %）；
4. 其余鲁棒性裕量（各规格最小裕量，容差 5 % 限值）。

容差数字是提议值，批准时可改；在容差内相同时，已选定的候选保持。**项目负责人做最终决定**，可以因为排序表达不了的原因（例如可制造性问题）不选排名第一的候选，但要在 issue 里写明理由。

**规格字段**：块规格里的 `owner:` 换成 `selected: <candidate>`（未选定为 `none`），显示的作者来自该候选的 `candidate.yaml`；`adc_top` 保留 `owner: many-question`。
块 `status` 改为 `behavioral`（未选定）→ `xtor-review`（已选定，待签核）→ `signoff`（45 角顶层回归通过）；`xtor-wip` 取消，改为候选自己的 `status`。
**只有选定的候选进入顶层混合运行**（`--view <block>=xtor`）。

**挑战**：任何人可以提交严格更好的候选来替换已选定的候选——满足全部资格，且按上述排序在容差之外更好（逐项比较，第一个不在容差内的项更好者胜）。
替换由项目负责人在 PR 里改 `selected:`，原候选保留在排行榜上。

## 5. 规格变更通知

沿用 `[<block>]` issue（CONTRIBUTING §4 第 6 条）。规格一变，所有候选的结果因输入哈希变化自动显示为 **stale**，必须重跑。新增：

* **每个活跃候选（`status` 为 `wip` 或 `ready`）必须确认**：作者在 issue 里回复，并在下一次 PR 里把 issue 号加进 `candidate.yaml` 的 `acknowledged`；
* 站点在候选行显示“未确认通知 #N”；未确认的候选在通知发出后不得被选定，也不进入顶层混合回归，直到确认并重跑；
* 通知由项目负责人发，不再逐个 @ 人（无法可靠送达），而靠排行榜上的提示和上面的检查清单。

## 6. 现有 owner 与认领怎么办

* 六个模块的 `owner:` 全部删除，换成 `selected: none`（`adc_top` 保持 `owner: many-question`）。目前没有开放的认领 PR；此后不再接受 `[<block>] claim`。
* #25、#26、#31 和 `adc_comp` 的标签是从 `many-question` 账号提交的，但**不一定是项目负责人自己的工作**，也可能是其他贡献者的 agent。
  迁移时每个候选的 `candidate.yaml` 记录真实的作者 / agent 名，由提交者在迁移 PR 里确认（确认前暂用 `{github: many-question}`）；
  它们与所有候选同等对待，项目负责人账号提交的候选也可以被挑战。
* `check owners` 退役：新的 `check candidates` 的路径白名单已经覆盖“PR 不能改 `specs/`”，所以任何人（含贡献者）的 PR 都无法再改 `selected`/`owner`，只有项目负责人能改。
* `CONTRIBUTING.md` 要重写的部分：§2（角色：贡献者 / 项目负责人，去掉“模块负责人”）、§3（选模块 → 看排行榜、选模块）、§4（认领 → 提交候选：命名、`candidate.yaml`、PR）、
  §5（可改范围表改为“自己的候选目录和结果”）、§9（`--view <block>=xtor:<name>`、结果路径）、§10（流程与状态）、§12（agent 清单）和英文摘要；
  同步改 PR 模板、issue 模板、`docs/handoff.md` 的角色段、`docs/workflow.md` §5、站点上的“认领方式”入口。

## 7. 实施计划

| # | PR | 内容 | 规模 |
|---|---|---|---|
| 1 | `[flow] candidates in the runner, specs and results` | `xtor:<name>` 视图键与路径解析；`candidate.yaml` 的读取与校验；端口契约和 rnl 检查遍历所有候选；结果路径 `xtor-<name>`、顶层签名；`adcflow candidates`（打分）、`adcflow migrate-candidate`；规格 `selected:` 字段；测试 | 中（约 500 行 + 测试） |
| 2 | `[ci] check candidates` | 路径白名单、作者与命名规则、大小与 `include` 检查；退役 `check owners`；`ci.yml` | 小（约 200 行 + 测试） |
| 3 | `[docs] contributing for open candidates` | 重写 CONTRIBUTING 与模板、handoff、workflow（第 6 节清单） | 小~中（文档） |
| 4 | `[arch]` 切换 | 六个模块 `owner` → `selected: none`；迁移 #25/#26/#31 与 `adc_comp` 的 `mc12`；PR 2 与 3 同时生效 | 小（项目负责人，逐个草稿 PR 的移动） |
| 5 | `[site] candidate leaderboard` | 数据层（调用 `adcflow candidates`）、模块页“候选”标签、首页“候选：N”列、开放 PR 候选的预览（沿用 `preview.py` 的安全规则）、通知确认提示 | 大（约 600 行 + 夹具测试） |

顺序：1 → 2 与 3 一起合并（切换点）→ 4 → 5。5 只依赖 1 的数据格式，1 合并后可与 2~4 并行。
切换前现有的草稿 PR 先留着不动；切换当天按第 1 节迁移。

## 8. 已决定（用户）

1. 排序和容差：顶层 ENOB 裕量 0.05 bit → 功耗 5 % → 面积代理 5 % → 其余鲁棒性裕量 5 % 限值；
2. “候选：N”包含 CI 通过的开放 PR，标“未评审”；
3. 只有项目负责人**已复核**的结果才能用于选定，所以要为排在前面的候选复跑；
4. 候选合并门槛：CI 全绿 + 路径白名单；设计评审放在选定时；
5. 功耗和面积代理按第 3 节定义；缺少功耗度量的模块由项目负责人补（`adc_cdac` 最先）；
6. 参与者可以在 `candidate.yaml` 声明显示名，以区分同一个人的不同 agent（第 2 节）。
