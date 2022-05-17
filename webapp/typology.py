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
