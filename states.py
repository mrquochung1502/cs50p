from do_not_modify import *
from assets import Target, TextRender, ModifyNumButton


class Start:
    def __init__(self, display, state):
        self.display = display
        self.state = state

    def text_display(self):
        TextRender('GRIDSHOT50', 70, TITLE_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 30))
        TextRender('Inspired by Gridshot from Aimlabs', 28, TEXT_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 42))
        TextRender('CS50P 2024 final project, made by NTQH with pygame-ce', 30,
                   TEXT_COLOR).render(self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))

    def main_menu(self):
        TextRender('Click anywhere to start', 35, TEXT_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 5))
        start = pygame.mouse.get_just_pressed()[0]
        if start:
            self.state.set_state('play')

        TextRender('Press TAB to see saved results', 25, TEXT_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60))
        scoreboard = pygame.key.get_just_pressed()
        if scoreboard[pygame.K_TAB]:
            self.state.set_state('scoreboard')

        TextRender('Press T to adjust settings', 25, TEXT_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 80))
        settings = pygame.key.get_just_pressed()
        if settings[pygame.K_t]:
            self.state.set_state('settings')

        TextRender('Press ESC to quit', 25, TEXT_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
        quit = pygame.key.get_just_pressed()
        if quit[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit(0)

    def run(self):
        self.display.fill(BG_COLOR)
        self.text_display()
        self.main_menu()


class Play:
    def __init__(self, display, state):
        self.display = display
        self.state = state

        # Ingame variables
        self.current_target_pos = []
        self.timer, self.score, self.accuracy, self.shot, self.hit = 0, 0, 0, 0, 0
        self.speed, self.bonus, self.agg_speed, self.agg_bonus = 0, 0, 0, 0

        # Initialize
        self.all_targets = pygame.sprite.Group()
        self.spawn_targets()
        self.start_timer = pygame.time.get_ticks()
        self.kill_time = pygame.time.get_ticks()

    def spawn_targets(self, recent_target=None):
        while len(self.current_target_pos) < NUM_OF_TARGETS:
            pos = choice(
                [pos for pos in GRID_POS if pos not in self.current_target_pos and pos != recent_target])
            self.current_target_pos.append(pos)
            Target(self.all_targets, pos)

    def shoot_target(self):
        if pygame.mouse.get_just_pressed()[0]:
            self.shot += 1
            self.shot_pos = pygame.mouse.get_pos()
            for target in self.all_targets:  # shot hit
                if target.rect.collidepoint(self.shot_pos):
                    if target.hitbox.get_at((self.shot_pos[0] - target.rect.x, self.shot_pos[1] - target.rect.y)):
                        self.current_target_pos.remove(target.rect.center)
                        recent_target = target.rect.center
                        target.kill()
                        self.hit += 1
                        self.speed = pygame.time.get_ticks() - self.kill_time
                        self.agg_speed += self.speed
                        self.bonus = round(BONUS * (BONUS_INTERVAL - self.speed) /
                                           BONUS_INTERVAL) if self.speed <= BONUS_INTERVAL else 0
                        self.agg_bonus += self.bonus
                        # more bonus for shorter interval between two consecutive hits, scaled in miliseconds
                        # no more bonus if the interval is greater than the bonus limit
                        self.score += BASE_SCORE + self.bonus
                        self.spawn_targets(recent_target)  # exclude from recently killed position
                        self.kill_time = pygame.time.get_ticks()
                        break
            else:  # shot missed
                self.score = 0 if (self.score - BONUS) <= 0 else self.score - BONUS

    def ui_display(self, setting):
        TextRender(f'{self.timer}s', 30, TEXT_COLOR).render(self.display, (WINDOW_WIDTH - 20, 20))
        TextRender(f'{self.score} pts', 30, TITLE_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, 20))
        TextRender(f'{self.accuracy}%', 30, TEXT_COLOR).render(self.display, (20, 20), True)
        if setting:
            TextRender(f'{self.hit}/{self.shot}', 25,
                       TEXT_COLOR).render(self.display, (20, 40), True)
            TextRender(f'Last speed: {self.speed}ms | Last bonus {self.bonus} pts', 22, TEXT_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, 40))
            TextRender(f'Total bonus:     {self.agg_bonus} pts', 20, TEXT_COLOR).render(
                self.display, (20, WINDOW_HEIGHT - 40), True)
            TextRender(f'Total intervals: {self.agg_speed}ms', 20, TEXT_COLOR).render(
                self.display, (20, WINDOW_HEIGHT - 20), True)

    def return_results(self):
        try:
            return {
                'score': self.score,
                'shot': self.shot,
                'hit': self.hit,
                'miss': self.shot - self.hit,
                'accuracy': self.accuracy,
                'agg_speed': self.agg_speed,
                'agg_bonus': self.agg_bonus,
                'avg_interval': round(self.agg_speed / self.hit),
                'avg_bonus': round(self.agg_bonus / self.hit)
            }
        except ZeroDivisionError:
            return None

    def premature_quit(self):
        quit = pygame.key.get_just_pressed()
        if quit[pygame.K_ESCAPE]:
            self.state.set_state('result')

    def run(self):
        # Update gameplay
        self.shoot_target()

        # Timer
        self.timer = TIMER - ((pygame.time.get_ticks() - self.start_timer) // 1000)

        # Accuracy
        try:
            self.accuracy = round((self.hit / self.shot) * 100, 2)
        except ZeroDivisionError:
            self.accuracy = 0

        # Draw
        self.display.fill(BG_COLOR)
        self.ui_display(UI_DETAILS)
        self.all_targets.draw(self.display)

        self.premature_quit()

        if self.timer == 0:
            self.state.set_state('result')


class Result:
    def __init__(self, display, state, result):
        self.display = display
        self.state = state
        self.result = result
        self.saved = False
        self.deleted = False
        try:
            with open(join('data/record.json'), 'r') as file:
                self.record = json.load(file)
        except FileNotFoundError:
            self.record = []
        self.high_score = f"{sorted(self.record)[-1]} pts" if self.record != [] else 'N/A'
        self.avg_score = f"{round(mean(self.record))} pts" if self.record != [] else 'N/A'
        if self.result:
            self.high_record = True if self.record == [
            ] or self.result['score'] > sorted(self.record)[-1] else False

    def stats_display(self):
        if self.result:
            if self.high_record:
                TextRender('NEW HIGH SCORE!', 45, TARGET_COLOR).render(
                    self.display, (WINDOW_WIDTH / 2, 80))
            TextRender('Result', 50, TITLE_COLOR).render(self.display, (WINDOW_WIDTH / 2, 130))
            self.save_result()
            TextRender(f"Score: {self.result['score']} pts (avg: {round(self.result['score']/TIMER)} pts / seconds)",
                       30, TEXT_COLOR).render(self.display, (425, 280), True)
            TextRender(f"(High score: {self.high_score}, avg: {self.avg_score})",
                       30, TITLE_COLOR).render(self.display, (425, 320), True)
            TextRender(f"Missed: {self.result['miss']} (-{self.result['miss']*BONUS} pts)",
                       30, TEXT_COLOR).render(self.display, (425, 360), True)
            TextRender(f"Accuracy: {self.result['accuracy']}% ({self.result['hit']}/{self.result['shot']})",
                       30, TEXT_COLOR).render(self.display, (425, 400), True)
            TextRender(f"Total intervals: {self.result['agg_speed']}ms (avg: {self.result['avg_interval']}ms / shot hit)",
                       30, TEXT_COLOR).render(self.display, (425, 440), True)
            TextRender(f"Total bonus: {self.result['agg_bonus']} pts (avg: {self.result['avg_bonus']} pts / shot hit)",
                       30, TEXT_COLOR).render(self.display, (425, 480), True)
        else:
            TextRender('Please score more for better results (0 hits recorded)', 30,
                       TITLE_COLOR).render(self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    def save_result(self):
        def to_save():
            if not self.saved:
                self.record.append(self.result['score'])
                with open(join('data/record.json'), 'w') as file:
                    json.dump(self.record, file, indent=4)
                    self.saved = True

        if self.high_record:
            TextRender('Result automatically saved for high score', 25,
                       TITLE_COLOR).render(self.display, (WINDOW_WIDTH / 2, 162))
            to_save()
        elif not self.saved:
            TextRender('Press S to save this result', 25, TITLE_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, 162))
            save = pygame.key.get_just_pressed()
            if save[pygame.K_s]:
                to_save()
        else:
            TextRender('Result saved!', 25, TITLE_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, 180))

    def delete_result(self):
        if self.record != []:
            TextRender('Press K to delete all saved results (can not undo!)', 25, TARGET_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100))
            delete = pygame.key.get_just_pressed()
            if delete[pygame.K_k]:
                remove(join('data/record.json'))
                self.deleted = True
        if self.deleted:
            TextRender('DELETED!', 25, TARGET_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80), bg_color='yellow')

    def return_main_menu(self):
        TextRender('Press ESC to return to the main screen', 25, TITLE_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 60))
        main_menu = pygame.key.get_just_pressed()
        if main_menu[pygame.K_ESCAPE]:
            self.state.set_state('start')

    def play_again(self):
        TextRender('Press SPACE to play again', 25, TITLE_COLOR).render(
            self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 40))
        restart = pygame.key.get_just_pressed()
        if restart[pygame.K_SPACE]:
            self.state.set_state('play')

    def run(self):
        self.display.fill(BG_COLOR)
        self.stats_display()
        self.play_again()
        self.return_main_menu()


