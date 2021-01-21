from dapi import Dapi
import sys
myAPIKey = sys.argv[1]
api = Dapi()

api.apiKey = myAPIKey
# api.saveGroupListData()
# api.getCBDataCont('교보생명보험', 2019)
api.getCBDataAll()
# api.getCBData('HMM', '2020')



