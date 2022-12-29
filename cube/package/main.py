from array import array

import js

import arcade
import arcade.gl

VERTEX_SOURCE = """
    precision highp float;
    attribute vec4 aVertexPosition;
    attribute vec4 aVertexColor;
    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;
    varying lowp vec4 vColor;
    void main(void) {
        gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
        vColor = aVertexColor;
    }
"""

FRAGMENT_SOURCE = """
precision highp float;
varying lowp vec4 vColor;
void main(void) {
    gl_FragColor = vColor;
}
"""

CUBE_POSITIONS = array("f", [
    -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, # Front face
    -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, # Back face
    -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, # Top face
    -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, # Bottom face
    1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, # Right face
    -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, # Left face
])

CUBE_COLORS = array("f", [
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 1.0,
    0.0, 0.0, 1.0, 1.0,
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 0.0, 1.0,
    1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0
])

CUBE_INDICES = array("h", [
    0, 1, 2, 0, 2, 3, # front
    4, 5, 6, 4, 6, 7, # back
    8, 9, 10, 8, 10, 11, # top
    12, 13, 14, 12, 14, 15, # bottom
    16, 17, 18, 16, 18, 19, # right
    20, 21, 22, 20, 22, 23, # left
])

class Game(arcade.Window):
    def __init__(self):
        super().__init__("Cube", 800, 600)

        self.cube_program = self.context.program(
            vertex_shader=VERTEX_SOURCE, fragment_shader=FRAGMENT_SOURCE
        )

        self.gl = self.context.gl

        self.buffers = self.init_buffers()

        self.program_info = {
            "program": self.cube_program._glo,
            "attribLocations": {
                "vertexPosition": self.gl.getAttribLocation(self.cube_program._glo, "aVertexPosition"),
                "vertexColor": self.gl.getAttribLocation(self.cube_program._glo, "aVertexColor"),
            },
            "uniformLocations": {
                "projectionMatrix": self.gl.getUniformLocation(self.cube_program._glo, "uProjectionMatrix"),
                "modelViewMatrix": self.gl.getUniformLocation(self.cube_program._glo, "uModelViewMatrix"),
            },
        }

        self.cube_rotation = 0

    def init_buffers(self):
        return {
            "position": arcade.gl.Buffer(self.context, CUBE_POSITIONS),
            "color": arcade.gl.Buffer(self.context, CUBE_COLORS),
            "index": arcade.gl.Buffer(self.context, CUBE_INDICES, arcade.gl.ELEMENT_ARRAY_BUFFER),
        }

    def on_update(self, delta_time):
        self.cube_rotation = self.cube_rotation + delta_time

    def on_draw(self):
        self.clear()

        num_components = 3
        type = self.gl.FLOAT
        normalize = False
        stride = 0
        offset = 0
        self.gl.bindBuffer(self.gl.ARRAY_BUFFER, self.buffers["position"]._glo)
        self.gl.vertexAttribPointer(
            self.program_info["attribLocations"]["vertexPosition"],
            num_components,
            type,
            normalize,
            stride,
            offset
        )
        self.gl.enableVertexAttribArray(self.program_info["attribLocations"]["vertexPosition"])

        num_components = 4
        type = self.gl.FLOAT
        normalize = False
        stride = 0
        offset = 0
        self.gl.bindBuffer(self.gl.ARRAY_BUFFER, self.buffers["color"]._glo)
        self.gl.vertexAttribPointer(
            self.program_info["attribLocations"]["vertexColor"],
            num_components,
            type,
            normalize,
            stride,
            offset
        )
        self.gl.enableVertexAttribArray(self.program_info["attribLocations"]["vertexColor"])

        self.gl.bindBuffer(self.gl.ELEMENT_ARRAY_BUFFER, self.buffers["index"]._glo)

        # This section will not work from Python for some reason, it's in extra.js
        js.useProgram(self.gl, self.program_info)
        js.doProjection(self.gl, self.program_info)
        js.doModelView(self.gl, self.program_info, self.cube_rotation)

        vertex_count = 36
        type = self.gl.UNSIGNED_SHORT
        offset = 0
        self.gl.drawElements(self.gl.TRIANGLES, vertex_count, type, offset)


def run():
    game = Game()
    arcade.run()
