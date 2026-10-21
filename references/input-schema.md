# 输入与运行

本说明适用于能执行Python的AI助手或本地命令行，不要求某个厂商的技能目录或调用前缀。先进入项目根目录；命令中的python指向安装了requirements.txt依赖的实际解释器，可按环境替换为python3或py -3。所有路径支持中文。图片与扫描PDF的识别依赖宿主AI视觉能力，脚本本身没有独立OCR引擎。

```json
{
  "settings": {
    "version": "大学", "new_per_day": 20,
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

`mode` 为 count 或 unit；单元模式 unit_days 只支持1或2。`version` 可写小学、初中、高中、四六级、考研；中学/中学版映射初中。大学/大学版/默认版仍是旧3500通用版。旧通用范围明确写通用小学、通用中学、通用大学。也支持 book-catalog.json 的书目 id、CET4/CET6。settings.book_metadata 保存实际版本、来源、授权和核对状态。`output_mode` 为 combined（日集中汇总）、daily（逐日）或 memory（整本纯记忆）。combined/daily 均按当天中英对照、中译英、英译中、一页反馈表排列后进入下一天。`days` 为 `3`、`3-5`、`1,3,5-7`，使用原计划天号。`start_date` 为 YYYY-MM-DD；null 使用第1天。复习开关 spaced=true；offsets 是学习日起的正整数偏移。seed 修改可重抽随机旧词。

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
