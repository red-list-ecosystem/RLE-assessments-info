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
    return render_template('assessments/info.html', info=info)
