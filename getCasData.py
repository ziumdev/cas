import time
import extConfig
import socket
import socketserver
import makeCRC as crc
import DatabaseClass


class MyTCPHandler(socketserver.BaseRequestHandler):
	maxValue = 0

	def handle(self):
		self.dataList = self.request.recv(1024).strip()
		val = self.dataList.decode('utf-8')
		print(val)
		try:
			if float(val) > 0:
				weight = val
				print("weight is " + str(weight))
				insertData(weight)
				print("insert OK")
		except Exception as e:
			print(e)


def getCasData():
	HOST = extConfig.casHost
	PORT = extConfig.casPort
	with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
		server.serve_forever()
	pass

# def getCasData():
# 	HOST = extConfig.casHost
# 	PORT = extConfig.casPort
#
# 	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	sock.bind((HOST, PORT))
# 	sock.listen()
# 	client_socket, addr = sock.accept()
# 	print('Connected by ' + str(addr))
# 	dataArr = []
#
# 	while True:
# 		print("HELLO")
# 		dataList = client_socket.recv(10)
# 		print(dataList)
# 		if len(dataList) > 0:
# 			for data in dataList:
# 				dataArr.append(data)
# 				if len(dataArr) == 10:
# 					# 데이터 저장하는 부분
# 					print(dataArr)
# 					weight = 60
# 					insertData(weight)
# 					break


def insertData(weight):
	db = DatabaseClass.Database
	db.__init__(DatabaseClass.Database)
	deviceNo = extConfig.unitId
	now = int(time.time())
	insertQuery = 'Insert into s_army.cas (device_no, weight, ftime) values (%s, %s, %s)'
	param = (deviceNo, weight, now)
	db.insertQuery(db, insertQuery, param)
	db.close(db)


def process(msg):
	crc.makecrctable()
	msgCrc = crc.crc16(msg, msg.__len__())
	quotient = int(msgCrc/256)
	msgCrcTuple=quotient, msgCrc-(256*quotient)
	msg+=msgCrcTuple
	return msg


