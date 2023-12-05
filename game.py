import digitalio
from adafruit_rgb_display import st7789
import board
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import random
import time

# 플레이어의 다양한 상태에 대한 스프라이트 파일 경로를 저장하는 딕셔너리
sprite_files = {
    # 각 키는 플레이어의 상태를 나타내며, 값은 해당 상태의 스프라이트 이미지 파일 경로
    "normal": ["/home/kau-esw/Desktop/DancingDino/img/player_idle1.PNG", "/home/kau-esw/Desktop/DancingDino/img/player_idle2.PNG"],
    "left": ["/home/kau-esw/Desktop/DancingDino/img/player_idle1.PNG", "/home/kau-esw/Desktop/DancingDino/img/player_left.PNG"],
    "right": ["/home/kau-esw/Desktop/DancingDino/img/player_idle1.PNG", "/home/kau-esw/Desktop/DancingDino/img/player_right.PNG"],
    "up": ["/home/kau-esw/Desktop/DancingDino/img/player_idle1.PNG", "/home/kau-esw/Desktop/DancingDino/img/player_up.PNG"],
    "down": ["/home/kau-esw/Desktop/DancingDino/img/player_idle1.PNG", "/home/kau-esw/Desktop/DancingDino/img/player_down.PNG"],
    "leftup": ["/home/kau-esw/Desktop/DancingDino/img/player_idle1.PNG", "/home/kau-esw/Desktop/DancingDino/img/player_leftup.PNG"],
    "rightup": ["/home/kau-esw/Desktop/DancingDino/img/player_idle1.PNG", "/home/kau-esw/Desktop/DancingDino/img/player_rightup.PNG"],
}

# 게임에서 사용되는 화살표 이미지를 불러오는 딕셔너리
arrow_images = {
    # 각 화살표 방향에 대한 이미지 파일 경로
    "up": Image.open("/home/kau-esw/Desktop/DancingDino/img/arrow_up.PNG"),
    "down": Image.open("/home/kau-esw/Desktop/DancingDino/img/arrow_down.PNG"),
    "left": Image.open("/home/kau-esw/Desktop/DancingDino/img/arrow_left.PNG"),
    "right": Image.open("/home/kau-esw/Desktop/DancingDino/img/arrow_right.PNG"),
    "leftup": Image.open("/home/kau-esw/Desktop/DancingDino/img/arrow_leftup.PNG"),
    "rightup": Image.open("/home/kau-esw/Desktop/DancingDino/img/arrow_rightup.PNG")
}

# 각 스테이지에 대한 배경 이미지 파일 경로를 저장하는 리스트
stage_bg = [
    "/home/kau-esw/Desktop/DancingDino/img/stage1.PNG",
    "/home/kau-esw/Desktop/DancingDino/img/stage2.PNG",
    "/home/kau-esw/Desktop/DancingDino/img/stage3.PNG"
]

# 스테이지의 최대 번호
stage_max = 3

class JoystickController:
    # 조이스틱 컨트롤러 클래스, 게임패드 입력을 처리
    BAUDRATE = 24000000  # SPI 통신의 전송 속도

    def __init__(self):
        # 클래스 초기화 시 실행되는 메서드들
        self._initialize_buttons()
        self._initialize_display()
        self._initialize_backlight()

    def _initialize_buttons(self):
        # 버튼을 초기화하는 메서드
        buttons = {
            "up": board.D17, "down": board.D22,
            "left": board.D27, "right": board.D23,
            "a": board.D5, "b": board.D6
        }
        self.button_states = {name: False for name in buttons}
        self.buttons = {name: digitalio.DigitalInOut(pin) for name, pin in buttons.items()}
        for button in self.buttons.values():
            button.direction = digitalio.Direction.INPUT

    def _initialize_display(self):
        # 디스플레이를 초기화하는 메서드
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)
        spi = board.SPI()
        self.disp = st7789.ST7789(
            spi, height=240, y_offset=80, rotation=180,
            cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=self.BAUDRATE
        )
        self.width = self.disp.width
        self.height = self.disp.height

    def _initialize_backlight(self):
        # 백라이트를 초기화하는 메서드
        backlight = digitalio.DigitalInOut(board.D26)
        backlight.switch_to_output()
        backlight.value = True

    def update(self):
        # 버튼 상태를 업데이트하는 메서드
        for name, button in self.buttons.items():
            self.button_states[name] = not button.value

    def is_button_pressed(self, button_name):
        # 특정 버튼이 눌렸는지 확인하는 메서드
        return self.button_states.get(button_name, False)

    def get_joystick_direction(self):
        # 조이스틱의 방향을 얻는 메서드
        directions = ["up", "down", "left", "right"]
        return [dir for dir in directions if self.is_button_pressed(dir)]

