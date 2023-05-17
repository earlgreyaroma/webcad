import requests
import json


class Client():

    def __init__(self):

        # api url
        self.baseUrl = 'https://cad.onshape.com/api/v6'
        self.headers = {'Content-Type':'application/json; charset=UTF-8; qs=0.09'}


    def auth(self, accessKey: str, secretKey: str):
        # pass args
        self.accessKey = accessKey
        self.secretKey = secretKey
    
        # create session and authenticate
        self.session = requests.Session()
        self.session.auth = (accessKey, secretKey)


    def get_documents(self):

        docsReq = self.session.get(self.baseUrl + '/documents', headers=self.headers)
        docs = docsReq.json()

        return docs


    def get_document(self, did: str):

        docReq = self.session.get(self.baseUrl + '/documents/' + did, headers=self.headers)
        doc = docReq.json()

        return doc


    def get_elements(self, did: str, wid: str):

        eleReq = self.session.get(self.baseUrl + '/documents/d/' + did + '/w/' + wid + '/elements', headers=self.headers)
        ele = eleReq.json()

        return ele


    def get_parts(self, did: str, wid: str, eid:str):
        
        partsReq = self.session.get(self.baseUrl + '/parts/d/' + did + '/w/' + wid + '/e/' + eid, headers=self.headers)
        parts = partsReq.json()

        return parts


    def get_gltf_pid(self, did: str, wid: str, eid: str, pid: str):

        headers = {'Content-Type':'model/gltf-binary; qs=0.09'}
        
        gltfReq = self.session.get(self.baseUrl + '/parts/d/' + did + '/w/' + wid + '/e/' + eid + '/partid/' + pid + '/gltf', headers=self.headers)
        gltf = gltfReq.json()

        return gltf

    def get_gltf(self, did: str, wid: str, eid: str):

        headers = {'Content-Type':'model/gltf-binary; qs=0.09'}
        
        gltfReq = self.session.get(self.baseUrl + '/partstudios/d/' + did + '/w/' + wid + '/e/' + eid + '/gltf', headers=self.headers)
        gltf = gltfReq.json()

        return gltf

    def get_gltf_assembly(self, did: str, wid: str, eid: str):

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
        tranRes = self.session.post(self.baseUrl + '/assemblies/d/' + did + '/w/' + wid + '/e/' + eid + '/translations', data=reqBodyJSON, headers=self.headers)
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
        gltfRes = self.session.get(self.baseUrl + '/documents/d/' + did + '/externaldata/' + edid, headers=self.headers)
        gltf = gltfRes.json()

        return gltf

    def get_variables(self, did: str, wid: str, eid: str):

        varReq = self.session.get(self.baseUrl + '/variables/d/' + did + '/w/' + wid + '/e/' + eid + '/variables', headers=self.headers)
        var = varReq.json()

        return var

    def get_dids(self):

        docsDid = {}
        docsDidReq = self.get_documents()

        for docDid in docsDidReq['items']:
            docsDid[docDid['name']] = docDid['id']

        return docsDid


    def get_wid(self, did: str):

        widReq = self.get_document(did)
        wid = widReq['defaultWorkspace']['id']

        return wid

    def get_eids(self, did: str, wid: str):
        
        eleReq = self.get_elements(did, wid)

        eids = {}
        for ele in eleReq:
            eids[ele['name']] = ele['id']

        return eids


    def get_pids(self, did: str, wid: str, eid: str):
        
        pidReq = self.get_parts(did, wid, eid)

        print(pidReq)
        pids = {}
        for pid in pidReq:
            pids[pid['name']] = pid['partId']

        return pids

    def get_variables_dict(self, did: str, wid: str, eid: str):

        variables = self.get_variables(did, wid, eid)[0]['variables']
        varList = {}
        for var in variables:
            varList[var['name']] = var['expression']

        return varList


    def change_varstudio_var(self, name: str, expression: str, did: str, wid: str, eid: str):

        variables = self.get_variables(did, wid, eid)[0]['variables']
        for idx, var in enumerate(variables):
            if var['name'] == name:
                variables[idx]['expression'] = expression

        variablesJSON = json.dumps(variables)

        varRes = self.session.post(self.baseUrl + '/variables/d/' + did + '/w/' + wid + '/e/' + eid + '/variables', data=variablesJSON, headers=self.headers)
        return varRes


    def copy_workspace(self, newName: str, did: str, wid: str, isPublic=False):
        
        # get file information
        infoReq = self.session.get(self.baseUrl + '/documents/' + did, headers=self.headers)
        info = infoReq.json()

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
        copyRes = self.session.post(self.baseUrl + '/documents/' + did + '/workspaces/' + wid + '/copy', data=copyInfosJson, headers=self.headers)
        copyDict = copyRes.json()

        return copyDict
        

def main():
    pass

if __name__ == "__main__":
    main()
