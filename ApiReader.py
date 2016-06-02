import requests
from requests.auth import HTTPDigestAuth
import json

jasonData = {}

newAddresses = []
inputAdresses = []
outputAddresses = []

def getAddressesALLFromTransactions(mainAddress):
	url = 'https://blockchain.info/rawaddr/'+mainAddress
	response = requests.get(url)
	if(response.ok):
		jData = json.loads(response.content)
		transactions = jData['txs'];

		jasonData[mainAddress] = {}
		jasonData[mainAddress]['pointsTo'] = []
		jasonData[mainAddress]['pointedBy'] = []

		for key in transactions:
			isOutcome = False

			TranInputsComplete = []
			TranOutputsComplete = []

			TranInputs = []
			TranOutputs = []

			inputs = key['inputs']
			outputs = key['out']

			for inp in inputs:
				inputaddr = inp['prev_out']['addr'];
				TranInputsComplete.append(inputaddr)
				if inputaddr != mainAddress:
					TranInputs.append(inputaddr)
				else:
					isOutcome = True

			for out in outputs:
				if 'addr' in out:
					outputaddr = out['addr']
					TranOutputsComplete.append(outputaddr)
					if outputaddr != mainAddress:
						TranOutputs.append(outputaddr)

			if isOutcome:
				jasonData[mainAddress]['pointsTo'] = jasonData[mainAddress]['pointsTo'] + TranOutputs
			else:
				jasonData[mainAddress]['pointedBy'] = jasonData[mainAddress]['pointedBy'] + TranInputs

	else:
	    response.raise_for_status()

	jasonData[mainAddress]['pointsTo'] = list(set(jasonData[mainAddress]['pointsTo']))
	jasonData[mainAddress]['pointedBy'] = list(set(jasonData[mainAddress]['pointedBy']))




getAddressesALLFromTransactions('1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F')

print(jasonData)

#with open('data.json', 'w') as outfile:
#    json.dump(jasonData, outfile)

#with open('data.json') as data_file:    
#    data = json.load(data_file)

#for key in data.keys():
#	print(key)



#	1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F
# satoshi : 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa