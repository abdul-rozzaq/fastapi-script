import threading
import time
import environs

from fastapi import FastAPI

from utils import RequestBody, get_ngrok_url, get_request, post_request


app = FastAPI()

env = environs.Env()
env.read_env()

part1, part2, msg = None, None, None

TIME_OUT = 10

ICORP_URL = "https://test.icorp.uz/interview.php"
NGROK_URL = env.str("NGROK_URL", get_ngrok_url())


@app.post("/")
async def handle_post(body: RequestBody):
    global part2
    part2 = body.part2

    return {"response": f"Qabul qilindi: {body.part2}"}


def send_request():
    global part1, msg

    time.sleep(1)

    msg = input("Habarni kiriting: ")

    response = post_request(ICORP_URL, json_data={"msg": msg, "url": NGROK_URL})
    part1 = response.get("part1")

    for i in range(TIME_OUT):
        if part2 is not None:
            break

        time.sleep(1)
    else:
        print("Part2 kelmadi")
        return

    code = f"{part1}{part2}"

    response = get_request(ICORP_URL, params={"code": code})
    message = response.get("msg")

    print("habar:", message)


def main():
    import uvicorn

    threading.Thread(target=send_request).start()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
