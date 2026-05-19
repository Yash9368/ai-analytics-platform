import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/leads", tags=["leads"])

# Store in standard credentials folder
JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "credentials", "leads.json")

class LeadSchema(BaseModel):
    id: str
    full_name: str
    email: str
    company_name: str
    phone_number: str
    message: str
    status: str = "New"
    created_at: str

class StatusUpdateSchema(BaseModel):
    status: str

def load_leads_from_file() -> list:
    if not os.path.exists(JSON_PATH):
        # Ensure credentials dir exists
        os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
        with open(JSON_PATH, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(JSON_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_leads_to_file(leads: list):
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    with open(JSON_PATH, "w") as f:
        json.dump(leads, f, indent=2)

@router.get("", response_model=List[LeadSchema])
def get_leads():
    return load_leads_from_file()

@router.post("", response_model=LeadSchema)
def create_lead(lead: LeadSchema):
    leads = load_leads_from_file()
    # Check if duplicate ID
    if any(l["id"] == lead.id for l in leads):
        return lead
    leads.insert(0, lead.dict())
    save_leads_to_file(leads)
    return lead

@router.put("/{lead_id}/status", response_model=LeadSchema)
def update_status(lead_id: str, status_payload: StatusUpdateSchema):
    leads = load_leads_from_file()
    for l in leads:
        if l["id"] == lead_id:
            l["status"] = status_payload.status
            save_leads_to_file(leads)
            return l
    raise HTTPException(status_code=404, detail="Lead not found")

@router.delete("/{lead_id}")
def delete_lead(lead_id: str):
    leads = load_leads_from_file()
    filtered = [l for l in leads if l["id"] != lead_id]
    if len(filtered) == len(leads):
        raise HTTPException(status_code=404, detail="Lead not found")
    save_leads_to_file(filtered)
    return {"status": "success", "message": "Lead deleted successfully"}
