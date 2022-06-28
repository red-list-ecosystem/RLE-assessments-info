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

bp = Blueprint('typology', __name__, url_prefix='/IUCN-GET')

@bp.route('/list')
@login_required
def efg_list():
    pg = get_pg_connection()
    cur = pg.cursor(cursor_factory=DictCursor)
    qry="""
SELECT biome_code, code, name, count(distinct eco_id) as neco
FROM functional_groups
LEFT JOIN rle.assessment_get_xwalk
ON efg_code=code
GROUP BY biome_code,code,name
ORDER BY biome_code,code
;"""
    cur.execute(qry)
    info=cur.fetchall()
    return render_template('typology/list.html', info=info)


@bp.route('/info/<efg>')
@login_required
def info(efg):
    pg = get_pg_connection()
    cur = pg.cursor(cursor_factory=DictCursor)

    qry="""
SELECT
name,asm_id,
eco_id,eco_name,
assessment_protocol_code,
risk_category_code,
overall_risk_category
FROM rle.assessments a
LEFT JOIN rle.assessment_overall o
USING(asm_id)
LEFT JOIN rle.assessment_units u
USING(eco_id)
LEFT JOIN rle.assessment_get_xwalk x
USING(eco_id)
WHERE efg_code=%s
ORDER BY assessment_protocol_code,name
""";
    cur.execute(qry,(efg,))
    results=cur.fetchall()


    return render_template('typology/info.html', results=results,efg_code=efg)
