import json, os, time, requests, pymysql
from flask import Flask, jsonify, request
from jose import jwt

ISSUER = os.getenv("OIDC_ISSUER", "http://authentication-identity-server:8080/realms/master")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "myapp")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
_JWKS, _TS = None, 0


def get_jwks():
    global _JWKS, _TS
    if not _JWKS or time.time() - _TS > 600:
        _JWKS = requests.get(JWKS_URL, timeout=5).json()
        _TS = time.time()
    return _JWKS


app = Flask(__name__)


@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")


@app.get("/student")
def student():
    with open("students.json") as f:
        return jsonify(json.load(f))


@app.get("/students-db")
def students_db():
    conn = pymysql.connect(
        host="relational-database-server", user="root", password="root",
        database="studentdb", cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
    conn.close()
    for r in rows:
        r["dob"] = str(r["dob"])
    return jsonify(rows)


@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    try:
        payload = jwt.decode(auth.split(" ", 1)[1], get_jwks(),
                             algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
        return jsonify(message="Secure resource OK",
                       preferred_username=payload.get("preferred_username"))
    except Exception as e:
        return jsonify(error=str(e)), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
