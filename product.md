Buatkan saya FEATURE endpoint API PRODUCT untuk proses CRUD dengan ketentuan berikut:

1. endpoint meliputi operasi create, read, update dan delete

2. buatkan endpoint CRUD di dalam file api/product.py

3. gunakan database yang sudah ada yaitu fastapi_sqlalchemy_crud_db

4. gunakan tabel yang sudah saya buatkan di dalam database tersebut dan sudah saling berelasi yaitu: brands, categories, products

5. untuk koneksi ke database gunakan yang sudah ada di file config/db.py

6. buatkan model-nya di dalam file models/product.py kemudian import ke dalam file models/index.py

7. buatkan schema-nya di dalam file schemas/product.py kemudian import ke dalam file schemas/index.py

8. ketentuan endpoint untuk masing-masing operasi (create, read, update dan delete) sebagai berikut:
   - POST: /api/product
   {
	"name": "Frozen Food",
	"brand_id": 1,
	"category_id": 1,
	"image": "assets/images/image.jpg",
	"qty": 100,
	"price": 12000.00
   }

   - GET ALL: /api/products
   {
	"name": "Frozen Food Rasa Ayam Gulai",
	"brand_id": 1,
	"category_id": 1,
	"image": "assets/images/image.jpg",
	"qty": 100,
	"price": 12000.00,
	"brand: {
	   "id": 1,
           "name": "CIDEA"
	},
	"category": {
	   "id": 1,
           "name": "FROZEN"
	}
   }

   - GET by id: /api/product/1

   - DELETE: /api/product/1

   - PUT: api/product/1
   {
	"name": "Frozen Food Rasa Ayam Gulai",
	"brand_id": 1,
	"category_id": 1,
	"image": "assets/images/image.jpg",
	"qty": 100,
	"price": 12000.00,
   }

9. gunakan token saat menjalankan endpoint untuk operasi create, read, update dan delete 
   - fungsi untuk pemeriksaan token login user sudah dibuatkan ada di dalam file middleware/auth.py

FEATURE LAIN:
1. Buatkan unit test product di dalam file test/test_product_api.py untuk masing-masing operasi CRUD