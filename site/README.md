# 项目网站生成器

把仓库内容生成为一个静态网站：概览、进展、验证结果、各模块页面（含可交互原理图）和渲染后的文档。
只读仓库里的文件，**不需要仿真服务器，也不需要 PDK**。每个 PR 都会构建一次（`.github/workflows/site.yml`），
合并到 `main` 后部署到 GitHub Pages。

## 本地构建

```bash
pip install -e . -r site/requirements.txt     # adcflow + markdown-it-py（一次性）
python site/build.py                          # 生成 build/site/
python site/build.py --serve                  # 构建并在 http://127.0.0.1:8000/ 预览
```

构建出错（规格/结果读取失败、文档里有死链、页面内链接或锚点失效）时返回非零退出码；`--no-strict` 只报告不失败。

## 数据来源

| 页面 | 来源（用 `adcflow` 的读取函数，不重复实现逻辑） |
|---|---|
| 概览 | `specs/arch.yaml`（`adcflow.arch.Arch` 的派生量）、`results/` 中顶层 ENOB、所有规格的判定统计 |
| 进展 | `specs/blocks/*.yaml`（状态、负责人、版本）、网表文件是否存在、`git` 标签与最近修改日期 |
| 验证 | `adcflow.checks.load_results` / `judge`：用当前限值重新判定每个结果文件，哈希不一致标“过期” |
| 模块 | 端口、指标、用例来自 `specs/blocks/<block>.yaml`；原理图来自该模块的视图与测试台网表 |
| 文档 | `docs/*.md`、`CONTRIBUTING.md`（仓库内链接改写成站内页面或 GitHub 链接） |
| 负责人 | 每个 `specs/blocks/<block>.yaml` 的 `owner:`：GitHub 用户名显示为 `@用户名`（链到其主页），`TBD` 显示“待认领”并链到协作流程；旁边链到标题以 `[<block>]` 开头的进行中 PR（GitHub 搜索） |
| 协作入口 | 顶栏“参与协作”和首页的协作区：链到渲染后的 `CONTRIBUTING.md`，并给出可复制的原始地址（`raw.githubusercontent.com/.../main/CONTRIBUTING.md`），交给自己的 agent 即可；文件不存在时入口自动隐藏 |

模块状态变化（例如 `design/xtor/<block>/` 出现网表、`status` 变为 `xtor-wip`）后，重新构建即可，页面不需要手改。

## 原理图

原理图由托管的 RNL 网页查看器（<https://rich-netlist.github.io/rnl/viewer/>）绘制：页面里嵌入 `viewer/?embed=1&url=<网表地址>`，
切换网表用 `postMessage`；“完整查看器”按钮用清单打开整个设计（见下）。查看器是从浏览器里去取网表的，所以网表必须能被
浏览器通过 HTTPS 访问，并允许跨域（CORS）；`@USE-PACKAGE(path="../rnl/adc28.rnl")` 这类相对路径要求保持 `design/` 的目录结构。

| `--netlist-base` | 网表位置 | 用途 |
|---|---|---|
| `pages`（默认） | 发布在站点旁边的 `repo/design/…`、`repo/tb/…`（同一目录结构） | 线上站点：和页面同一次构建、同一个提交，GitHub Pages 自带 `Access-Control-Allow-Origin: *` |
| `raw` | `https://raw.githubusercontent.com/<repo>/<提交>/…`（固定到提交，需先推送） | PR 预览与本地检查：不依赖本机服务器 |
| 任意 URL 前缀 | 该前缀下的仓库目录结构 | 特殊托管 |

本地用默认的 `pages` 模式时，网表由本机 `127.0.0.1` 提供，而查看器页面在 `https://` 上：新版 Chrome 会拦截公网页面访问本机地址
（“本地网络访问”权限），此时在地址栏允许该权限，或者改用 `--netlist-base raw`。`--serve` 已经给出 CORS 头。

### 完整查看器与清单（manifest）

