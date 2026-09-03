import json
import datetime

def dispatch_alert(room_id, camera_id, track_id, duration, confidence):
    """Monta o payload JSON e simula o disparo assíncrono para o painel."""
    event = {
        "event": "phone_use_sustained",
        "room_id": room_id,
        "track_id": f"t-{track_id}",
        "started_at": datetime.datetime.utcnow().isoformat() + "Z",
        "duration_ms": int(duration * 1000),
        "confidence": round(float(confidence), 2),
        "source": camera_id
    }
    
    payload = json.dumps(event, indent=2)
    print(f"\n[EVENT GATEWAY] DISPARO DE EVENTO ASSÍNCRONO:\n{payload}\n")
