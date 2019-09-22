import abc
import os

from PIL import Image
from PIL import ImageDraw

from pacai.util import util

# TODO(eriq): This should eventually be false.
DEFAULT_SAVE_FRAMES = True
DEFAULT_SAVE_EVERY_N_FRAMES = 3

SQUARE_SIZE = 50

GIF_FPS = 10
GIF_FRAME_DURATION_MS = int(1.0 / GIF_FPS * 1000.0)
GIF_FILENAME = 'test.gif'

# By default, the sprite sheet is adjacent to this file.
DEFAULT_SPRITES = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pacman-sprites.png')

# TODO(eriq): This is specific for the Pacman-style games.
class AbstractView(abc.ABC):
    """
    A abstarct view that represents all the necessary functionality a specific
    view should implement.
    """

    def __init__(self,
            saveFrames = DEFAULT_SAVE_FRAMES, saveEveryNFrames = DEFAULT_SAVE_EVERY_N_FRAMES):
        self._saveFrames = saveFrames
        self._saveEveryNFrames = saveEveryNFrames
        self._frameCount = 0
        self._keyFrames = []

        self._sprites = Frame.loadSpriteSheet(DEFAULT_SPRITES)

    def finish(self):
        """
        Signal that the game is over and the UI should cleanup.
        """

        if (self._saveFrames and len(self._keyFrames) > 0):
            images = [frame.toImage(self._sprites) for frame in self._keyFrames]
            images[0].save(GIF_FILENAME, save_all = True, append_images = images,
                    duration = GIF_FRAME_DURATION_MS, loop = 0, optimize = True)

    def initialize(self, state):
        """
        Perform an initial drawing of the view.
        """

        self.update(state, forceDraw = True)

    def update(self, state, forceDraw = False):
        """
        Materialize the view, given a state.
        """

        if (state.isOver()):
            forceDraw = True

        frame = Frame(state)
        if (state.isOver()
                or (self._saveFrames and self._frameCount % self._saveEveryNFrames == 0)):
            self._keyFrames.append(frame)

        self._drawFrame(state, frame, forceDraw = forceDraw)
        self._frameCount += 1

    @abc.abstractmethod
    def _drawFrame(self, state, frame, forceDraw = False):
        """
        The real work for each view implementation.
        From a frame, output to whatever medium this view utilizes.
        """

        pass

    def pause(self):
        # TODO(eriq): Deprecated. From old interface.
        pass

    def draw(self, state):
        # TODO(eriq): Deprecated. From old interface.
        pass

# Note: Having this outside of Frame is a bit hacky,
# but we need to do it to clear up some static cyclic dependencies.
def _computeWallCode(hasWallN, hasWallE, hasWallS, hasWallW):
    """
    Given information about a wall's cardinal neighbors,
    compute the correct type of wall to use.
    The computation is similar to POSIX permission bits,
    all combinations produce unique sums.
    """

    WALL_BASE = 100

    N_WALL = 1
    E_WALL = 2
    S_WALL = 4
    W_WALL = 8

    code = WALL_BASE

    if (hasWallN):
        code += N_WALL

    if (hasWallE):
        code += E_WALL

    if (hasWallS):
        code += S_WALL

    if (hasWallW):
        code += W_WALL

    return code

