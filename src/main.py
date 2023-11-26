import time

def main():
    joystick = JoystickController()
    player = Player()

    while True:
        # 조이스틱 입력 업데이트
        joystick.update()

        # 예시: 사용자 입력에 따라 자세 업데이트
        if joystick.is_button_pressed("left"):
            player.update_pose("left")
        else:
            player.update_pose("normal")

        player.update_animation()
        player.render()

        time.sleep(0.2)

if __name__ == "__main__":
    main()