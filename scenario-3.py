import os
from dotenv import load_dotenv
from threading import Timer
from fastapi import FastAPI, Query
from vonage import Auth, Vonage
from vonage_voice import Talk, Connect, NccoAction, PhoneEndpoint, Stream

load_dotenv()

APPLICATION_ID = os.getenv("APPLICATION_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

VONAGE_VIRTUAL_NUMBER = "your-vonage-number-goes-here"
AGENT_NUMBER = "your-agent-number-here"

AUDIO_URL = "https://download.samplelib.com/mp3/sample-12s.mp3"

app = FastAPI()


def transfer_call(call_id):
    print("Transferring the call ... ")

    ncco: list[NccoAction] = [
        Talk(
            text="Hello, one moment please while your call is being forwarded to our agent."
        ),
        Connect(
            from_=VONAGE_VIRTUAL_NUMBER, endpoint=[PhoneEndpoint(number=AGENT_NUMBER)]
        ),
    ]

    client = Vonage(
        Auth(
            application_id=APPLICATION_ID,
            private_key=PRIVATE_KEY,
        )
    )

    client.voice.transfer_call_ncco(uuid=call_id, ncco=ncco)


@app.get("/webhooks/answer")
async def answer_call(call_id: str = Query(..., alias="uuid")):
    print(f"The UUID for this call is:====> {call_id}")

    Timer(30, transfer_call, [call_id]).start()

    ncco: list[NccoAction] = [
        Talk(
            text="Hello, our agents are assisting other customers. Please hold and we will connect you as soon as possible."
        ),
        Stream(streamUrl=[AUDIO_URL], loop=0),
    ]

    return [action.model_dump(by_alias=True, exclude_none=True) for action in ncco]
