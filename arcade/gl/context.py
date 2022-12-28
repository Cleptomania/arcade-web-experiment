from typing import Optional, Tuple

from .program import Program


class Context:
    def __init__(self, canvas):
        self.gl = canvas.getContext("webgl2")
        
        self.active_program: Optional[Program] = None

    def clear(self, color: Tuple[float, float, float, float]):
        # Temporary
        self.gl.clearDepth(1.0)
        self.gl.enable(self.gl.DEPTH_TEST)
        self.gl.depthFunc(self.gl.LEQUAL)

        self.gl.clearColor(*color)
        self.gl.clear(self.gl.COLOR_BUFFER_BIT | self.gl.DEPTH_BUFFER_BIT)

    def program(
        self,
        *,
        vertex_shader: str,
        fragment_shader: str
    ) -> Program:
        return Program.create(self, vertex_shader, fragment_shader)