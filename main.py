import threading
import time
from pydantic import BaseModel

import requests
import environs

from fastapi import FastAPI


class RequestBody(BaseModel):
    part2: str


app = FastAPI()

env = environs.Env()
env.read_env()

part1 = None
part2 = None
msg = None

TIME_OUT = 10

ICORP_URL = "https://test.icorp.uz/interview.php"
NGROK_URL = env.str("NGROK_URL", "https://stable-kingfish-sought.ngrok-free.app")


@app.post("/")
async def handle_post(body: RequestBody):
    global part2
    part2 = body.part2

    return {"response": f"Qabul qilindi: {body.part2}"}


def send_request():
    global part1, msg

    time.sleep(1)

    msg = input("Habarni kiriting: ")

    response = requests.post(ICORP_URL, json={"msg": msg, "url": NGROK_URL})

    part1 = response.json().get("part1")

    for i in range(TIME_OUT):
        if part2 is not None:
            break

        time.sleep(1)
    else:
        print("Part2 kelmadi")
        return

    code = f"{part1}{part2}"

    print("code:", code)

    response = requests.get(ICORP_URL, params={"code": code})
    message = response.json().get("msg")

    print("habar:", message)


def main():
    import uvicorn

    threading.Thread(target=send_request).start()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
