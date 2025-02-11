import os
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)
app.name = "UDA_FLASK_APP"

# File database lisensi (pakai JSON biar simpel)
LICENSE_DB = "licenses.json"

# Jika database belum ada, buat default
if not os.path.exists(LICENSE_DB):
    with open(LICENSE_DB, "w") as f:
        json.dump({}, f)

# Fungsi baca database
def load_db():
    with open(LICENSE_DB, "r") as f:
        return json.load(f)

# Fungsi simpan database
def save_db(data):
    with open(LICENSE_DB, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/register', methods=['POST'])
def register_key():
    """Registrasi key ke device"""
    data = request.json
    key = data.get("key")
    device_id = data.get("device_id")
    expired_time = time.time() + (30 * 24 * 60 * 60)  # Expired dalam 30 hari

    db = load_db()
    
    if key in db:
        return jsonify({"status": "error", "message": "Key sudah terdaftar!"})

    db[key] = {"device_id": device_id, "expired": expired_time}
    save_db(db)
    
    return jsonify({"status": "success", "message": "Key berhasil didaftarkan!", "expired": expired_time})

@app.route('/verify', methods=['GET'])
def verify_key():
    """Verifikasi key lisensi"""
    key = request.args.get('key')
    device_id = request.args.get('device_id')

    db = load_db()

    if key not in db:
        return jsonify({"status": "error", "message": "Key tidak valid!"})

    if db[key]["device_id"] != device_id:
        return jsonify({"status": "error", "message": "Key sudah digunakan di device lain!"})

    if time.time() > db[key]["expired"]:
        return jsonify({"status": "error", "message": "Key sudah expired!"})

    return jsonify({"status": "success", "message": "Key valid dan aktif!"})

if __name__ == '__main__':
    print(f"🚀 {app.name} berjalan di port 5000...")
    app.run(host='0.0.0.0', port=5000)