class Player:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.health = 100
        self.armor = 100
        self.ammo = 60
        self.active = 0
        self.inventory = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, da):
        self.angle += da
    def pick_up():
        pass
    def drop():
        pass

