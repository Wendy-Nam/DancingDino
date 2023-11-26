class Player:
    def __init__(self):
        self.direction = "None"

    def update_direction(self, joystick_direction):
        if joystick_direction:
            self.direction = " and ".join(joystick_direction)
        else:
            self.direction = "None"

    def display_direction(self):
        print(f"Player direction: {self.direction}")