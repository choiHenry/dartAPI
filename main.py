from dapi import Dapi
import sys
# myAPIKey = sys.argv[1]
myAPIKey = "7946dcde119af7656afc01157071c0ab9488b9ad"
api = Dapi()

api.apiKey = myAPIKey
# api.saveGroupListData()
# api.getCBDataCont('넷마블', 2020)
# api.getCBDataAll()
api.getCBData('KG케미칼', '2020')



