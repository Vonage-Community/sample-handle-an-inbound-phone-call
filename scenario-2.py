from fastapi import FastAPI, Query
from vonage_voice import Talk, Connect, NccoAction, PhoneEndpoint

VONAGE_VIRTUAL_NUMBER = "your-vonage-number-goes-here"
AGENT_NUMBER = "your-agent-number-here"

app = FastAPI()


@app.get("/webhooks/answer")
async def answer_call():

    ncco: list[NccoAction] = [
        Talk(
            text="Hello, one moment please while your call is being forwarded to our agent."
        ),
        Connect(
            from_=VONAGE_VIRTUAL_NUMBER, endpoint=[PhoneEndpoint(number=AGENT_NUMBER)]
        ),
    ]

    return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]
