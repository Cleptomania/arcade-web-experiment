import math
import time

import js
from pyodide.ffi import create_proxy

then = 0
cube_rotation = 0.0

def load_shader(gl, type, source):
    shader = gl.createShader(type)
    gl.shaderSource(shader, source)
    gl.compileShader(shader)
    if not gl.getShaderParameter(shader, gl.COMPILE_STATUS):
        print(f"An error occurred during shader compilation: {gl.getShaderInfoLog(shader)}")
        gl.deleteShader(shader)
        return None
    return shader


def init_shader_program(gl, vertex_source, fragment_source):
    vertex_shader = load_shader(gl, gl.VERTEX_SHADER, vertex_source)
    fragment_shader = load_shader(gl, gl.FRAGMENT_SHADER, fragment_source)

    shader_program = gl.createProgram()
    gl.attachShader(shader_program, vertex_shader)
    gl.attachShader(shader_program, fragment_shader)
    gl.linkProgram(shader_program)

    if not gl.getProgramParameter(shader_program, gl.LINK_STATUS):
        print(f"An error occurred during shader program creation: {gl.getProgramInfoLog(shader_program)}")
        return None
        
    return shader_program


def init_position_buffer(gl):
    position_buffer = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, position_buffer)
    positions = [
        -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, # Front face
        -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, -1.0, # Back face
        -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, # Top face
        -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, 1.0, # Bottom face
        1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, # Right face
        -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0, -1.0, # Left face
    ]
    gl.bufferData(gl.ARRAY_BUFFER, js.Float32Array.new(positions), gl.STATIC_DRAW)
    return position_buffer


def init_color_buffer(gl):
        color_buffer = gl.createBuffer()
        gl.bindBuffer(gl.ARRAY_BUFFER, color_buffer)
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
        gl.bufferData(gl.ARRAY_BUFFER, js.Float32Array.new(colors), gl.STATIC_DRAW)
        return color_buffer


def init_index_buffer(gl):
    indices_buffer = gl.createBuffer()
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indices_buffer)
    indices = [
        0, 1, 2, 0, 2, 3, # front
        4, 5, 6, 4, 6, 7, # back
        8, 9, 10, 8, 10, 11, # top
        12, 13, 14, 12, 14, 15, # bottom
        16, 17, 18, 16, 18, 19, # right
        20, 21, 22, 20, 22, 23, # left
    ]
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, js.Uint16Array.new(indices), gl.STATIC_DRAW)
    return indices_buffer


def init_buffers(gl):
    return {
        "position": init_position_buffer(gl),
        "color": init_color_buffer(gl),
        "index": init_index_buffer(gl),
    }

def draw_scene(gl, program_info, buffers, cube_rotation):    
    gl.clearColor(0.0, 0.0, 0.0, 1.0)
    gl.clearDepth(1.0)
    gl.enable(gl.DEPTH_TEST)
    gl.depthFunc(gl.LEQUAL)

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)

    num_components = 3
    type = gl.FLOAT
    normalize = False
    stride = 0
    offset = 0
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers["position"])
    gl.vertexAttribPointer(
        program_info["attribLocations"]["vertexPosition"],
        num_components,
        type,
        normalize,
        stride,
        offset
    )
    gl.enableVertexAttribArray(program_info["attribLocations"]["vertexPosition"])

    num_components = 4
    type = gl.FLOAT
    normalize = False
    stride = 0
    offset = 0
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers["color"])
    gl.vertexAttribPointer(
        program_info["attribLocations"]["vertexColor"],
        num_components,
        type,
        normalize,
        stride,
        offset
    )
    gl.enableVertexAttribArray(program_info["attribLocations"]["vertexColor"])

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers["index"])


    #gl.useProgram(program_info["program"])
    js.useProgram(gl, program_info)
    js.doProjection(gl, program_info)
    js.doModelView(gl, program_info, cube_rotation)

    # fov = (45 * math.pi) / 180
    # aspect = 800 / 600
    # znear = 0.1
    # zfar = 100.0
    # projection_matrix = js.mat4.create()

    # js.mat4.perspective(projection_matrix, fov, aspect, znear, zfar)

    # model_view_matrix = js.mat4.create()

    # js.mat4.translate(
    #     model_view_matrix,
    #     model_view_matrix,
    #     [-0.0, 0.0, -6.0]
    # )

    # js.mat4.rotate(
    #     model_view_matrix,
    #     model_view_matrix,
    #     cube_rotation,
    #     [0, 0, 1]
    # )

    # js.mat4.rotate(
    #     model_view_matrix,
    #     model_view_matrix,
    #     cube_rotation * 0.7,
    #     [0, 1, 0]
    # )

    # js.mat4.rotate(
    #     model_view_matrix,
    #     model_view_matrix,
    #     cube_rotation * 0.3,
    #     [1, 0, 0]
    # )

    # gl.uniformMatrix4fv(
    #     program_info["uniformLocations"]["projectionMatrix"],
    #     False,
    #     projection_matrix
    # )

    # gl.uniformMatrix4fv(
    #     program_info["uniformLocations"]["modelViewMatrix"],
    #     False,
    #     model_view_matrix
    # )

    #js.drawScene(gl, program_info, buffers, cube_rotation)

    vertex_count = 36
    type = gl.UNSIGNED_SHORT
    offset = 0
    gl.drawElements(gl.TRIANGLES, vertex_count, type, offset)



def run():
    global then
    global cube_rotation
    canvas = js.document.createElement("canvas")
    canvas.id = "arcade-window"
    canvas.width = 800
    canvas.height = 600
    js.document.body.appendChild(canvas)

    gl = canvas.getContext("webgl")

    if gl is None:
        print("Failed to initialize WebGL")
        return

    vertex_source = """
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

    fragment_source = """
    precision highp float;
    varying lowp vec4 vColor;
    void main(void) {
        gl_FragColor = vColor;
    }
    """

    shader_program = init_shader_program(gl, vertex_source, fragment_source)
    
    program_info = {
        "program": shader_program,
        "attribLocations": {
            "vertexPosition": gl.getAttribLocation(shader_program, "aVertexPosition"),
            "vertexColor": gl.getAttribLocation(shader_program, "aVertexColor"),
        },
        "uniformLocations": {
            "projectionMatrix": gl.getUniformLocation(shader_program, "uProjectionMatrix"),
            "modelViewMatrix": gl.getUniformLocation(shader_program, "uModelViewMatrix"),
        },
    }

    buffers = init_buffers(gl)

    def render(now):
        global then
        global cube_rotation
        now = now * 0.001
        delta_time = now - then
        then = now

        draw_scene(gl, program_info, buffers, cube_rotation)
        cube_rotation = cube_rotation + delta_time

        js.requestAnimationFrame(render_proxy)

    render_proxy = create_proxy(render)
    
    js.requestAnimationFrame(render_proxy)