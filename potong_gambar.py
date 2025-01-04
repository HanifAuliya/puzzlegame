from PIL import Image

# Membuka gambar
image = Image.open('image.jpg')  # Ganti 'image.jpg' dengan nama file gambar Anda

# Mendefinisikan jumlah kolom dan baris untuk potongan puzzle
rows = 2
columns = 3

# Mendapatkan ukuran gambar
img_width, img_height = image.size
piece_width = img_width // columns
piece_height = img_height // rows

# Memotong gambar menjadi 6 bagian
pieces = []
for row in range(rows):
    for col in range(columns):
        left = col * piece_width
        top = row * piece_height
        right = (col + 1) * piece_width
        bottom = (row + 1) * piece_height
        piece = image.crop((left, top, right, bottom))
        pieces.append(piece)
        piece.save(f"puzzle_piece_{row}_{col}.jpg")  # Menyimpan potongan gambar
