from fastapi import APIRouter, BackgroundTasks
from app.api.services.trainer import GATrainer

router = APIRouter()

@router.post("/train")
def train_agent(background_tasks: BackgroundTasks):
    """Trigger GA training asynchronously."""
    def run_training():
        trainer = GATrainer()
        trainer.train()
    background_tasks.add_task(run_training)
    return {"status": "Training started"}

@router.get("/weights")
def get_trained_weights():
    """Fetch saved trained weights if available."""
    import os, json
    path = "app/logs/training/trained_weights.json"
    if not os.path.exists(path):
        return {"error": "No trained weights found"}
    with open(path) as f:
        data = json.load(f)
    return {"weights": data}
