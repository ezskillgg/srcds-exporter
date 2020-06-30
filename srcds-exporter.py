#!/usr/bin/env python3
import valve.rcon
from flask import Flask, request, redirect
app = Flask(__name__)

fields_translate = {
    "CPU": "srcds_cpu",
    "NetIn": "srcds_netin",
    "NetOut": "srcds_netout",
    "Uptime": "srcds_uptime",
    "Maps": "srcds_maps",
    "FPS": "srcds_fps",
    "Players": "srcds_players",
    "Svms": "srcds_svms",
    "+-ms": "srcds_varms",
    "~tick": "srcds_tick",
}
fields_help = {
    "srcds_status": "server status",
    "srcds_cpu": "process niceness",
    "srcds_netin": "received traffic, kbps",
    "srcds_netout": "sent traffic, kbps",
    "srcds_uptime": "server uptime, minutes",
    "srcds_maps": "number of maps played on that server since it's start",
    "srcds_fps": "server's tick: 10 on idle",
    "srcds_players": "number of players",
    "srcds_svms": "ms per sim frame",
    "srcds_varms": "ms variance",
    "srcds_tick": "time in ms per tick"
}

@app.route('/')
def index():
    return redirect('/metrics')

@app.route('/metrics')
def metrics():
    host = request.args.get("ip")
    port = request.args.get("port")
    password = request.args.get("password")

    out = []
    out.append("#HELP srcds_status server status")
    out.append("#TYPE srcds_status gauge")

    try:
        raw_data = valve.rcon.execute((host,int(port)), password, "stats")
        (header, values) = raw_data.splitlines()
        header_fields = header.split()
        values_fields = values.split()
    except Exception:
        out.append("srcds_status 0")
        return "\n".join(out)
    
    i = 0

    out.append("srcds_status 1")
    while i < len(header_fields):
        f = fields_translate.get(header_fields[i])
        if not f:
            continue
        out.append("#HELP {} {}".format(f, fields_help[f]))
        out.append("#TYPE {} gauge".format(f))
        out.append("{} {}".format(f, values_fields[i]))
        i = i + 1
    
    return "\n".join(out)
    



if __name__ == '__main__':
    app.run(debug=False, port=9591, host='0.0.0.0')