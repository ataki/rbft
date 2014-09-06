from backend.core import db
from backend import app
from backend.core import Security, SQLAlchemyUserDatastore, \
    RoleMixin
import simplejson as json


class Permit(db.Model):
    __tablename__ = 'sfp_permit'

    # Original fields
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_number = db.Column(db.String(16))
    total_records_by_case = db.Column(db.Integer)
    project_name = db.Column(db.String(256))
    net_units = db.Column(db.Integer)
    block_lot = db.Column(db.String(16))
    min_filed = db.Column(db.DateTime)
    max_action = db.Column(db.DateTime)
    allowed_height = db.Column(db.Float)
    plan_area = db.Column(db.Integer)
    case_decision_date = db.Column(db.DateTime