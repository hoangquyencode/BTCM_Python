import pygame
import random
import sys
import json
from datetime import datetime
import os


# ======= NHẬP TÊN NGƯỜI CHƠI =======
while True:
    Nguoi_choi = input("Nhập tên người chơi: ").strip()
    if Nguoi_choi:
        break
    print("Bạn chưa nhập tên. Vui lòng nhập lại!!!")

bat_dau_choi = datetime.now()

# ======= KHỞI TẠO PYGAME =======
pygame.init()
pygame.mixer.init()

# Âm thanh
catch_sound = pygame.mixer.Sound("catch.wav")
miss_sound = pygame.mixer.Sound("miss.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# Màn hình
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Panic")
clock = pygame.time.Clock()

# ======= TẠO CHẢO =======
pan_img = pygame.Surface((100, 20), pygame.SRCALPHA)
pygame.draw.ellipse(pan_img, (100, 50, 50), pan_img.get_rect())

# ======= TẠO PIZZA =======
pizza_img = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(pizza_img, (255, 200, 0), (20, 20), 20)
for _ in range(5):
    x = random.randint(8, 32)
    y = random.randint(8, 32)
    pygame.draw.circle(pizza_img, (139, 69, 19), (x, y), 3)

font = pygame.font.SysFont(None, 36)

Diemso = 0
So_pizza_roi = 0
fall_speed = 3

# ======= CLASS CHẢO =======
class Pan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pan_img
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 40

    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0] - self.rect.width // 2
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)

# ======= CLASS PIZZA =======
class Pizza(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pizza_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        global So_pizza_roi
        self.rect.y += fall_speed
        if self.rect.top > HEIGHT:
            So_pizza_roi += 1
            miss_sound.play()
            self.kill()

# ======= SPRITE GROUPS =======
pan = Pan()
all_sprites = pygame.sprite.Group(pan)
pizza_group = pygame.sprite.Group()

# ======= VẼ CHỮ =======
def draw_text(surface, text, x, y, color=(0, 0, 0)):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

# ======= VÒNG LẶP GAME =======
running = True
spawn_timer = 0

while running:
    clock.tick(60)
    screen.fill((135, 206, 250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spawn_timer += 1
    if spawn_timer > 50:
        pizza = Pizza()
        all_sprites.add(pizza)
        pizza_group.add(pizza)
        spawn_timer = 0

    all_sprites.update()

    hits = pygame.sprite.spritecollide(pan, pizza_group, True)
    if hits:
        catch_sound.play()
    Diemso += len(hits)

    fall_speed = 3 + Diemso // 5

    all_sprites.draw(screen)
    draw_text(screen, f"Score: {Diemso}", 10, 10)
    draw_text(screen, f"Missed: {So_pizza_roi}/3", 10, 40)

    if So_pizza_roi >= 3:
        gameover_sound.play()
        draw_text(screen, "GAME OVER", WIDTH // 2 - 100, HEIGHT // 2, (255, 0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()

# ======= GHI KẾT QUẢ GAME =======
ket_thuc_choi = datetime.now()

ket_qua = {
    "Nguoi_choi": Nguoi_choi,
    "Diemso": Diemso,
    "So_pizza_roi": So_pizza_roi,
    "tong_so_pizza": Diemso + So_pizza_roi,
    "bat_dau_choi": bat_dau_choi.strftime("%Y-%m-%d %H:%M:%S"),
    "ket_thuc_choi": ket_thuc_choi.strftime("%Y-%m-%d %H:%M:%S")
}

file_path = "DLgame.json"
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
else:
    data = []

data.append(ket_qua)

with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

print("Kết quả game đã được lưu vào DLgame.json")

# ======= CHỜ NGƯỜI DÙNG ĐÓNG GAME THỦ CÔNG =======
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
pygame.quit()
sys.exit()
