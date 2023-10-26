from app import app, db
from app.models import Visitor

@app.shell_context_processor
def makeShellContext():
    return {"db":db, "Visitor": Visitor}