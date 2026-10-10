"""Deterministic printable vocabulary plans; OCR and semantic review belong to Codex."""
import argparse
import copy
import datetime as dt
import json
import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = dict(version='大学', new_per_day=20, mode='count', unit_days=1,
                start_date=None, spaced=False, offsets=[1, 3, 7, 14],
                surprise=False, surprise_count=5, seed=20261010,
                output_mode='combined', days=None, translation_pos_hint=True)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def norm(text):
    return re.sub(r'\s+', ' ', str(text)).strip().casefold()


def settings(raw):
    cfg = copy.deepcopy(DEFAULTS)
    cfg.update(raw or {})
    cfg['version'] = {'默认版': '大学', '小学版': '小学', '中学版': '初中', '中学': '初中',
                      '大学版': '大学', '高中版': '高中', '初中版': '初中',
                      'CET4': '四级', 'CET6': '六级', '考研版': '考研'}.get(cfg['version'], cfg['version'])
    catalog = read(ROOT / 'assets/book-catalog.json')
    selected = next((b for b in catalog['books'] if cfg['version'] in (b['stage'], b['id'])), None)
    if selected:
        cfg['version'] = selected['stage']
        cfg['book_metadata'] = copy.deepcopy(selected)
    elif cfg['version'] in ('大学', '通用小学', '通用中学', '通用大学'):
        cfg['book_metadata'] = dict(name='通用精选兼容版', stage=cfg['version'], is_official_syllabus=False)
    else:
        raise ValueError('请选择小学、初中、高中、四级、六级、考研或通用小学/通用中学/通用大学（大学为旧默认兼容版）')
    for field in ('new_per_day', 'surprise_count', 'unit_days'):
        if not isinstance(cfg[field], int) or isinstance(cfg[field], bool) or cfg[field] < 1:
            raise ValueError(field + ' 必须为正整数')
    if cfg['mode'] not in ('count', 'unit') or cfg['unit_days'] not in (1, 2):
        raise ValueError('学习模式为 count/unit，单元天数为1或2')
    if cfg['output_mode'] not in ('combined', 'daily', 'memory', 'periods'):
        raise ValueError('输出模式为 combined/daily/memory/periods')
    if not isinstance(cfg['offsets'], list) or any(type(n) is not int or n < 1 for n in cfg['offsets']):
        raise ValueError('复习偏移必须为正整数列表')
    if cfg['spaced'] and not cfg['offsets']:
        raise ValueError('开启复习时至少设置一个偏移')
    cfg['offsets'] = sorted(set(cfg['offsets']))
    if cfg['start_date']:
        dt.date.fromisoformat(cfg['start_date'])
    return cfg


def dictionary(version='大学'):
    catalog = read(ROOT / 'assets/book-catalog.json')
    selected = next((b for b in catalog['books'] if version in (b['stage'], b['id'])), None)
    if selected:
        data = read(ROOT / 'assets' / selected['file'])
        data['ranges'] = {version: [e['normalized_word'] for e in data['entries']]}
        return data
    data = read(ROOT / 'assets/vocabulary.json')
    legacy = {'大学': '大学', '通用小学': '小学', '通用中学': '中学', '通用大学': '大学'}[version]
    index = {e['normalized_word']: e for e in data['entries']}
    data['entries'] = [index[w] for w in data['ranges'][legacy]]
    data['ranges'] = {version: list(data['ranges'][legacy])}
    return data


