from flask import Blueprint
from app.services.house_master_service import HouseMasterServices
from flask_jwt_extended import jwt_required

house_master_bp = Blueprint('house_master', __name__)
house_master_services = HouseMasterServices()


@house_master_bp.route("/dashboard")
@jwt_required(optional=True)
def house_master_dashboard():
    try:
        pending_data = house_master_services.pending_approvals()
        return pending_data
    except Exception as e:
        raise e
    

@house_master_bp.route("/approval/<string:user_id>", methods=['POST'])
def approve_alumni(user_id):
    try:
        approve = house_master_services.approve_alumni(user_id)
        return approve
    except Exception as e:
        raise e


@house_master_bp.route("/reject/<string:user_id>", methods=['POST'])
def reject_alumni(user_id):
    try:
        reject = house_master_services.reject_alumni(user_id)
        return reject
    except Exception as e:
        raise e
    

