import pygame
import sys
from random import randint
from os.path import join

import button
import player
import phantom

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
GROUND_Y = 600
PHANTOM_SPAWN_INTERVAL_MS = 500


class GameState:
    MAIN_MENU = "game-menu"
    PAUSE_MENU = "pause-menu"
    PLAYING = "game"
    SETTINGS = "settings"
    DEATH_MENU = "dead-menu"


def load_menu_images():
    image_names = [
        'play_img', 'quit_img', 'settings_img',
        'play_hover_img', 'settings_hover_img', 'quit_hover_img',
        'settings_icon', 'settings_hover_icon',
        'resume_button', 'menu_button',
        'resume_hover_button', 'menu_hover_button'
    ]

    images = {}
    for name in image_names:
        images[name] = pygame.image.load(join("images", "game-menu", f"{name}.png"))

    return images


def check_collisions(player_sprite, phantom_group, death_sound):
    global current_state

    for phantom_sprite in phantom_group:
        if phantom_sprite.hitbox.colliderect(player_sprite.rect):
            death_sound.play()
            phantom_group.empty()
            current_state = GameState.DEATH_MENU


def show_countdown_intro(surface, background_image, countdown_audio_files):
    global phantom_event

    large_font = pygame.font.Font(join('images', 'minecraft.ttf'), 120)
    small_font = pygame.font.Font(join('images', 'minecraft.ttf'), 40)

    pygame.time.set_timer(phantom_event, 0)
    start_time = pygame.time.get_ticks()

    countdown_texts = ["3", "2", "1", "GO"]
    countdown_durations = [1000, 2000, 3000, 4000]
    audio_played = [False, False, False, False]

    running = True
    while running:
        surface.blit(background_image, (0, 0))
        elapsed_time = pygame.time.get_ticks() - start_time

        current_text = None
        for i, duration in enumerate(countdown_durations):
            if elapsed_time < duration:
                current_text = countdown_texts[i]
                if not audio_played[i]:
                    sound = pygame.mixer.Sound(countdown_audio_files[i])
                    sound.play()
                    audio_played[i] = True
                break

        if current_text is None:
            running = False
            continue

        countdown_surface = large_font.render(current_text, True, "darkorange")
        countdown_rect = countdown_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 300))
        surface.blit(countdown_surface, countdown_rect)

        controls_surface = small_font.render("Use A and D to move", True, "darkorange")
        controls_rect = controls_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200))
        surface.blit(controls_surface, controls_rect)

        pygame.display.update()

    return pygame.time.get_ticks()


def reset_game_session():
    global intro_completed, pause_time_total, pause_start_time, session_score
    global all_sprites, all_phantoms, player_sprite

    intro_completed = False
    session_score = 0
    pause_time_total = 0
    pause_start_time = 0

    player_sprite.rect.midbottom = (WINDOW_WIDTH / 2, 600)

    all_sprites.empty()
    all_phantoms.empty()
    all_sprites.add(player_sprite)


def render_game(surface, ground_y):
    global intro_completed, game_start_time, session_score

    surface.fill('darkgray')
    surface.blit(game_background, (0, 0))

    ground_rect = pygame.Rect((0, ground_y), (1280, 100))

    if not intro_completed:
        game_start_time = show_countdown_intro(surface, game_background, countdown_audio_files)
        intro_completed = True
        pygame.time.set_timer(phantom_event, PHANTOM_SPAWN_INTERVAL_MS)

    render_score(surface)

    if player_sprite.rect.colliderect(ground_rect):
        player_sprite.rect.bottom = ground_rect.top

    check_collisions(player_sprite, all_phantoms, death_sfx)

    all_sprites.update(dt)
    all_sprites.draw(surface)


def render_death_menu(surface, score):
    global current_state

    surface.fill('lightskyblue2')

    large_font = pygame.font.Font(join('images', 'minecraft.ttf'), 150)
    medium_font = pygame.font.Font(join('images', 'minecraft.ttf'), 80)

    title_surface = large_font.render("You Died!", True, (240, 240, 240))
    title_rect = title_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 180))
    surface.blit(title_surface, title_rect)

    score_surface = medium_font.render(f"Score: {score}", True, (240, 240, 240))
    score_rect = score_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
    surface.blit(score_surface, score_rect)

    if menu_button.draw(surface):
        current_state = GameState.MAIN_MENU


def render_score(surface):
    global pause_time_total, game_start_time, session_score, high_score

    large_font = pygame.font.Font(join('images', 'minecraft.ttf'), 120)
    current_time = pygame.time.get_ticks()

    score = ((current_time - game_start_time) / 1000) - pause_time_total
    session_score = round(score, 1)

    score_surface = large_font.render(str(session_score), True, (240, 240, 240))
    score_rect = score_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 300))
    surface.blit(score_surface, score_rect)

    if session_score > high_score:
        save_high_score(session_score)


def load_high_score():
    filename = join('resources', 'high_score.txt')
    try:
        with open(filename, "r") as file:
            content = file.read().strip()
            return float(content) if content else 0.0
    except (FileNotFoundError, ValueError):
        return 0.0