def prepare(data):
    cfg = settings(data.get('settings'))
    vocab = dictionary(cfg['version'])
    index, exact, priority = {}, {}, {}
    for i, item in enumerate(vocab['entries']):
        for word in [item['word']] + item.get('aliases', []):
            index.setdefault(norm(word), item)
            exact.setdefault(word, item)
            priority.setdefault(norm(word), i)
    entries, conflicts, seen, group_order = [], [], set(), {}
    for i, original in enumerate(data['entries']):
        e = copy.deepcopy(original)
        if e.get('uncertain'):
            raise ValueError('请先确认识别不清的内容：' + str(e.get('source', i)))
        if not str(e.get('word', '')).strip():
            raise ValueError('存在空单词')
        e['word'] = str(e['word']).strip()
        e['meaning'] = str(e.get('meaning', '')).strip()
        e['book'] = str(e.get('book', '词汇材料'))
        e['unit'] = str(e.get('unit', ''))
        key = (e['book'], e['unit'], e.get('group_order', 0))
        group_order.setdefault(key, len(group_order))
        e['_group'] = key
        e['_group_rank'] = (e.get('group_order', group_order[key]), group_order[key])
        e['_order'] = e.get('order', i)
        e['source'] = str(e.get('source', '客户材料'))
        match = exact.get(e['word']) or index.get(norm(e['word']))
        e['core'] = norm(e['word']) in priority
        e['_priority'] = priority.get(norm(e['word']), 99999)
        if match:
            e['suggested_meaning'] = match['translation']
            if e['meaning'] and match['translation'] and norm(e['meaning']) not in norm(match['translation']):
                conflicts.append(dict(word=e['word'], customer=e['meaning'],
                                      dictionary=match['translation'], source=e['source']))
        # Keep separately listed syllabus senses, and case-distinct source words such as Miss/miss.
        dedup = (e['word'], norm(e['meaning']), norm(e.get('pos', '')),
                 e.get('source_row') if e.get('builtin') else None)
        if dedup in seen:
            continue
        seen.add(dedup)
        entries.append(e)
    if cfg.get('preserve_source_order'):
        entries.sort(key=lambda e: (e['_group_rank'], e['_order']))
    else:
        entries.sort(key=lambda e: (e['_group_rank'], bool(e.get('proper_name')),
                                   not e['core'], e['_order']))
    for i, e in enumerate(entries):
        e['id'] = i + 1
        for field in ('_group', '_group_rank', '_order', '_priority'):
            e.pop(field, None)
    return dict(settings=cfg, entries=entries, conflicts=conflicts)


def make_plan(data):
    cfg = settings(data.get('settings'))
    # Export only print-safe fields. Dictionary suggestions and conflicts never enter the plan.
    entries = []
    for e in data['entries']:
        if not e.get('meaning') or (e.get('builtin') and not e.get('reviewed')):
            raise ValueError('请先核对并填写释义：' + e['word'])
        entries.append({k: e[k] for k in ('word', 'meaning', 'book', 'unit', 'source', 'pos') if k in e})
    if not entries:
        raise ValueError('没有可打印词汇')
    batches = []
    if cfg['mode'] == 'count':
        batches = [list(range(i, min(i + cfg['new_per_day'], len(entries))))
                   for i in range(0, len(entries), cfg['new_per_day'])]
    else:
        groups = []
        for i, e in enumerate(entries):
            if not e.get('unit'):
                raise ValueError('单元模式要求明确单元；无单元请使用每天词数模式')
            key = (e.get('book'), e['unit'])
            if not groups or groups[-1][0] != key:
                groups.append((key, []))
            groups[-1][1].append(i)
        for _, ids in groups:
            size = math.ceil(len(ids) / cfg['unit_days'])
            batches.extend(ids[i:i+size] for i in range(0, len(ids), size))
    total_days = len(batches) + (max(cfg['offsets']) if cfg['spaced'] else 0)
    due = {}
    if cfg['spaced']:
        for day, batch in enumerate(batches, 1):
            for offset in cfg['offsets']:
                due.setdefault(day + offset, []).extend(batch)
    rng, learned, days = random.Random(cfg['seed']), [], []
    for day in range(1, total_days + 1):
        new = batches[day - 1] if day <= len(batches) else []
        review = list(dict.fromkeys(due.get(day, [])))
        extra = []
        if cfg['surprise'] and new and len(learned) >= math.ceil(len(entries) * .5):
            pool = [i for i in learned if i not in review]
            extra = rng.sample(pool, min(len(pool), cfg['surprise_count']))
        all_ids = new + review + extra
        date = (dt.date.fromisoformat(cfg['start_date']) + dt.timedelta(days=day-1)).isoformat() if cfg['start_date'] else None
        days.append(dict(day=day, date=date, new=new, review=review, surprise=extra, entries=all_ids))
        learned.extend(new)
    return dict(format_version=1, settings=cfg, entries=entries, days=days,
                statistics=dict(new_words=len(entries), learning_days=len(batches),
                                total_days=total_days,
                                max_daily_words=max(len(d['entries']) for d in days)))


