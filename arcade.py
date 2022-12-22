from __future__ import annotations

import js
from pyodide.ffi import create_once_callable

_window: Window = None

def get_window() -> Window:
    return _window

def set_window(window: Window) -> None:
    global _window
    _window = window


class Window:
    def __init__(self, title: str, width: int, height: int):
        self.width = width
        self.height = height

        js.document.title = title
        self._canvas = js.document.createElement("canvas")
        self._canvas.id = "arcade-window"
        self._canvas.width = width
        self._canvas.height = height
        js.document.body.appendChild(self._canvas)

        self.context = Context(self._canvas)

        self._then = 0

        set_window(self)

    def on_draw(self):
        pass

    def on_update(self, delta_time):
        pass

    def clear(self, color: tuple = (0.0, 0.0, 0.0, 1.0)):
        self.context.clear(color)

    def run(self, now):
        delta_time = now - self._then
        self._then = now

        self.on_update(delta_time)
        self.on_draw()

        js.requestAnimationFrame(create_once_callable(self.run))

class Context:
    def __init__(self, canvas):
        self.gl = canvas.getContext("webgl")
        self.shader_programs = {}
        
        self.gl.clearDepth(1.0)
        self.gl.enable(self.gl.DEPTH_TEST)
        self.gl.depthFunc(self.gl.LEQUAL)

    def clear(self, color: tuple = (0.0, 0.0, 0.0, 1.0)):
        self.gl.clearColor(*color)
        self.gl.clear(self.gl.COLOR_BUFFER_BIT | self.gl.DEPTH_BUFFER_BIT)

    def create_shader(self, name: str, vertex_source: str, fragment_source: str):
        shader_program = ShaderProgram.create(self, vertex_source, fragment_source)
        if shader_program is not None:
            self.shader_programs[name] = shader_program

class ShaderProgram:
    def __init__(self, context: Context):
        self._context = context
        self.gl_id = None

    @classmethod
    def create(cls, context: Context, vertex_source: str, fragment_source: str):
        shader_program = cls(context)
        
        gl = context.gl

        vertex_shader = shader_program.load_shader(gl.VERTEX_SHADER, vertex_source)
        fragment_shader = shader_program.load_shader(gl.FRAGMENT_SHADER, fragment_source)

        shader_program.gl_id = gl.createProgram()
        gl.attachShader(shader_program.gl_id, vertex_shader)
        gl.attachShader(shader_program.gl_id, fragment_shader)
        gl.linkProgram(shader_program.gl_id)

        if not gl.getProgramParameter(shader_program.gl_id, gl.LINK_STATUS):
            print(f"An error occured while linking shader program: {gl.getProgramInfoLog(shader_program)}")
            return None

        return shader_program

    def load_shader(self, type: int, source: str):
        gl = self._context.gl
        shader_id = gl.createShader(type)
        gl.shaderSource(shader_id, source)
        gl.compileShader(shader_id)

        if not gl.getShaderParameter(shader_id, gl.COMPILE_STATUS):
            print(f"An error occurred while compiling shaders: {gl.getShaderInfoLog(shader_id)}")
            gl.deleteShader(shader_id)
            return None
        
        return shader_id

def run():
    window = get_window()
    js.requestAnimationFrame(create_once_callable(window.run))

