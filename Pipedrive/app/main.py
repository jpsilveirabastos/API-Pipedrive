from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from healthcheck import HealthCheck
from typing import Any, Dict
from starlette.responses import Response
from .core import db
from .crud.save_data import SaveData
from .core.config import USER_WEBHOOK, PASSWORD_WEBHOOK

security = HTTPBasic()
health = HealthCheck()
app = FastAPI()

@app.post("/webhook/")
def webhook(request: Dict[Any,Any], credentials: HTTPBasicCredentials = Depends(security)):

    if (credentials.username != USER_WEBHOOK) or (credentials.password != PASSWORD_WEBHOOK):
        return 'Authentication failed'

    else:
        pipedrive_m = db.Db.tables()
        cur,conn = db.Db.connect()
        SaveData(cur,conn,pipedrive_m).save_data(request)
        db.Db.disconnect(cur, conn)

    return request

@app.post("/activity/")
def activity(request: Dict[Any,Any], credentials: HTTPBasicCredentials = Depends(security)):
    if (credentials.username != USER_WEBHOOK) or (credentials.password != PASSWORD_WEBHOOK):
        return 'Authentication failed'
        
    else:
        cur,conn = db.Db.connect()
        SaveData(cur,conn).save_activity(request)
        db.Db.disconnect(cur, conn)

    return request

@app.get("/health-check/", include_in_schema=False)
def healthcheck():
    message, status_code, headers = health.run()
    return Response(content=message, status_code=status_code, headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, debug=True, reload=True)
