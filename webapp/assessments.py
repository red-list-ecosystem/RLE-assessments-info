from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from webapp.auth import login_required
from webapp.db import get_db
from webapp.pg import get_pg_connection
from psycopg2.extras import DictCursor

bp = Blueprint('assessments', __name__, url_prefix='/assessments')

@bp.route('/info/<id>')
@login_required
def info(id):
    pg = get_pg_connection()
    cur = pg.cursor(cursor_factory=DictCursor)
    qry="""
        SELECT *
        FROM rle.assessments
        WHERE asm_id=%s
        ;"""
    cur.execute(qry,(id,))
    info=cur.fetchone()

    qry="""
        SELECT eco_id, eco_name, eco_name_orig, eco_name_lang, countries,max(date_part('year',assessment_date))::int as yr, overall_risk_category as cat,string_agg(efg_code, ' / ') as codes,string_agg(url, ' :: ') as urls
        FROM rle.assessment_overall o
        LEFT JOIN rle.assessment_units u USING (eco_id)
        LEFT JOIN rle.assessment_get_xwalk x USING (eco_id)
        LEFT JOIN rle.assessment_links as k USING (eco_id,asm_id)
        WHERE asm_id like %s
        GROUP BY eco_id,eco_name, eco_name_orig, eco_name_lang, countries,overall_risk_category
        ORDER BY eco_name
    ;"""

    cur.execute(qry,(id,))
    units=cur.fetchall()
    cats=dict()
    for unit in units:
        x=unit['cat']
        if x in cats.keys():
            cats[x]=cats[x]+1
        else:
            cats[x]=1

    return render_template('assessments/info.html', info=info, units=units, cats=cats)
