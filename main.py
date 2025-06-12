from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
PORT = int(os.getenv('PORT', 5000))

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor, sslmode='require')
    return conn

# ========================================
# 1️⃣ CREATE RESEP
# ========================================
@app.route('/api/resep', methods=['POST'])
def create_resep():
    data = request.get_json()
    user_email = data.get('user_email')
    nama = data.get('nama')
    deskripsi = data.get('deskripsi', '')
    kategori = data.get('kategori', '')
    image_id = data.get('image_id')
    delete_hash = data.get('delete_hash')

    if not all([user_email, nama, image_id, delete_hash]):
        return jsonify({'error': 'Field wajib: user_email, nama, image_id, delete_hash'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO resep (user_email, nama, deskripsi, kategori, image_id, delete_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (user_email, nama, deskripsi, kategori, image_id, delete_hash))
        new_resep = cur.fetchone()
        conn.commit()
        return jsonify({'message': 'Resep berhasil ditambahkan', 'resep': new_resep}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ========================================
# 2️⃣ READ ALL RESEP
# ========================================
@app.route('/api/resep', methods=['GET'])
def get_all_resep():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM resep ORDER BY created_at DESC;")
        resep_list = cur.fetchall()
        return jsonify(resep_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ========================================
# 3️⃣ READ SINGLE RESEP
# ========================================
@app.route('/api/resep/<int:recipe_id>', methods=['GET'])
def get_resep(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM resep WHERE recipe_id = %s;", (recipe_id,))
        resep = cur.fetchone()
        if resep:
            return jsonify(resep)
        else:
            return jsonify({'error': 'Resep tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ========================================
# 4️⃣ UPDATE RESEP
# ========================================
@app.route('/api/resep/<int:recipe_id>', methods=['PUT'])
def update_resep(recipe_id):
    data = request.get_json()
    user_email = data.get('user_email')
    nama = data.get('nama')
    deskripsi = data.get('deskripsi', '')
    kategori = data.get('kategori', '')
    image_id = data.get('image_id')
    delete_hash = data.get('delete_hash')

    if not all([user_email, nama, image_id, delete_hash]):
        return jsonify({'error': 'Field wajib: user_email, nama, image_id, delete_hash'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE resep
            SET user_email = %s, nama = %s, deskripsi = %s, kategori = %s, image_id = %s, delete_hash = %s
            WHERE recipe_id = %s
            RETURNING *;
        """, (user_email, nama, deskripsi, kategori, image_id, delete_hash, recipe_id))
        updated_resep = cur.fetchone()
        conn.commit()
        if updated_resep:
            return jsonify({'message': 'Resep berhasil diperbarui', 'resep': updated_resep})
        else:
            return jsonify({'error': 'Resep tidak ditemukan'}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ========================================
# 5️⃣ DELETE RESEP
# ========================================
@app.route('/api/resep/<int:recipe_id>', methods=['DELETE'])
def delete_resep(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM resep WHERE recipe_id = %s RETURNING *;", (recipe_id,))
        deleted_resep = cur.fetchone()
        conn.commit()
        if deleted_resep:
            return jsonify({'message': 'Resep berhasil dihapus', 'resep': deleted_resep})
        else:
            return jsonify({'error': 'Resep tidak ditemukan'}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ========================================
# 6️⃣ (Opsional) READ RECIPE_DATA (untuk tampilan ringkas)
# ========================================
@app.route('/api/recipe_data', methods=['GET'])
def get_all_recipe_data():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM recipe_data;")
        recipe_data_list = cur.fetchall()
        return jsonify(recipe_data_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
