import pygame
import random
import sys
import os
from pygame.locals import *
from random import shuffle

# Inisialisasi Pygame
pygame.init()

# Inisialisasi Mixer untuk audio
pygame.mixer.init()

# Ukuran layar
screen_width = 1200
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Puzzle Game')

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (100, 200, 255)
BUTTON_HOVER_COLOR = (50, 150, 255)
POPUP_BG_COLOR = (240, 240, 240)
TEXT_COLOR = (30, 30, 30)

#font
font = pygame.font.SysFont('Arial', 24)  # Inisialisasi font
header_font = pygame.font.SysFont('Arial', 32, bold=True)  # Font untuk header

def resource_path(relative_path):
    """ Dapatkan path ke resource, mendukung PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Muat suara efek tombol menggunakan resource_path
put_sound = pygame.mixer.Sound(resource_path('assets/put_sound.wav'))
button_sound = pygame.mixer.Sound(resource_path('assets/start_button.wav'))
yeay_sound = pygame.mixer.Sound(resource_path('assets/sound_yeay.wav'))
sad_sound = pygame.mixer.Sound(resource_path('assets/sound_sad.wav'))

# Muat file musik menggunakan resource_path
pygame.mixer.music.load(resource_path('assets/background_music.ogg'))

# Setel volume (opsional, 0.0 hingga 1.0)
pygame.mixer.music.set_volume(0.3)


# Mainkan musik latar belakang (loop tak terbatas)
pygame.mixer.music.play(-1)

# Memuat gambar yang akan digunakan di soal dari folder 'assets'
image1 = pygame.image.load(resource_path('assets/Picture1.jpg'))  # Aksi bocah SD
image2 = pygame.image.load(resource_path('assets/Picture2.jpg'))  # Koin untuk Aceh
image3 = pygame.image.load(resource_path('assets/Picture3.jpg'))  # Pemilu OSIS

# Puzzle pieces yang akan ditampilkan setelah selesai
puzzle_pieces = [
    pygame.transform.scale(pygame.image.load(resource_path('assets/puzzle_piece_0_0.jpg')), (200, 200)),
    pygame.transform.scale(pygame.image.load(resource_path('assets/puzzle_piece_0_1.jpg')), (200, 200)),
    pygame.transform.scale(pygame.image.load(resource_path('assets/puzzle_piece_0_2.jpg')), (200, 200)),
    pygame.transform.scale(pygame.image.load(resource_path('assets/puzzle_piece_1_0.jpg')), (200, 200)),
    pygame.transform.scale(pygame.image.load(resource_path('assets/puzzle_piece_1_1.jpg')), (200, 200)),
    pygame.transform.scale(pygame.image.load(resource_path('assets/puzzle_piece_1_2.jpg')), (200, 200))
]

# Posisi tetap untuk potongan puzzle (3 di atas, 3 di bawah)
puzzle_positions = [
    (100, 100),  # Puzzle 1
    (300, 100),  # Puzzle 2
    (500, 100),  # Puzzle 3
    (100, 300),  # Puzzle 4
    (300, 300),  # Puzzle 5
    (500, 300)   # Puzzle 6
]

# Pertanyaan dan jawaban
questions = [
    {"question": "Aksi seorang bocah SD di Pandawan, Kabupaten Hulu Sungai Tengah yang tetap berdiri mengikuti peringatan HUT RI meski teman-temannya ke luar barisan.", "image": image1, "correct_answer": 0},
    {"question": "Perbuatan Yang Mencerminkan Sikap Dan Suasana Kekeluargaan Dan Kegotongroyongan Adalah Merupakan Pengamalan Pancasila Yaitu Sila", "correct_answer": 1},
    {"question": "Peserta Didik Yang Rela Menyisihkan Uang Sakunya Untuk Membantu Meringankan Korban Bencana Merupakan Salah Satu Perbuatan Yang Mencerminkan Pengamalan Pancasila Yaitu Sila", "image": image2, "correct_answer": 2},
    {"question": "Mengembangkan Sikap Saling Menghormati Kebebasan Menjalankan Ibadah Sesuai Dengan Agama Dan Kepercayaannya Masing-Masing, Merupakan Nilai-Nilai Yang Terkandung Dalam Pancasila Yaitu Sila", "correct_answer": 3},
    {"question": "Dari Gambar Tersebut Menggambarkan Adanya Penerapan Nilai-Nilai Pancasila Yaitu Sila", "image": image3, "correct_answer": 4},
    {"question": "Pancasila Dijadikan Sebagai Pedoman Dalam Kehidupan Bermasyarakat, Berbangsa Dan Bernegara", "correct_answer": 5}
]

# Jawaban untuk tiap soal
answer_texts = [
    "Persatuan Indonesia",
    "Keadilan Sosial Bagi Seluruh Rakyat Indonesia",
    "Kemanuasiaan Yang Adil dan Beradab",
    "Ketuhanan Yang Maha Esa",
    "Kerakyatan yg dipimpin oleh Hikmah Kebijaksanaan dlm Permusyawaratan/Perwakilan",
    "Pancasila Sebagai Pandangan Hidup"
]

# Acak soal dan jawaban saat game mulai
shuffle(questions)

# Simpan jawaban yang dipilih oleh pemain
placed_answers = [None] * 6  # Menyimpan jawaban dari setiap soal

def wrap_text(text, font, max_width):
    """Membungkus teks jika terlalu panjang untuk kotak."""
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        # Cek apakah penambahan kata berikutnya akan melebihi lebar maksimum
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)  # Tambahkan baris terakhir
    return lines

# Jawaban sekarang berupa gambar dengan teks jawaban di dalamnya
answer_images = []
for i, text in enumerate(answer_texts):
    answer_img = pygame.Surface((200, 200))  # Kotak ukuran 200 x 200
    answer_img.fill(WHITE)
    pygame.draw.rect(answer_img, BLACK, (0, 0, 200, 200), 2)  # Border hitam
    
    # Bungkus teks menggunakan fungsi wrap_text yang sudah didefinisikan di atas
    wrapped_text = wrap_text(text, font, 170)  # max_width 170 untuk padding kiri-kanan
    
    # Hitung tinggi total dari teks yang dibungkus, misalnya tinggi tiap baris sekitar 25px
    total_text_height = len(wrapped_text) * 25  # Asumsi tinggi tiap baris teks 25px
    
    # Hitung posisi vertikal agar teks berada di tengah
    y_offset = (200 - total_text_height) // 2  # Sesuaikan teks agar berada di tengah vertikal
    
    # Render setiap baris teks yang sudah dibungkus
    for line in wrapped_text:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(100, y_offset))  # Rata tengah horizontal di x=100
        answer_img.blit(text_surface, text_rect)
        y_offset += 25  # Tambahkan jarak antar baris (lebih kecil dari 30 untuk lebih banyak ruang)
    
    answer_images.append(answer_img)

# Jawaban sekarang berupa gambar dengan teks, jadi kita shuffle urutannya
answers = list(range(len(answer_images)))
shuffle(answers)




# Ukuran potongan puzzle diperbesar agar lebih sesuai dan lebih rapat
piece_width = 200
piece_height = 200
gap = 2  # Jarak antar border agar puzzle tampak lebih rapat

# Posisi puzzle grid (untuk soal)
puzzle_positions = [(50, 100), (252, 100), (454, 100),
                    (50, 302), (252, 302), (454, 302)]

# Posisi jawaban (susunan di bawah puzzle, ke-6 jawaban)
answer_positions = [(50, 540), (300, 540), (550, 540),
                    (800, 540), (800, 320), (800, 100)]

# Status pop-up
show_popup = False
popup_question = None
popup_image = None
dragging = False  # Apakah sedang melakukan drag-and-drop
drag_index = None  # Index dari jawaban yang sedang di-drag
drag_offset = (0, 0)

# Fungsi untuk memeriksa apakah semua jawaban sudah terisi
def check_all_answers_filled(placed_answers):
    return all(answer is not None for answer in placed_answers)

# Fungsi untuk menampilkan teks di layar
def draw_text(text, font, color, surface, x, y):
    """Render dan tampilkan teks di layar pada posisi x, y."""
    text_obj = font.render(text, True, color)  # Pastikan font sudah diinisialisasi
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Fungsi untuk menampilkan pop-up soal dengan gambar di atas dan teks di bawah
def draw_popup(question, image=None):
    # Pop-up positioning
    popup_rect = pygame.Rect(screen_width // 4, screen_height // 4, screen_width // 2, screen_height // 2)
    
    # Draw rounded popup with shadow effect
    pygame.draw.rect(screen, (50, 50, 50), popup_rect.move(5, 5), border_radius=20)  # Shadow
    pygame.draw.rect(screen, POPUP_BG_COLOR, popup_rect, border_radius=20)  # Pop-up background
    pygame.draw.rect(screen, BLACK, popup_rect, 5, border_radius=20)  # Pop-up border
    
    # If an image is provided, display it above the question
    if image:
        image_rect = pygame.Rect(screen_width // 2 - 150, screen_height // 4 + 20, 300, 200)
        screen.blit(pygame.transform.scale(image, image_rect.size), image_rect)
        text_y_position = image_rect.bottom + 20
    else:
        text_y_position = screen_height // 4 + 50
    
    # Display question text, ensure it wraps within the popup
    wrapped_text = wrap_text(question, font, popup_rect.width - 30)  # 20 px padding on both sides
    for i, line in enumerate(wrapped_text):
        draw_text(line, font, TEXT_COLOR, screen, popup_rect.centerx, text_y_position + i * 30)

    # Geser tombol lebih ke bawah dengan menambah lebih banyak jarak dari bottom
    button_y_position = popup_rect.bottom - 60  # Geser tombol ke bawah lebih dari posisi sebelumnya

    # Draw the modern button with rounded corners and hover effect
    draw_modern_button(screen, "Tutup", popup_rect.centerx - 50, button_y_position, 100, 50, close_popup)


def wrap_text(text, font, max_width):
    """Wrap text based on the max width to prevent overflowing."""
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)  # Add the last line
    return lines

def draw_modern_button(screen, text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    # Button colors
    BUTTON_COLOR = (30, 144, 255)
    BUTTON_HOVER_COLOR = (100, 149, 237)
    BUTTON_TEXT_COLOR = WHITE

    # Check if the mouse is hovering over the button
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height), border_radius=10)
        if click[0] == 1 and action is not None:
            button_sound.play()
            action()  # Perform the action when clicked
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height), border_radius=10)

    # Draw button text
    draw_text(text, font, BUTTON_TEXT_COLOR, screen, x + width // 2, y + height // 2)

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text centered at x, y."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


# Fungsi untuk membuat tombol dengan efek hover
def draw_button(surface, text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            button_sound.play()
            pygame.time.delay(200)  # Delay 200 milidetik (0,2 detik)
            action()
    else:
        pygame.draw.rect(surface, color, (x, y, width, height))

    draw_text(text, font, BLACK, surface, x + width // 2, y + height // 2)

# Fungsi untuk menutup pop-up
def close_popup():
    global show_popup
    show_popup = False

    
def quit_game():
    sys.exit()  # Keluar dari program

# Fungsi untuk menangani drag and drop dengan mekanisme tahan dan lepas
def handle_dragging(event, answers, placed_answers, score, correct, incorrect):
    global dragging, drag_index, drag_offset
    cursor_changed = False  # Flag untuk memastikan kursor berubah saat dibutuhkan

    if event.type == MOUSEBUTTONDOWN:
        # Cek apakah sedang mendrag jawaban (klik jawaban terlebih dahulu)
        for i, pos in enumerate(answer_positions):
            answer_rect = pygame.Rect(pos[0], pos[1], piece_width, piece_height)
            if answer_rect.collidepoint(event.pos) and answers[i] is not None:  # Klik pada jawaban
                dragging = True
                drag_index = i
                drag_offset = (answer_positions[i][0] - event.pos[0], answer_positions[i][1] - event.pos[1])
                return score, correct, incorrect  # Keluar dari fungsi setelah mendeteksi klik pada jawaban

        # Jika tidak mendrag jawaban, baru cek puzzle
        if not dragging:  # Hanya buka popup jika tidak sedang mendrag jawaban
            for i, pos in enumerate(puzzle_positions):
                puzzle_rect = pygame.Rect(pos[0], pos[1], piece_width, piece_height)

                # Cek apakah ada jawaban yang berada di atas puzzle ini
                jawaban_di_atas_puzzle = False
                for j, jawaban_pos in enumerate(answer_positions):
                    answer_rect = pygame.Rect(jawaban_pos[0], jawaban_pos[1], piece_width, piece_height)
                    if answer_rect.collidepoint(puzzle_rect.center) and answers[j] is not None:
                        jawaban_di_atas_puzzle = True  # Ada jawaban di atas puzzle, abaikan klik
                        break

                # Hanya buka pop-up jika tidak ada jawaban di atas puzzle
                if puzzle_rect.collidepoint(event.pos) and placed_answers[i] is None and not jawaban_di_atas_puzzle:
                    show_popup = True
                    popup_question = questions[i]["question"]
                    popup_image = questions[i].get("image", None)
                    return score, correct, incorrect

    elif event.type == MOUSEBUTTONUP and dragging:
        for i, pos in enumerate(puzzle_positions):
            puzzle_rect = pygame.Rect(pos[0], pos[1], piece_width, piece_height)
            if puzzle_rect.collidepoint(event.pos) and placed_answers[i] is None:  # Jika tempat belum diisi
                placed_answers[i] = answers[drag_index]  # Letakkan jawaban di tempat
                put_sound.play()  # Mainkan suara saat jawaban dilepaskan
                if answers[drag_index] == questions[i]["correct_answer"]:  # Jika jawaban benar
                    score += 100 / len(questions)  # Tambahkan poin untuk jawaban yang benar
                    correct += 1
                else:
                    incorrect += 1
                answers[drag_index] = None  # Hapus jawaban dari posisi awal
        dragging = False  # Akhiri drag
        drag_index = None

    elif event.type == MOUSEMOTION:
        # Cek apakah mouse berada di atas jawaban
        for i, pos in enumerate(answer_positions):
            answer_rect = pygame.Rect(pos[0], pos[1], piece_width, piece_height)
            if answer_rect.collidepoint(event.pos) and answers[i] is not None:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Ubah kursor menjadi pointer
                cursor_changed = True
                break
        
        # Cek apakah mouse berada di atas puzzle yang belum diisi
        if not cursor_changed:  # Jika kursor belum berubah, cek puzzle
            for i, pos in enumerate(puzzle_positions):
                puzzle_rect = pygame.Rect(pos[0], pos[1], piece_width, piece_height)
                if puzzle_rect.collidepoint(event.pos) and placed_answers[i] is None:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Ubah kursor menjadi pointer
                    cursor_changed = True
                    break

        # Pindahkan posisi jawaban sesuai pergerakan mouse saat dragging
        if dragging:
            answer_positions[drag_index] = (event.pos[0] + drag_offset[0], event.pos[1] + drag_offset[1])

    # Jika tidak ada kursor yang diubah, kembalikan ke kursor default
    if not cursor_changed:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Ubah kursor kembali ke default

    return score, correct, incorrect

# Fungsi untuk menyelesaikan permainan, menampilkan gambar puzzle, lalu menampilkan skor
def finish_game(score, correct, incorrect, placed_answers):
    screen.fill(WHITE)

    # Pastikan placed_answers berisi jawaban untuk semua puzzle (0-5)
    assert len(placed_answers) == 6, "Jumlah jawaban yang ditempatkan tidak sesuai!"

    # Lacak gambar yang sudah digunakan
    used_pieces = set()

    # Step 1: Tempatkan gambar untuk jawaban yang benar
    for i, pos in enumerate(puzzle_positions):
        if placed_answers[i] == questions[i]['correct_answer']:
            # Tampilkan gambar sesuai dengan index puzzle (gambar benar untuk jawaban benar)
            screen.blit(puzzle_pieces[i], (pos[0], pos[1]))
            used_pieces.add(i)  # Tandai gambar ini sebagai sudah digunakan

    # Step 2: Tempatkan gambar untuk jawaban yang salah, secara acak tapi tidak boleh sama dengan indeks puzzle
    wrong_positions = [i for i in range(len(puzzle_positions)) if placed_answers[i] != questions[i]['correct_answer']]

    # Ambil gambar yang belum digunakan, dan pastikan mereka tidak sesuai dengan posisi puzzle yang salah
    available_pieces = [j for j in range(len(puzzle_pieces)) if j not in used_pieces]

   # Pastikan bahwa setiap gambar di available_pieces digunakan
    for i in wrong_positions:
        if available_pieces:
            # Ambil gambar acak dari available_pieces yang tidak sesuai dengan indeks puzzle
            valid_pieces = [j for j in available_pieces if j != i]
            if valid_pieces:  # Pastikan masih ada gambar yang valid untuk dipilih
                wrong_piece_index = random.choice(valid_pieces)
                screen.blit(puzzle_pieces[wrong_piece_index], puzzle_positions[i])  # Tempatkan di posisi salah
                used_pieces.add(wrong_piece_index)  # Tandai gambar ini sebagai sudah digunakan
                available_pieces.remove(wrong_piece_index)  # Hapus gambar yang sudah dipakai dari daftar
            else:
                # Jika tidak ada gambar yang valid, tampilkan pesan "Coba lagi, kamu salah"
                pygame.draw.rect(screen, WHITE, (puzzle_positions[i][0], puzzle_positions[i][1], piece_width, piece_height))
                pygame.draw.rect(screen, BLACK, (puzzle_positions[i][0], puzzle_positions[i][1], piece_width, piece_height), 2)
                draw_text("Coba lagi, kamu salah", font, BLACK, screen, puzzle_positions[i][0] + piece_width // 2, puzzle_positions[i][1] + piece_height // 2)
        else:
            # Jika tidak ada lagi gambar yang tersisa, tampilkan pesan "Coba lagi, kamu salah"
            pygame.draw.rect(screen, WHITE, (puzzle_positions[i][0], puzzle_positions[i][1], piece_width, piece_height))
            pygame.draw.rect(screen, BLACK, (puzzle_positions[i][0], puzzle_positions[i][1], piece_width, piece_height), 2)
            draw_text("Coba lagi, kamu salah", font, BLACK, screen, puzzle_positions[i][0] + piece_width // 2, puzzle_positions[i][1] + piece_height // 2)

    pygame.display.update()
    pygame.time.delay(3000)  # Tampilkan hasil puzzle selama 3 detik

    # Mainkan suara berdasarkan jumlah jawaban benar
    if correct >= 5:
        yeay_sound.play()  # Jika jawaban benar >= 5, mainkan suara 'yeay'
    else:
        sad_sound.play()  # Jika jawaban benar < 5, mainkan suara 'sad'

    # Tampilkan skor di sisi kanan layar
    right_offset = 250
    draw_text(f"Skor Anda: {int(score)}", header_font, BLACK, screen, screen_width - right_offset, screen_height // 2 - 100)
    draw_text(f"Jawaban benar: {correct}", font, BLACK, screen, screen_width - right_offset, screen_height // 2 - 50)
    draw_text(f"Jawaban salah: {incorrect}", font, BLACK, screen, screen_width - right_offset, screen_height // 2)

    # Update display setelah menampilkan skor
    pygame.display.update()
    
    # Game loop untuk menampilkan tombol "Keluar"
    running = True
    while running:
        draw_button(screen, "Keluar", screen_width - right_offset - 50, screen_height // 2 + 50, 100, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, main_menu)
        pygame.display.update()

         # Event handling for quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()  # Pastikan aplikasi keluar

    # Kembali ke menu utama setelah selesai
    main_menu()

def main_menu():
    global placed_answers, score, correct, incorrect, show_popup, popup_question, popup_image, answers

    # Reset variabel permainan saat kembali ke menu utama
    placed_answers = [None] * 6  # Reset jawaban yang ditempatkan
    score = 0                     # Reset skor
    correct = 0                   # Reset jumlah jawaban benar
    incorrect = 0                 # Reset jumlah jawaban salah
    show_popup = False            # Reset status popup
    popup_question = None         # Reset pertanyaan di popup
    popup_image = None            # Reset gambar di popup
    answers = list(range(6))      # Reset jawaban yang tersedia

    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Main Menu", header_font, BLACK, screen, screen_width // 2, screen_height // 2 - 100)
        draw_button(screen, "Mulai", screen_width // 2 - 50, screen_height // 2, 100, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, game_loop)
        draw_button(screen, "Keluar", screen_width // 2 - 50, screen_height // 2 + 100, 100, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, quit_game)

        # Event handling for quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()  # Pastikan aplikasi keluar

        pygame.display.update()



# Loop utama game
def game_loop():
    global show_popup, popup_question, popup_image, answer_positions
    clock = pygame.time.Clock()

    # Reset variabel permainan
    placed_answers = [None] * 6  # Reset jawaban yang ditempatkan
    score = 0                     # Reset skor
    correct = 0                   # Reset jumlah jawaban benar
    incorrect = 0                 # Reset jumlah jawaban salah
    show_popup = False            # Tutup popup
    popup_question = None         # Reset pertanyaan di popup
    popup_image = None            # Reset gambar di popup

    # Acak soal dan jawaban saat game mulai
    shuffle(questions)
    # Reset posisi jawaban ke posisi awalnya
    answer_positions = [(50, 540), (300, 540), (550, 540),
                        (800, 540), (800, 320), (800, 100)]

    running = True

    while running:
        screen.fill(WHITE)

        # Tampilkan instruksi permainan di bagian atas layar
        draw_text("Objektif: Pasangkan gambar dengan benar berdasarkan soal yang diberikan!", font, BLACK, screen, screen_width // 2, 30)
        draw_text("Mekanisme: Klik puzzle untuk melihat soal ,Kemudian drag dan drop gambar ke kotak yang sesuai.", font, BLACK, screen, screen_width // 2, 60)

        # Tampilkan grid puzzle dan jawaban
        for i, pos in enumerate(puzzle_positions):
            pygame.draw.rect(screen, BLACK, (pos[0], pos[1], piece_width, piece_height), 2)
            if placed_answers[i] is None:
                draw_text(str(i + 1), font, BLACK, screen, pos[0] + piece_width // 2, pos[1] + piece_height // 2)
            else:
                screen.blit(answer_images[placed_answers[i]], (pos[0], pos[1]))

        for i, pos in enumerate(answer_positions):
            if answers[i] is not None:
                screen.blit(answer_images[answers[i]], (pos[0], pos[1]))

        # Tampilkan pop-up jika aktif
        if show_popup:
            draw_popup(popup_question, popup_image)

        # Event handling
        for event in pygame.event.get():
            # Event handling for quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()  # Pastikan aplikasi keluar
            elif event.type == MOUSEBUTTONDOWN and not show_popup:
                for i, pos in enumerate(puzzle_positions):
                    puzzle_rect = pygame.Rect(pos[0], pos[1], piece_width, piece_height)
                    if puzzle_rect.collidepoint(event.pos) and placed_answers[i] is None:
                        show_popup = True
                        popup_question = questions[i]["question"]
                        popup_image = questions[i].get("image", None)
            elif event.type == MOUSEBUTTONDOWN and show_popup:
                close_rect = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 150, 100, 50)
                if close_rect.collidepoint(event.pos):
                    close_popup()

            if not show_popup:
                score, correct, incorrect = handle_dragging(event, answers, placed_answers, score, correct, incorrect)

        if check_all_answers_filled(placed_answers):
            pygame.time.delay(1000)
            finish_game(score, correct, incorrect, placed_answers)
            running = False

        
        pygame.display.update()
        clock.tick(30)


# Panggil menu utama saat game dimulai
main_menu()