class ScoreBoard(Result):
    # Display top 24 (12 each column) highest recorded score
    def record_display(self):
        TextRender('Saved Results', 45, TITLE_COLOR).render(self.display, (WINDOW_WIDTH / 2, 130))
        if self.record != []:
            j = 0
            for i, score in enumerate(sorted(self.record, reverse=True), start=1):
                if i == 25:
                    break
                j = i + 1 if i < 13 else 13
                if i in range(1, 4):
                    TextRender(f"No{i}. {score} pts", 30, TITLE_COLOR).render(
                        self.display, (425, 170 + i * 30), True)
                elif i in range(4, 13):
                    TextRender(f"No{i}. {score} pts", 30, TEXT_COLOR).render(
                        self.display, (425, 170 + i * 30), True)
                else:
                    TextRender(f"No{i}. {score} pts", 30, TEXT_COLOR).render(
                        self.display, (725, 170 + (i - 12) * 30), True)
            TextRender(f"Average: {self.avg_score}", 30, TITLE_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, 170 + j * 30))
        else:
            TextRender('No saved results found!', 30, TITLE_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    def run(self):
        self.display.fill(BG_COLOR)
        self.record_display()
        self.delete_result()
        self.return_main_menu()


class Settings(Result):
    def __init__(self, display, state):
        self.display = display
        self.state = state
        self.settings = load_settings()
        self.modified = False

        self.custom_timer = ModifyNumButton(self.display, self.settings['timer'], (850, 250))
        self.ui_details = ModifyNumButton(self.display, self.settings['ui_details'], (850, 280))
        self.num_of_targets = ModifyNumButton(
            self.display, self.settings['num_of_targets'], (850, 310))
        self.base_score = ModifyNumButton(self.display, self.settings['base_score'], (850, 340))
        self.bonus_interval = ModifyNumButton(
            self.display, self.settings['bonus_interval'], (850, 370))
        self.edge = ModifyNumButton(self.display, self.settings['edge'], (850, 400))

    def display_settings(self):
        TextRender('Settings', 45, TITLE_COLOR).render(self.display, (WINDOW_WIDTH / 2, 100))

        TextRender('Time per round (seconds):', 30, TEXT_COLOR).render(
            self.display, (350, 250), True)
        self.custom_timer.update_num(range(5, 61), sep=5)

        TextRender('UI details:', 30, TEXT_COLOR).render(self.display, (350, 280), True)
        self.ui_details.update_num(bi=True)

        TextRender('Number of targets:', 30, TEXT_COLOR).render(self.display, (350, 310), True)
        self.num_of_targets.update_num(range(1, 4))

        TextRender('Base score:', 30, TEXT_COLOR).render(self.display, (350, 340), True)
        self.base_score.update_num(range(1, 101), sep=10)

        TextRender('Bonus interval (milliseconds):', 30,
                   TEXT_COLOR).render(self.display, (350, 370), True)
        self.bonus_interval.update_num(range(500, 1501), sep=100)

        TextRender('Edge of the grid (targets):', 30, TEXT_COLOR).render(
            self.display, (350, 400), True)
        self.edge.update_num(range(2, 8))

    def modify_settings(self):
        custom_settings = {
            'timer': self.custom_timer.return_value(),
            'ui_details': self.ui_details.return_value(),
            'num_of_targets': self.num_of_targets.return_value(),
            'base_score': self.base_score.return_value(),
            'bonus_interval': self.bonus_interval.return_value(),
            'edge': self.edge.return_value()
        }

        def to_save():
            with open(join('data/custom_settings.json'), 'w') as file:
                json.dump(custom_settings, file)
            try:
                remove(join('data/record.json'))
            except FileNotFoundError:
                pass
            self.settings = load_settings()
            self.modified = True

        def to_reset():
            remove(join('data/custom_settings.json'))
            try:
                remove(join('data/record.json'))
            except FileNotFoundError:
                pass
            self.__init__(self.display, self.state)
            self.modified = True

        if custom_settings != self.settings:
            TextRender('Press S to save this settings', 25, TITLE_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, 140))
            TextRender('All saved results will be deleted (can not undo!)', 25,
                       TARGET_COLOR).render(self.display, (WINDOW_WIDTH / 2, 160))

            save = pygame.key.get_just_pressed()
            if save[pygame.K_s]:
                to_save()

        if self.settings != default_settings:
            TextRender('Press Y to restore default settings', 25, TITLE_COLOR).render(
                self.display, (WINDOW_WIDTH / 2, 600))
            TextRender('All saved results will be deleted (can not undo!)', 25,
                       TARGET_COLOR).render(self.display, (WINDOW_WIDTH / 2, 620))

            restore = pygame.key.get_just_pressed()
            if restore[pygame.K_y]:
                to_reset()

    def run(self):
        self.display.fill(BG_COLOR)
        self.display_settings()
        self.modify_settings()
        self.return_main_menu()
