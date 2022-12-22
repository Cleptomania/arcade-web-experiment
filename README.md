# arcade-web

## What is this?

This is the very early experimentation at creating a companion package to [Arcade](https://github.com/pythonarcade/arcade) which can be run
using [Pyodide](https://github.com/pyodide/pyodide) in the browser.

Currently this repo is just experimentation and seeing what is possible, what works, and what doesn't. Nothing here is representative of what
a final version of this might look like.

## How do I run it?

Currently there is a "library" module named `arcade.py` and a test application module named `test.py`. These two modules make up the python application.
The library module is what would eventually be the `arcade-web` API, while the test application is intended to be an example usage of it. The implementation here
is extremely subject to change and is not even a little bit what the final module would look like, it's quick and dirty to enable experimentation.

In order to run this, you need to compile the two python files into a file named `test.zip` and then run an HTTP server(for example with `python -m http.server`)
in the root directory of this project. The reason you can't just open the HTML file is because of filesystem/CORS security issues in browsers. Once you're running
the HTTP server just navigate to https://localhost:8000 and you should see the example.

For convenience, there is a `build.sh` script which will update the zip file, as this needs re-created anytime modifications are made to the python files.