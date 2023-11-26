from PIL import Image

sprite_files = {
    "normal": ["player_idle1.PNG", "player_idle2.PNG"],
    "left": ["player_idle1.PNG", "player_left.PNG"],
    "right": ["player_idle1.PNG", "player_right.PNG"],
    "up": ["player_idle1.PNG", "player_up.PNG"],
    "upleft": ["player_idle1.PNG", "player_up.PNG", "player_upleft.PNG"],
    "upright": ["player_idle1.PNG", "player_up.PNG", "player_upright.PNG"],
}

class Player:
    def __init__(self, sprite_files, disp):
        self.sprites = {pose: [Image.open(file) for file in files] for pose, files in sprite_files.items()}
        self.current_sprite_index = 0
        self.current_pose = 'normal'
        self.disp = disp
        self.last_update_time = time.time()
        self.update_interval = 0.2  # 업데이트 간격

    def update_pose(self, pose):
        self.current_pose = pose
        self.current_sprite_index = 0

    def update_animation(self):
        current_time = time.time()
        if current_time - self.last_update_time >= self.update_interval:
            self.last_update_time = current_time
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites[self.current_pose])

    def render(self):
        sprite = self.sprites[self.current_pose][self.current_sprite_index]
        image = Image.new("RGB", (self.disp.width, self.disp.height))
        image.paste(sprite, (100, 100))  # 스프라이트를 이미지에 붙입니다 (위치 조정 가능)
        self.disp.image(image)