def select_days(plan, expression=None):
    expression = expression or plan['settings'].get('days')
    if not expression:
        return plan['days']
    chosen = set()
    for part in str(expression).split(','):
        if re.fullmatch(r'\d+-\d+', part):
            a, b = map(int, part.split('-'))
            if a > b:
                raise ValueError('日期范围起点不能大于终点')
            chosen.update(range(a, b+1))
        elif part.isdigit():
            chosen.add(int(part))
        else:
            raise ValueError('天数选择示例：1,3,5-7')
    if not chosen or min(chosen) < 1 or max(chosen) > len(plan['days']):
        raise ValueError('天数超出计划范围')
    return [d for d in plan['days'] if d['day'] in chosen]


def day_label(day):
    return day['date'] or '第%d天' % day['day']


def summary(day, entries):
    def describe(ids):
        if not ids:
            return '无'
        labels = list(dict.fromkeys(entries[i].get('unit') or entries[i].get('book', '词汇') for i in ids))
        title = '、'.join(labels[:3]) + ('等' if len(labels) > 3 else '')
        return '%s %d词' % (title, len(ids))
    return '%s：新学%s；复习%s。' % (day_label(day), describe(day['new']), describe(day['review'] + day['surprise']))


def document(plan, days, target):
    from print_layout import practice_document
    practice_document(plan, days, target)


def export(plan, out, expression=None, mode=None):
    out = Path(out)
    days = select_days(plan, expression)
    mode = mode or plan['settings']['output_mode']
    files = [('单词总版记忆表.docx', [])] if mode == 'memory' else ([('1.docx', days)] if mode == 'combined' else [(str(d['day']) + '.docx', [d]) for d in days])
    if (out / 'plan.json').exists() or any((out / name).exists() for name, _ in files):
        raise ValueError('输出已存在，请使用新的批次目录')
    out.mkdir(parents=True, exist_ok=True)
    write(out / 'plan.json', plan)
    for name, selected in files:
        if mode == 'memory':
            from print_layout import memory_document
            memory_document(plan, out / name)
        else:
            document(plan, selected, out / name)
    return [str(out / name) for name, _ in files]


def extract(path):
    path = Path(path)
    if path.suffix.lower() == '.xlsx':
        from excel_input import extract_excel
        return extract_excel(path)
    if path.suffix.lower() == '.docx':
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
        doc = Document(path)
        blocks = []
        for element in doc.element.body:
            if element.tag.endswith('}p'):
                text = Paragraph(element, doc).text
                if text.strip():
                    blocks.append(dict(type='paragraph', text=text))
            elif element.tag.endswith('}tbl'):
                blocks.append(dict(type='table', rows=[[c.text for c in r.cells] for r in Table(element, doc).rows]))
        return dict(source=str(path), blocks=blocks, needs_semantic_pairing=True)
    if path.suffix.lower() == '.pdf':
        from pypdf import PdfReader
        pages = [p.extract_text() or '' for p in PdfReader(path).pages]
        return dict(source=str(path), pages=[dict(page=i+1, text=t, needs_vision=not t.strip()) for i, t in enumerate(pages)], needs_semantic_pairing=True)
    raise ValueError('extract 支持 Word/PDF/Excel .xlsx；图片请使用 AI 视觉识别')


