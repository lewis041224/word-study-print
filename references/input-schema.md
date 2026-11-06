# 输入与运行

本说明适用于能执行Python的AI助手或本地命令行，不要求某个厂商的技能目录或调用前缀。先进入项目根目录；命令中的python指向安装了requirements.txt依赖的实际解释器，可按环境替换为python3或py -3。所有路径支持中文。图片与扫描PDF的识别依赖宿主AI视觉能力，脚本本身没有独立OCR引擎。

```json
{
  "settings": {
    "version": "用户材料", "new_per_day": 20,
    "mode": "count", "unit_days": 1,
    "start_date": null, "spaced": false,
    "offsets": [1, 3, 7, 14],
    "surprise": false, "surprise_count": 5, "seed": 20261010,
    "output_mode": "combined", "days": null, "translation_pos_hint": true
  },
  "entries": [
    {"word": "apple", "meaning": "苹果", "book": "教材A", "unit": "Unit 1",
     "group_order": 1, "order": 1, "source": "照片2 正文Unit 1",
     "proper_name": false, "reviewed": true}
  ]
}
```

`mode`为count或unit，unit_days支持1或2。`version`仅支持小学、初中、高中，词源无默认；上传照片或指定用户材料时使用version="用户材料"（别名provided），不自动选内置学段，中学映射初中，旧大学/通用/四六级/考研调用名不再提供。output_mode支持combined、daily、memory和periods；days用于原计划日号筛选，start_date为空时为相对天数，spaced与offsets控制间隔复习。

`group_order` 是宿主AI或使用者阅读后确认的单元/来源组顺序；`order` 为组内顺序。缺省时保持输入次序；自然排序不能替代正文判断。同一本书同一单元使用同一 group_order。无单元材料在 count 模式按来源组组织；unit 模式要求每项有单元。`meaning` 是最终打印的客户释义；缺省时从词库补充 `suggested_meaning`，需核对后赋值。`pos` 为单独的词性字段，默认只在中文侧显示；英译中默认位于右侧答题栏开头，translation_pos_hint=false 可不显示提示。客户词性优先；内置词性是候选，冲突由宿主AI或使用者结合语境核对。

```text
python scripts/study.py extract "材料.docx" --out raw.json
python scripts/study.py books --out books.json
python scripts/study.py builtin --version 小学 --out draft.json
python scripts/study.py prepare input.json --out prepared.json
python scripts/study.py build prepared.json --out output-batch
python scripts/study.py build prepared.json --out memory-batch --mode memory
python scripts/study.py reprint output-batch/plan.json --out reprint-batch --days 3-5
```

extract保留Word段落/表格顺序；PDF文本按页保留，扫描无文字时标记needs_vision；Excel .xlsx保留工作表、非空行、逐格坐标、原文和合并范围。公式不执行，标为formula=true。横纵排版、乱码、混合列需要AI核对。builtin可加 `--limit 40` 先核对小批；正式整册不要因此漏掉其余条目。

## Excel与分期打包

```text
python scripts/study.py extract 材料.xlsx --out raw.json
python scripts/study.py import-xlsx 材料.xlsx --pairs A:B,C:D --start-row 2 --numbered --out draft.json
python scripts/study.py import-xlsx 材料.xlsx --sheet 词汇 --pairs A:B --pos-column C --unit-column D --out draft.json
python scripts/study.py build prepared.json --out batch --mode periods --period-days 30 --remainder-first --include-memory --title 初中 --zip
```

列对按各工作表、各列对、从上到下读取。word与meaning两侧都带相同数字序号时，numbered核对后移除编号；序号不一致、公式或配对缺项会指出位置并停止。未指定sheet时处理全部工作表，需确认每张表的列对兼容。不同布局先extract并进行语义配对；列对导入不自动处理标题行或合并的单元标题。旧.xls先另存为.xlsx。导入设置preserve_source_order=true，prepare按来源组和原序保留排列；核对后可补unit/group_order。

output_mode另支持periods。命令行period-days控制期长，remainder-first将余数作为首期（整除时首期仍为完整期），include-memory附整本纯记忆表，zip在批次目录旁打包。分期使用完整计划，不与days选择混用。文件名1-N.docx表示第1/N期；保留跨期复习。ZIP只收本批次生成的Word、使用说明与指定来源许可文本，默认不打入上传原件或中间识别数据。

prepare 的 conflicts 是候选差异：可能存在同义表达，需语义复核。工具按所选书的词目和原表拼写别名匹配，保留客户拼写；可疑拼写另由宿主AI或使用者查核，绝不自动替换客户词形。未确认的识别结果不进入准备好的词表。builtin 保留 source_raw、source_row、source_sense、pdf_page 和 aliases；原表分列的同形词以及 Miss/miss 不因空释义而合并。派生词不自动增加为主词目。

build 会拒绝空释义/未核对的内置词条。plan.json 保存所有日子与随机选词，打印选择不会改变完整计划。会建立新目录并拒绝覆盖现有 Word/plan.json。个人学习进度与掌握程度不由本工具推断。

## 环境与失败恢复

先运行python scripts/study.py doctor。生成Word只需python-docx，读取PDF需pypdf，读取Excel需openpyxl；安装到doctor.executable对应的环境。build/reprint在临时目录完成后才交付；失败会清理本次临时产物，修复缺项后可使用原目标重试。已有成品目录不覆盖，改用新批次。异常断电或强制结束进程可能留下临时目录；不宣称能自动恢复所有崩溃。

## 形式与体量

words_per_page为1–20的每页目标词数，默认建议20，与new_per_day不同。spaced默认false，默认combined四部分按天排列。include_memory默认false；true时加整本总表。output_mode="memory"只生成总表，无练习空栏、复习重复或反馈表。period_days建议30，分期CLI --period-days优先于JSON设置。estimate input.json --mode memory等命令在生成前估算页数，不写Word。长释义、字体替换可能使实际页数增加。

词源缺失时prepare/build会提示先选择，不回退小学。明确执行import-xlsx已选择用户文件，version默认为用户材料；builtin必须显式提供--version 小学/初中/高中。原计划reprint保留旧内容，不据此重新引入已删除词库。