# TODO(eriq): Frames can probably be more effiicent with bit packing.
class Frame(object):
    """
    A general representation of that can be seen on-screen at a given time.
    """

    # For the walls, we have a different sprite depending on what sides (lines) are present.
    # An 'X' in the name indicates that a wall is not there.
    # To get the pacman "tubular" look, adjacent walls will look connected
    # and not have a line between them.
    WALL_NESW = _computeWallCode(False, False, False, False)
    WALL_NESX = _computeWallCode(False, False, False, True)
    WALL_NEXW = _computeWallCode(False, False, True,  False)
    WALL_NEXX = _computeWallCode(False, False, True,  True)
    WALL_NXSW = _computeWallCode(False, True,  False, False)
    WALL_NXSX = _computeWallCode(False, True,  False, True)
    WALL_NXXW = _computeWallCode(False, True,  True,  False)
    WALL_NXXX = _computeWallCode(False, True,  True,  True)
    WALL_XESW = _computeWallCode(True,  False, False, False)
    WALL_XESX = _computeWallCode(True,  False, False, True)
    WALL_XEXW = _computeWallCode(True,  False, True,  False)
    WALL_XEXX = _computeWallCode(True,  False, True,  True)
    WALL_XXSW = _computeWallCode(True,  True,  False, False)
    WALL_XXSX = _computeWallCode(True,  True,  False, True)
    WALL_XXXW = _computeWallCode(True,  True,  True,  False)
    WALL_XXXX = _computeWallCode(True,  True,  True,  True)


    # Token to mark what can occupy different locations.
    EMPTY = 0
    WALL = 1
    FOOD = 2
    CAPSULE = 3
    PACMAN_1 = 10
    PACMAN_2 = 11
    PACMAN_3 = 12
    PACMAN_4 = 13
    PACMAN_5 = 14
    PACMAN_6 = 15
    GHOST_1 = 20
    GHOST_2 = 21
    GHOST_3 = 22
    GHOST_4 = 23
    GHOST_5 = 24
    GHOST_6 = 25
    SCARED_GHOST = 30

    def __init__(self, state):
        self._height = state.getInitialLayout().getHeight()
        self._width = state.getInitialLayout().getWidth()

        # All items on the board are at integral potision.
        self._board = self._buildBoard(state)

        # Agents may not be at integral positions, so they are represented independently.
        self._agentTokens = self._getAgentTokens(state)

    def getAgents(self):
        return self._agentTokens

    def getDiscreteAgents(self):
        """
        Get the agentTokens, but with interger positions.
        """

        agentTokens = {}

        for (position, agent) in self._agentTokens.items():
            agentTokens[util.nearestPoint(position)] = agent

        return agentTokens

    def getHeight(self):
        return self._height

    def getToken(self, x, y):
        return self._board[x][y]

    def getCol(self, x):
        return self._board[x]

    def getWidth(self):
        return self._width

    @staticmethod
    def isGhost(token):
        return token >= Frame.GHOST_1 and token <= Frame.GHOST_6

    @staticmethod
    def isPacman(token):
        return token >= Frame.PACMAN_1 and token <= Frame.PACMAN_6

    @staticmethod
    def isWall(token):
        return token >= Frame.WALL_NESW and token <= Frame.WALL_XXXX

    @staticmethod
    def loadSpriteSheet(path):
        spritesheet = Image.open(path)

        sprites = {
            Frame.PACMAN_1: Frame._cropSprite(spritesheet, 0, 0),
            Frame.GHOST_1: Frame._cropSprite(spritesheet, 1, 0),
            Frame.GHOST_2: Frame._cropSprite(spritesheet, 2, 0),
            Frame.SCARED_GHOST: Frame._cropSprite(spritesheet, 3, 0),
            Frame.FOOD: Frame._cropSprite(spritesheet, 4, 0),
            Frame.CAPSULE: Frame._cropSprite(spritesheet, 5, 0),

            Frame.WALL_NESW: Frame._cropSprite(spritesheet, 6, 0),
            Frame.WALL_NESX: Frame._cropSprite(spritesheet, 6, 1),
            Frame.WALL_NEXW: Frame._cropSprite(spritesheet, 6, 2),
            Frame.WALL_NEXX: Frame._cropSprite(spritesheet, 6, 3),
            Frame.WALL_NXSW: Frame._cropSprite(spritesheet, 7, 0),
            Frame.WALL_NXSX: Frame._cropSprite(spritesheet, 7, 1),
            Frame.WALL_NXXW: Frame._cropSprite(spritesheet, 7, 2),
            Frame.WALL_NXXX: Frame._cropSprite(spritesheet, 7, 3),
            Frame.WALL_XESW: Frame._cropSprite(spritesheet, 8, 0),
            Frame.WALL_XESX: Frame._cropSprite(spritesheet, 8, 1),
            Frame.WALL_XEXW: Frame._cropSprite(spritesheet, 8, 2),
            Frame.WALL_XEXX: Frame._cropSprite(spritesheet, 8, 3),
            Frame.WALL_XXSW: Frame._cropSprite(spritesheet, 9, 0),
            Frame.WALL_XXSX: Frame._cropSprite(spritesheet, 9, 1),
            Frame.WALL_XXXW: Frame._cropSprite(spritesheet, 9, 2),
            Frame.WALL_XXXX: Frame._cropSprite(spritesheet, 9, 3),
        }

        return sprites

    @staticmethod
    def _cropSprite(spritesheet, row, col):
        # (left, upper, right, lower)
        rectangle = (
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
            (col + 1) * SQUARE_SIZE,
            (row + 1) * SQUARE_SIZE,
        )

        return spritesheet.crop(rectangle)

    def _buildBoard(self, state):
        board = self._width * [None]
        for x in range(self._width):

            items = self._height * [Frame.EMPTY]
            for y in range(self._height):
                if (state.hasWall(x, y)):
                    items[y] = self._getWallToken(x, y, state)
                elif (state.hasFood(x, y)):
                    items[y] = Frame.FOOD
                elif (state.hasCapsule(x, y)):
                    items[y] = Frame.CAPSULE

            board[x] = items

        return board

    def _getWallToken(self, x, y, state):
        hasWallN = False
        hasWallE = False
        hasWallS = False
        hasWallW = False

        if (y != self._height - 1):
            hasWallN = state.hasWall(x, y + 1)

        if (x != self._width - 1):
            hasWallE = state.hasWall(x + 1, y)

        if (y != 0):
            hasWallS = state.hasWall(x, y - 1)

        if (x != 0):
            hasWallW = state.hasWall(x - 1, y)

        return _computeWallCode(hasWallN, hasWallE, hasWallS, hasWallW)

    def _getAgentTokens(self, state):
        """
        Returns: {(x, y): token, ...}
        """

        tokens = {}

        for agentIndex in range(state.getNumAgents()):
            agentState = state.getAgentState(agentIndex)
            position = agentState.getPosition()

            if (agentState.isPacman()):
                tokens[position] = Frame.PACMAN_1
            elif (agentState.isScaredGhost()):
                tokens[position] = Frame.SCARED_GHOST
            else:
                tokens[position] = Frame.GHOST_1 + (agentIndex - 1)

        return tokens

    def toImage(self, sprites = {}):
        image = Image.new('RGB', (self._width * SQUARE_SIZE, self._height * SQUARE_SIZE))
        draw = ImageDraw.Draw(image)

        # First, draw the board.
        for x in range(self._width):
            for y in range(self._height):
                self._placeToken(x, y, self._board[x][y], sprites, image, draw)

        # Now, overlay the agents.
        for ((x, y), agentToken) in self._agentTokens.items():
            self._placeToken(x, y, agentToken, sprites, image, draw)

        return image

    def _placeToken(self, x, y, token, sprites, image, draw):
        startPoint = self._toImageCoords(x, y)
        endPoint = self._toImageCoords(x + 1, y - 1)

        if (token in sprites):
            image.paste(sprites[token], startPoint, sprites[token])
        else:
            color = self._tokenToColor(token)
            draw.rectangle([startPoint, endPoint], fill = color)

    def _toImageCoords(self, x, y):
        # PIL has (0, 0) as the upper-left, while pacai has it as the lower-left.
        return (int(x * SQUARE_SIZE), int((self._height - 1 - y) * SQUARE_SIZE))

    def _tokenToColor(self, token):
        if (token == Frame.EMPTY):
            return (0, 0, 0)
        if (self.isWall(token)):
            return (0, 51, 255)
        if (token == Frame.FOOD):
            return (255, 255, 255)
        elif (token == Frame.CAPSULE):
            return (255, 0, 255)
        elif (self.isGhost(token)):
            return (229, 0, 0)
        elif (self.isPacman(token)):
            return (255, 255, 61)
        elif (token == Frame.SCARED_GHOST):
            return (0, 255, 0)
        else:
            return (0, 0, 0)
