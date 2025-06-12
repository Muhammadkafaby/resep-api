# Resep API

API ini menyediakan endpoint RESTful untuk mengelola data resep makanan menggunakan Flask dan PostgreSQL. Anda dapat melakukan operasi CRUD (Create, Read, Update, Delete) pada data resep melalui endpoint yang tersedia.

## Base URL

```
https://resep-api-849c0e113bf0.herokuapp.com
```

## Daftar Endpoint

### 1. Create Resep

- **URL:** `/api/resep`
- **Method:** `POST`
- **Body JSON:**
  - user_email (wajib)
  - nama (wajib)
  - deskripsi (opsional)
  - kategori (opsional)
  - image_id (wajib)
  - delete_hash (wajib)
- **Contoh Body:**
  ```json
  {
    "user_email": "user@email.com",
    "nama": "Nasi Goreng",
    "deskripsi": "Enak dan mudah",
    "kategori": "Makanan",
    "image_id": "img123",
    "delete_hash": "delhash123"
  }
  ```
- **Response:** 201 Created, data resep yang baru

### 2. Get Semua Resep

- **URL:** `/api/resep`
- **Method:** `GET`
- **Response:** 200 OK, list resep

### 3. Get Resep Berdasarkan ID

- **URL:** `/api/resep/<recipe_id>`
- **Method:** `GET`
- **Response:**
  - 200 OK, data resep
  - 404 Not Found jika tidak ditemukan

### 4. Update Resep

- **URL:** `/api/resep/<recipe_id>`
- **Method:** `PUT`
- **Body JSON:** sama seperti Create
- **Response:**
  - 200 OK, data resep yang diperbarui
  - 404 Not Found jika tidak ditemukan

### 5. Delete Resep

- **URL:** `/api/resep/<recipe_id>`
- **Method:** `DELETE`
- **Response:**
  - 200 OK, data resep yang dihapus
  - 404 Not Found jika tidak ditemukan

### 6. Get Semua Recipe Data (Opsional)

Digunakan untuk mengambil data ringkas dari tabel `recipe_data`.

- **URL:** `/api/recipe_data`
- **Method:** `GET`
- **Response:** 200 OK, list recipe_data

## Environment Variable

- `DATABASE_URL`: URL koneksi PostgreSQL
- `PORT`: Port aplikasi (default 5000)

## Menjalankan Lokal

1. Install dependensi:
   ```
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi:
   ```
   python main.py
   ```

## Deploy ke Heroku

1. Pastikan file `Procfile` dan `requirements.txt` sudah sesuai.
2. Deploy dengan perintah:
   ```
   git add .
   git commit -m "deploy"
   git push heroku master
   ```

## Testing dengan Postman

Tersedia file koleksi Postman (`Resep-API.postman_collection.json`) yang dapat diimpor ke Postman untuk mencoba seluruh endpoint.

---

Untuk pertanyaan lebih lanjut, silakan hubungi pengembang.
