import json
import os
import time
from datetime import datetime, timezone
from urllib.parse import unquote

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "fifa-predictor-table")
TOURNAMENT = os.environ.get("TOURNAMENT", "FIFA2026")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("CORS_ORIGIN", "*"),
    "Access-Control-Allow-Headers": "content-type,authorization",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
}

OFFICIAL_RESULTS_TIMELINE = [
    {"slot":"R16-left-0", "winner":"CAN", "availableAt":"2026-06-29T23:30:00+05:30", "summary":"Canada advanced over South Africa"},
    {"slot":"R16-left-1", "winner":"PAR", "availableAt":"2026-06-30T04:00:00+05:30", "summary":"Paraguay advanced over Germany"},
    {"slot":"R16-left-2", "winner":"MAR", "availableAt":"2026-06-30T09:45:00+05:30", "summary":"Morocco advanced over Netherlands"},
    {"slot":"R16-left-3", "winner":"BRA", "availableAt":"2026-06-29T23:30:00+05:30", "summary":"Brazil advanced over Japan"},
    {"slot":"R16-left-4", "winner":"FRA", "availableAt":"2026-07-01T04:45:00+05:30", "summary":"France advanced over Sweden"},
    {"slot":"R16-left-5", "winner":"NOR", "availableAt":"2026-07-01T02:00:00+05:30", "summary":"Norway advanced over Ivory Coast"},
    {"slot":"R16-left-6", "winner":"MEX", "availableAt":"2026-07-01T10:45:00+05:30", "summary":"Mexico advanced over Ecuador"},
    {"slot":"R16-left-7", "winner":"ENG", "availableAt":"2026-07-02T00:15:00+05:30", "summary":"England advanced over DR Congo"},
    {"slot":"R16-right-0", "winner":"USA", "availableAt":"2026-07-02T08:45:00+05:30", "summary":"USA advanced over Bosnia and Herzegovina"},
    {"slot":"R16-right-1", "winner":"BEL", "availableAt":"2026-07-02T08:30:00+05:30", "summary":"Belgium advanced over Senegal"},
    {"slot":"R16-right-2", "winner":"POR", "availableAt":"2026-07-03T06:50:00+05:30", "summary":"Portugal advanced over Croatia"},
    {"slot":"R16-right-3", "winner":"ESP", "availableAt":"2026-07-03T02:44:00+05:30", "summary":"Spain advanced over Austria"},
    {"slot":"R16-right-4", "winner":"SUI", "availableAt":"2026-07-03T10:40:00+05:30", "summary":"Switzerland advanced over Algeria"},
    {"slot":"QF-left-0", "winner":"MAR", "availableAt":"2026-07-05T08:30:00+05:30", "summary":"Morocco advanced over Canada"},
    {"slot":"QF-left-1", "winner":"FRA", "availableAt":"2026-07-05T06:00:00+05:30", "summary":"France advanced over Paraguay"},
    {"slot":"QF-left-2", "winner":"NOR", "availableAt":"2026-07-06T08:30:00+05:30", "summary":"Norway advanced over Brazil"},
    {"slot":"QF-left-3", "winner":"ENG", "availableAt":"2026-07-06T10:30:00+05:30", "summary":"England advanced over Mexico"},
    {"slot":"QF-right-0", "winner":"BEL", "availableAt":"2026-07-07T08:30:00+05:30", "summary":"Belgium advanced over USA"},
    {"slot":"QF-right-1", "winner":"ESP", "availableAt":"2026-07-07T06:00:00+05:30", "summary":"Spain advanced over Portugal"},
    {"slot":"QF-right-2", "winner":"SUI", "availableAt":"2026-07-08T08:30:00+05:30", "summary":"Switzerland advanced over Colombia"},
    {"slot":"QF-right-3", "winner":"ARG", "availableAt":"2026-07-08T10:30:00+05:30", "summary":"Argentina advanced over Egypt"},
]


def response(status, body=None):
    return {"statusCode": status, "headers": CORS_HEADERS, "body": json.dumps(body or {}, default=str)}


def parse_body(event):
    return json.loads(event.get("body") or "{}")


def now_ms():
    return int(time.time() * 1000)


def user_pk(user_id):
    return f"USER#{user_id}"


def parse_dt(value):
    return datetime.fromisoformat(value)


def compute_official_results(now=None):
    now = now or datetime.now(timezone.utc).astimezone()
    selections = {}
    completed = []
    for item in OFFICIAL_RESULTS_TIMELINE:
        if now >= parse_dt(item["availableAt"]):
            selections[item["slot"]] = item["winner"]
            completed.append(item)
    return selections, completed


def put_user(user_id, display_name=None, color=None):
    item = {
        "pk": user_pk(user_id),
        "sk": "PROFILE",
        "userId": user_id,
        "displayName": display_name or user_id,
        "color": color or ("#00e5ff" if user_id == "FIFA 2026" else "#32d583"),
        "updatedAt": now_ms(),
    }
    table.put_item(Item=item)
    return item


def put_prediction(user_id, display_name, color, selections):
    put_user(user_id, display_name, color)
    item = {
        "pk": user_pk(user_id),
        "sk": f"PREDICTION#{TOURNAMENT}",
        "userId": user_id,
        "displayName": display_name or user_id,
        "color": color or ("#00e5ff" if user_id == "FIFA 2026" else "#32d583"),
        "tournament": TOURNAMENT,
        "selections": selections or {},
        "updatedAt": now_ms(),
    }
    table.put_item(Item=item)
    return item


