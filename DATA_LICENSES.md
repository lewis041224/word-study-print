# 数据许可与来源

根目录 MIT 许可证覆盖本项目程序、skill 说明和自编示例，不覆盖第三方词表、释义、教材与字体。

| 数据 | 来源 | 授权及说明 |
| --- | --- | --- |
| 通用3500精选及部分英汉释义 | [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT)，固定提交 `bc015ed2e24a7abef49fc6dbbb7fe32c1dadaf8b` | 按上游 MIT 许可保留 `assets/ECDICT-LICENSE`；选择与简化不代表释义已全面人工验证 |
| 小学/初中词目 | 义务教育英语课程标准2022，二级星号与三级主表 | 来源、原文行、页码及原PDF摘要见书目与JSON；未附完整教材或PDF。本项目不宣称对官方原表拥有版权或可重新许可 |
| 高中词目 | 普通高中英语课标2017年版2020修订附录2 | 同上；主表3000行，不补成3500词 |
| 四六级词目 | 中国教育考试网2016考试大纲 | 提取版，尚有41行计数差异；不宣称已完整核验或官方授权 |
| 考研词目与释义、其他书部分补充释义 | [exam-data/NETEMVocabulary](https://github.com/exam-data/NETEMVocabulary)，固定提交 `70dc6b68c855f21e666a7a291ff8ead5ca1f7b44` | 数据 **CC BY-NC-SA 4.0**：署名、非商业、相同方式共享。该仓库程序的 MIT 不适用于其词库 |

## 原始授权文本

- `assets/ECDICT-LICENSE`：ECDICT 上游 MIT 原文。
- `assets/licenses/NETEMVocabulary-LICENSE.txt`：NETEMVocabulary 数据授权原文。
- `assets/licenses/ATTRIBUTION.md`：词目、释义与加工说明。
- `assets/book-catalog.json`：对应版本、下载来源、摘要和核对状态。
- `assets/books/*.json`：逐条保留词目来源与 `translation_source`。

不同数据混在一个 JSON 中并不改变上游许可。含 NETEM 派生部分的文件不以根目录 MIT 重新授权；在权利尚未逐项拆分前，整份派生词书按非商业用途分发并保留相同方式共享要求。可商用的程序可以配合自行输入、合法取得商业授权的词汇使用。

官方来源中没有明确转载许可的部分，不应据此宣称获得商业授权；本项目提供来源与提取记录以供核查。客户提交材料的授权由使用者确认，工具不取得材料所有权。

释义简化、词性匹配和版式安排有 AI 辅助；不把 AI 辅助复核称为出版级或整库人工校对。用户应根据具体学习任务核对最终内容。
