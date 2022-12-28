import js

import arcade

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

    def init_position_buffer(self):
        position_buffer = self.gl.createBuffer()
        self.gl.bindBuffer(self.gl.ARRAY_BUFFER, position_buffer)
        positions = [
            -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, # Front face
            -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, # Back face
            -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, # Top face
            -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, # Bottom face
            1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, # Right face
            -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, # Left face
        ]
        self.gl.bufferData(self.gl.ARRAY_BUFFER, js.Float32Array.new(positions), self.gl.STATIC_DRAW)
        return position_buffer


    def init_color_buffer(self):
        color_buffer = self.gl.createBuffer()
        self.gl.bindBuffer(self.gl.ARRAY_BUFFER, color_buffer)
        colors = [
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
        ]
        self.gl.bufferData(self.gl.ARRAY_BUFFER, js.Float32Array.new(colors), self.gl.STATIC_DRAW)
        return color_buffer


    def init_index_buffer(self):
        indices_buffer = self.gl.createBuffer()
        self.gl.bindBuffer(self.gl.ELEMENT_ARRAY_BUFFER, indices_buffer)
        indices = [
            0, 1, 2, 0, 2, 3, # front
            4, 5, 6, 4, 6, 7, # back
            8, 9, 10, 8, 10, 11, # top
            12, 13, 14, 12, 14, 15, # bottom
            16, 17, 18, 16, 18, 19, # right
            20, 21, 22, 20, 22, 23, # left
        ]
        self.gl.bufferData(self.gl.ELEMENT_ARRAY_BUFFER, js.Uint16Array.new(indices), self.gl.STATIC_DRAW)
        return indices_buffer


    def init_buffers(self):
        return {
            "position": self.init_position_buffer(),
            "color": self.init_color_buffer(),
            "index": self.init_index_buffer(),
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
        self.gl.bindBuffer(self.gl.ARRAY_BUFFER, self.buffers["position"])
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
        self.gl.bindBuffer(self.gl.ARRAY_BUFFER, self.buffers["color"])
        self.gl.vertexAttribPointer(
            self.program_info["attribLocations"]["vertexColor"],
            num_components,
            type,
            normalize,
            stride,
            offset
        )
        self.gl.enableVertexAttribArray(self.program_info["attribLocations"]["vertexColor"])

        self.gl.bindBuffer(self.gl.ELEMENT_ARRAY_BUFFER, self.buffers["index"])

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
