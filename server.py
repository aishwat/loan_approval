import uvicorn, os, sys

sys.path.append(".")
import pprint as pp

from datetime import datetime
from fastapi import FastAPI, Response, status
from models import Customer, Resp
from utils import matchAddress, calculateAge, roundup

# from loguru import logger
# logs_dir = os.path.join(os.path.dirname(__file__) + '/logs/')
# logger.add(logs_dir + "/file.log", rotation="500 MB", retention="10 days", backtrace=True, diagnose=True)
# logger.add(lambda msg: alerts.slack_notify(msg), level="ERROR")

app = FastAPI()


@app.get("/")
async def ping():
    return {"message": "Server up"}


@app.post("/status")
async def get_status(c: Customer, response: Response):
    try:
        resp = Resp()
        if c.income <= 20000:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'Income LE 20k'
            return resp
        if c.bureauScore < 600:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'BureauScore LE 600'
            return resp
        if c.applicationScore < 600:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'ApplicationScore LE 600'
            return resp
        if c.maxDelL12M > 30:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'maxDelL12M GT 30'
            return resp

        born = datetime.strptime(c.dob, '%m/%d/%Y').date()
        age = calculateAge(born)
        if age < 21:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'Age LT 21'
            return resp
        if age > 55:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'Age GT 55'
            return resp

        add_score = matchAddress(c.currentAddress, c.bureauAddress)
        resp.addressMatchingScore = add_score

        if add_score < 80:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'Address Matching Score LT 80'
            return resp

        headroom = (c.income * (c.allowedFoir / 100)) - c.existingEMI
        loanAmount = min(roundup(headroom * c.loanTenure), 500000)
        if loanAmount < 10000:
            resp.approvalStatus = 'Rejected'
            resp.reasonCode = 'Loan Amount LT 10k'
            return resp

        resp.approvalStatus = 'Approved'
        resp.loanAmount = loanAmount
        resp.loanTenure = c.loanTenure
        return resp

    except Exception as e:
        # logger.error('{} {} {}\n'.format('/status', c, e))
        response.body = str(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return str(e)


if __name__ == "__main__":
    # logger.info("server up")
    uvicorn.run(app, host="0.0.0.0", port=8000)
