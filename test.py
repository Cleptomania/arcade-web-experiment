import math

from js import mat4, to_f32, to_ui16
from pyodide.ffi import to_js

import arcade

VERTEX_SOURCE = """
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
    varying lowp vec4 vColor;

    void main(void) {
        gl_FragColor = vColor;
    }
"""


class Game(arcade.Window):
    def __init__(self):
        super().__init__("mycanvas", 800, 600)
        self.context.create_shader("square", VERTEX_SOURCE, FRAGMENT_SOURCE)
        self.position_buffer = None
        self.color_buffer = None
        self.indices_buffer = None
        self.cube_rotation = 0.0

    def setup(self):
        gl = self.context.gl

        self.position_buffer = gl.createBuffer()
        gl.bindBuffer(gl.ARRAY_BUFFER, self.position_buffer)
        positions = [
            -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0,
            -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0,
            -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0,
            -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0,
            1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0,
            -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0,  
        ]
        gl.bufferData(gl.ARRAY_BUFFER, to_f32(to_js(positions)), gl.STATIC_DRAW)

        self.color_buffer = gl.createBuffer()
        gl.bindBuffer(gl.ARRAY_BUFFER, self.color_buffer)
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
            1.0, 0.0, 1.0, 1.0,
        ]
        gl.bufferData(gl.ARRAY_BUFFER, to_f32(to_js(colors)), gl.STATIC_DRAW)

        self.indices_buffer = gl.createBuffer()
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, self.indices_buffer)
        indices = [
            0, 1, 2, 0, 2, 3,
            4, 5, 6, 4, 6, 7,
            8, 9, 10, 8, 10, 11,
            12, 13, 14, 12, 14, 15,
            16, 17, 18, 16, 18, 19,
            20, 21, 22, 20, 22, 23,
        ]
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, to_ui16(to_js(indices)), gl.STATIC_DRAW)

    def on_draw(self):
        self.clear()

        gl = self.context.gl

        program = self.context.shader_programs["square"]

        # Calculate project/modelview matrix
        fov = (45 * math.pi) / 180
        aspect = self.width / self.height
        znear = 0.1
        zfar = 100.0
        projection_matrix = mat4.create()
        mat4.perspective(projection_matrix, fov, aspect, znear, zfar)

        model_view_matrix = mat4.create()
        mat4.translate(model_view_matrix, model_view_matrix, [0.0, 0.0, -6.0])
        mat4.rotate(model_view_matrix, model_view_matrix, self.cube_rotation, [0, 0, 1])
        mat4.rotate(model_view_matrix, model_view_matrix, self.cube_rotation * 0.7, [0, 1, 0])
        mat4.rotate(model_view_matrix, model_view_matrix, self.cube_rotation * 0.3, [1, 0, 0])

        # Setup array attributes for vertex position buffer
        vertex_position = gl.getAttribLocation(program.gl_id, "aVertexPosition")
        num_components = 3
        type = gl.FLOAT
        normalize = False
        stride = 0
        offset = 0
        gl.bindBuffer(gl.ARRAY_BUFFER, self.position_buffer)
        gl.vertexAttribPointer(
            vertex_position,
            num_components,
            type,
            normalize,
            stride,
            offset
        )
        gl.enableVertexAttribArray(vertex_position)

        # Setup array attributes for vertex color buffer
        vertex_color = gl.getAttribLocation(program.gl_id, "aVertexColor")
        num_components = 4
        type = gl.FLOAT
        normalize = False
        stride = 0
        offset = 0
        gl.bindBuffer(gl.ARRAY_BUFFER, self.color_buffer)
        gl.vertexAttribPointer(
            vertex_color,
            num_components,
            type,
            normalize,
            stride,
            offset
        )
        gl.enableVertexAttribArray(vertex_color)

        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, self.indices_buffer)
        
        # Setup uniforms for project/modelview matrix
        projection_matrix_uniform = gl.getUniformLocation(program.gl_id, "uProjectionMatrix")
        model_view_matrix_uniform = gl.getUniformLocation(program.gl_id, "uModelViewMatrix")
        gl.useProgram(program.gl_id)
        gl.uniformMatrix4fv(
            projection_matrix_uniform, False, model_view_matrix
        )
        gl.uniformMatrix4fv(
            model_view_matrix_uniform, False, projection_matrix
        )

        # Draw it
        offset = 0
        vertex_count = 36
        type = gl.UNSIGNED_SHORT
        gl.drawElements(gl.TRIANGLES, vertex_count, type, offset)

    def on_update(self, delta_time):
        self.cube_rotation += delta_time

def main():
    game = Game()
    game.setup()
    arcade.run()