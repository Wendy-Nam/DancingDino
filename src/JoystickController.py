import digitalio
import board

class JoystickController:
    def __init__(self):
        # 버튼 설정
        self.button_U = digitalio.DigitalInOut(board.D17)
        self.button_D = digitalio.DigitalInOut(board.D22)
        self.button_L = digitalio.DigitalInOut(board.D27)
        self.button_R = digitalio.DigitalInOut(board.D23)
        self.button_A = digitalio.DigitalInOut(board.D5) 
        self.button_B = digitalio.DigitalInOut(board.D6)
        # 버튼 입력 방향 설정
        self.button_U.direction = digitalio.Direction.INPUT
        self.button_D.direction = digitalio.Direction.INPUT
        self.button_L.direction = digitalio.Direction.INPUT
        self.button_R.direction = digitalio.Direction.INPUT
        self.button_A.direction = digitalio.Direction.INPUT
        self.button_B.direction = digitalio.Direction.INPUT
        # 버튼 상태
        self.button_states = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "a": False,  # A 버튼 상태
            "b": False   # B 버튼 상태 추가
        }

    def update(self):
        # 각 버튼의 상태를 업데이트
        self.button_states["up"] = not self.button_U.value
        self.button_states["down"] = not self.button_D.value
        self.button_states["left"] = not self.button_L.value
        self.button_states["right"] = not self.button_R.value
        self.button_states["a"] = not self.button_A.value 
        self.button_states["b"] = not self.button_B.value

    def is_button_pressed(self, button):
        # 특정 버튼이 눌렸는지 확인
        return self.button_states.get(button, False)

    def get_joystick_direction(self):
        # 조이스틱 방향 반환 (버튼 기반)
        direction = []
        if self.is_button_pressed("up"):
            direction.append("up")
        if self.is_button_pressed("down"):
            direction.append("down")
        if self.is_button_pressed("left"):
            direction.append("left")
        if self.is_button_pressed("right"):
            direction.append("right")
        return direction
