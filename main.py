import pygame, GameMatrix, math, sys

pygame.init()
clock = pygame.time.Clock()

pygame.mixer.init()

#Game Class
class GameC:
    def __init__(self):
        # display setting, change them if you want!
        self.width = 105
        self.height = 60
        self.gridSize = 13
        self.size = (self.width * self.gridSize, self.height * self.gridSize)
        self.screen = pygame.display.set_mode(self.size)
        self.isRunning = False
        self.framebyframe = False
        self.showGrid = True
        # add any other colors inside the tuple!
        self.cellColors = ((0, 0, 0), (230, 230, 230), (0, 230, 230), (0, 230, 0))
        self.Game = GameMatrix.Matrix()
        self.GameFlip = GameMatrix.Matrix()
        self.Game.build(self.width, self.height)
        self.GameFlip.build(self.width, self.height)
        # Connects NodeData for better file saving
        self.Game.NodesData = self.GameFlip.NodesData
        pygame.display.set_caption("Thank You Mrs. Warren!", "TYMW")
        self.icon = pygame.image.load("GameAttributesAndData\GameIcon.png")
        pygame.display.set_icon(self.icon)

    def checkCell(self, node):
        neighbors = []
        x = node.Xm
        y = node.Ym
        #find neighbors inefficiently
        neighbors.append(self.Game.get(x - 1, y + 1).key)
        neighbors.append(self.Game.get(x, y + 1).key)
        neighbors.append(self.Game.get(x + 1, y + 1).key)
        neighbors.append(self.Game.get(x - 1, y).key)
        neighbors.append(self.Game.get(x + 1, y).key)
        neighbors.append(self.Game.get(x - 1, y - 1).key)
        neighbors.append(self.Game.get(x, y - 1).key)
        neighbors.append(self.Game.get(x + 1, y - 1).key)

        neighborCount = 0

        for neighbor in neighbors:
            if neighbor == 1:
                neighborCount += 1

        if neighborCount == 2 and node.key == 0:
            node.key = 1

        elif node.key == 1:
            if neighborCount < 3:
                node.key = 2

            elif neighborCount > 5:
                node.key = 2

        elif node.key == 2:
            node.key = 3

        elif node.key == 3:
            node.key = 0

        return node

    def update(self):
        self.Game.transmit(self.GameFlip)
        for node in self.GameFlip.Nodes:
            node = self.checkCell(node)
        self.Game.transmit(self.GameFlip)
        self.framebyframe = False

    def eventHandler(self):
        #Handles events sent by the user
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #find the cords to "place" a cell
                    (Mx, My) = pygame.mouse.get_pos()
                    Nx, Ny = math.ceil(Mx / self.gridSize), math.ceil(My / self.gridSize)
                    if self.GameFlip.get(Nx, Ny).key != 1:
                        self.GameFlip.get(Nx, Ny).key = 1

                    else:
                        self.GameFlip.get(Nx, Ny).key = 0

                if event.button == 2:
                    #find the cords to "place" a cell
                    (Mx, My) = pygame.mouse.get_pos()
                    Nx, Ny = math.ceil(Mx / self.gridSize), math.ceil(My / self.gridSize)
                    if self.GameFlip.get(Nx, Ny).key != 2:
                        self.GameFlip.get(Nx, Ny).key = 2

                    else:
                        self.GameFlip.get(Nx, Ny).key = 0

                if event.button == 3:
                    #find the cords to "place" a cell
                    (Mx, My) = pygame.mouse.get_pos()
                    Nx, Ny = math.ceil(Mx / self.gridSize), math.ceil(My / self.gridSize)
                    if self.GameFlip.get(Nx, Ny).key != 3:
                        self.GameFlip.get(Nx, Ny).key = 3

                    else:
                        self.GameFlip.get(Nx, Ny).key = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #start/stop
                    if self.isRunning:
                        self.isRunning = False

                    else:
                        self.isRunning = True

                elif event.key == pygame.K_f:
                    #frame by frame
                    self.framebyframe = True

                elif event.key == pygame.K_c:
                    for node in self.GameFlip.Nodes:
                        node.key = 0

                elif event.key == pygame.K_g:
                    #toggle grid
                    if self.showGrid:
                        self.showGrid = False

                    else:
                        self.showGrid = True

                elif event.key == pygame.K_s:
                    self.GameFlip.save("StarWarsCell")
                    self.GameFlip.save("StarWarsCellBackup")
                    
                elif event.key == pygame.K_l:
                    try:
                        self.GameFlip = self.GameFlip.load("StarWarsCell")

                    except:
                        self.GameFlip = self.GameFlip.load("StarWarsCellBackup")
                    self.Game.transmit(self.GameFlip)
                    self.Game.NodesData = self.GameFlip.NodesData
                    self.Game.sizeX, self.Game.sizeY, self.Game.size = self.GameFlip.sizeX, self.GameFlip.sizeY, self.GameFlip.size

                elif event.key == pygame.K_ESCAPE:
                    #exit
                    pygame.display.quit(), sys.exit()

            elif event.type == pygame.QUIT:
                #exit
                pygame.display.quit(), sys.exit()

    def draw(self):
        #draws everything onto the screen

        #draws cells onto the screen
        for node in self.GameFlip.Nodes:
            if self.GameFlip.get(node.Xm, node.Ym).key == 1:
                pygame.draw.rect(self.screen, self.cellColors[1], ((node.Xm - 1) * self.gridSize, (node.Ym - 1) * self.gridSize, self.gridSize, self.gridSize))

            elif self.GameFlip.get(node.Xm, node.Ym).key == 2:
                pygame.draw.rect(self.screen, self.cellColors[2], ((node.Xm - 1) * self.gridSize, (node.Ym - 1) * self.gridSize, self.gridSize, self.gridSize))

            elif self.GameFlip.get(node.Xm, node.Ym).key == 3:
                pygame.draw.rect(self.screen, self.cellColors[3], ((node.Xm - 1) * self.gridSize, (node.Ym - 1) * self.gridSize, self.gridSize, self.gridSize))

        #draws the grid
        if self.showGrid:
            for column in range(1, self.width):
                pygame.draw.line(self.screen, "gray", (column * self.gridSize, 0), (column * self.gridSize, self.height * self.gridSize))

            for row in range(1, self.height):
                pygame.draw.line(self.screen, "gray", (0, row * self.gridSize), (self.width * self.gridSize, row * self.gridSize))

Game = GameC()
def main():
    pygame.mixer.music.load("GameAttributesAndData/Thanks.mp3")

    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(3)
    try:
        Game.GameFlip = Game.GameFlip.load("StarWarsCell")

    except:
        Game.GameFlip = Game.GameFlip.load("StarWarsCellBackup")
    Game.Game.transmit(Game.GameFlip)
    Game.Game.NodesData = Game.GameFlip.NodesData
    Game.Game.sizeX, Game.Game.sizeY, Game.Game.size = Game.GameFlip.sizeX, Game.GameFlip.sizeY, Game.GameFlip.size
    #Game loop
    while True:
        clock.tick(70)
        Game.screen.fill(Game.cellColors[0])
        if Game.isRunning or Game.framebyframe:
            Game.update()

        Game.draw()
        Game.eventHandler()
        pygame.display.flip()

if __name__ == '__main__':
    main()