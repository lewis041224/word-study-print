# Word Study Print 背单词打印 · 3.1 手机版

优先支持“手机拍照 → 宿主AI识别整理 → 导出可打印DOCX”；也支持Word、PDF、可选Excel输入与小初高内置词表。支持通用AI助手；图片与扫描PDF识别依赖宿主AI视觉，程序不内置OCR或模型API。

## 最少需要什么

生成DOCX：**Python 3.10+和python-docx**。不要求sudo、LibreOffice或预装中文字体。未安装字体不妨碍写入Word，但实际打开和打印可能替换字体；云端没有字体时，PDF预览也可能显示异常，不能据此认定词汇缺失。

手机云环境也需宿主有读取项目、执行Python和导出文件的能力；单纯聊天或浏览网页不等于能生成文件。作者反馈曾在豆包生成成功，不代表其他镜像、架构或版本已验证。

## 先探测，再按需安装

下载完整项目，进入根目录，使用实际Python解释器（可能是python3或py -3）：

```sh
python scripts/study.py doctor
python -m pip install -r requirements.txt
```

doctor输出当前解释器、Python版本、架构、依赖可导入状态、Word/PDF/Excel能力及中文建议。只读，不联网安装、不修改系统。缺pip、网络或权限时由宿主说明实际限制；优先使用独立venv，不自动sudo、不使用break-system-packages。不要把作者本机的依赖当成用户环境已有。

| 功能 | 额外条件 |
| --- | --- |
| 词书目录、候选JSON、准备词表 | Python标准库 |
| 生成或读取Word | python-docx，requirements.txt |
| 提取文字PDF | pypdf，requirements-pdf.txt |
| 读取Excel | openpyxl，requirements-excel.txt |
| 全部文件输入支持 | requirements-all.txt |
| 图片、扫描PDF识别 | 宿主AI视觉能力 |
| 渲染预览与分页视觉核验 | 可用的Word/LibreOffice、渲染工具与字体 |

按任务安装，例如python -m pip install -r requirements-excel.txt。依赖装在doctor显示的同一个解释器中。Python支持范围维持3.10+，没有据第三方报告宣称3.9或ARM设备已在本项目验证。

## 内置词表

| 版本 | 来源 | 条目行 |
| --- | --- | ---: |
| 小学 | 2022义务教育课标二级星号词目 | 505 |
| 初中 | 2022义务教育课标三级主表，包含小学基础 | 1600 |
| 高中 | 2017年版2020修订高中课标附录2 | 3000 |

已移除四六级、考研及旧通用词库，词源不设默认值：用户材料、小学、初中、高中由用户明确选择。其他学段仍可处理用户自带材料，不自动删除内置库之外的词；上传照片时以用户材料处理，不强制选择内置学段。完整来源与独立许可见[DATA_LICENSES.md](DATA_LICENSES.md)。历史包许可不追溯改变。

## 首次使用先选择形式

导入后首次响应或首次调用时，宿主先介绍功能并按[拍照到Word流程](references/photo-to-word.md)收集配置。普通ZIP没有统一的安装回调，不能保证所有平台在安装瞬间弹窗。`python scripts/study.py start`会返回可供宿主展示的介绍与选项，不自动执行安装或生成。

| 设置 | 建议预设 |
| --- | --- |
| 词源 | **无默认：用户材料/小学/初中/高中** |
| 文档形式 | 四部分练习：中英对照、中译英、英译中、反馈表 |
| 艾宾浩斯间隔复习 | 关闭 |
| 每页目标词数 | 20，可改1–20；固定16pt版式，长释义可能额外换页 |
| 每天新词数 | 20，复习另计；不是每页词数 |
| 输出组织 | 汇总一份；也可逐日或分期 |
| 每期天数 | 分期时建议30，可修改 |
| 另附整本总表 | 默认不附；可选另附或**只要总表** |
| 依赖预设 | Word核心；Excel导入依赖可另选，不输出Excel |

生成前用`estimate`说明体量：20个词、一天、每页20词、不复习，四部分通常估算4页，单独总表约1页。开启复习会使练习重复、增加页数；长释义及字体替换可能使实际页数超过估算。

## 给AI的通用用法

导入完整项目，或授权宿主读取项目目录，再说：

```text
读取项目根目录SKILL.md，先运行doctor确认能力。
使用我拍照上传的词汇，先展示识别结果；
每页20词，不启用间隔复习，保留默认四部分，汇总一份Word。
```

宿主按能力完成识别、单元/页序整理及释义词性核对。客户原文优先，真正冲突单独反馈，不写入Word。使用方式不要求某个产品的技能目录或专用调用前缀，agents/openai.yaml是可选界面元数据。

## 手机能否复用

手机打开GitHub只说明能访问源码，不代表有执行环境。优先路径是在手机上传照片，由具备视觉、Python与导出能力的AI云端处理，手机只负责收图和下载，不要求本地安装编译器。Android本地Termux有可行基础，但依赖安装需实测；iOS本地及所有豆包版本均未获得通用验证。官方依据与边界见[手机兼容性调查](references/mobile-compatibility.md)。

## 本地命令

```sh
python scripts/study.py start
python scripts/study.py books
python scripts/study.py builtin --version 小学 --out draft.json
python scripts/study.py prepare examples/input.json --out prepared.json
python scripts/study.py estimate prepared.json
python scripts/study.py build prepared.json --out outputs/demo
python scripts/study.py build prepared.json --out outputs/periods --mode periods --period-days 30 --remainder-first --include-memory --title 小学 --zip
python scripts/study.py reprint outputs/demo/plan.json --out outputs/reprint --days 1-2
```

builtin草稿需要核对suggested_meaning及pos，填写meaning并设reviewed=true后才能生成；examples/input.json为已确认的自编12词示例。参数、Excel列对、逐日版和纯记忆表见[输入与运行](references/input-schema.md)。

## 输出与失败恢复

默认每天20个新词，复习另计；间隔复习默认关闭，可设置+1、+3、+7、+14天。按天集中排列中英对照、中译英、英译中、当天一页反馈表。词性在中文侧，每页优先20词，长释义或尾页可减少。支持汇总、逐日、30天分期、余数首期、纯记忆表和ZIP。

先在临时目录生成，全部成功后才交付正式批次。缺依赖或正常报错不再留下阻止重试的半成品plan.json；已有成品不覆盖。断电、强制杀进程等崩溃恢复未承诺，旧成品和旧计划不会自动删除。

没有预览工具时可核对词数、顺序和文档结构，但须说明未完成视觉分页检查；结构检查不能证明没有分页或字体问题。生成Word不依赖渲染工具，最终仍建议在手机或电脑的Word/WPS等应用中预览后打印。没有导出入口的宿主无法自动给出下载链接。

## 授权与限制

程序及自编示例MIT，署名lewis041224；第三方数据按独立来源处理。词性、释义仍为自动选义与AI辅助候选，未整库人工校对；复习方案不承诺对每个人最优。3.1“手机版”指优先适配手机拍照与云端生成流程，不是独立手机App；真实手机、各云端账号及原生依赖仍需实测。

## 手机版示例

[下载8词模拟照片与两种Word示例](https://github.com/lewis041224/word-study-print/releases/download/v3.1.0/mobile-photo-demo-v3.1.0.zip)。模拟照片经当前宿主AI整理，默认四部分练习4页、只要总表1页，已在本机渲染检查；不是真实手机或盲测OCR结果。
