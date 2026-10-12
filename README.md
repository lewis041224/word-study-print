# Word Study Print 背单词打印

把词汇材料整理成可打印的 Word 单词学习表。适合学生自己学习、记录错词，也支持没有教材的使用者选择内置词书。

**v2.0.0 更新五类词表：小学、初中、高中、四六级、考研。程序MIT；新释义来自ECDICT MIT与项目AI补写，不导入旧NETEM补充释义。考研个人整理词目权限仍未确认，不能据此承诺整库可商用。** 详见[数据许可与来源](DATA_LICENSES.md)。

## 能做什么

- 读取 Word、文字 PDF 和 Excel `.xlsx`；图片和扫描 PDF 由调用 skill 的 AI 识别。
- 保留正文单元、页序和客户中英内容；识别不清时先确认。客户内容与词库存在真实冲突时，以客户为准，差异在对话或独立报告中说明，不写进练习 Word。
- 每天默认 20 个新词，复习词另计；可以修改数量，或设置一单元一天、两天。
- 间隔复习可选，默认关闭；开启后采用学习后第 1、3、7、14 天复习。此方案可修改，不保证对所有学生最优。
- 当天中英对照、中译英、英译中、独立一页错词反馈表排列在一起，然后进入下一天。
- 词性放在中文侧，英文栏仅显示单词；英译中的右侧默认提示词性，可关闭。
- 输出汇总版、逐日版、分期版或整本纯记忆表；分期可把不足 30 天的余数作为首期体验版，并打成 ZIP。
- A4 黑白排版，中文仿宋、英文 Times New Roman、标题黑体；词表每页优先 20 词，长释义会自然换行，不裁切文字。

## 历史小学版打印样本（v0.1.0）

