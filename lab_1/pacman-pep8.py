import pygame
import numpy as np
import tcod
import random
from enum import Enum


class Direction(Enum):
    """Enum representing the possible directions for movement."""
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    NONE = 4


def translate_screen_to_maze(in_coords, in_size=32):
    """Translate screen coordinates to maze coordinates.

    Args:
        in_coords (tuple): Screen coordinates (x, y).
        in_size (int): Size of each cell in the maze.

    Returns:
        tuple: Translated maze coordinates (maze_x, maze_y).
    """
    return int(in_coords[0] / in_size), int(in_coords[1] / in_size)


def translate_maze_to_screen(in_coords, in_size=32):
    """Translate maze coordinates to screen coordinates.

    Args:
        in_coords (tuple): Maze coordinates (maze_x, maze_y).
        in_size (int): Size of each cell in the maze.

    Returns:
        tuple: Translated screen coordinates (screen_x, screen_y).
    """
    return in_coords[0] * in_size, in_coords[1] * in_size


class GameObject:
    """Base class for all game objects in the Pacman game."""

    def __init__(
            self, 
            in_surface, 
            x, y, 
            in_size: int, in_color=(255, 0, 0), 
            is_circle: bool = False):
        """Returns a game object.

        Args:
            in_surface: The surface on which the object will be drawn.
            x (int): The x-coordinate of the object.
            y (int): The y-coordinate of the object.
            in_size (int): The size of the object.
            in_color (tuple): The color of the object (RGB).
            is_circle (bool): Whether the object is circular.
        """
        self._size = in_size
        self._renderer: GameRenderer = in_surface
        self._surface = in_surface._screen
        self.y = y
        self.x = x
        self._color = in_color
        self._circle = is_circle
        self._shape = pygame.Rect(self.x, self.y, in_size, in_size)

    def draw(self):
        """Draw the game object on the surface."""
        if self._circle:
            pygame.draw.circle(
                self._surface, 
                self._color, 
                (self.x, self.y), 
                self._size)
        else:
            rect_object = pygame.Rect(
                self.x, self.y, 
                self._size, self._size)
            pygame.draw.rect(
                self._surface, 
                self._color, 
                rect_object, 
                border_radius=4)

    def tick(self):
        """Update the game object state 
        (to be implemented in subclasses)."""
        pass

    def get_shape(self):
        """Get the shape of the game object.

        Returns:
            pygame.Rect: The shape of the game object.
        """
        return self._shape

    def set_position(self, in_x, in_y):
        """Set the position of the game object.

        Args:
            in_x (int): The new x-coordinate.
            in_y (int): The new y-coordinate.
        """
        self.x = in_x
        self.y = in_y

    def get_position(self):
        """Get the current position of the game object.

        Returns:
            tuple: The current position (x, y).
        """
        return self.x, self.y


class Wall(GameObject):
    """Class representing a wall in the maze."""

    def __init__(self, in_surface, x, y, in_size: int, in_color=(0, 0, 255)):
        """Returns a wall object.

        Args:
            in_surface: The surface on which the wall will be drawn.
            x (int): The x-coordinate of the wall.
            y (int): The y-coordinate of the wall.
            in_size (int): The size of the wall.
            in_color (tuple): The color of the wall (RGB).
        """
        super().__init__(in_surface, x * in_size, y * in_size, in_size, in_color)


