import pygame
import numpy as np

# Inisialisasi pygame
pygame.init()

# Konstanta layar
WIDTH, HEIGHT = 1420, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulasi 3 Rotary Encoder")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Posisi encoder relatif dalam bentuk segitiga
ENCODER_POS = np.array([
    [0, -50],   # Encoder atas (0 derajat terhadap X)
    [-43, 25],  # Encoder kiri bawah (45 derajat terhadap X)
    [43, 25]    # Encoder kanan bawah (135 derajat terhadap X)
])

# Sudut awal encoder terhadap sumbu X
ENCODER_ANGLES = np.array([0, 45, 135])

# Nilai encoder
encoder_values = np.array([0, 0, 0])

# Posisi dan orientasi robot
# robot_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)
robot_pos = np.array([WIDTH // 2, HEIGHT // 2], dtype=float)

robot_angle = 0  # Derajat
velocity = np.array([0.0, 0.0])
rotation_speed = 5  # Derajat per langkah

# Jarak encoder dari pusat robot (untuk rotasi)
RADIUS = 50


def rotation_matrix(angle):
    rad = np.radians(angle)
    return np.array([
        [np.cos(rad), -np.sin(rad)],
        [np.sin(rad), np.cos(rad)]
    ])


# Loop utama
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Kontrol dengan WASD dan rotasi dengan arrow kanan/kiri
    keys = pygame.key.get_pressed()
    movement = np.array([0.0, 0.0])
    rotation = 0
    if keys[pygame.K_w]:
        movement += [0, -1]
    if keys[pygame.K_s]:
        movement += [0, 1]
    if keys[pygame.K_a]:
        movement += [-1, 0]
    if keys[pygame.K_d]:
        movement += [1, 0]
    if keys[pygame.K_LEFT]:
        rotation -= rotation_speed
    if keys[pygame.K_RIGHT]:
        rotation += rotation_speed
    
    # Perbarui sudut robot
    robot_angle += rotation
    robot_angle %= 360  # Normalisasi sudut
    
    # Rotasi matriks untuk mengikuti arah robot
    rot_matrix = rotation_matrix(robot_angle)
    rotated_movement = rot_matrix @ movement
    
    # Perbarui posisi robot
    velocity = rotated_movement * 2
    robot_pos += velocity
    
    # Perbarui sudut encoder akibat rotasi robot
    ENCODER_ANGLES = (ENCODER_ANGLES + rotation) % 360
    
    # Hitung perubahan encoder berdasarkan gerakan linier
    angle_rad = np.radians(ENCODER_ANGLES)
    encoder_matrix = np.array([
        [np.cos(ang), np.sin(ang)] for ang in angle_rad
    ])
    encoder_delta = encoder_matrix @ velocity
    
    # Hitung perubahan encoder akibat rotasi robot
    rotation_rad = np.radians(rotation)
    rotation_effect = RADIUS * rotation_rad  # Perubahan jarak akibat rotasi
    encoder_rotation_delta = np.array([-rotation_effect, rotation_effect, rotation_effect])
    
    # Gabungkan perubahan akibat translasi dan rotasi
    encoder_values += (encoder_delta + encoder_rotation_delta).astype(int)
    
    # Gambar robot dan encoder
    pygame.draw.circle(screen, BLACK, robot_pos.astype(int), 50, 2)
    # Gambar encoder berbentuk "T"
    for i, pos in enumerate(ENCODER_POS):
        rotated_pos = rot_matrix @ pos
        encoder_screen_pos = robot_pos + rotated_pos  # Posisi encoder di layar
        
        # Hitung arah garis encoder
        encoder_dir = (rot_matrix @ (pos * 0.5))  # Setengah panjang garis utama
        
        # Garis utama encoder
        pygame.draw.line(screen, RED, encoder_screen_pos.astype(int), 
                        (encoder_screen_pos + encoder_dir).astype(int), 4)
        
        # Garis melintang untuk membentuk "T"
        perpendicular_dir = np.array([-encoder_dir[1], encoder_dir[0]])  # Rotasi 90 derajat
        pygame.draw.line(screen, RED, 
                        (encoder_screen_pos + encoder_dir - perpendicular_dir * 0.3).astype(int), 
                        (encoder_screen_pos + encoder_dir + perpendicular_dir * 0.3).astype(int), 4)

    
    # Tampilkan nilai encoder
    font = pygame.font.Font(None, 30)
    for i, val in enumerate(encoder_values):
        text = font.render(f"Encoder {i+1}: {val}", True, BLACK)
        screen.blit(text, (20, 20 + i * 30))
    
    # Tampilkan koordinat robot
    coord_text = font.render(f"Posisi: ({int(robot_pos[0])}, {int(robot_pos[1])})", True, BLACK)
    screen.blit(coord_text, (20, 120))
    
    # Tampilkan sudut robot
    angle_text = font.render(f"Sudut: {int(robot_angle)}°", True, BLACK)
    screen.blit(angle_text, (20, 150))
    
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()