from socketserver import *
import urllib.request
import json
import requests
import socket 
import pandas as pd

X = pd.read_csv(r'x_unix.csv')
X = X.set_index('Unix')

y = pd.read_csv(r'y_unix.csv')

frontend_url = 'http://predictor-frontend.default.svc.cluster.local/live-data'
predictor_url = 'http://xgboost.default.svc.cluster.local/get_predict'
host = '0.0.0.0'
port = 32000
addr = (host,port)

class MyTCPHandler(StreamRequestHandler):
	def handle(self): 
#         TCP to index
		self.data = self.request.recv(1024)
		index = int(self.data.decode('utf-8'))
		dict_pic = {
            'obs_datetime':y.Unix[index],
            'observed' : round(y.Aggregate[index], 5),
            'pred_datetime': X.index[index]
            }
#		index to POST-predictor
		headers = {'content-type': 'application/json'}
		body = X.iloc[index].to_json(orient = 'index')
		pred_response = requests.post(predictor_url, json=body, headers=headers)
		dict_pic.update(json.loads(pred_response.text))
#       predictor JSON to frontend
		front_response = requests.post(frontend_url, json=dict_pic, headers=headers)
if __name__ == "__main__":
	server = TCPServer(addr, MyTCPHandler)
	print('starting server... for exit press Ctrl+C')
	server.serve_forever()
