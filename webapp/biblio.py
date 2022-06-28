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

bp = Blueprint('references', __name__, url_prefix='/refs')

@bp.route('/list', defaults={'protocol': None})
@bp.route('/list/<protocol>')
@login_required
def ref_list(protocol):
    pg = get_pg_connection()
    cur = pg.cursor(cursor_factory=DictCursor)
    if protocol == None:
        qry="""
        SELECT asm_id,ref_code,assessment_protocol_code,risk_category_code,n_units,name, ref_cite
        FROM rle.assessments
        LEFT JOIN ref_list
        USING (ref_code);
        """
    else:
        qry="""
        SELECT asm_id,ref_code,assessment_protocol_code,risk_category_code,n_units,name, ref_cite
        FROM rle.assessments
        LEFT JOIN ref_list
        USING (ref_code)
        WHERE assessment_protocol_code = %s;
        """
    cur.execute(qry,(protocol,))
    info=cur.fetchall()

    return render_template('references/list.html', info=info)
