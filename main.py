import asyncio
import environs

from fastapi import FastAPI

from utils import AppState, RequestBody, get_ngrok_url, get_request, post_request


async def lifespan(app: FastAPI):
    asyncio.create_task(send_request())
    yield


app = FastAPI(lifespan=lifespan)

state = AppState()

env = environs.Env()
env.read_env()

MESSAGE = "Hello world!"

ICORP_URL = "https://test.icorp.uz/interview.php"
NGROK_URL = env.str("NGROK_URL", default="") or get_ngrok_url()


@app.post("/")
async def handle_post(body: RequestBody):
    state.part2 = body.part2
    return {"response": f"Qabul qilindi: {body.part2}"}


async def send_request():
    response = await post_request(ICORP_URL, json_data={"msg": MESSAGE, "url": NGROK_URL})
    state.part1 = response.get("part1")

    for i in range(10):
        if state.part2 is not None:
            break

        await asyncio.sleep(1)
    else:
        print("Part2 kelmadi")
        return

    code = f"{state.part1}{state.part2}"

    response = await get_request(ICORP_URL, params={"code": code})
    message = response.get("msg")

    print("habar:", message)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
