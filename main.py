import os
import logging
from dotenv import load_dotenv
from kite import gen_acc_token
from kiteconnect import KiteConnect, KiteTicker
load_dotenv()

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# access_token = gen_acc_token()
kws = KiteTicker(os.environ.get('KITE_API_KEY'), 'dyQq2ZDD2ws0ogKRGLOc68FXbegxLeDP')

@app.websocket("/ws/feed")
def websocket_endpoint(websocket: WebSocket):
    def on_ticks(ws, ticks):
        # Callback to receive ticks.
        print(("Ticks: {}".format(ticks)))
        websocket.send_json({ 'message': str(ticks) })
        # websocket.send_json(ticks)

    def on_connect(ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe([63061511])

        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_FULL, [63061511])

    def on_close(ws, code, reason):
        # On connection close stop the main loop
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    websocket.accept()

    for i in range(10):
        websocket.send_json({'message': i})
    # kws.on_ticks = on_ticks
    # kws.on_connect = on_connect
    # kws.on_close = on_close
    # kws.connect()

    while True:
        pass
        # data = await websocket.receive_text()
        # await websocket.send_text(f"Message text was: {data}")

app.mount("/", StaticFiles(directory="static", html=True), name="static")