class Player:
    """
    플레이어 클래스: 스프라이트 관리 및 렌더링
    """
    def __init__(self, sprite_files, disp):
        self.sprites = {pose: [Image.open(file) for file in files] for pose, files in sprite_files.items()}
        self.current_sprite_index = 0
        self.current_pose = 'normal'
        self.disp = disp
        self.last_update_time = time.time()
        self.update_interval = 0.5  # 업데이트 간격

    def update_pose(self, pose):
        # 플레이어의 포즈를 업데이트하는 메서드
        self.current_pose = pose
        self.current_sprite_index = 0

    def update_animation(self):
        # 애니메이션을 업데이트하는 메서드
        current_time = time.time()
        if current_time - self.last_update_time >= self.update_interval:
            self.last_update_time = current_time
            if self.current_pose:
                self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites[self.current_pose])

    def render(self, draw, image):
        # 플레이어를 렌더링하는 메서드
        if self.current_pose:
            sprite = self.sprites[self.current_pose][self.current_sprite_index]
            image.paste(sprite, (100, 160), sprite)
        return image

class Arrow:
    """
    화살표 이동 및 렌더링
    """
    def __init__(self, direction, y_start, screen_width, screen_height, arrow_images, long=False, speed=10, hold_duration=0):
        self.direction = direction
        self.x = screen_width // 2
        self.y = y_start
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.long = long
        self.active = True
        self.arrow_image = arrow_images[direction]  # 이미지를 딕셔너리에서 불러옴
        self.speed = 10
        # 홀드 화살표에 필요한 변수
        self.hold_start_y = None
        self.hold_end_y = None
        self.is_holding = False
        self.hold_success = False
        self.hold_duration = hold_duration  # 홀드 지속 시간 (초)
        self.tail_length = hold_duration * speed  # 꼬리 길이 계산

    def render(self, draw, image):
        # 화살표를 렌더링하는 메서드
        image_x = self.x - self.arrow_image.width // 2
        image_y = self.y - self.arrow_image.height // 2

        if self.long:
            # 꼬리의 시작점은 화살표 이미지 하단에 맞춤
            tail_start_y = image_y + self.arrow_image.height // 2
            tail_start = (self.x, tail_start_y)

            # 꼬리의 끝점 계산 (화면 위로 넘어가지 않도록 최대값 설정)
            tail_end_y = max(self.y - self.tail_length, 0)
            tail_end = (self.x, tail_end_y)

            # 사각형 좌표 설정
            rect_coords = [
                tail_start[0] - 15, tail_end[1],  # 왼쪽 상단
                tail_start[0] + 15, tail_start[1]  # 오른쪽 하단
            ]
            draw.rectangle(rect_coords, fill="yellow")
            
            # 꼬리가 화면 상단을 넘어가지 않는 경우에만 화살표 그리기
            if tail_end_y > 0:
                image.paste(self.arrow_image, (image_x, image_y), self.arrow_image)
        else:
            image.paste(self.arrow_image, (image_x, image_y), self.arrow_image)


    def update(self):
        # 화살표 위치를 업데이트하는 메서드
        self.y += self.speed
        if self.long:
            if self.is_holding:
                if self.hold_start_y is None:
                    self.hold_start_y = self.y
                elif self.y - self.hold_start_y >= self.tail_length:
                    self.hold_end_y = self.y
                    self.is_holding = False
                    self.hold_success = True
            elif self.hold_start_y is not None and self.y - self.hold_start_y < self.tail_length:
                self.hold_success = False
        if self.y > self.screen_height:
            self.active = False

    def check_hold(self, joystick):
        # 홀드 상태 확인
        if self.long:
            self.is_holding = joystick.is_button_pressed(self.direction) and joystick.is_button_pressed("a")
