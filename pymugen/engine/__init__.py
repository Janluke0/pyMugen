import arcade, os 
from ..formats.sff import SFF
from ..formats.air import from_file, LOOP_START
from PIL import Image
from functools import cmp_to_key

_DBG = True

SPRITE_SCALING = 3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move Sprite with Keyboard Example"

MOVEMENT_SPEED = 5
arcade.Texture

class Player(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.sff = SFF("../../tests/test_data/kfm/kfmv1.sff")
        #20 is walking animation
        t = from_file("../../tests/test_data/kfm/kfm.air", "utf-8-sig") 
        self._actions = next((a for a in t if a.code==0)), next((a for a in t if a.code==20))
        self._action = self._actions[0]
        self._frame_pointer = 0

        self._texture_map = {}
        frame = self._action.animation_elements[0]
        t = frame.group_number, frame.image_number
        self._texture_map[t] = len(self.textures)
        self.append_texture(arcade.Texture(f"spr_{t[0]}-{t[1]}", self.sff.get_image(*t,use_PIL=True)))
        self.texture = self.textures[0]

        self._texture_ticks = 0
        self.mirrored = False
        self.fixed_width, self.fixed_height = self.width, self.height

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

        if self.velocity[0] == .0 and self.velocity[1] == .0:
            if self._action != self._actions[0]:
                self._frame_pointer = 0
            self._action = self._actions[0]
        else:
            if self._action != self._actions[1]:
                self._frame_pointer = 0
            self._action = self._actions[1]
        
        
        
        # Figure out if we should face left or right
        if self.change_x < 0:
            self.mirrored = True
        elif self.change_x > 0:
            self.mirrored = False
            
        self.animation_tick()
    
    #def update_animation(self, time_delta):
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

        if t not in self._texture_map:
            img = self.sff.get_image(t[0],t[1],use_PIL=True)
            if self.mirrored:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)

            #FIXME if sprites has different sizes the bigger is shrinked
            # but not the first time (same problem with animation tools) 
            #img = arcade.trim_image(img)
            if False:# img.width < self.fixed_width:
                img = padding(img,(self.fixed_height,self.fixed_width))
            
            self.append_texture(arcade.Texture(f"spr_{t[0]}-{t[1]}{'_m' if self.mirrored else ''}",img))
            #########FIXME: box size looks fine but not positioning 
            boxes = []
            for cb in frame.collision_boxes:
                x0, y0, x2, y2 = cb
                y0, y2 = -y0 - img.height//2, -y2 - img.height//2
                if not self.mirrored:
                    x0, x2 = x0 - img.width//6, x2 - img.width//6
                else:
                    x0, x2 = x0 + img.width//8, x2 + img.width//8
                boxes.append([(x0,y0), (x2,y2)])
            self._texture_map[t] = len(self.textures)-1, merge(boxes)[-1]
            
            #self.center_x = frame.x_offset
            #self.center_y = frame.y_offset
            #########
        self.set_hit_box(self._texture_map[t][1])
        self.set_texture(self._texture_map[t][0])
        

        #print(self.width,self.height)
        #print(self.texture.__dict__)

def padding(old_im, new_size):
    old_size = old_im.size

    print(old_size, new_size)

    new_im = Image.new("RGBA", new_size)   
    new_im.paste(old_im, ((new_size[0]-old_size[0])//2,
                        (new_size[1]-old_size[1])//2))
    return new_im

def merge(boxes):
#https://stackoverflow.com/a/13851341
    points = set()
    for (x1, y1), (x2, y2) in boxes:
        for pt in ((x1, y1), (x2, y1), (x2, y2), (x1, y2)):
            if pt in points: # Shared vertice, remove it.
                points.remove(pt)
            else:
                points.add(pt)
    points = list(points)

    def y_then_x(a, b):
        if a[1] < b[1] or (a[1] == b[1] and a[0] < b[0]):
            return -1
        elif a == b:
            return 0
        else:
            return 1

    sort_x = sorted(points)
    sort_y = sorted(points, key=cmp_to_key(y_then_x))

    edges_h = {}
    edges_v = {}

    i = 0
    while i < len(points):
        curr_y = sort_y[i][1]
        while i < len(points) and sort_y[i][1] == curr_y: #//6chars comments, remove it
            edges_h[sort_y[i]] = sort_y[i + 1]
            edges_h[sort_y[i + 1]] = sort_y[i]
            i += 2
    i = 0
    while i < len(points):
        curr_x = sort_x[i][0]
        while i < len(points) and sort_x[i][0] == curr_x:
            edges_v[sort_x[i]] = sort_x[i + 1]
            edges_v[sort_x[i + 1]] = sort_x[i]
            i += 2

    # Get all the polygons.
    p = []
    while edges_h:
        # We can start with any point.
        polygon = [(edges_h.popitem()[0], 0)]
        while True:
            curr, e = polygon[-1]
            if e == 0:
                next_vertex = edges_v.pop(curr)
                polygon.append((next_vertex, 1))
            else:
                next_vertex = edges_h.pop(curr)
                polygon.append((next_vertex, 0))
            if polygon[-1] == polygon[0]:
                # Closed polygon
                polygon.pop()
                break
        # Remove implementation-markers from the polygon.
        poly = [point for point, _ in polygon]
        for vertex in poly:
            if vertex in edges_h: edges_h.pop(vertex)
            if vertex in edges_v: edges_v.pop(vertex)

        p.append(poly)
    return p


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
        if _DBG:            
            tx_size = 30
            output = f"Action:{str(self.player_list[0]._action.code)}\n"
            output += f"Texture: {self.player_list[0]._frame_pointer}"
            y = SCREEN_WIDTH//2
            arcade.draw_text(output, 5, y, arcade.color.WHITE, tx_size)

        # Draw all the sprites.
        self.player_list.draw()
        self.player_list.draw_hit_boxes((0,255,0))

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            pass#self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            pass#self.player_sprite.change_y = -MOVEMENT_SPEED
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

