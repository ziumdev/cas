import psycopg2
from psycopg2.extras import RealDictCursor
import DatabaseClass
import extConfig
from flask_restful import Resource, reqparse
import json
from decimal import Decimal


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


class getCasDbData(Resource):
    def post(self):
        try:
            db = DatabaseClass.Database
            db.__init__(DatabaseClass.Database)
            parser = reqparse.RequestParser()
            parser.add_argument('startTime', required=True, type=float, help='startTime is requested')
            parser.add_argument('endTime', required=True, type=float, help='endTime is requested')
            args = parser.parse_args()
            qry = 'select * from public.cas where ftime between %s and %s ;'        # 데이터를 가져오는 쿼리
            param = (args['startTime'], args['endTime'])
            resultList = db.parameterQuery(DatabaseClass.Database, qry, param)
            db.close(DatabaseClass.Database)
            return json.dumps({
                "responseCode": 2000,
                "count": len(resultList),
                "result": resultList
            }, cls=JSONEncoder)

        except Exception as e:
            return json.dumps({
                "responseCode" : 4004,
                'error': str(e)
            }, default=default)


class getLatestCasDbData(Resource):
    def post(self):
        latestQry = 'select * from public.cas where ftime = (select max(ftime) from public.cas);'  # 마지막 데이터를 가져오는 쿼리
        db = DatabaseClass.Database
        db.__init__(DatabaseClass.Database)
        result = db.query(db, latestQry)
        db.close(DatabaseClass.Database)
        print(result)
        print(result['ftime'])
        return json.dumps({
                "responseCode": 2000,
                "result": {
                    'id': result['id'],
                    'device_no': result['device_no'],
                    'weight': str(result['weight']),
                    'ftime': str(result['ftime'])
                }
            }, default=default)
