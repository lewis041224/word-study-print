"""Export a complete plan into periods, preserving reviews across boundaries."""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def periods(total_days, period_days=30, remainder_first=False):
    if type(period_days) is not int or period_days < 1:
        raise ValueError('period-days 必须为正整数')
    if total_days < 1:
        raise ValueError('学习计划为空')
    first = (total_days % period_days or period_days) if remainder_first else period_days
    result, start = [], 1
    while start <= total_days:
        end = min(total_days, start + (first if start == 1 else period_days) - 1)
        result.append((start, end))
        start = end + 1
    return result


def export_periods(plan, out, period_days=30, remainder_first=False, include_memory=False, title='单词'):
    from print_layout import practice_document, memory_document
    from study import write
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError('输出目录非空，请使用新的批次目录')
    title = str(title).strip()
    if not title or any(c in title for c in '<>:"/\\|?*') or title.endswith(('.', ' ')):
        raise ValueError('书名不能包含文件名保留字符')
    spans = periods(len(plan['days']), period_days, remainder_first)
    out.mkdir(parents=True, exist_ok=True)
    write(out/'plan.json', plan)
    write(out/'分期索引.json', spans)
    files = []
    for number, (start, end) in enumerate(spans, 1):
        target = out/f'{number}-{len(spans)}.docx'
        days = [d for d in plan['days'] if start <= d['day'] <= end]
        practice_document(plan, days, target, f'{title} 第{number}/{len(spans)}期 第{start}至{end}天')
        files.append(target)
    if include_memory:
        target = out/f'{title}单词总版记忆表.docx'
        memory_document(plan, target, f'{title}单词总版记忆表')
        files.append(target)
    s = plan['settings']
    notes = [f'{title}，{len(plan["entries"])}条词汇，每天{s["new_per_day"]}个新词，复习另计。',
             f'新学{plan["statistics"]["learning_days"]}天，全计划{len(plan["days"])}天。',
             f'间隔复习：{s["spaced"]}，学习后复习偏移：{s["offsets"]}天；随机旧词：{s["surprise"]}。',
             '每天中英对照、中译英、英译中、一页反馈表集中排列；词性在中文侧。',
             '文件名1-N表示第1/N期；首期是否余数在前：'+str(remainder_first)+'。',
             '纯记忆表每词一次，不含互译练习、复习日程和反馈表。',
             '可在运行时说“每天10个新词”“关闭复习”或“英译中不显示词性提示”。',
             '程序与词库许可分开；商业使用前查看来源与许可说明。']
    notes.extend(s.get('book_metadata', {}).get('warnings', []))
    (out/'使用说明.txt').write_text('\n'.join(notes)+'\n', encoding='utf-8')
    return [str(f) for f in files]


def zip_output(out, files=None):
    out = Path(out)
    target = out.parent/(out.name+'.zip')
    if target.exists():
        raise ValueError('ZIP已存在，请使用新的批次目录')
    selected = [Path(f) for f in files] if files is not None else sorted(out.glob('*.docx'))
    selected += [f for f in (out/'使用说明.txt', out/'来源与许可说明.txt') if f.exists()]
    with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
        for file in selected:
            if file.resolve().parent != out.resolve():
                raise ValueError('打包文件不属于本批次目录')
            archive.write(file, file.name)
    return str(target)
