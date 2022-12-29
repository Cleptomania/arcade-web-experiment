from typing import TYPE_CHECKING

import js

from arcade.arcade_types import BufferProtocol
from arcade.gl import constants

if TYPE_CHECKING:
    from arcade.gl import Context

class Buffer:

    _usages = {
        "static": constants.STATIC_DRAW,
        "dynamic": constants.DYNAMIC_DRAW,
        "stream": constants.STREAM_DRAW,
    }

    def __init__(
        self,
        ctx: "Context",
        data: BufferProtocol,
        usage: str = "static"
    ):
        self._ctx = ctx
        gl = self._ctx.gl
        self._glo = gl.createBuffer()
        self._usage = Buffer._usages[usage]

        self.nbytes = len(data) * data.itemsize

        self._js_array_buffer = js.ArrayBuffer.new(self.nbytes)
        self._js_array_buffer.assign(data)

        gl.bindBuffer(gl.ARRAY_BUFFER, self._glo)
        gl.bufferData(gl.ARRAY_BUFFER, self._js_array_buffer, self._usage)



