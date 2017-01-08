import requests
import json

from dbg import dbg
from config import config
from backend.auth import do_hmac

class Client:
	user    = config["user"]
	secret  = config["secret"]
	url     = config["backend"]

	next_id = 0

	def put(self, data, retry=True):
		jsondata = json.dumps(data)
		postdata = {
			"auth" : {
				"user" : 0,
				"hash" : do_hmac(self.secret + str(self.next_id), jsondata),
				"id"   : self.next_id
			},
			"data" : jsondata
		}
		r = requests.put(self.url + "/conns", json=postdata, timeout=20.0)
		r = r.json()
		self.next_id = r["next"]
		if r["ok"]:
			return r
		elif retry:
			msg = None
			if "msg" in r:
				msg = r["msg"]
			dbg("Backend upload failed, retrying (" + str(msg) + ")")
			return self.put(data, False)
		else:
			raise IOError(r["msg"])