class GameRenderer:
    """Class responsible for rendering the game objects on the screen."""

    def __init__(self, in_width: int, in_height: int):
        """Returns the game renderer.

        Args:
            in_width (int): The width of the game window.
            in_height (int): The height of the game window.
        """
        pygame.init()
        self._width = in_width
        self._height = in_height
        self._screen = pygame.display.set_mode((in_width, in_height))
        pygame.display.set_caption('Pacman')
        self._clock = pygame.time.Clock()
        self._done = False
        self._game_objects = []
        self._walls = []
        self._cookies = []
        self._hero: Hero = None

    def tick(self, in_fps: int):
        """Update the game state and render the objects.

        Args:
            in_fps (int): Frames per second for the game loop.
        """
        black = (0, 0, 0)
        while not self._done:
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()

            pygame.display.flip()
            self._clock.tick(in_fps)
            self._screen.fill(black)
            self._handle_events()
        print("Game over")

    def add_game_object(self, obj: GameObject):
        """Add a game object to the renderer.

        Args:
            obj (GameObject): The game object to add.
        """
        self._game_objects.append(obj)

    def add_cookie(self, obj: GameObject):
        """Add a cookie object to the renderer.

        Args:
            obj (GameObject): The cookie object to add.
        """
        self._game_objects.append(obj)
        self._cookies.append(obj)

    def add_wall(self, obj: Wall):
        """Add a wall object to the renderer.

        Args:
            obj (Wall): The wall object to add.
        """
        self.add_game_object(obj)
        self._walls.append(obj)

    def get_walls(self):
        """Get the list of walls in the game.

        Returns:
            list: List of wall objects.
        """
        return self._walls

    def get_cookies(self):
        """Get the list of cookies in the game.

        Returns:
            list: List of cookie objects.
        """
        return self._cookies

    def get_game_objects(self):
        """Get the list of all game objects.

        Returns:
            list: List of all game objects.
        """
        return self._game_objects

    def add_hero(self, in_hero):
        """Add the hero object to the renderer.

        Args:
            in_hero: The hero object to add.
        """
        self.add_game_object(in_hero)
        self._hero = in_hero

    def _handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self._hero.set_direction(Direction.UP)
        elif pressed[pygame.K_LEFT]:
            self._hero.set_direction(Direction.LEFT)
        elif pressed[pygame.K_DOWN]:
            self._hero.set_direction(Direction.DOWN)
        elif pressed[pygame.K_RIGHT]:
            self._hero.set_direction(Direction.RIGHT)


class MovableObject(GameObject):
    """Class representing a movable object in the game."""

    def __init__(
            self, 
            in_surface, 
            x, y, 
            in_size: int, in_color=(255, 0, 0), 
            is_circle: bool = False):
        """Returns a movable object.

        Args:
            in_surface: The surface on which the object will be drawn.
            x (int): The x-coordinate of the object.
            y (int): The y-coordinate of the object.
            in_size (int): The size of the object.
            in_color (tuple): The color of the object (RGB).
            is_circle (bool): Whether the object is circular.
        """
        super().__init__(in_surface, x, y, in_size, in_color, is_circle)
        self.current_direction = Direction.NONE
        self.direction_buffer = Direction.NONE
        self.last_working_direction = Direction.NONE
        self.location_queue = []
        self.next_target = None

    def get_next_location(self):
        """Get the next location from the movement queue.

        Returns:
            tuple: The next location (x, y) or None if the queue is empty.
        """
        if len(self.location_queue) == 0: return None
        else: self.location_queue.pop(0)

    def set_direction(self, in_direction):
        """Set the current direction of movement.

        Args:
            in_direction (Direction): The direction to set.
        """
        self.current_direction = in_direction
        self.direction_buffer = in_direction

    def collides_with_wall(self, in_position):
        """Check if the object collides with any wall.

        Args:
            in_position (tuple): The position to check (x, y).

        Returns:
            bool: True if there is a collision, False otherwise.
        """
        collision_rect = pygame.Rect(
            in_position[0], 
            in_position[1], 
            self._size, 
            self._size)
        collides = False
        walls = self._renderer.get_walls()
        for wall in walls:
            collides = collision_rect.colliderect(wall.get_shape())
            if collides:
                break
        return collides

    def check_collision_in_direction(self, in_direction: Direction):
        """Check for collision in the specified direction.

        Args:
            in_direction (Direction): The direction to check.

        Returns:
            tuple: A tuple containing a boolean 
            indicating collision and the desired position.
        """
        desired_position = (0, 0)
        if in_direction == Direction.NONE:
            return False, desired_position
        if in_direction == Direction.UP:
            desired_position = (self.x, self.y - 1)
        elif in_direction == Direction.DOWN:
            desired_position = (self.x, self.y + 1)
        elif in_direction == Direction.LEFT:
            desired_position = (self.x - 1, self.y)
        elif in_direction == Direction.RIGHT:
            desired_position = (self.x + 1, self.y)

        return self.collides_with_wall(desired_position), desired_position

    def automatic_move(self, in_direction: Direction):
        """Automatically move the object in the specified direction.

        Args:
            in_direction (Direction): The direction to move in.
        """
        pass

    def tick(self):
        """Update the object's state and handle movement."""
        self.reached_target()
        self.automatic_move(self.current_direction)

    def reached_target(self):
        """Handle logic when the object reaches its target 
        (to be implemented in subclasses)."""
        pass


