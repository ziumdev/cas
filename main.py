from flask import Flask
from flask_apscheduler import APScheduler
from flask_restful import Api
import getCasData, getCasApi

app = Flask(__name__)
api = Api(app)

#  파라미터 추가 (시작시간, 종료시간)
api.add_resource(getCasApi.getCasDbData, "/getCasData")
api.add_resource(getCasApi.getLatestCasDbData, "/getLatestCasData")

if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(id='get cas data', func=getCasData.getCasData)  # 중량 감지기 테스트
    scheduler.start()
    app.run(host='0.0.0.0', port=50001)