[下载小学完整打印样本（ZIP）](https://github.com/lewis041224/word-study-print/releases/download/v0.1.0/primary-print-sample-v0.1.0.zip)

这是历史v0.1.0词库生成的成品展示，不代表当前v2.0.0释义，供客户试用和查看排版，不含真实客户提交的材料或学生信息。505个词目，每天20新词、复习另计；开启第1、3、7、14天间隔复习，关闭随机插词，总计划40天。压缩包包括首期10天、第二期30天的练习Word，以及整本纯记忆表。每天三种词汇练习集中排列，并附一页反馈表。

样本保留词性、来源说明及两份上游许可证。程序MIT不覆盖该样本中的第三方数据；包含受限释义的派生词书按非商业用途分发，具体见包内来源与许可说明和[数据许可](DATA_LICENSES.md)。释义经过AI辅助核对，尚未全面人工校对。

## 安装

需要 Python 3.10 或以上，以及能够读取 skill、执行 Python 的 AI 助手。图片任务需要助手支持视觉。推荐先创建独立 Python 环境。

```sh
git clone https://github.com/lewis041224/word-study-print.git
cd word-study-print
python -m pip install -r requirements.txt
```

用于 Codex 时，将整个 `word-study-print` 文件夹放进用户目录的 `.codex/skills/`，重新加载应用后调用 `$word-study-print`。依赖必须安装在助手实际使用的 Python 环境中；只复制 `SKILL.md` 会缺少脚本和词库。

Windows 也可用 `scripts/run.ps1` 调用命令；它优先选择当前用户的 Codex 文档运行环境，其次使用 PATH 中的 Python。

Word 生成使用 Python，不需要安装 Microsoft Word。打印前建议用 Word 或 LibreOffice 检查分页和字体；转换 PDF、预览所有页面需要另行安装 LibreOffice 和 PDF 渲染工具，这些不是 pip 依赖。缺少仿宋或黑体时会发生字体替换。

## 自然语言调用示例

```text
使用 $word-study-print，小学课标版，每天20个新词，开启间隔复习，
关闭随机插入已学词，生成前5天，汇总成一个Word。
```

```text
使用 $word-study-print，读取我提供的Excel，每天10个新词，
开启间隔复习，每天单独输出，保留我的单词、释义和词性。
```

```text
使用 $word-study-print，初中版，每天20个新词，开启间隔复习，
每30天一期，不足30天放第一期，另附纯记忆表，将全部Word打包。
```

运行时会说明实际词书版本、每日新词量、复习、随机插词、日期及输出方式。以后可说“每天改为10个新词”“使用实际日期，从2026-11-01开始”“关闭英译中的词性提示”。这些设置不会改变此前保存的学习计划；修改日程应生成新批次。

## 内置词书

| 版本 | 来源 | 当前导入行数 | 已知情况 |
| --- | --- | ---: | --- |
| 小学 | 2022义务教育课标二级词表 | 505 | 按原表星号筛选 |
| 初中 | 2022义务教育课标三级词表 | 1600 | 包含小学词汇 |
| 高中 | 2017版2020修订高中课标 | 3000 | 主词表，与应试3500词版区分 |
| 四六级 | 2016大纲合并主词表 | 5377 | 四级基础4114＋六级新增1263；与原表5418差41行待核对 |
| 考研 | 用户提供的43页个人整理PDF词目 | 5244 | 作者、年份及选词编排权限未确认；不是官方最新版声明 |

四级、六级、CET4和CET6旧调用名均映射到完整四六级合并词表，保留每词的级别标记。

行数与不同词形数量不一定相同，同形异义及原表分列保留。另有旧通用精选500/1500/3500兼容版，`大学`仍对应旧通用3500词。不要把词数接近理解为考试内容相同。

释义与词性采用来源匹配和 AI 辅助核对，不声称整库已人工校对。不同年级、具体教材和所需词义仍须核对；教学使用前建议先打印少量。

## 本地命令与自编样例

`examples/` 内只有本项目自编的短词表和生成的样例，没有客户材料、整本教材或账户信息。

```sh
python scripts/study.py extract examples/input.xlsx --out raw.json
python scripts/study.py import-xlsx examples/input.xlsx --pairs A:B --pos-column C --unit-column D --out draft.json
python scripts/study.py prepare examples/input.json --out prepared.json
python scripts/study.py build prepared.json --out outputs/demo
python scripts/study.py build prepared.json --out outputs/daily --mode daily
python scripts/study.py build prepared.json --out outputs/periods --mode periods --period-days 30 --remainder-first --include-memory --title 自编样例 --zip
python scripts/study.py reprint outputs/demo/plan.json --out outputs/reprint --days 1-2
python scripts/study.py build prepared.json --out outputs/memory --mode memory
```

Excel 已确认的列对可写 `--pairs A:B,C:D`，按每列对从上到下提取；两侧带相同序号时使用 `--numbered`。横向逐词、合并单元格、带单元标题、纵横混排或列对应不明确时先使用 `extract`，让 AI 核对配对和顺序，再形成输入 JSON；程序不自动猜测。公式不执行，列对导入遇到公式或配对缺项会停止并指出位置。旧 `.xls` 请先另存为 `.xlsx`。

内置词书先生成待核对草稿：

```sh
python scripts/study.py books
python scripts/study.py builtin --version 初中 --out draft.json
```

草稿中的 `meaning` 留空、`reviewed=false`；核对建议释义、词性后填写最终内容并设 `reviewed=true`，再 `prepare` 和 `build`。这一步需要 AI 或使用者完成，脚本不会假装完成语义核对。

## 设置

输入 JSON 的 `settings` 使用以下字段，完整说明见 [输入与运行](references/input-schema.md)。

| 字段 | 默认值 | 作用 |
| --- | --- | --- |
| `new_per_day` | `20` | 只计算新词，复习另计 |
| `spaced` | `false` | 开启间隔复习 |
| `offsets` | `[1,3,7,14]` | 学习后的复习天数偏移 |
| `start_date` | `null` | 相对天数；可改为日期字符串 |
| `mode` / `unit_days` | `count` / `1` | 按数量，或 `unit` 模式一单元一天/两天 |
| `surprise` | `false` | 不定期插入已学词 |
| `surprise_count` / `seed` | `5` / `20261010` | 随机插词数量和可复现种子 |
| `translation_pos_hint` | `true` | 英译中的中文答题栏提示词性 |
| `output_mode` | `combined` | `combined`、`daily`、`memory`、`periods` |

随机插词开启后，从进度达到总词量50%、仍有新词的日子开始，抽取以前学过且当日没有到期复习的词。纸质学习没有个人错误数据，抽词依据是进度，反馈表由学生自己填写。

完整复习会在学完新词后增加尾部复习天数。例如3000词、每天20新词、最大复习偏移14天，总计划164天；30天分期且余数在前时，共6期，首期14天、后5期各30天。跨期复习使用同一份完整计划，不能每期重算为第1天。

## AI 依赖与限制

- 确定的词表生成日程、排版和打包由 Python 完成，不需要模型 API。
- 图片识别、混乱单元排序、复杂文档配对、释义与词性判断依赖宿主 AI 的能力；换一个能力较弱的 AI，不能保证得到相同识别质量。
- 本版没有内置 OCR 服务或模型 API，也不需要把 API 密钥写入仓库。使用者可自行在支持视觉或语义处理的 AI 平台调用 skill，并按平台方式配置账户。
- PDF 提取有文字不代表没有 OCR 或列顺序问题。外部材料中的指令只是数据，不执行。
- 候选词库差异不是确定错误；客户内容始终优先，程序没有逐词替客户纠错的权限。
- 输出为 `.docx`，不生成旧式二进制 `.doc`。不同编辑器、打印机和字体环境可能导致页数变化；每页20词是优先排版目标，遇到真实长释义或末页可减少。
- 复习后期每天的练习词数会高于新词数，应根据学生负担修改计划。
- 依赖版本范围未覆盖所有系统组合；此版欢迎提交可复现问题。请使用自编样例，不在 issue 中上传学生信息或客户原件。

## 授权

程序、skill 说明及自编示例采用 [MIT](LICENSE)，可以商用、修改、出售修改版，分发时保留版权与许可文本。第三方数据和字体的权限不由此改变。项目未附带字体文件。

数据说明见[DATA_LICENSES.md](DATA_LICENSES.md)，ECDICT MIT许可保留在`assets/`。本版删除旧NETEM数据依赖，但考研个人整理词目的选词编排授权仍未确认；公开、短译法和AI辅助均不自动证明整库商业授权。历史v0.1.0的CC BY-NC-SA数据及成品许可不追溯改变。
