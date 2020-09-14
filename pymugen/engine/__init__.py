import arcade, os 
from ..formats.sff import SFF
from ..formats.air import from_file, LOOP_START

SPRITE_SCALING = 3

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite with Keyboard Example"

MOVEMENT_SPEED = 5
arcade.Texture

class Player(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.sff = SFF("../../tests/test_data/android16/android16.sff")
        #20 is walking animation
        self._action = next((a for a in from_file("../../tests/test_data/android16/android16.air", "latin-1") if a.code==20))
        self._frame_pointer = 0

        self._texture_map = {}
        frame = self._action.animation_elements[0]
        t = frame.group_number, frame.image_number
        self._texture_map[t] = len(self.textures)
        self.append_texture(arcade.Texture(f"spr_{t[0]}-{t[1]}", self.sff.get_image(*t,use_PIL=True)))
        self.texture = self.textures[0]

        self._texture_ticks = 0
        self.mirrored = False

    def update(self):
        #print("update")
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

        
        
        # Figure out if we should face left or right
        if self.change_x < 0:
            self.mirrored = True
        elif self.change_x > 0:
            self.mirrored = False
            
        self.animation_tick()

    def animation_tick(self):
        """update self.texture"""
        frame = self._action.animation_elements[self._frame_pointer]
        if frame.time > self._texture_ticks:
            self._texture_ticks += 1
            return 

        self._texture_ticks = 0

        self._frame_pointer +=1
        if self._frame_pointer == len( self._action.animation_elements) -1:
            self._frame_pointer = 0
        frame = self._action.animation_elements[self._frame_pointer]
        t = frame.group_number, frame.image_number, self.mirrored
        from PIL import Image
        if t not in self._texture_map:
            self._texture_map[t] = len(self.textures)
            img = self.sff.get_image(*t,use_PIL=True)
            if self.mirrored:
                #FIXME: loose color on transpose :/
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            self.append_texture(arcade.Texture(f"spr_{t[0]}-{t[1]}{'_m' if self.mirrored else ''}",img))
        self.texture = self.textures[self._texture_map[t]]

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Player(None, SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

