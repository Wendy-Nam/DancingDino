import time

def main():
    joystick = JoystickController()
    player = Player()

    while True:
        # 조이스틱 입력 업데이트
        joystick.update()

        # 플레이어 방향 업데이트
        player.update_direction(joystick.get_joystick_direction())

        # 플레이어 방향 출력
        player.display_direction()

        # A 및 B 버튼 상태 출력
        if joystick.is_button_pressed("a"):
            print("A button pressed")
        if joystick.is_button_pressed("b"):
            print("B button pressed")
        # 콘솔 출력이 너무 빠르게 되지 않도록 잠시 대기
        time.sleep(0.1)

if __name__ == "__main__":
    main()