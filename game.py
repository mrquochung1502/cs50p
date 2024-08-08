from states import *


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gridshot50')
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
        self.running = True
        self.restart_alert = False

        # Start the game
        self.state = GameState(self.display_surface)
        self.state.set_state('start')

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.execute_state()
            if self.state.get_state() == 'play':
                self.state.result = self.state.running_state.return_results()
            if self.state.get_state() == 'settings':
                if self.state.running_state.modified:
                    self.restart_alert = True
            if self.restart_alert:
                TextRender('Changes saved! Please restart by pressing R to apply changes',
                           25, TARGET_COLOR).render(self.display_surface, (WINDOW_WIDTH / 2, 70))
                restart = pygame.key.get_just_pressed()
                if restart[pygame.K_r]:
                    execv(sys.executable, [sys.executable] + sys.argv)

            pygame.display.update()
        pygame.quit()
        sys.exit(0)


class GameState:
    def __init__(self, display_surface):
        self.display = display_surface
        self.running_state, self.current_state = None, None
        self.result = None

    def get_state(self):
        return self.current_state

    def execute_state(self):
        self.running_state.run()

    def set_state(self, state):
        self.current_state = state
        match self.current_state:
            case 'start':
                self.running_state = Start(self.display, self)
            case 'play':
                self.running_state = Play(self.display, self)
            case 'result':
                self.running_state = Result(self.display, self, self.result)
            case 'scoreboard':
                self.running_state = ScoreBoard(self.display, self, self.result)
            case 'settings':
                self.running_state = Settings(self.display, self)