class Hero(MovableObject):
    """Class representing the hero character in the game."""

    def __init__(self, in_surface, x, y, in_size: int):
        """Returns the hero object.

        Args:
            in_surface: The surface on which the hero will be drawn.
            x (int): The x-coordinate of the hero.
            y (int): The y-coordinate of the hero.
            in_size (int): The size of the hero.
        """
        super().__init__(in_surface, x, y, in_size, (255, 255, 0), False)
        self.last_non_colliding_position = (0, 0)

    def tick(self):
        """Update the hero's state and handle movement."""
        # TELEPORT
        if self.x < 0:
            self.x = self._renderer._width

        if self.x > self._renderer._width:
            self.x = 0

        self.last_non_colliding_position = self.get_position()

        if self.check_collision_in_direction(self.direction_buffer)[0]:
            self.automatic_move(self.current_direction)
        else:
            self.automatic_move(self.direction_buffer)
            self.current_direction = self.direction_buffer

        if self.collides_with_wall((self.x, self.y)):
            self.set_position(
                self.last_non_colliding_position[0], 
                self.last_non_colliding_position[1])

        self.handle_cookie_pickup()

    def automatic_move(self, in_direction: Direction):
        """Automatically move the hero in the specified direction.

        Args:
            in_direction (Direction): The direction to move in.
        """
        collision_result = self.check_collision_in_direction(in_direction)

        desired_position_collides = collision_result[0]
        if not desired_position_collides:
            self.last_working_direction = self.current_direction
            desired_position = collision_result[1]
            self.set_position(desired_position[0], desired_position[1])
        else:
            self.current_direction = self.last_working_direction

    def handle_cookie_pickup(self):
        """Handle the logic for picking up cookies."""
        collision_rect = pygame.Rect(self.x, self.y, self._size, self._size)
        cookies = self._renderer.get_cookies()
        game_objects = self._renderer.get_game_objects()
        for cookie in cookies:
            collides = collision_rect.colliderect(cookie.get_shape())
            if collides and cookie in game_objects:
                game_objects.remove(cookie)

    def draw(self):
        """Draw the hero on the surface."""
        half_size = self._size / 2
        pygame.draw.circle(
            self._surface, 
            self._color, 
            (self.x + half_size, self.y + half_size), 
            half_size)


class Ghost(MovableObject):
    """Class representing a ghost in the game."""

    def __init__(
            self, 
            in_surface, 
            x, y, 
            in_size: int, 
            in_game_controller, 
            in_color=(255, 0, 0)):
        """Returns a ghost object.

        Args:
            in_surface: The surface on which the ghost will be drawn.
            x (int): The x-coordinate of the ghost.
            y (int): The y-coordinate of the ghost.
            in_size (int): The size of the ghost.
            in_game_controller: The game controller 
                managing the ghost's behavior.
            in_color (tuple): The color of the ghost (RGB).
        """
        super().__init__(in_surface, x, y, in_size, in_color, False)
        self.game_controller = in_game_controller

    def reached_target(self):
        """Handle logic when the ghost reaches its target."""
        if (self.x, self.y) == self.next_target:
            self.next_target = self.get_next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def set_new_path(self, in_path):
        """Set a new path for the ghost to follow.

        Args:
            in_path (list): The new path as a list of (x, y) tuples.
        """
        for item in in_path:
            self.location_queue.append(item)
        self.next_target = self.get_next_location()

    def calculate_direction_to_next_target(self) -> Direction:
        """Calculate the direction to the next target.

        Returns:
            Direction: The direction towards the next target.
        """
        if self.next_target is None:
            self.game_controller.request_new_random_path(self)
            return Direction.NONE
        diff_x = self.next_target[0] - self.x
        diff_y = self.next_target[1] - self.y
        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT
        self.game_controller.request_new_random_path(self)
        return Direction.NONE

    def automatic_move(self, in_direction: Direction):
        """Automatically move the ghost in the specified direction.

        Args:
            in_direction (Direction): The direction to move in.
        """
        if in_direction == Direction.UP:
            self.set_position(self.x, self.y - 1)
        elif in_direction == Direction.DOWN:
            self.set_position(self.x, self.y + 1)
        elif in_direction == Direction.LEFT:
            self.set_position(self.x - 1, self.y)
        elif in_direction == Direction.RIGHT:
            self.set_position(self.x + 1, self.y)


class Cookie(GameObject):
    """Class representing a cookie in the game."""

    def __init__(self, in_surface, x, y):
        """Returns a cookie object.

        Args:
            in_surface: The surface on which the cookie will be drawn.
            x (int): The x-coordinate of the cookie.
            y (int): The y-coordinate of the cookie.
        """
        super().__init__(in_surface, x, y, 4, (255, 255, 0), True)


