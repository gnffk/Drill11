# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import game_world
import game_framework

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'




# Boy Run Speed
# fill here
PIXEL_PER_METER= (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH*1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM/60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS* PIXEL_PER_METER)
# Boy Action Speed
# fill here
TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4



class Run:

    @staticmethod
    def enter(bird):
        if right_down or left_up: # 오른쪽으로 RUN
            bird.dir, bird.action, bird.face_dir = 1, 1, 1
        elif left_down or right_up: # 왼쪽으로 RUN
            bird.dir, bird.action, bird.face_dir = -1, 0, -1

    @staticmethod
    def exit(bird):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        bird.x += bird.dir * 4
        bird.x = clamp(25, bird.x, 1600 - 25)
        if bird.x>1600-184:
            bird.dir, bird.action, bird.face_dir = -1, 0, -1
        if bird.x<184:
            bird.dir, bird.action, bird.face_dir = 1, 1, 1

    @staticmethod
    def draw(bird):
        if bird.dir== 1:
            bird.image.clip_draw(int(bird.frame) * 180, 0 * 168, 184, 168, bird.x, bird.y+200)
        if bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 180, 0 * 168, 184, 168, 0,'h', bird.x, bird.y + 200,184,168)
            print(bird.action)
class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run


    def start(self):
        self.cur_state.enter(self.bird)

    def update(self):
        self.cur_state.do(self.bird)

    def draw(self):
        self.cur_state.draw(self.bird)


class Bird:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.cur_state.draw(self)
        self.font.draw(self.x -60,self.y+50,f'(Time:{get_time():.2f})',(255,255,0))