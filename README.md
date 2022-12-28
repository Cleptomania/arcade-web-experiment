# arcade-web

## What is this?

This is the very early experimentation at creating a companion package to [Arcade](https://github.com/pythonarcade/arcade) which can be run
using [Pyodide](https://github.com/pyodide/pyodide) in the browser.

Currently this repo is just experimentation and seeing what is possible, what works, and what doesn't. Nothing here is representative of what
a final version of this might look like.

## How do I run it?

Each folder in this directory(at least at time of writing) is a different example. To access them, you can run the `server.py` file located at the root. This will give you an HTTP server locally, which by default can be accessed at port 8000(this can be changed by providing the `-p` argument when running).

Once running, if you visit http://localhost:8000/webgl_cube for example, you will see the WebGL Cube example in your browser.

## How does that work?

`server.py` is a small wrapper over Python's `http.server` and `socketserver` modules which when any directory is requested with a `.zip` appended will automatically zip the directory and serve that back. This allows for run-time generation of the Python package to be served to pyodide. If you peek inside a given example, you will see an `index.html` file as the entrypoint, and a `package` folder which contains the Python package. Additionally there may also be an `extra.js` file which may contain any necessary custom JavaScript code for the example.

The `arcade` folder is special, it contains the code for the actual `arcade` package which gets imported in the examples.

Any files/folders other than these, should be documented by a README within that specific example