class Stage:
    """
    게임 스테이지의 배경 및 게임 상태를 관리
    """
    def __init__(self, player, joystick):
        self.player = player
        self.joystick = joystick
        self.disp = joystick.disp
        self.stage_backgrounds = stage_bg
        self.zones = [(0, 60), (60, 110), (110, 140)]  # 점수 존 위치
        self.arrow_types = ["left", "right", "down", "up", "rightup", "leftup"]
        self.arrow_images = arrow_images  # 화살표 이미지 딕셔너리
        self.spawn_interval = 2  # 화살표 생성 간격 (초)
        self.stage_arrow_speed = [10, 13, 16] # 화살표 이동 간격 (속도)
        self.last_spawn_time = time.time()
        self.start_stage_screen = True
        self.stage_nb = 0
        self.animation_state = "idle"  # 애니메이션 상태
        self.animation_timer = 0       # 애니메이션 타이머
        self.init_states()
        self.should_replay = False 
    
    def init_states(self):
        # 스테이지 상태를 초기화하는 메서드
        self.stage_over = False
        self.current_stage_image = None
        self.score = 0
        self.feedback = ""
        self.combo_count = 0
        self.timer = 30.0  # 30-second timer
        self.arrows = []
        self.start_animation()

    def start_stage(self):
        # 스테이지를 시작하는 메서드
        self.init_states()
        self.current_stage_image = Image.open(self.stage_backgrounds[self.stage_nb])
        self.start_stage_screen = False

    def end_stage(self):
        # 스테이지를 종료하는 메서드
        self.stage_over = True
        if self.score < 1000:
            self.should_replay = True  # Set to replay if score is less than 1000
        else:
            self.should_replay = False  # Don't replay if score is 1000 or more
            self.stage_nb += 1
    
    def start_animation(self):
        self.animation_state = "ready"
        self.animation_timer = 1  # 'Ready~?'를 1초간 표시

    def update_animation(self):
        # 애니메이션 상태 업데이트 로직
        if self.animation_state != "idle":
            self.animation_timer -= 0.25
            if self.animation_timer <= 0:
                # 애니메이션 상태 전환 로직
                # 'ready' -> 'countdown3' -> 'countdown2' -> 'countdown1' -> 'start' -> 'idle'
                animation_sequence = ["ready", "countdown3", "countdown2", "countdown1", "start"]
                try:
                    next_state = animation_sequence[animation_sequence.index(self.animation_state) + 1]
                    self.animation_state = next_state
                    self.animation_timer = 1
                except IndexError:
                    self.animation_state = "idle"

    def render_animation(self, draw, disp_width, disp_height):
        # 애니메이션 렌더링 로직
        if self.animation_state in ["ready", "countdown3", "countdown2", "countdown1", "start"]:
            if self.animation_state == "ready":
                text = "Ready~?"
            elif self.animation_state == "start":
                text = "Start!!!" 
            else:
                text = self.animation_state
                text = text.replace("countdown", "")
            text_x, text_y = (disp_width // 2, disp_height // 2)
            fill_color = (255, 0, 0)
            stroke_color = (0, 0, 0)
            draw.text((text_x, text_y), text, stroke_width=1, fill=fill_color, stroke_fill=stroke_color, anchor="mm")

    def update_score(self, feedback):
        # 점수를 업데이트하는 메서드
        self.feedback = feedback
        if feedback == "Perfect":
            self.combo_count += 1  # 콤보 카운트 증가
            combo_bonus = (1 + self.combo_count * 0.1) if self.combo_count > 1 else 1
            self.score += int(50 * combo_bonus)  # 콤보 보너스 점수 적용
        elif feedback == "Good":
            self.score += 30
            self.combo_count = 0  # 콤보 리셋
        elif feedback == "Miss":
            self.score -= 30
            self.combo_count = 0  # 콤보 리셋
    
    def render_zones(self, draw, disp_width, disp_height, image):
        # 게임의 점수 존을 렌더링하는 메서드
        image = image.convert("RGBA")
        zone_heights = [60, 50, 30]
        zone_colors = [(255, 0, 0, 50), (0, 255, 0, 50), (0, 0, 255, 50)]
        current_y = 0
        for i in range(3):
            zone_height = zone_heights[i]
            zone_image = Image.new("RGBA", (disp_width, zone_height), zone_colors[i])
            image.alpha_composite(zone_image, (0, current_y))
            current_y += zone_height
        # 다시 RGB 모드로 변환
        image = image.convert("RGB")
        return image
    
    def render_text(self, draw):
        # 텍스트(점수, 타이머, 피드백)를 렌더링하는 메서드
        fill_color = (255, 255, 0)
        stroke_color = (0, 0, 0)
        perfect_color = (255, 0, 0)  # Red
        good_color = (0, 255, 0)     # Green
        miss_color = (0, 0, 255)     # Blue

        draw.text((15, 15), f"Score: {self.score}", stroke_width=1, fill=fill_color, stroke_fill=stroke_color)
        draw.text((15, 30), f"Time Left: {int(self.timer)}", stroke_width=1, fill=fill_color, stroke_fill=stroke_color)
        if self.combo_count > 0:  # 콤보가 0보다 크면 콤보 텍스트 표시
            draw.text((50, 120), f"Combo x {self.combo_count}", fill=(255, 0, 0),  stroke_width=1, stroke_fill=(255,255, 0))
        if self.feedback:
            if self.feedback == "Perfect":
                text_color = perfect_color
            elif self.feedback == "Good":
                text_color = good_color
            elif self.feedback == "Miss":
                text_color = miss_color
            draw.text((50, 150), self.feedback, fill=text_color, stroke_width=1)
            self.feedback = ""

    def render_background(self, draw, disp_width, disp_height, image):
        # 배경 이미지를 렌더링하는 메서드
        if self.current_stage_image:
            image.paste(self.current_stage_image, (0, 0), self.current_stage_image)
        return image

    def render(self, draw, disp_width, disp_height, image):
        # 스테이지를 렌더링하는 메서드
        if self.stage_over:
            if self.should_replay:
                draw.text((10, 10), "replay the stage? (press 'b' button)", fill=(255, 255, 255))
            else:
                draw.text((10, 10), "success!", fill=(255, 255, 255))
                time.sleep(2)  # Wait for 2 seconds before proceeding to the next stage
        if self.start_stage_screen:
            draw.text((10, 10), "Press 'A' to Start Stage", fill=(255, 255, 255))
        elif not self.animation_state == 'idle':
            self.render_background(draw, disp_width, disp_height, image)
            self.render_animation(draw, disp_width, disp_width)
            image = self.player.render(draw, image)
        elif not self.stage_over:
            image = self.render_background(draw, disp_width, disp_height, image)
            self.render_text(draw)
            for arrow in self.arrows:
                arrow.render(draw, image)
            image = self.render_zones(draw, disp_width, disp_height, image)
            image = self.player.render(draw, image)
        else:
            draw.text((10, 40), f"Final Score: {self.score}", fill=(255, 255, 255))
        return image
        
    def update(self):
        # 스테이지 상태를 업데이트하는 메서드
        if self.stage_over and self.stage_nb == 3:
            return True
        if self.stage_over:
            if not self.should_replay:
                self.start_stage()
            elif self.should_replay and self.joystick.is_button_pressed('b'):
                self.start_stage()
            return False
        elif self.start_stage_screen and self.joystick.is_button_pressed('a'):
            self.start_stage()
            return False
        elif not self.animation_state == 'idle':
            self.update_animation()
        elif not self.stage_over:
            pose = self.get_charactor_pose()
            self.player.update_pose(pose)
            self.spawn_arrow()
            self.player.update_animation()
            # Check for player input and update the score
            feedback = self.check_hit(pose)
            self.update_arrows()
            if feedback:
                self.update_score(feedback)
            # Update the timer
            self.timer -= 0.3
            if self.timer <= 0:
                self.end_stage()
            return False

    def get_charactor_pose(self):
        # 캐릭터의 포즈를 얻는 메서드
        direction = self.joystick.get_joystick_direction()
        if len(direction) == 0:
            return 'normal'
        elif len(direction) == 1:
            return direction[0]
        elif (direction[0] == "left" and direction[1] == "up") or (direction[0] == "up" and direction[1] == "left"):
            return "leftup"
        elif (direction[0] == "right" and direction[1] == "up") or (direction[0] == "up" and direction[1] == "right"):
            return "rightup"

    def spawn_arrow(self):
        # 새로운 화살표를 생성하는 메서드
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = current_time
            direction = random.choice(self.arrow_types)
            if self.arrow_types != "leftup" or self.arrow_types != "rightup":
                isLong = random.choice([True, False])
            # 새 화살표 객체 생성 시 화살표 이미지 딕셔너리 참조 포함
            if isLong:
                hold_duration = random.randint(3, 5)  # 예를 들어 1~3초 사이의 홀드 시간
                new_arrow = Arrow(direction, 0, self.disp.width, self.disp.height, self.arrow_images, long=True, speed=self.stage_arrow_speed[self.stage_nb], hold_duration=hold_duration)
                self.arrows.append(new_arrow)
            else:
                new_arrow = Arrow(direction, 0, self.disp.width, self.disp.height, self.arrow_images, long=False, speed=self.stage_arrow_speed[self.stage_nb])
                self.arrows.append(new_arrow)
    
    def update_arrows(self):
        # 화살표를 업데이트하는 메서드
        for arrow in self.arrows:
            arrow.check_hold(self.joystick)
            arrow.update()
        # 비활성화된 화살표 제거
        self.arrows = [arrow for arrow in self.arrows if arrow.active]   

    def check_hit(self, player_input):
        # 플레이어 입력을 확인하는 메서드
        if len(self.arrows) == 0:
            return ""
        arrow = self.arrows[0]
        zone = self.calculate_zone(arrow.y)
        if arrow.long and arrow.active:
            # 홀드 화살표 처리
            if arrow.direction == player_input:
                if arrow.hold_success:
                    arrow.active = False
                return "Perfect"
            elif arrow.direction != player_input and player_input != 'normal':
                arrow.active = False
                return "Miss"
            elif zone == -1:
                arrow.active = False
                return "Miss"
        else:
            if (zone == -1) or (arrow.active and arrow.direction != player_input and player_input != 'normal'):
                arrow.active = False
                return "Miss"
            if arrow.active and arrow.direction == player_input:
                arrow.active = False
                if zone == 2:
                    return "Perfect"
                elif zone == 1:
                    return "Good"
                else:
                    return "Miss"
        return ""
        
    def calculate_zone(self, arrow_y):
        # 화살표가 어떤 점수 존에 있는지 계산하는 메서드
        arrow_bottom = arrow_y + 30  # arrow 박스가 zone에 겹쳐지는 지 계산
        if arrow_bottom > self.zones[2][1]: # zone을 넘어감
            return -1
        for idx, (start, end) in enumerate(self.zones):
            if start <= arrow_bottom <= end:
                return idx
        return None 

class Game:
    """
    게임 메인 클래스, 게임의 메인 루프와 상태를 관리
    """
    def __init__(self, joystick, player, master):
        # 게임 초기화
        self.player = player
        self.joystick = joystick
        self.disp = joystick.disp
        self.start_screen = True
        self.game_over = False
        self.master = master
        self.canvas = tk.Canvas(master, width=240, height=320)
        self.canvas.pack()
        self.stage = Stage(player, joystick)
        self.opening_frames = []  # 오프닝 애니메이션 프레임을 저장할 리스트

    def load_opening_frames(self):
        # 오프닝 애니메이션 프레임을 로드하는 메서드
        for i in range(1, 25):
            frame_path = f"/home/kau-esw/Desktop/DancingDino/img/opening/{i}.png"  # 이미지 프레임 경로 설정
            frame_image = Image.open(frame_path)  # PIL로 이미지 열기
            self.opening_frames.append(frame_image)

    def show_opening_animation(self):
        # 오프닝 애니메이션을 보여주는 메서드
        for frame in self.opening_frames:
            # 각 프레임을 Tkinter PhotoImage로 변환하여 캔버스에 표시
            tk_frame = ImageTk.PhotoImage(frame)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_frame)
            self.canvas.image = tk_frame  # 참조 유지
            self.master.update()  # 화면 업데이트
            time.sleep(0.6)  # 각 프레임 간의 딜레이 설정

    def start_game(self):
        # 게임을 시작하는 메서드
        self.start_screen = False
    
    def update(self):
        # 게임 상태를 업데이트하는 메서드
        self.joystick.update()
        # 게임 상태에 따른 로직 분기
        if self.start_screen and self.joystick.is_button_pressed('b'):
            self.load_opening_frames()  # 오프닝 애니메이션 프레임 로드
            self.show_opening_animation()  # 오프닝 애니메이션 보여주기
            self.start_game()
        elif not self.game_over:
            self.game_over = self.stage.update()
            self.render()
        else:
            return
        self.master.after(250, self.update)
            # 게임 종료 화면 처리 추가

    def render(self):
        # 게임을 렌더링하는 메서드
        image = Image.new("RGB", (self.disp.width, self.disp.height))
        draw = ImageDraw.Draw(image)
        if self.start_screen:
            draw.text((10, 10), "Press 'B' to Start", fill=(255, 255, 255))
        elif not self.game_over:
            # Render game elements as before
            image = self.stage.render(draw, self.disp.width, self.disp.height, image)
            # self.disp.image(image)
        else:
            # Display game-over screen with final score
            draw.text((10, 10), "Game Clear", fill=(255, 255, 255))
         # Tkinter에서 이미지를 캔버스에 렌더링
        tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image  # 참조 유지

def main():
    """
    메인 함수, 게임 인스턴스를 생성하고 게임 루프를 실행
    """
    root = tk.Tk()
    joystick = JoystickController()
    player = Player(sprite_files, joystick.disp)
    game = Game(joystick, player, root)
    game.update()
    root.mainloop()

if __name__ == "__main__":
    main()