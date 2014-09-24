from pritunl.constants import *
from pritunl.organization import Organization
from pritunl.event import Event
from pritunl.log_entry import LogEntry
import pritunl.utils as utils
from pritunl import app_server
import flask

@app_server.app.route('/organization', methods=['GET'])
@app_server.app.route('/organization/<org_id>', methods=['GET'])
@app_server.auth
def org_get(org_id=None):
    if org_id:
        return utils.jsonify(Organization.get_org(id=org_id).dict())

    orgs = []
    for org in Organization.iter_orgs():
        orgs.append(org.dict())
    return utils.jsonify(orgs)

@app_server.app.route('/organization', methods=['POST'])
@app_server.auth
def org_post():
    name = utils.filter_str(flask.request.json['name'])
    org = Organization.new_org(name=name, type=ORG_DEFAULT)
    org.commit()
    LogEntry(message='Created new organization "%s".' % org.name)
    Event(type=ORGS_UPDATED)
    return utils.jsonify(org.dict())

@app_server.app.route('/organization/<org_id>', methods=['PUT'])
@app_server.auth
def org_put(org_id):
    org = Organization.get_org(id=org_id)
    name = utils.filter_str(flask.request.json['name'])
    org.name = name
    org.commit()
    Event(type=ORGS_UPDATED)
    return utils.jsonify(org.dict())

@app_server.app.route('/organization/<org_id>', methods=['DELETE'])
@app_server.auth
def org_delete(org_id):
    org = Organization.get_org(id=org_id)
    name = org.name
    org.remove()
    LogEntry(message='Deleted organization "%s".' % name)
    Event(type=ORGS_UPDATED)
    return utils.jsonify({})