def save_high_score(score):
    global high_score

    filename = join('resources', 'high_score.txt')
    with open(filename, 'w') as file:
        file.write(str(float(score)))

    high_score = score


pygame.init()
pygame.display.set_caption("Falling Cats")

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
icon = pygame.image.load(join('images', 'icon_img.jpg'))
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
running = True
current_state = GameState.MAIN_MENU

game_music_files = [
    'resources/game_music.mp3',
    'resources/game_music2.mp3',
    'resources/game_music3.mp3'
]
phantom_sound_files = [
    'resources/phantom.mp3',
    'resources/phantom2.mp3',
    'resources/phantom3.mp3'
]

countdown_audio_files = [
    'resources/countdown_ready.wav',  # for "3"
    'resources/countdown_ready.wav',  # for "2"
    'resources/countdown_go.wav',     # for "1"
    'resources/countdown_go.wav'      # for "GO"
]

click_sfx = pygame.mixer.Sound(join('resources', 'click.mp3'))
death_sfx = pygame.mixer.Sound(join('resources', 'death.mp3'))
death_sfx.set_volume(0.3)

pygame.mixer.music.load(game_music_files[randint(0, len(game_music_files) - 1)])
pygame.mixer.music.set_volume(0.5)

menu_images = load_menu_images()

game_background = pygame.image.load(join('images', 'bg_img.png')).convert()
game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

play_button = button.Button(
    WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100,
    menu_images["play_img"], 5,
    menu_images["play_hover_img"], click_sfx
)
settings_button = button.Button(
    WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
    menu_images["settings_img"], 5,
    menu_images["settings_hover_img"], click_sfx
)
quit_button = button.Button(
    WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100,
    menu_images["quit_img"], 5,
    menu_images["quit_hover_img"], click_sfx
)
gear_icon_button = button.Button(
    WINDOW_WIDTH - 100, 100,
    menu_images["settings_icon"], 5,
    menu_images["settings_hover_icon"], click_sfx
)
resume_button = button.Button(
    WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50,
    menu_images["resume_button"], 5,
    menu_images["resume_hover_button"], click_sfx
)
menu_button = button.Button(
    WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50,
    menu_images["menu_button"], 5,
    menu_images["menu_hover_button"], click_sfx
)

all_sprites = pygame.sprite.Group()
all_phantoms = pygame.sprite.Group()
player_sprite = player.Player(all_sprites, WINDOW_WIDTH, WINDOW_HEIGHT, 8)

phantom_event = pygame.event.custom_type()
pygame.time.set_timer(phantom_event, 0)

intro_completed = False
game_start_time = 0
pause_time_total = 0
pause_start_time = 0
session_score = 0
high_score = load_high_score()

music_playing = False

while running:
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == phantom_event and current_state == GameState.PLAYING and intro_completed:
            spawn_x = randint(0, WINDOW_WIDTH)
            spawn_y = randint(-200, -100)
            phantom.Phantom((spawn_x, spawn_y), 0.6, (all_sprites, all_phantoms), phantom_sound_files)

    display_surface.fill((0, 0, 0))

    if current_state == GameState.MAIN_MENU:
        pygame.mixer.music.load(game_music_files[randint(0, len(game_music_files) - 1)])
        pygame.mixer.music.set_volume(0.5)

        display_surface.fill('lightskyblue2')

        high_score_font = pygame.font.Font(join('images', 'minecraft.ttf'), 70)
        high_score_text = high_score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 250))
        display_surface.blit(high_score_text, high_score_rect)

        if play_button.draw(display_surface):
            reset_game_session()
            current_state = GameState.PLAYING

        if settings_button.draw(display_surface):
            current_state = GameState.SETTINGS

        if quit_button.draw(display_surface):
            running = False

    elif current_state == GameState.PLAYING:
        if not music_playing:
            pygame.mixer.music.play(-1)
            music_playing = True

        render_game(display_surface, GROUND_Y)

        if gear_icon_button.draw(display_surface):
            pause_start_time = pygame.time.get_ticks()
            current_state = GameState.PAUSE_MENU

    elif current_state == GameState.PAUSE_MENU:
        pygame.mixer.music.pause()
        music_playing = False

        display_surface.fill('lightskyblue2')

        if menu_button.draw(display_surface):
            current_state = GameState.MAIN_MENU

        if resume_button.draw(display_surface):
            pause_duration = (pygame.time.get_ticks() - pause_start_time) / 1000
            pause_time_total += pause_duration
            current_state = GameState.PLAYING

    elif current_state == GameState.DEATH_MENU:
        pygame.mixer.music.stop()
        music_playing = False
        render_death_menu(display_surface, session_score)

    elif current_state == GameState.SETTINGS:
        display_surface.fill('lightskyblue2')

        large_font = pygame.font.Font(join('images', 'minecraft.ttf'), 120)
        coming_soon_surface = large_font.render("COMING SOON", True, (0, 0, 0))
        coming_soon_rect = coming_soon_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
        display_surface.blit(coming_soon_surface, coming_soon_rect)

        if menu_button.draw(display_surface):
            current_state = GameState.MAIN_MENU

    pygame.display.update()

pygame.quit()
sys.exit()