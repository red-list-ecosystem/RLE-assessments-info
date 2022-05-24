from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from webapp.auth import login_required
from webapp.db import get_db
from webapp.pg import get_pg_connection
from datetime import datetime, timedelta
import folium
from folium.plugins import MarkerCluster
import pycountry
from psycopg2.extras import DictCursor

bp = Blueprint('countries', __name__, url_prefix='/countries')

@bp.route('/list', defaults={'protocol': None})
@bp.route('/list/<protocol>')
@login_required
def country_list(protocol):
    pg = get_pg_connection()
    cur = pg.cursor()
    if protocol == None:
        qry="""
        WITH A AS (SELECT unnest(countries) AS iso2,eco_id FROM rle.assessment_units),
        b AS (SELECT unnest(countries) as iso2,asm_id FROM rle.assessments)
        SELECT iso2,count(distinct asm_id) as nasm,count(distinct eco_id) as neco
        FROM a
        LEFT JOIN b
        USING (iso2)
        GROUP BY iso2
        ORDER BY neco DESC ,nasm DESC;"""
    else:
        qry="""
        WITH A AS (SELECT unnest(countries) AS iso2,eco_id FROM rle.assessment_units),
        b AS (SELECT unnest(countries) as iso2,asm_id FROM rle.assessments)
        SELECT iso2,count(distinct asm_id) as nasm,count(distinct eco_id) as neco
        FROM a
        LEFT JOIN b
        USING (iso2)
        GROUP BY iso2 ORDER BY nasm DESC ,neco DESC;"""
    cur.execute(qry,(protocol,))
    info=cur.fetchall()
    records=list()
    for item in info:
        cntr=pycountry.countries.get(alpha_2=item[0])
        record={'country':cntr.name,'code':item[0],'assessments':item[1],'units':item[2]}
        records.append(record)
    return render_template('countries/list.html', info=records)

@bp.route('/info/<iso2>')
@login_required
def info(iso2):
    country=pycountry.countries.get(alpha_2=iso2)
    pg = get_pg_connection()
    cur = pg.cursor(cursor_factory=DictCursor)
    qry="""
  SELECT distinct ref_code, asm_id ,name, assessment_protocol_code, risk_category_code
  FROM rle.assessments a
  LEFT JOIN ref_list r
  USING(ref_code)
  WHERE %s=ANY(a.countries)""";
    cur.execute(qry,(iso2,))
    info=cur.fetchall()

    qry="""
SELECT asm_id, overall_risk_category,
COUNT(DISTINCT eco_id) neco
FROM rle.assessments a
LEFT JOIN rle.assessment_overall o
USING(asm_id)
LEFT JOIN rle.assessment_units u
USING(eco_id)
WHERE %s=ANY(u.countries)
GROUP BY assessment_protocol_code,name,asm_id,risk_category_code,overall_risk_category
ORDER BY assessment_protocol_code,name
""";
    cur.execute(qry,(iso2,))
    categories=cur.fetchall()

    records=dict()
    totals=dict()

    for item in info:
        records[item['asm_id']]={
        'ref_code':item['ref_code'],
        'name':item['name'],
        'assessment_protocol_code':item['assessment_protocol_code'],
        'risk_category_code':item['risk_category_code'],
        'total':0
        }
    for item in categories:
        cat=item['overall_risk_category']
        records[item['asm_id']][cat]=item['neco']
        records[item['asm_id']]['total']=records[item['asm_id']]['total']+item['neco']
        if cat not in totals.keys():
            totals[cat]=item['neco']
        else:
            totals[cat]=totals[cat]+item['neco']

    return render_template('countries/info.html', info=records,country=country, totals=totals)
