from DungeonGenerator.Room import room

# todo contenido que no se mueve de donde inicia hereda esta clase
class content:
    # variables
    
    
    def __init__(self, room, content_x_pos, content_y_pos):
        self.content_x_pos = room.x + content_x_pos
        self.content_y_pos = room.y + content_y_pos

# contenido donde el jugador puede colocarse encima
# todo contenido que tiene un efecto cuando el jugador se para en ellas
# hereda esta clase
class trampa(content):
    
    def __init__(self, room, content_x_pos, content_y_pos):
        super().__init__(room, content_x_pos, content_y_pos)
        self.color = (255,127,80)
    
    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color
    
    def setDmg(self, dmg):
        self.dmg =  dmg
    
    def getDmg(self):
        return self.dmg

# contenido roca. El jugador no puede pasar por estas tiles
class roca(content):
    def __init__(self, room, content_x_pos, content_y_pos):
        super().__init__(room, content_x_pos, content_y_pos)
        self.color = (6, 32, 39)