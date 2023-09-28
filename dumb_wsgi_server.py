from waitress import serve
import app
serve(app.app, listen='*:5000')