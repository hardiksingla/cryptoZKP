from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
import os
from models import MockPassport
from credential_service import CredentialService
from proof_service import ProofService

app = FastAPI(title="zk-creds Demo")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
credential_service = CredentialService()
proof_service = ProofService()

# Serve static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def root():
    """Redirect to the demo page"""
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.post("/issue-credential")
async def issue_credential(file: UploadFile = File(...)):
    """Issue anonymous credential from mock passport"""
    try:
        # Read passport data
        content = await file.read()
        passport_data = json.loads(content)
        
        # Validate required fields
        required_fields = ["name", "birth_year", "country", "passport_number", "expiry_year"]
        for field in required_fields:
            if field not in passport_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Create passport object
        passport = MockPassport(
            name=passport_data["name"],
            birth_year=int(passport_data["birth_year"]),
            country=passport_data["country"],
            passport_number=passport_data["passport_number"],
            expiry_year=int(passport_data["expiry_year"])
        )
        
        # Issue credential
        credential = credential_service.issue_credential(passport)
        
        return {
            "success": True,
            "credential_id": credential.commitment,
            "message": "Credential issued successfully",
            "stats": {
                "commitment": credential.commitment[:16] + "...",
                "merkle_index": credential.merkle_index
            }
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error issuing credential: {str(e)}")

@app.post("/verify-age")
async def verify_age(request: dict):
    """Generate and verify age proof"""
    try:
        credential_id = request.get("credential_id")
        min_age = request.get("min_age", 18)
        
        if not credential_id:
            raise HTTPException(status_code=400, detail="credential_id is required")
        
        # Get credential
        credential = credential_service.get_credential(credential_id)
        if not credential:
            raise HTTPException(status_code=404, detail="Credential not found")
        
        # Verify credential is in merkle tree
        is_member = credential_service.verify_credential_membership(credential_id)
        if not is_member:
            raise HTTPException(status_code=400, detail="Credential not in tree")
        
        # Generate age proof
        age_proof = proof_service.generate_age_proof(
            credential.birth_year, 
            credential.nonce, 
            min_age
        )
        
        # Check if person is old enough (from public signal)
        is_old_enough = bool(age_proof.public_signals[0]) if age_proof.public_signals else False
        
        return {
            "success": True,
            "is_old_enough": is_old_enough,
            "proof_valid": age_proof.is_valid,
            "commitment": hex(age_proof.public_signals[1]) if len(age_proof.public_signals) > 1 else None,
            "message": f"Age verification {'passed' if is_old_enough else 'failed'}",
            "details": {
                "min_age_required": min_age,
                "proof_type": "zk-SNARK (simulated)",
                "privacy_preserved": True
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verifying age: {str(e)}")

@app.get("/merkle-root")
async def get_merkle_root():
    """Get current merkle tree root"""
    return {
        "root": credential_service.get_merkle_root(),
        "root_short": credential_service.get_merkle_root()[:16] + "..."
    }

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    total_creds = len(credential_service.credentials)
    root = credential_service.get_merkle_root()
    
    return {
        "total_credentials": total_creds,
        "merkle_root": root,
        "merkle_root_short": root[:16] + "..." if root != "0" else "0",
        "system_status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "demo-1.0"}

if __name__ == "__main__":
    import uvicorn
    print("Starting zk-creds demo server...")
    print("Open your browser to: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)