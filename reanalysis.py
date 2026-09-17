"""Reproduce descriptive checks of rounded website aggregates. Python standard library only."""
import json
from pathlib import Path

def analyze(d):
 out={}
 for h,v in d.items():
  n=v['kpis']['total'];rows=[]
  approx_total=sum(r['total']*r['cancel_rate']/100 for r in v['segment'])
  for r in v['segment']:
   est=r['total']*r['cancel_rate']/100
   rows.append(dict(**r,estimated_cancellations=est,booking_share=r['total']/n,cancellation_share=est/approx_total,rounding_bound=r['total']*.0005))
  lead=v['leadtime']; estlead=sum(r['total']*r['cancel_rate']/100 for r in lead)
  out[h]=dict(segment=sorted(rows,key=lambda x:-x['estimated_cancellations']),lead=dict(estimated_cancellations=estlead,long_booking_share=lead[-1]['total']/n,long_cancellation_share=lead[-1]['total']*lead[-1]['cancel_rate']/100/estlead),coverage={k:sum(r.get('total',r.get('bookings',0)) for r in v[k]) for k in ['segment','channel','seasonal','leadtime','deposit']},channels=[dict(**r,revenue_per_record=r['revenue']/r['total']) for r in v['channel']],seasonality=[dict(**r,covered_month_occurrences=3 if r['month'] in ['July','August'] else 2,bookings_per_occurrence=r['bookings']/(3 if r['month'] in ['July','August'] else 2)) for r in v['seasonal']])
 c=d['City Hotel']['leadtime']; r=d['Resort Hotel']['leadtime'];cn=sum(x['total'] for x in c);rn=sum(x['total'] for x in r)
 common=[(x['total']+y['total'])/(cn+rn) for x,y in zip(c,r)]
 assert abs(sum(common)-1)<1e-12
 out['lead_adjustment']={
 'city_observed':sum(x['total']*x['cancel_rate'] for x in c)/cn,
 'resort_observed':sum(x['total']*x['cancel_rate'] for x in r)/rn,
 'city_standardized':sum(w*x['cancel_rate'] for w,x in zip(common,c)),
 'resort_standardized':sum(w*x['cancel_rate'] for w,x in zip(common,r))}
 return out

if __name__=='__main__':
 p=Path(__file__).resolve().parent
 result=analyze(json.loads((p/'aggregate-data.json').read_text()))
 (p/'analysis-results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['lead_adjustment'],indent=2))
 for h in ['All','City Hotel','Resort Hotel']:
  print(h,'lead',result[h]['lead'],'seasonal highest',max(result[h]['seasonality'],key=lambda x:x['bookings_per_occurrence']))
