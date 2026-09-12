"""Append evidence-backed manual observations and summarise measured denominators."""
import argparse,datetime,json,pathlib,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
PATH=ROOT/'seo/monitoring/observations.jsonl'
def check(row):
    prompts=json.loads((ROOT/'seo/monitoring/prompts.json').read_text());matched=next((p for p in prompts if p['id']==row.get('promptId')),None)
    if not matched or row.get('platform') not in matched['platforms']:raise ValueError('Unknown prompt or platform')
    datetime.date.fromisoformat(row['date'])
    if row.get('status') not in {'observed','not_shown','unavailable'}:raise ValueError('Explicit observation status required')
    if not row.get('evidenceFile') or not row.get('location'):raise ValueError('Evidence reference and locale required')
    if row['status']=='observed' and type(row.get('directSiteMentioned')) is not bool:raise ValueError('Observed answers need an explicit mention boolean')
    if row['status']!='observed' and row.get('directSiteMentioned') is not None:raise ValueError('Unavailable/not-shown is not a negative mention')
    for url in row.get('sourcesCited',[]):
        if urllib.parse.urlsplit(url).scheme not in {'http','https'}:raise ValueError('Citations must be page URLs')
    return {**row,'prompt':matched['prompt']}
def summary(rows):
    result={}
    for platform in ['Google Search','Google AI Overview','Google AI Mode','ChatGPT Search']:
        group=[x for x in rows if x['platform']==platform];measured=[x for x in group if x['status']=='observed']
        result[platform]={'observed':len(measured),'notShown':sum(x['status']=='not_shown' for x in group),'unavailable':sum(x['status']=='unavailable' for x in group),'mentionRate':sum(x['directSiteMentioned'] for x in measured)/len(measured) if measured else None}
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--record');parser.add_argument('--month',help='Filter YYYY-MM');args=parser.parse_args()
    if args.record:
        row=check(json.loads(pathlib.Path(args.record).read_text()))
        with PATH.open('a') as f:f.write(json.dumps(row)+'\n')
    rows=[json.loads(s) for s in PATH.read_text().splitlines() if s] if PATH.exists() else []
    if args.month:rows=[r for r in rows if r['date'].startswith(args.month)]
    print(json.dumps(summary(rows),indent=2))