def refresh_official_results():
    selections, completed = compute_official_results()
    item = put_prediction("FIFA 2026", "FIFA 2026", "#00e5ff", selections)
    item["completed"] = completed
    item["refreshedAt"] = datetime.now(timezone.utc).isoformat()
    return item


def get_prediction(user_id):
    result = table.get_item(Key={"pk": user_pk(user_id), "sk": f"PREDICTION#{TOURNAMENT}"})
    return result.get("Item")


def get_all_users_and_predictions(refresh_official=True):
    if refresh_official:
        refresh_official_results()
    scan = table.scan()
    items = scan.get("Items", [])
    while "LastEvaluatedKey" in scan:
        scan = table.scan(ExclusiveStartKey=scan["LastEvaluatedKey"])
        items.extend(scan.get("Items", []))

    users = {}
    for item in items:
        if item.get("sk") == "PROFILE":
            users[item["userId"]] = {"userId": item["userId"], "displayName": item.get("displayName", item["userId"]), "color": item.get("color", "#32d583"), "selections": {}}
    for item in items:
        if item.get("sk") == f"PREDICTION#{TOURNAMENT}":
            uid = item["userId"]
            users.setdefault(uid, {"userId": uid, "displayName": item.get("displayName", uid), "color": item.get("color", "#32d583"), "selections": {}})
            users[uid]["selections"] = item.get("selections", {})
            users[uid]["updatedAt"] = item.get("updatedAt")
    users.setdefault("Default User", {"userId":"Default User", "displayName":"Default User", "color":"#32d583", "selections":{}})
    users.setdefault("FIFA 2026", {"userId":"FIFA 2026", "displayName":"FIFA 2026", "color":"#00e5ff", "selections":refresh_official_results().get("selections", {})})
    return users


def score_user(selections, official):
    if not official:
        return 0
    keys = list(official.keys())
    return round(sum(1 for k in keys if selections.get(k) == official.get(k)) / len(keys) * 10, 1)


def leaderboard():
    users = get_all_users_and_predictions(refresh_official=True)
    official = users.get("FIFA 2026", {}).get("selections", {})
    rows = []
    for uid, user in users.items():
        if uid == "FIFA 2026":
            continue
        selections = user.get("selections", {})
        rows.append({"rank": 0, "userId": uid, "displayName": user.get("displayName", uid), "color": user.get("color"), "completedPicks": len(selections), "champion": selections.get("CHAMPION"), "score": score_user(selections, official), "updatedAt": user.get("updatedAt")})
    rows.sort(key=lambda r: (-r["score"], -r["completedPicks"], r["displayName"].lower()))
    for i, row in enumerate(rows, 1):
        row["rank"] = i
    return rows


def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod")
    path = (event.get("rawPath") or event.get("path") or "/").rstrip("/") or "/"
    if method == "OPTIONS":
        return response(204, {})
    try:
        if method == "GET" and path == "/health":
            return response(200, {"ok": True, "table": TABLE_NAME})
        if path == "/official-results/refresh" and method in ("GET", "POST"):
            official = refresh_official_results()
            return response(200, {"userId":"FIFA 2026", "selections": official.get("selections", {}), "completed": official.get("completed", []), "refreshedAt": official.get("refreshedAt")})
        if method == "PUT" and path == "/official-results":
            body = parse_body(event)
            item = put_prediction("FIFA 2026", "FIFA 2026", "#00e5ff", body.get("selections", {}))
            return response(200, item)
        if method == "GET" and path == "/state":
            official = refresh_official_results()
            return response(200, {"users": get_all_users_and_predictions(refresh_official=False), "leaderboard": leaderboard(), "officialResults": {"selections": official.get("selections", {}), "refreshedAt": official.get("refreshedAt")}})
        if method == "GET" and path == "/leaderboard":
            return response(200, {"leaderboard": leaderboard()})
        if method == "GET" and path == "/users":
            return response(200, {"users": list(get_all_users_and_predictions().values())})
        if method == "POST" and path == "/users":
            body = parse_body(event)
            user_id = body.get("userId") or body.get("displayName")
            if not user_id:
                return response(400, {"error":"userId is required"})
            if user_id == "FIFA 2026":
                return response(403, {"error":"FIFA 2026 is read-only"})
            return response(200, put_user(user_id, body.get("displayName"), body.get("color")))
        if path.startswith("/predictions/"):
            user_id = unquote(path.split("/predictions/", 1)[1])
            if method == "GET":
                if user_id == "FIFA 2026":
                    return response(200, refresh_official_results())
                return response(200, get_prediction(user_id) or {"userId":user_id, "selections":{}})
            if method == "POST":
                if user_id == "FIFA 2026":
                    return response(403, {"error":"FIFA 2026 is read-only. Use /official-results/refresh or PUT /official-results."})
                body = parse_body(event)
                return response(200, put_prediction(user_id, body.get("displayName", user_id), body.get("color"), body.get("selections", {})))
        return response(404, {"error":"not found", "method":method, "path":path})
    except Exception as exc:
        print("ERROR", repr(exc))
        return response(500, {"error": str(exc)})