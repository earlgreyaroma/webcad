import requests
import json


class Client():

    def __init__(self):

        # api url
        self.baseUrl = 'https://cad.onshape.com/api/v6'
        self.headers = {'Content-Type':'application/json; charset=UTF-8; qs=0.09'}

        self.did = None
        self.did_name = None
        self.wid = None
        self.eid = None
        self.eid_name = None
        self.veid = None
        self.veid_name = None
        self.pid = None

    def auth(self, accessKey: str, secretKey: str):
        # pass args
        self.accessKey = accessKey
        self.secretKey = secretKey
    
        # create session and authenticate
        self.session = requests.Session()
        self.session.auth = (accessKey, secretKey)

        checkRes = self.session.get(self.baseUrl + '/users/sessioninfo', headers=self.headers)
        status_code = checkRes.status_code

        if status_code == 200:
            check = checkRes.json()
            state = check['state']
            if state == 1:
                result = True
            else:
                result = False
        else:
            result = False

        return result

    def get_documents(self):

        docsRes = self.session.get(self.baseUrl + '/documents', headers=self.headers)
        docs = docsRes.json()

        return docs

    def get_dids(self):

        dids = {}
        didsRes = self.get_documents()

        for did in didsRes['items']:
            dids[did['name']] = did['id']

        return dids

    def set_did(self, did: str):
        self.did = did

    def get_document(self):

        docRes = self.session.get(self.baseUrl + '/documents/' + self.did, headers=self.headers)
        doc = docRes.json()

        return doc

    def get_wid(self):

        widRes = self.get_document()
        wid = widRes['defaultWorkspace']['id']

        return wid

    def set_wid(self, wid: str):
        self.wid = wid

    def get_elements(self):

        elesRes = self.session.get(self.baseUrl + '/documents/d/' + self.did + '/w/' + self.wid + '/elements', headers=self.headers)
        eles = elesRes.json()

        return eles

    def get_eids(self):
        
        eidRes = self.get_elements()

        eids = {}
        for eid in eidRes:
            eids[eid['name']] = eid['id']

        return eids

    def set_eid(self, eid: str):
        self.eid = eid

    def set_veid(self, veid: str):
        self.veid = veid

    def get_variables(self):

        varsRes = self.session.get(self.baseUrl + '/variables/d/' + self.did + '/w/' + self.wid + '/e/' + self.veid + '/variables', headers=self.headers)
        _vars = varsRes.json()

        return _vars

    def get_variables_dict(self):

        _vars = self.get_variables()[0]['variables']
        varsList = {}
        for var in _vars:
            varsList[var['name']] = var['expression']

        return varsList


    def change_varstudio_var(self, name: str, expression: str):

        variables = self.get_variables()[0]['variables']
        for idx, var in enumerate(variables):
            if var['name'] == name:
                variables[idx]['expression'] = expression
        variablesJSON = json.dumps(variables)

        varRes = self.session.post(self.baseUrl + '/variables/d/' + self.did + '/w/' + self.wid + '/e/' + self.veid + '/variables', data=variablesJSON, headers=self.headers)
        
        return varRes

    def get_thumbnail(self, size: str):

        thumbRes = self.session.get(self.baseUrl + '/thumbnails/d/' + self.did + '/w/' + self.wid + '/e/' + self.eid + '/s/' + size, headers=self.headers)
        thumb = thumbRes.content
        return thumb

    def set_eid_name(self, eid_name: str):
        self.eid_name = eid_name

    def set_veid_name(self, veid_name: str):
        self.veid_name = veid_name

    def copy_workspace(self, newName: str, isPublic=False):
        
        # get file information
        infoRes = self.session.get(self.baseUrl + '/documents/' + self.did, headers=self.headers)
        info = infoRes.json()

        # create required body for post request
        copyInfos = {
            'betaCapabilityIds': info['betaCapabilityIds'],
            'isPublic': isPublic,
            'newName': newName,
            'ownerId': info['owner']['id'],
            'ownerTypeIndex': info['owner']['type'],
            'parentId': info['parentId'],
            'projectId': info['projectId']
        }
        copyInfosJson = json.dumps(copyInfos)

        # create copy via API command
        copyRes = self.session.post(self.baseUrl + '/documents/' + self.did + '/workspaces/' + self.wid + '/copy', data=copyInfosJson, headers=self.headers)
        copyDict = copyRes.json()
        newDid = copyDict['newDocumentId']
        newWid = copyDict['newWorkspaceId']

        return [newDid, newWid]
        
    def get_gltf(self):

        headers = {'Content-Type':'model/gltf-binary; qs=0.09'}
        
        gltfReq = self.session.get(self.baseUrl + '/partstudios/d/' + self.did + '/w/' + self.wid + '/e/' + self.eid + '/gltf', headers=self.headers)
        gltf = gltfReq.json()

        return gltf

    def get_gltf_assembly(self):

        # create request body
        reqBody = {
            "allowFaultyParts": False,
            "angularTolerance": 0.01,
            "distanceTolerance": 0.01,
            "formatName": "GLTF",
            "importWithinDocument": True,
            "maximumChordLength": 0.01,
            "storeInDocument": False
        }
        reqBodyJSON = json.dumps(reqBody)

        # get assembly translation and tid
        tranRes = self.session.post(self.baseUrl + '/assemblies/d/' + self.did + '/w/' + self.wid + '/e/' + self.eid + '/translations', data=reqBodyJSON, headers=self.headers)
        tran = tranRes.json()
        tid = tran['id']

        # check if request status is DONE and extract external data id
        reqStatus = ''
        while reqStatus != 'DONE':
            statusRes = self.session.get(self.baseUrl + '/translations/' + tid, headers=self.headers)
            status = statusRes.json()
            reqStatus = status['requestState']
        edid = status['resultExternalDataIds'][0]

        # get gltf object
        gltfRes = self.session.get(self.baseUrl + '/documents/d/' + self.did + '/externaldata/' + edid, headers=self.headers)
        gltf = gltfRes.json()

        return gltf

    def set_pid(self, pid: str):
        self.pid = pid






    def get_parts(self):
        
        partsReq = self.session.get(self.baseUrl + '/parts/d/' + self.did + '/w/' + self.wid + '/e/' + self.eid, headers=self.headers)
        parts = partsReq.json()

        return parts


    def get_gltf_pid(self):

        headers = {'Content-Type':'model/gltf-binary; qs=0.09'}
        
        gltfReq = self.session.get(self.baseUrl + '/parts/d/' + self.did + '/w/' + self.wid + '/e/' + self.eid + '/partid/' + self.pid + '/gltf', headers=self.headers)
        gltf = gltfReq.json()

        return gltf



    def get_gltf_assembly(self):

        # create request body
        reqBody = {
            "allowFaultyParts": False,
            "angularTolerance": 0.01,
            "distanceTolerance": 0.01,
            "formatName": "GLTF",
            "importWithinDocument": True,
            "maximumChordLength": 0.01,
            "storeInDocument": False
        }
        reqBodyJSON = json.dumps(reqBody)

        # get assembly translation and tid
        tranRes = self.session.post(self.baseUrl + '/assemblies/d/' + self.did + '/w/' + self.wid + '/e/' + self.eid + '/translations', data=reqBodyJSON, headers=self.headers)
        tran = tranRes.json()
        tid = tran['id']

        # check if request status is DONE and extract external data id
        reqStatus = ''
        while reqStatus != 'DONE':
            statusRes = self.session.get(self.baseUrl + '/translations/' + tid, headers=self.headers)
            status = statusRes.json()
            reqStatus = status['requestState']
        edid = status['resultExternalDataIds'][0]

        # get gltf object
        gltfRes = self.session.get(self.baseUrl + '/documents/d/' + self.did + '/externaldata/' + edid, headers=self.headers)
        gltf = gltfRes.json()

        return gltf







    def get_pids(self):
        
        pidReq = self.get_parts()

        print(pidReq)
        pids = {}
        for pid in pidReq:
            pids[pid['name']] = pid['partId']

        return pids






def main():
    pass

if __name__ == "__main__":
    main()