class Pathfinder:
    """Class for calculating paths in the maze using A* algorithm."""

    def __init__(self, in_arr):
        """Returns the pathfinder.

        Args:
            in_arr (list): The maze represented as a 2D array.
        """
        cost = np.array(in_arr, dtype=np.bool_).tolist()
        self.pf = tcod.path.AStar(cost=cost, diagonal=0)

    def get_path(self, from_x, from_y, to_x, to_y) -> object:
        """Get the path from one point to another.

        Args:
            from_x (int): Starting x-coordinate.
            from_y (int): Starting y-coordinate.
            to_x (int): Target x-coordinate.
            to_y (int): Target y-coordinate.

        Returns:
            list: List of (x, y) tuples representing the path.
        """
        res = self.pf.get_path(from_x, from_y, to_x, to_y)
        return [(sub[1], sub[0]) for sub in res]

class PacmanGameController:
    """
    Class that manages the Pacman game.

    This class is responsible for initializing the game, creating the maze,
    controlling the ghosts, and handling collisions with cookies.
    """

    def __init__(self):
        """
        Initializes the Pacman game controller.

        Creates an ASCII maze, converts it into a numpy array,
        initializes paths for the ghosts, and defines available spaces.
        """
        self.ascii_maze = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XP           XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X                          X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X XXXX XX XXXXXXXX XX XXXX X",
            "X      XX    XX    XX      X",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XXXXX XX XXXXX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX X   G  X XX XXXXXX",
            "          X G    X          ",
            "XXXXXX XX X   G  X XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX          XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "XXXXXX XX XXXXXXXX XX XXXXXX",
            "X            XX            X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X XXXX XXXXX XX XXXXX XXXX X",
            "X   XX       G        XX   X",
            "XXX XX XX XXXXXXXX XX XX XXX",
            "XXX XX XX XXXXXXXX XX XX XXX",
            "X      XX    XX    XX      X",
            "X XXXXXXXXXX XX XXXXXXXXXX X",
            "X XXXXXXXXXX XX XXXXXXXXXX X",
            "X                          X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]

        self.numpy_maze = []
        self.cookie_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.ghost_colors = [
            (255, 184, 255),
            (255, 0, 20),
            (0, 255, 255),
            (255, 184, 82)
        ]
        self.size = (0, 0)
        self.convert_maze_to_numpy()
        self.p = Pathfinder(self.numpy_maze)

    def request_new_random_path(self, in_ghost: Ghost):
        """
        Requests a new random path for the ghost.

        Chooses a random available space and computes the path
        from the ghost's current position to the chosen space.

        :param in_ghost: The ghost object that needs to have a new path set.
        """
        random_space = random.choice(self.reachable_spaces)
        current_maze_coord = translate_screen_to_maze(in_ghost.get_position())

        path = self.p.get_path(current_maze_coord[1], 
                               current_maze_coord[0], 
                               random_space[1],
                               random_space[0])
        test_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.set_new_path(test_path)

    def convert_maze_to_numpy(self):
        """
        Converts the ASCII maze into a numpy array.

        Creates a binary representation of the maze, determines
        available spaces, and identifies ghost spawn locations.
        """
        for x, row in enumerate(self.ascii_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):
                if column == "G":
                    self.ghost_spawns.append((y, x))

                if column == "X":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
            self.numpy_maze.append(binary_row)


if __name__ == "__main__":
    unified_size = 32
    pacman_game = PacmanGameController()
    size = pacman_game.size
    game_renderer = GameRenderer(
        size[0] * unified_size, 
        size[1] * unified_size)

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game_renderer.add_wall(Wall(
                    game_renderer, 
                    x, y, 
                    unified_size))
    
    for cookie_space in pacman_game.cookie_spaces:
        translated = translate_maze_to_screen(cookie_space)
        cookie = Cookie(
            game_renderer, 
            translated[0] + unified_size / 2, 
            translated[1] + unified_size / 2
        )
        game_renderer.add_cookie(cookie)

    for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
        translated = translate_maze_to_screen(ghost_spawn)
        ghost = Ghost(game_renderer, 
                      translated[0], 
                      translated[1], 
                      unified_size, 
                      pacman_game,
                      pacman_game.ghost_colors[i % 4])
        game_renderer.add_game_object(ghost)

    pacman = Hero(game_renderer, unified_size, unified_size, unified_size)
    game_renderer.add_hero(pacman)
    game_renderer.tick(120)