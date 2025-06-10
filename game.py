from tkinter import *
import random
import os

# === Setup Window ===
root = Tk()
root.title("Trash Catcher Game")
root.resizable(False, False)

canvas_width = 400
canvas_height = 400
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='skyblue')
canvas.pack()

# === Load Gambar Sampah ===
trash_images = [
    PhotoImage(file="kaleng.png"),
    PhotoImage(file="paprika.png"),
    PhotoImage(file="cone.png"),
    PhotoImage(file="kertas.png"),
    PhotoImage(file="ikan.png"),
]

# Untuk menyimpan referensi gambar aktif
active_egg_images = []

# === Load Gambar Tong Sampah ===
basket_img = PhotoImage(file="tong_sampah.png")

# === Fungsi High Score ===
def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(new_high_score):
    with open("highscore.txt", "w") as f:
        f.write(str(new_high_score))

# === Tanah ===
canvas.create_rectangle(0, canvas_height - 30, canvas_width, canvas_height, fill='lightgreen')

# === Game Variables ===
basket = None
score = 0
lives = 3
high_score = load_high_score()
eggs = []
egg_speed = 5
egg_interval = 2000
game_over_text = None
play_again_button = None

# === UI Text ===
score_text = canvas.create_text(10, 10, anchor='nw', font=('Arial', 14), fill='black', text="")
lives_text = canvas.create_text(300, 10, anchor='nw', font=('Arial', 14), fill='black', text="")
high_score_text = canvas.create_text(150, 10, anchor='nw', font=('Arial', 14), fill='black', text=f"High Score: {high_score}")

# === Fungsi Game ===
def start_game():
    global score, lives, basket, eggs, game_over_text, play_again_button, active_egg_images

    # Reset
    score = 0
    lives = 3
    eggs.clear()
    active_egg_images.clear()
    canvas.delete("egg")
    canvas.itemconfigure(score_text, text=f"Score: {score}")
    canvas.itemconfigure(lives_text, text=f"Lives: {lives}")

    # Buat ulang keranjang
    if basket:
        canvas.delete(basket)
    basket_x = canvas_width // 2
    basket_y = canvas_height - 50
    basket = canvas.create_image(basket_x, basket_y, image=basket_img, anchor='n')

    # Hapus Game Over dan tombol
    if game_over_text:
        canvas.delete(game_over_text)
        game_over_text = None
    if play_again_button:
        play_again_button.destroy()
        play_again_button = None

    # Jalankan game
    create_egg()
    move_eggs()
    canvas.bind_all("<Left>", move_left)
    canvas.bind_all("<Right>", move_right)

def create_egg():
    if lives > 0:
        x = random.randint(10, canvas_width - 30)
        img = random.choice(trash_images)
        egg = canvas.create_image(x + 10, 10, image=img, anchor='n', tags="egg")
        eggs.append(egg)
        active_egg_images.append(img)  # Simpan referensi image
        root.after(egg_interval, create_egg)

def move_eggs():
    if lives == 0:
        return
    for egg in eggs[:]:
        canvas.move(egg, 0, egg_speed)
        egg_pos = canvas.bbox(egg)
        basket_pos = canvas.bbox(basket)

        if egg_pos and egg_pos[3] >= canvas_height - 30:
            idx = eggs.index(egg)
            eggs.remove(egg)
            canvas.delete(egg)
            del active_egg_images[idx]
            lose_life()
        elif egg_pos and basket_pos and (basket_pos[0] < egg_pos[0] < basket_pos[2]) and (basket_pos[1] < egg_pos[3] < basket_pos[3]):
            idx = eggs.index(egg)
            eggs.remove(egg)
            canvas.delete(egg)
            del active_egg_images[idx]
            increase_score()
    root.after(50, move_eggs)

def increase_score():
    global score, high_score
    score += 1
    canvas.itemconfigure(score_text, text=f"Score: {score}")
    if score > high_score:
        high_score = score
        canvas.itemconfigure(high_score_text, text=f"High Score: {high_score}")
        save_high_score(high_score)

def lose_life():
    global lives, game_over_text, play_again_button
    lives -= 1
    canvas.itemconfigure(lives_text, text=f"Lives: {lives}")
    if lives == 0:
        canvas.unbind_all("<Left>")
        canvas.unbind_all("<Right>")
        save_high_score(high_score)
        game_over_text = canvas.create_text(canvas_width/2, canvas_height/2 - 30, text="Game Over", font=('Arial', 24), fill='red')
        play_again_button = Button(root, text="Play Again", font=('Arial', 12), command=start_game)
        play_again_button.place(x=canvas_width/2 - 40, y=canvas_height/2 + 10)

# === Kontrol ===
def move_left(event):
    pos = canvas.bbox(basket)
    if pos and pos[0] > 0:
        canvas.move(basket, -20, 0)

def move_right(event):
    pos = canvas.bbox(basket)
    if pos and pos[2] < canvas_width:
        canvas.move(basket, 20, 0)

# === Mulai Game ===
start_game()
root.mainloop()