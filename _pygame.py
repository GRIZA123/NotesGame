import pygame
from configsound import get_frequency,get_note_from_frequency,stream,RATE,CHUNK
from configofgame import WIDTH,HEIGHT,SPEED,NOTE_PART
from functions.f import set_list_pos,get_note_height

class Game:
    def __init__(self):
        self.running = False
        self.screen = None
        self.clock = None
        self.width = WIDTH
        self.height = HEIGHT
        self.speed = SPEED

    def FirstCreation(self):
        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Game Project')
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.list_of_pos = set_list_pos(HEIGHT,NOTE_PART)
        print(self.list_of_pos)
        
        self.balls = [{"pos": [50, 400], "radius": 10, "color": (255, 0, 0)}]

    def cyclegame(self):
        try:
            while self.running:
                self.cycleevent()

                self.screen.fill((255, 255, 255))
                self.update_game()

                pygame.display.flip()
                self.clock.tick(60)
        except:pass

    def cycleevent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.balls.append({"pos": [mouse_x, mouse_y], "radius": 10, "color": (255, 0, 0)})                         

    def update_game(self):
        for line in self.list_of_pos:
            line[0][0] -= self.speed
            line[1][0] -= self.speed

        self.list_of_pos = [line for line in self.list_of_pos if line[1][0] > 0]
        for line in self.list_of_pos:
            pygame.draw.line(self.screen, (0, 0, 0), tuple(line[0]), tuple(line[1]), 2)

        if len(self.list_of_pos) < 5 and (self.list_of_pos[-1][1][0] < self.width):
            last_line = self.list_of_pos[-1]
            new_start = [last_line[1][0] + 100, last_line[1][1]]
            new_end = [new_start[0] + 200, new_start[1] - 100]
            self.list_of_pos.append([new_start, new_end])

        for ball in self.balls:
            pygame.draw.circle(self.screen, ball["color"], ball["pos"], ball["radius"])
            for line in self.list_of_pos:
                if self.check_collision(ball, line):
                    ball["color"] = (0, 255, 0)
                    
        data = stream.read(CHUNK, exception_on_overflow=False)
        frequency = get_frequency(data, RATE)
        note = get_note_from_frequency(frequency)
        
        y = get_note_height(HEIGHT,note)
        
        text_surface = self.font.render(f"{frequency:.2f} -> {note}", True, (0, 0, 0))
        self.screen.blit(text_surface, (100, y-30))
        self.balls[0]["pos"] = [50, y-30]

    def check_collision(self, ball, line):
        x1, y1 = line[0]
        x2, y2 = line[1]
        px, py = ball["pos"]

        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return False

        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        distance = ((px - closest_x) ** 2 + (py - closest_y) ** 2) ** 0.5
        return distance <= ball["radius"]

    def cleanup(self):
        pygame.quit()
        
