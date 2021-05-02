import websocket, requests, subprocess, os, time, json, sys

def eval_js(wsock, js):
    data = json.dumps({
        "id": 1337,
        "method": "Runtime.evaluate",
        "params": {
            "contextId": 1,
            "includeCommandLineAPI": True,
            "generatePreview": False,
            "objectGroup": "console",
            "expression": js,
            "returnByValue": False,
            "userGesture": True
        }
    })
    wsock.send(data)
    return wsock.recv()

p = subprocess.Popen([os.environ["LOCALAPPDATA"] + r"\Programs\cb-exam-player\2021 Digital AP Exams.exe", "--inspect=31337", "--remote-debugging-port=42069"])
node_url = requests.get("http://localhost:31337/json").json()[0]["webSocketDebuggerUrl"]
ws_node = websocket.create_connection(node_url)

print("Waiting for webapp to launch...")
while True:
    if "electron.stp-prod.collegeboard.org" in eval_js(ws_node, 'require("electron").BrowserWindow.getAllWindows()[0].webContents.getURL()'):
        break
    
    time.sleep(1)

page_url = requests.get("http://localhost:42069/json").json()[0]["webSocketDebuggerUrl"]
ws_page = websocket.create_connection(page_url)

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
elif __file__:
    app_path = os.path.dirname(os.path.abspath(__file__))

print(app_path)
print("Injecting scripts...")
inject_node = open(app_path + "/inject_node.js", "r").read()
inject_page = open(app_path + "/inject_page.js", "r").read()
eval_js(ws_node, inject_node)
eval_js(ws_page, inject_page)
print("Done! Press Ctrl-C to exit testing app")

try:
    p.wait()
except KeyboardInterrupt:
    pass
