import requests
from requests.auth import HTTPDigestAuth
import json


def getAddressesALLFromTransactions(mainAddress):
	newAddresses = []
	address = '1C72zLBwBxzEUaZRH3BUBJUQbaZJWYysm8'
	url = 'https://blockchain.info/rawaddr/'+mainAddress
	response = requests.get(url)
	print(address+'\n')
	if(response.ok):
		jData = json.loads(response.content)
		transactions = jData['txs'];
		for key in transactions:
			print(key['hash'])
			inputs = key['inputs']
			outputs = key['out']
			print('inputs:')
			for inp in inputs:
				inputaddr = inp['prev_out']['addr'];
				print(inputaddr)
				if inputaddr != address:
					newAddresses.append(inputaddr)
			print('outputs:')
			for out in outputs:
				outputaddr = out['addr']
				print(outputaddr)
				if outputaddr != address:
					newAddresses.append(outputaddr)
			print('')
	else:
	    response.raise_for_status()
	return newAddresses



addresses = getAddressesALLFromTransactions('1C72zLBwBxzEUaZRH3BUBJUQbaZJWYysm8')
