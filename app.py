from flask import Flask, request, jsonify
from supabase import create_client
import os

app = Flask(__name__)

# =====================================================================
# CONFIGURATION: Just paste your Supabase Anon Key in the quotes below!
# =====================================================================
SUPABASE_URL = "https://cmuldpdmkengtdnuqbwg.supabase.co"
SUPABASE_KEY = "sb_publishable_gHCc75Jb7KecZFKZvuu_qg_lY17ql-6"

# This is your secret password for your HTML frontend to talk to this backend
OFFICIAL_CLIENT_TOKEN = "AI_FLOW_SECURE_TOKEN_2026"
# =====================================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend is live and running!"})

@app.route("/api/scan-card", methods=["POST"])
def scan_card():
    # 1. Verify the frontend password
    client_token = request.headers.get("X-Client-Token")
    if client_token != OFFICIAL_CLIENT_TOKEN:
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    # 2. Grab inputs
    data = request.json or {}
    class_code = data.get("class_code")
    math_email = data.get("math_email")
    math_password = data.get("math_password")

    if not class_code or not math_email or not math_password:
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    try:
        # 3. Connect and execute Supabase function safely
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        rpc_response = supabase.rpc("unbox_and_login_card", {
            "class_code": class_code,
            "math_email": math_email,
            "math_password": math_password
        }).execute()

        return jsonify(rpc_response.data)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
