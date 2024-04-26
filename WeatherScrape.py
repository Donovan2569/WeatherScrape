import requests     # Used to access website
import pygame       # Used for GUI
import sys          # Used to cleanly stop program
import os           # Used to easily find file location

# Accesses the file path that the program is stored in and changes the directory to the location of the images
script_path = os.path.dirname(os.path.abspath(__file__)) + "\\Images"
os.chdir(script_path)

# Initialized pygame
pygame.init()

# Gets size of users screen and sets constants for the height and width
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Constant variables for colors and FPS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# API key found at https://home.openweathermap.org/api_keys
api_key = "" # Need your own api key as they should remain private
api_url = 'https://api.openweathermap.org/data/2.5/weather' # Link for the api to work

message = ""
sky = ""

# Fuction that goes to open weather to get all info
def Find_City(city):
    # Includes global variables
    global sky, message, Found
    
    # Uses get to request the website
    response = requests.get(
        url=api_url,
        params={
            "q": city,
            "appid": api_key,
            "units": "imperial",
        }
    )

    # Checks if the request was successful
    if response:
        # Pulls the json data from the website, finding the temperature and weather description
        # Ex: 82 F, sunny
        weather_data = response.json()
        message = f"The temperature in {city} is {weather_data['main']['temp']}°F"
        sky = f"If you look outside you'll see {weather_data['weather'][0].get('description')}"
        Found = True
    else:
        city = ""
        Found = False
    
    return city

# Sets screen to the width and height - 50 of users screen
# Allows the user to resize the window, while opening in Fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT-50), pygame.RESIZABLE)

# Titles the app
pygame.display.set_caption("WeatherScrape")

clock = pygame.time.Clock()

buffer = ""
city = ""

# Variables for the color of the textbox
color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color("gray15")

color = color_passive

# Variables to determine if city is found, or textbox is active
active = True
Found = True

# Main loop
while True:
    # Event handling for exiting, resizing, clicking, and typing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True  
                color = color_active
            else:
                color = color_passive
                active = False
        elif event.type == pygame.KEYDOWN:
            if active == True:
                if event.key == pygame.K_RETURN:
                    buffer = Find_City(city)
                elif event.key == pygame.K_BACKSPACE:
                    city = city[:-1]
                else:
                    city += event.unicode
            if event.key == pygame.K_ESCAPE:
                city, buffer, message, sky = "", "", "", ""
        
    # Draw background
    screen.fill(BLACK)
    
    # Sets the font for the text
    font = pygame.font.Font(None, 75)
    
    # Instructs the user to enter a city name
    text_surface = font.render("Input your city name", True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2 , (HEIGHT // 2) - 75))
    screen.blit(text_surface, text_rect)
    
    # Displays an empty textbox where the user types
    if buffer == "":
        # Display textbox
        input_rect = pygame.Rect(WIDTH // 2 - 250 , (HEIGHT // 2), 500, 55)
        pygame.draw.rect(screen, color, input_rect, 2)

        # Places input text in the middle of the textbox
        text_surface = font.render(city, True, WHITE)
        screen.blit(text_surface, input_rect)
        input_rect.w = max(500, text_surface.get_width() + 20)
    
    # Set the background based on the weather
    if 'rain' in sky:
        image_path = f"{script_path}\\rain.jpg"
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image,(0,0))
    elif 'cloud' in sky:
        image_path = f"{script_path}\\cloudy.jpg"
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image,(0,0))
    elif sky != "":
        image_path = f"{script_path}\sunny.jpg"
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(image,(0,0))
        
    # Tells the user city is not found
    if not Found:
        font = pygame.font.Font(None, 25)
        text_surface = font.render("City not found. Check for typos", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2 , (HEIGHT // 2) + 100))
        screen.blit(text_surface, text_rect)
        
    # Changes color of text based on the backgroud displayed.
    if 'rain' in sky:
        text_surface = font.render(message, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        text_surface = font.render(sky, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2 , HEIGHT // 2 + 75))
        screen.blit(text_surface, text_rect)
        font = pygame.font.Font(None, 25)
        text_surface = font.render("Press ESC to reset app", True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2 , (HEIGHT // 2) + 100))
        screen.blit(text_surface, text_rect)
    elif sky != "":
        text_surface = font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text_surface, text_rect)
        text_surface = font.render(sky, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2 , HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        font = pygame.font.Font(None, 25)
        text_surface = font.render("Press ESC to search another city", True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2 , (HEIGHT // 2) + 100))
        screen.blit(text_surface, text_rect)
        
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