“完整查看器”链接（顶栏、概览、各模块的查看器）不是直接打开单个网表，而是打开 `viewer/?manifest=<清单地址>`。每个网表一个清单，
写在站点的 `manifests/<网表>.json`（格式 1，见 RNL 仓库 `apps/web/README.md` 的 External manifests）：列出 `design/`、`tb/` 下全部
网表和 RNL 文件（`design/rnl/adc28.rnl` 和生成的模块符号、Verilog-A 符号文件，`pool` 按这个顺序），每个文件带 SHA-256 和大小，
`base` 指向文件的位置（上表的 `pages` 或 `raw`）。查看器按清单把整个设计放进它的库里，所以顶层原理图能逐层展开、符号都能解析。
清单里的哈希来自构建所用的提交（`raw` 模式取 git 里提交的内容），查看器会逐个校验。

没有可用的文件地址时（本地默认构建，既没有 `--base-url` 也不是 `raw`），清单不生成，链接退回打开单个网表。

### 嵌入式查看器里的“使用框”（usages）

RNL 嵌入式查看器（`embed=1`）目前没有关闭使用框的参数（`embed`、`url`、`manifest`、`level`、`background`、`grid`、`names`、`origin`
之外没有别的），清单的 `display.usages` 也只对完整查看器生效。要让嵌入默认不画使用框，需要上游查看器先提供这个选项。

## 实时进展（进行中的 PR 与通知）

首页的“实时进展”表和每个模块页的“进行中”面板显示 GitHub 上标题以 `[<block>]` 开头的**进行中 PR**（编号、标题、草稿 / 待评审、作者、最近更新、
CI 状态：通过 / 失败 / 运行中）和**未关闭的通知（issue）**（标题、评论数）。数据在构建时用 GitHub API 取（`sitegen/live.py`；在 Actions 里用作业的
只读 `GITHUB_TOKEN`，本地用环境变量 `GITHUB_TOKEN` / `GH_TOKEN`，没有也会试一次匿名请求），页面上标“数据更新于 <UTC 时间>”。

* 只保留元数据：PR 和 issue 的正文、评论内容不请求、不显示。所有标题都做 HTML 转义。
* API 不可用（没有令牌、限流、断网）时构建照常成功，面板写“无法获取实时数据”和时间。`--no-live` 完全不联网。
* 标题或作者名触发工艺名称检查（`sitegen/guard.py`）的条目被丢掉并在构建日志里记一行，不会让整个构建失败。
* 工作流 `site.yml` 每小时（`17 * * * *`）重建并部署一次，所以这些数据最多落后一个小时；`push` 到 `main` 和手动触发也会部署，PR 只构建并上传预览。
  构建作业的权限只有只读的 `contents`、`pull-requests`、`issues`、`checks`、`statuses`；写 Pages 的权限只给部署作业。
  仓库 60 天没有活动时 GitHub 会停掉定时工作流，重新启用即可。
* 数据层的测试用固定的 JSON 夹具，不联网：`tests/test_site_live.py`。

### 草稿预览（`sitegen/preview.py`）

模块页用标签页组织：“主分支”（主分支的全部内容，含“进行中”面板）是默认标签，每个有预览的 PR 一个“草稿 PR #N”标签（带 CI 徽标）。
当前标签写在 URL 的 hash 里（`#pr26`；主分支没有 hash），所以可以直接链接、刷新后保持，首页表里的链接会打开对应标签；左右方向键 / Home / End 切换。
没有 JavaScript 时所有面板都显示、依次排列、各有标题。藏在隐藏标签里的嵌入查看器在标签第一次显示时才开始加载，加载在隐藏状态完成的会在显示时再适配一次。
结果的证据图默认折叠（`<details>` “图（N）”，图片是懒加载的），点缩略图放大。

每个模块页的主分支内容下面，对该模块每个进行中的 `[<block>]` PR（最新的 3 个）显示一个单独的“草稿预览 PR #N @ <sha>”区块：
按该 PR 提交里的 `specs/blocks/<block>.yaml` 和 `results/<block>/**` 填的指标表（值、限值、判定、适用工艺角的覆盖，过期标记、证据链接、图）、
用清单打开该提交 `design/xtor/<block>/` 网表的查看器，以及网表最近一次改动和 PR 的最近提交标题。首页表里有单独的“草稿预览（未评审）”一列。

