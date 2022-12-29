from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from arcade.gl import Context

class Program:
    def __init__(self, ctx: "Context"):
        self._ctx = ctx
        self._glo = None

    @classmethod
    def create(cls, ctx: "Context", vertex_source: str, fragment_source: str):
        program = cls(ctx)

        gl = ctx.gl

        vertex_shader = Program.load_shader(gl, gl.VERTEX_SHADER, vertex_source)
        fragment_shader = Program.load_shader(gl, gl.FRAGMENT_SHADER, fragment_source)

        program._glo = gl.createProgram()
        gl.attachShader(program._glo, vertex_shader)
        gl.attachShader(program._glo, fragment_shader)
        gl.linkProgram(program._glo)

        if not gl.getProgramParameter(program._glo, gl.LINK_STATUS):
            print(
                f"Error occured while linking program: {gl.getProgramInfoLog(program)}"
            )
            return None
        
        return program


    @staticmethod
    def load_shader(gl, type: int, source: str):
        shader = gl.createShader(type)
        gl.shaderSource(shader, source)
        gl.compileShader(shader)

        if not gl.getShaderParameter(shader, gl.COMPILE_STATUS):
            print(
                f"Error occurred while compiling shaders: {gl.getShaderInfoLog(shader)}"
            )
            gl.deleteShader(shader)
            return None
        
        return shader