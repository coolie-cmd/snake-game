import pygame
import random

#initialize pygame
pygame.init()

#colors
Black = (0, 0, 0)
white = (255, 255, 255)
green = (0,255,0)
red = (255, 0, 0)

#font for score
font = pygame.font.SysFont('arial',25)

#game restart
def reset_game():
    global snake_pos, snake_body, direction, change_to, food_pos, food_spawn, score, game_over
    snake_pos = [width//2, height//2]
    snake_body = [[width//2, height//2]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(1, (width//block_size)) * block_size,
                random.randrange(1, (height//block_size)) * block_size]
    food_spawn = True
    score = 0
    game_over = False


# Game Over function
def game_over_screen():
    screen.fill(Black)
    game_over_text = font.render('GAME OVER! LOSER! ', True, red)
    score_text = font.render(f'Final Score: {score}', True, white)
    restart_text = font.render('Press R to Restart or Q to Quit', True, white)
    
    screen.blit(game_over_text, (width//2 - 80, height//2 - 50))
    screen.blit(score_text, (width//2 - 80, height//2))
    screen.blit(restart_text, (width//2 - 150, height//2 + 50))
    
    pygame.display.flip()

#screen dimensions
width = 600
height = 400
block_size = 20 #size of each snake segment

#create the screen
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("snake game")

#clock for controlling frame rate
clock = pygame.time.Clock()

#snake starting position and body 
snake_pos = [width//2, height //2] # start in center
snake_body = [[width//2, height//2]]

#direction(starts moving right )
direction = 'RIGHT'
change_to = direction

# Food position
food_pos = [random.randrange(1, (width//block_size)) * block_size,
            random.randrange(1, (height//block_size)) * block_size]
food_spawn = True

# Score
score = 0

#game over flag 
game_over = False

#game loop 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to ='LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Make sure snake doesn't reverse into itself
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    # Move the snake
    if direction == 'UP':
        snake_pos[1] -= block_size
    elif direction == 'DOWN':
        snake_pos[1] += block_size
    elif direction == 'LEFT':
        snake_pos[0] -= block_size
    elif direction == 'RIGHT':
        snake_pos[0] += block_size

     # Game Over conditions
    # Hit the walls
    if snake_pos[0] < 0 or snake_pos[0] >= width:
        game_over = True
    if snake_pos[1] < 0 or snake_pos[1] >= height:
        game_over = True
    
    # Hit itself
    for block in snake_body[1:]:  # Skip the head
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over = True
    
    # If game over, show screen and wait
    if game_over:
        game_over_screen()
        
        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart
                        reset_game()
                        waiting = False
                        game_over = False
                    elif event.key == pygame.K_q:  # Quit
                        running = False
                        waiting = False

    # Update snake body
    snake_body.insert(0, list(snake_pos))

    # Check if snake ate food
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()  # Only remove tail if no food eaten
    
    # Spawn new food
    if not food_spawn:
        food_pos = [random.randrange(1, (width//block_size)) * block_size,
                   random.randrange(1, (height//block_size)) * block_size]
        food_spawn = True
    
    # Fill screen with black
    screen.fill(Black)
    
    # Draw the snake
    for segment in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(segment[0], segment[1], block_size, block_size))
    
        # Draw food
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], block_size, block_size))
    
       # Draw score
    score_text = font.render(f'Score: {score}', True, white)
    screen.blit(score_text, (10, 10))


    #update display
    pygame.display.flip()

    #control game speed (10 FPS)
    clock.tick(10)

pygame.quit()