内容是未评审的，所以有硬规则：

* 区块上标“未评审的草稿，不是签核证据”；它不进主分支的状态、判定和任何统计（首页“主分支状态”列和关键数字只用主分支数据）。
* 只预览 CI「contracts, drawings, results」通过的提交；否则只显示元数据和原因。
* 先过和主分支一样的检查：工艺名称检查（`guard.py`）和 `adcflow check hygiene` 的规则（服务器 / 路径 / 模型卡等）覆盖取自 PR 的全部内容（结果、规格、
  查看器会取的网表、图的说明、提交标题）。任何一处不过，该 PR 就不显示任何内容，只保留元数据行，并在构建日志里写原因。
* 从不运行 PR 的任何代码：用 `git fetch origin +refs/pull/<N>/head`（fork 的 PR 也一样）取提交，再用 `git cat-file blob` 当数据读（不做过滤、不跟符号链接），
  JSON / YAML / 文本由主分支的生成器解析。
* 图只取不超过 200 kB 的 PNG（与 `adcflow check results` 同一个上限），复制到 `preview/pr<N>/`。
* 判定用 PR 自己的规格和它自己的输入文件重算（`Block.verdicts` / `content_hash`），工艺角定义用主分支的 `specs/corners.yaml`。
* 测试用夹具 git 仓库：`tests/test_site_preview.py`。

## 验证结果的证据与图

* 页面里每个结果都链到它的证据文件：GitHub 上构建提交里的 `results/<block>/<test>/<view>/<corner>.json`（规格表里是“最差值”所在的结果文件，
  工艺角明细里是每个结果文件）；概览的行为级 ENOB 也一样。
* 结果 JSON 可以带图：`"figures": [{"file": "<stem>.<tag>.png", "caption": "..."}]`，PNG 放在 JSON 旁边。页面显示缩略图和说明，点击放大；
  PNG 会被复制到站点的相同路径（`results/.../*.png`）。没有 `figures` 字段的结果照常显示；列出了但文件不存在会让构建失败。

## 工艺名称检查

站点只写“28 nm HPC+”。构建最后会扫描输出里所有文本文件（页面、脚本、发布的网表和 RNL、清单），发现工艺厂名称就失败
（`sitegen/guard.py`；检查代码里只存名称的哈希，源码里没有明文）。仓库里别处的出现要在源文件里清掉。

## 文件

```
site/
  build.py             入口：读取数据、生成页面、复制网表、检查内链
  sitegen/data.py      从 specs / results / git 收集页面数据（调用 adcflow）
  sitegen/render.py    各页面的 HTML
  sitegen/md.py        Markdown → HTML（标题锚点、仓库内链接改写）
  sitegen/linkcheck.py 构建后的内链与锚点检查
  sitegen/live.py      GitHub 上进行中的 PR 与通知（只取元数据，失败不影响构建）
  sitegen/livepanel.py 上述数据的 HTML（转义）
  sitegen/manifest.py  查看器清单（每个网表一个，带 SHA-256）
  sitegen/guard.py     输出里不得出现工艺厂名称（只存哈希）
  static/style.css     样式（明 / 暗主题，手机与桌面）
  static/app.js        主题切换与原理图查看器的嵌入逻辑
```

不引入前端构建工具；除了 `markdown-it-py`，只用 Python 标准库与 `adcflow` 已有依赖。页面不请求任何第三方资源
（字体用系统字体），只有原理图 iframe 会访问 RNL 查看器。

## 约束

* 不得把服务器名、服务器路径、PDK 路径或模型数据放进站点（`python -m adcflow check hygiene` 必须保持干净）。
  生成器只读已跟踪的设计、规格、结果与文档文件，不读 `site.local.yaml`。
* 站点是仓库的视图：内容以仓库为准，改文字请改 `specs/`、`docs/`，不要改生成出来的页面。