def main():
    parser = argparse.ArgumentParser(description='背单词打印工具')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('books')
    p.add_argument('--out')
    for cmd in ('extract', 'prepare', 'build', 'reprint'):
        p = sub.add_parser(cmd)
        p.add_argument('input')
        p.add_argument('--out', required=True)
        if cmd in ('build', 'reprint'):
            p.add_argument('--days')
            p.add_argument('--mode', choices=['combined', 'daily', 'memory', 'periods'])
            p.add_argument('--period-days', type=int, default=30)
            p.add_argument('--remainder-first', action='store_true')
            p.add_argument('--include-memory', action='store_true')
            p.add_argument('--title', default='单词')
            p.add_argument('--zip', action='store_true')
    p = sub.add_parser('import-xlsx')
    p.add_argument('input')
    p.add_argument('--pairs', required=True)
    p.add_argument('--sheet')
    p.add_argument('--start-row', type=int, default=2)
    p.add_argument('--numbered', action='store_true')
    p.add_argument('--pos-column')
    p.add_argument('--unit-column')
    p.add_argument('--version', default='大学')
    p.add_argument('--out', required=True)
    p = sub.add_parser('builtin')
    p.add_argument('--version', default='大学')
    p.add_argument('--limit', type=int)
    p.add_argument('--out', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'books':
            catalog = read(ROOT / 'assets/book-catalog.json')
            if args.out:
                write(args.out, catalog)
            else:
                print(json.dumps(catalog, ensure_ascii=False, indent=2))
        elif args.command == 'extract':
            write(args.out, extract(args.input))
        elif args.command == 'import-xlsx':
            from excel_input import import_pairs
            result = import_pairs(args.input, args.pairs, args.sheet, args.start_row,
                                  args.numbered, args.pos_column, args.unit_column, args.version)
            write(args.out, result)
            print(json.dumps(dict(entries=len(result['entries']), needs_semantic_review=True)))
        elif args.command == 'builtin':
            cfg = settings(dict(version=args.version))
            vocab = dictionary(cfg['version'])
            items = vocab['entries']
            if args.limit is not None:
                if args.limit < 1:
                    raise ValueError('limit 必须为正整数')
                items = items[:args.limit]
            title = cfg['book_metadata']['name']
            print_title = title.replace('（提取待核对版）', '')
            entries = []
            for i, item in enumerate(items):
                e = dict(word=item['word'], meaning='', suggested_meaning=item.get('print_meaning') or item['translation'],
                         book=print_title, source='内置词库：' + print_title, builtin=True, reviewed=False, order=i)
                if item.get('print_pos'):
                    e['pos'] = item['print_pos']
                for field in ('aliases', 'source_raw', 'source_row', 'source_sense', 'pdf_page', 'translation_source'):
                    if field in item:
                        e[field] = copy.deepcopy(item[field])
                entries.append(e)
            write(args.out, dict(settings=cfg, entries=entries))
            print(json.dumps(dict(book=title, entries=len(entries), status=cfg['book_metadata'].get('status'),
                                  warnings=cfg['book_metadata'].get('warnings', [])), ensure_ascii=False))
        elif args.command == 'prepare':
            result = prepare(read(args.input))
            write(args.out, result)
            print(json.dumps(dict(conflict_candidates=len(result['conflicts']), entries=len(result['entries'])), ensure_ascii=False))
        else:
            plan = read(args.input) if args.command == 'reprint' else make_plan(read(args.input))
            mode = args.mode or plan['settings']['output_mode']
            if mode == 'periods':
                if args.days or plan['settings'].get('days'):
                    raise ValueError('分期必须使用完整计划；选定天数请用combined或daily')
                from batch_export import export_periods
                files = export_periods(plan, args.out, args.period_days, args.remainder_first,
                                       args.include_memory, args.title)
            else:
                files = export(plan, args.out, args.days, mode)
                if args.include_memory and mode != 'memory':
                    from print_layout import memory_document
                    target = Path(args.out)/'单词总版记忆表.docx'
                    memory_document(plan, target)
                    files.append(str(target))
            if args.zip:
                from batch_export import zip_output
                files.append(zip_output(args.out, files))
            print(json.dumps(dict(files=files, statistics=plan['statistics'], settings=plan['settings']), ensure_ascii=False))
    except (ValueError, KeyError, ImportError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
