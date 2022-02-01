def sendSMS(mobile):
	import requests
	url = "https://www.fast2sms.com/dev/bulkV2"
	msg = "Registration confirmation eAuction"
	querystring = {"authorization":"0r67OnEBKLwbIMzYSC1h3Xcas5dVPJkgWlUfyNeopTiGm4FDAH7QFbJN1BncvXMO0EdeaGYZftlsT3j5","sender_id":"VM-INUNIV","message":msg,"language":"english","route":"p","numbers":mobile}
	headers = {
    'cache-control': "no-cache"
}
	response = requests.request("GET", url,headers=headers, params=querystring)

	print(response.text)
