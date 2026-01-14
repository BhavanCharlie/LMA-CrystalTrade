from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
from datetime import datetime, timedelta
import uuid
from passlib.context import CryptContext
from jose import JWTError, jwt

from services.document_processor import DocumentProcessor
from services.ai_analyzer import AIAnalyzer
from services.due_diligence_engine import DueDiligenceEngine
from services.report_generator import ReportGenerator
from services.trade_readiness_engine import TradeReadinessEngine
from services.transfer_simulator import TransferSimulator
from services.lma_deviation_engine import LMADeviationEngine
from services.buyer_fit_analyzer import BuyerFitAnalyzer
from services.negotiation_insights import NegotiationInsightsGenerator
from services.monitoring_service import MonitoringService
from services.auction_service import AuctionService
from services.evidence_log import EvidenceLogService
from database import get_db, init_db
from models import (
    Analysis, Document, Report, TradeReadiness, TransferSimulation,
    LMADeviation, BuyerFit, NegotiationInsight, MonitoringRule, MonitoringAlert,
    Auction, Bid, EvidenceLog, AuditEvent, Deal, User
)
from feature_flags import is_feature_enabled

app = FastAPI(title="CrystalTrade API", version="1.0.0")

# CORS configuration - allow frontend URL from environment or default to localhost
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:5174",
]

# Add production frontend URL if provided
if FRONTEND_URL and FRONTEND_URL not in allowed_origins:
    allowed_origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication configuration
SECRET_KEY = os.getenv("SECRET_KEY", "crystal-trade-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Initialize database
init_db()

# Create demo users on startup (for free tier deployment without shell access)
def create_demo_users_on_startup():
    """Create demo users if they don't exist"""
    try:
        db = next(get_db())
        
        # Check if demo user exists
        demo_user = db.query(User).filter(User.username == "demo").first()
        if not demo_user:
            import bcrypt
            demo_hash = bcrypt.hashpw("demo123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            demo_user = User(
                id=str(uuid.uuid4()),
                email="demo@crystaltrade.com",
                username="demo",
                hashed_password=demo_hash,
                full_name="Demo User",
                is_active=True,
                is_admin=False
            )
            db.add(demo_user)
            print("✅ Demo user created: demo/demo123")
        
        # Check if admin user exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            import bcrypt
            admin_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin_user = User(
                id=str(uuid.uuid4()),
                email="admin@crystaltrade.com",
                username="admin",
                hashed_password=admin_hash,
                full_name="Admin User",
                is_active=True,
                is_admin=True
            )
            db.add(admin_user)
            print("✅ Admin user created: admin/admin123")
        
        db.commit()
        db.close()
    except Exception as e:
        print(f"Note: Could not create demo users: {e}")

# Create demo users
create_demo_users_on_startup()

# Initialize services
document_processor = DocumentProcessor()
ai_analyzer = AIAnalyzer()
due_diligence_engine = DueDiligenceEngine()
report_generator = ReportGenerator()
trade_readiness_engine = TradeReadinessEngine()
transfer_simulator = TransferSimulator()
lma_deviation_engine = LMADeviationEngine()
buyer_fit_analyzer = BuyerFitAnalyzer()
negotiation_insights_generator = NegotiationInsightsGenerator()
monitoring_service = MonitoringService()
auction_service = AuctionService()
evidence_log_service = EvidenceLogService()


# Authentication helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using bcrypt directly for compatibility"""
    try:
        # Try passlib first (for new passwords)
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, AttributeError):
        # Fallback to bcrypt directly (for compatibility with directly created hashes)
        import bcrypt
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt directly for compatibility"""
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()


# Pydantic models for authentication
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str]
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class AnalysisResponse(BaseModel):
    id: str
    loan_name: str
    status: str
    risk_score: Optional[int] = None
    risk_breakdown: Optional[dict] = None
    compliance_checks: Optional[List[dict]] = None
    extracted_terms: Optional[dict] = None
    recommendations: Optional[List[str]] = None
    created_at: str
    updated_at: str


@app.get("/")
async def root():
    return {"message": "CrystalTrade API - Transparent Loan Trading"}


# Authentication endpoints
@app.post("/api/v1/auth/signup", response_model=Token)
async def signup(user_data: UserCreate):
    """Create a new user account"""
    db = next(get_db())
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
        
        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            id=user_id,
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True,
            is_admin=False,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_user.id}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=new_user.id,
                email=new_user.email,
                username=new_user.username,
                full_name=new_user.full_name,
                is_admin=new_user.is_admin,
                created_at=new_user.created_at,
            )
        }
    finally:
        db.close()


@app.post("/api/v1/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with username/email and password - optimized for speed"""
    db = next(get_db())
    try:
        # Optimized: Try username first (most common), then email
        # This avoids OR query which can be slower
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user:
            user = db.query(User).filter(User.email == form_data.username).first()
        
        # Early return if user not found (before expensive password verification)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active before password verification
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Verify password (this is intentionally slow for security, but only runs if user exists)
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token (fast operation)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_admin=user.is_admin,
                created_at=user.created_at,
            )
        }
    finally:
        db.close()


@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
    )


@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...), loan_name: Optional[str] = None):
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Process document
        document_data = await document_processor.process_document(file_path, file.filename)
        
        # Create analysis record
        analysis_id = str(uuid.uuid4())
        analysis = Analysis(
            id=analysis_id,
            loan_name=loan_name or file.filename,
            status="pending",
            document_path=file_path,
            document_type=document_data.get("type", "unknown"),
        )
        
        db = next(get_db())
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return {
            "analysis_id": analysis_id,
            "loan_name": analysis.loan_name,
            "status": "pending",
            "message": "Document uploaded successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyses/{analysis_id}/start")
async def start_analysis(analysis_id: str, background_tasks: BackgroundTasks):
    try:
        db = next(get_db())
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis.status = "processing"
        db.commit()
        
        # Start background analysis
        background_tasks.add_task(process_analysis, analysis_id)
        
        return {"message": "Analysis started", "analysis_id": analysis_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def process_analysis(analysis_id: str):
    """Background task to process analysis"""
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        return
    
    try:
        # Step 1: Extract text from document
        document_text = await document_processor.extract_text(analysis.document_path)
        
        # Step 2: AI Analysis
        ai_results = await ai_analyzer.analyze_document(document_text, analysis.document_path)
        
        # Step 3: Due Diligence Checks
        compliance_results = await due_diligence_engine.run_checks(
            document_text, ai_results
        )
        
        # Step 4: Risk Scoring
        risk_assessment = await due_diligence_engine.calculate_risk_score(
            ai_results, compliance_results
        )
        
        # Step 5: Generate Recommendations
        recommendations = await due_diligence_engine.generate_recommendations(
            risk_assessment, compliance_results
        )
        
        # Update analysis
        analysis.status = "completed"
        analysis.risk_score = risk_assessment["overall_score"]
        analysis.risk_breakdown = risk_assessment["breakdown"]
        analysis.compliance_checks = compliance_results
        analysis.extracted_terms = ai_results.get("extracted_terms", {})
        analysis.recommendations = recommendations
        analysis.updated_at = datetime.utcnow()
        
        db.commit()
        
    except Exception as e:
        analysis.status = "failed"
        analysis.error_message = str(e)
        db.commit()
        print(f"Analysis failed: {e}")


@app.get("/api/v1/analyses/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "id": analysis.id,
        "loan_name": analysis.loan_name,
        "status": analysis.status,
        "risk_score": analysis.risk_score,
        "risk_breakdown": analysis.risk_breakdown,
        "compliance_checks": analysis.compliance_checks or [],
        "extracted_terms": analysis.extracted_terms or {},
        "recommendations": analysis.recommendations or [],
        "created_at": analysis.created_at.isoformat(),
        "updated_at": analysis.updated_at.isoformat() if analysis.updated_at else analysis.created_at.isoformat(),
    }


@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats():
    """Optimized dashboard stats - combine queries where possible"""
    db = next(get_db())
    try:
        from sqlalchemy import func, case
        
        # Get all counts in one query using conditional aggregation
        stats = db.query(
            func.count(Analysis.id).label('total'),
            func.sum(case((Analysis.status == "completed", 1), else_=0)).label('completed'),
            func.sum(case((Analysis.status == "processing", 1), else_=0)).label('in_progress'),
            func.sum(case((Analysis.status == "completed", case((Analysis.risk_score >= 70, 1), else_=0)), else_=0)).label('high_risk'),
            func.sum(case((Analysis.status == "completed", case((Analysis.risk_score >= 40, case((Analysis.risk_score < 70, 1), else_=0)), else_=0)), else_=0)).label('medium_risk'),
            func.sum(case((Analysis.status == "completed", case((Analysis.risk_score < 40, 1), else_=0)), else_=0)).label('low_risk'),
        ).first()
        
        # Get recent analyses
        recent_analyses = db.query(Analysis).order_by(
            Analysis.created_at.desc()
        ).limit(10).all()
        
        return {
            "total_analyses": stats.total or 0,
            "completed": stats.completed or 0,
            "in_progress": stats.in_progress or 0,
            "high_risk": stats.high_risk or 0,
            "medium_risk": stats.medium_risk or 0,
            "low_risk": stats.low_risk or 0,
            "recent_analyses": [
                {
                    "id": a.id,
                    "loan_name": a.loan_name,
                    "risk_score": a.risk_score or 0,
                    "status": a.status,
                    "created_at": a.created_at.isoformat(),
                }
                for a in recent_analyses
            ],
        }
    finally:
        db.close()


@app.get("/api/v1/reports")
async def get_reports():
    db = next(get_db())
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    
    return [
        {
            "id": r.id,
            "analysis_id": r.analysis_id,
            "loan_name": r.loan_name,
            "report_type": r.report_type,
            "created_at": r.created_at.isoformat(),
            "download_url": r.file_path if os.path.exists(r.file_path) else None,
        }
        for r in reports
    ]


class ReportRequest(BaseModel):
    analysis_id: str
    report_type: str = "executive"


@app.post("/api/v1/reports/generate")
async def generate_report(request: ReportRequest):
    analysis_id = request.analysis_id
    report_type = request.report_type
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.status != "completed":
        raise HTTPException(
            status_code=400, detail="Analysis must be completed to generate report"
        )
    
    # Generate report
    report_path = await report_generator.generate_report(
        analysis, report_type
    )
    
    # Save report record
    report = Report(
        id=str(uuid.uuid4()),
        analysis_id=analysis_id,
        loan_name=analysis.loan_name,
        report_type=report_type,
        file_path=report_path,
    )
    
    db.add(report)
    db.commit()
    
    return {
        "id": report.id,
        "analysis_id": analysis_id,
        "report_type": report_type,
        "download_url": f"/api/v1/reports/{report.id}/download",
    }


@app.get("/api/v1/reports/{report_id}/download")
async def download_report(report_id: str):
    db = next(get_db())
    report = db.query(Report).filter(Report.id == report_id).first()
    
    if not report or not os.path.exists(report.file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(
        report.file_path,
        media_type="application/pdf",
        filename=f"{report.loan_name}_{report.report_type}.pdf",
    )


# ============================================================================
# Loan Markets Features API Endpoints
# ============================================================================

@app.get("/api/v1/analyses/{analysis_id}/trade-readiness")
async def get_trade_readiness(analysis_id: str):
    """Get trade readiness score for an analysis"""
    if not is_feature_enabled("MARKET_INTEL"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail="Analysis must be completed")
    
    # Check if already calculated
    trade_readiness = db.query(TradeReadiness).filter(
        TradeReadiness.analysis_id == analysis_id
    ).first()
    
    if trade_readiness:
        return {
            "id": trade_readiness.id,
            "analysis_id": analysis_id,
            "score": trade_readiness.score,
            "label": trade_readiness.label,
            "breakdown": trade_readiness.breakdown,
            "confidence": trade_readiness.confidence,
            "evidence_links": trade_readiness.evidence_links,
        }
    
    # Calculate trade readiness
    analysis_data = {
        "document_path": analysis.document_path,
        "document_type": analysis.document_type,
    }
    
    result = await trade_readiness_engine.calculate_trade_readiness(
        analysis_data,
        analysis.extracted_terms or {},
        analysis.compliance_checks or [],
    )
    
    # Save to database
    trade_readiness = TradeReadiness(
        id=str(uuid.uuid4()),
        analysis_id=analysis_id,
        score=result["score"],
        label=result["label"],
        breakdown=result["breakdown"],
        confidence=result["confidence"],
        evidence_links=result["evidence_links"],
    )
    
    db.add(trade_readiness)
    db.commit()
    
    return {
        "id": trade_readiness.id,
        "analysis_id": analysis_id,
        **result,
    }


@app.get("/api/v1/analyses/{analysis_id}/transfer-simulation")
async def get_transfer_simulation(analysis_id: str):
    """Get transfer simulation for an analysis"""
    if not is_feature_enabled("TRANSFER_SIM"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail="Analysis must be completed")
    
    # Check if already calculated - get all simulations for this analysis
    existing_simulations = db.query(TransferSimulation).filter(
        TransferSimulation.analysis_id == analysis_id
    ).all()
    
    if existing_simulations:
        # Reconstruct pathways array from database
        pathways = []
        for sim in existing_simulations:
            pathways.append({
                "type": sim.pathway_type,
                "required_consents": sim.required_consents or [],
                "estimated_timeline_days": sim.estimated_timeline_days,
                "blockers": sim.blockers or [],
                "recommended_actions": sim.recommended_actions or [],
                "playbook": sim.playbook or "",
            })
        
        # If we only have one pathway, calculate the other one
        if len(pathways) == 1:
            # Calculate missing pathway
            result = await transfer_simulator.simulate_transfer_pathway(
                analysis_id,
                analysis.extracted_terms or {},
                analysis.compliance_checks or [],
            )
            # Find the missing pathway type
            existing_type = pathways[0]["type"]
            for pathway in result["pathways"]:
                if pathway["type"] != existing_type:
                    pathways.append(pathway)
                    # Save the missing pathway
                    new_sim = TransferSimulation(
                        id=str(uuid.uuid4()),
                        analysis_id=analysis_id,
                        pathway_type=pathway["type"],
                        required_consents=pathway["required_consents"],
                        estimated_timeline_days=pathway["estimated_timeline_days"],
                        blockers=pathway["blockers"],
                        recommended_actions=pathway["recommended_actions"],
                        playbook=pathway["playbook"],
                    )
                    db.add(new_sim)
                    db.commit()
                    break
        
        return {
            "pathways": pathways,
            "analysis_id": analysis_id,
            "simulated_at": existing_simulations[0].created_at.isoformat() if existing_simulations else datetime.utcnow().isoformat(),
        }
    
    # Calculate simulation
    result = await transfer_simulator.simulate_transfer_pathway(
        analysis_id,
        analysis.extracted_terms or {},
        analysis.compliance_checks or [],
    )
    
    # Save both pathways to database
    for pathway in result["pathways"]:
        simulation = TransferSimulation(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            pathway_type=pathway["type"],
            required_consents=pathway["required_consents"],
            estimated_timeline_days=pathway["estimated_timeline_days"],
            blockers=pathway["blockers"],
            recommended_actions=pathway["recommended_actions"],
            playbook=pathway["playbook"],
        )
        db.add(simulation)
    
    db.commit()
    
    return result


@app.get("/api/v1/analyses/{analysis_id}/lma-deviations")
async def get_lma_deviations(analysis_id: str):
    """Get LMA deviations for an analysis"""
    if not is_feature_enabled("LMA_DEVIATION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    try:
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        if analysis.status != "completed":
            raise HTTPException(status_code=400, detail="Analysis must be completed")
        
        # Check if deviations already exist in database
        existing_deviations = db.query(LMADeviation).filter(
            LMADeviation.analysis_id == analysis_id
        ).all()
        
        if existing_deviations:
            # Reconstruct response from database
            deviations = []
            for dev in existing_deviations:
                deviations.append({
                    "id": dev.id,
                    "clause_type": dev.clause_type or "Unknown",
                    "severity": dev.deviation_severity or "low",  # Map to frontend expected field
                    "deviation_severity": dev.deviation_severity or "low",  # Keep for compatibility
                    "market_impact": dev.market_impact or "No impact assessment available",
                    "clause_text": dev.clause_text or "",
                    "clause_reference": dev.section_reference or dev.page_reference or None,
                    "recommendation": _generate_recommendation(dev.deviation_severity, dev.clause_type, dev.market_impact),
                    "deviation_details": dev.baseline_template or "",
                    "lma_standard": dev.baseline_template or "",
                    "confidence": dev.confidence or 0.0,
                })
            
            # Calculate severity breakdown
            severity_breakdown = {
                "high": len([d for d in deviations if d.get("severity") == "high"]),
                "medium": len([d for d in deviations if d.get("severity") == "medium"]),
                "low": len([d for d in deviations if d.get("severity") == "low"]),
            }
            
            return {
                "deviations": deviations,
                "deviation_count": len(deviations),
                "severity_breakdown": severity_breakdown,
                "analysis_id": analysis_id,
            }
        
        # Calculate new deviations
        document_text = ""  # Would extract from document_path
        
        result = await lma_deviation_engine.analyze_deviations(
            analysis_id,
            analysis.document_path or "",
            analysis.extracted_terms or {},
            document_text,
        )
        
        # Save deviations to database
        for deviation in result["deviations"]:
            # Check if deviation already exists (by id)
            existing = db.query(LMADeviation).filter(LMADeviation.id == deviation.get("id")).first()
            if not existing:
                lma_dev = LMADeviation(
                    id=deviation.get("id", str(uuid.uuid4())),
                    analysis_id=analysis_id,
                    document_id=deviation.get("document_id", ""),
                    clause_text=deviation.get("clause_text", ""),
                    clause_type=deviation.get("clause_type", ""),
                    deviation_severity=deviation.get("deviation_severity", "low"),
                    market_impact=deviation.get("market_impact", ""),
                    baseline_template=deviation.get("baseline_template", ""),
                    confidence=deviation.get("confidence", 0.0),
                    page_reference=deviation.get("page_reference", ""),
                    section_reference=deviation.get("section_reference", ""),
                )
                db.add(lma_dev)
        
        db.commit()
        
        # Transform result to match frontend expectations
        transformed_deviations = []
        for deviation in result["deviations"]:
            transformed_deviations.append({
                "id": deviation.get("id"),
                "clause_type": deviation.get("clause_type", "Unknown"),
                "severity": deviation.get("deviation_severity", "low"),  # Map to frontend expected field
                "deviation_severity": deviation.get("deviation_severity", "low"),  # Keep for compatibility
                "market_impact": deviation.get("market_impact", "No impact assessment available"),
                "clause_text": deviation.get("clause_text", ""),
                "clause_reference": deviation.get("section_reference") or deviation.get("page_reference") or None,
                "recommendation": _generate_recommendation(
                    deviation.get("deviation_severity", "low"),
                    deviation.get("clause_type", ""),
                    deviation.get("market_impact", "")
                ),
                "deviation_details": deviation.get("baseline_template", ""),
                "lma_standard": deviation.get("baseline_template", ""),
                "confidence": deviation.get("confidence", 0.0),
            })
        
        return {
            "deviations": transformed_deviations,
            "deviation_count": result.get("deviation_count", len(transformed_deviations)),
            "severity_breakdown": result.get("severity_breakdown", {}),
            "analysis_id": analysis_id,
        }
    finally:
        db.close()


def _generate_recommendation(severity: str, clause_type: str, market_impact: str) -> str:
    """Generate a recommendation based on deviation severity and type"""
    if severity == "high":
        return f"Review {clause_type} clause immediately. Consider negotiating alignment with LMA standards to improve marketability."
    elif severity == "medium":
        return f"Monitor {clause_type} clause. May require additional documentation or clarification for some buyers."
    else:
        return f"Minor deviation in {clause_type} clause. Generally acceptable but note for buyer disclosure."


@app.get("/api/v1/analyses/{analysis_id}/buyer-fit")
async def get_buyer_fit(analysis_id: str):
    """Get buyer fit analysis for an analysis"""
    if not is_feature_enabled("BUYER_FIT"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail="Analysis must be completed")
    
    result = await buyer_fit_analyzer.analyze_buyer_fit(
        analysis_id,
        analysis.extracted_terms or {},
        analysis.compliance_checks or [],
    )
    
    # Save buyer fits to database
    for buyer_fit in result["buyer_fits"]:
        bf = BuyerFit(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            buyer_type=buyer_fit["buyer_type"],
            fit_score=buyer_fit["fit_score"],
            indicators=buyer_fit["indicators"],
            reasoning=buyer_fit["reasoning"],
            diligence_summary=buyer_fit["diligence_summary"],
        )
        db.add(bf)
    
    db.commit()
    
    return result


@app.get("/api/v1/analyses/{analysis_id}/negotiation-insights")
async def get_negotiation_insights(analysis_id: str):
    """Get negotiation insights for an analysis"""
    if not is_feature_enabled("NEGOTIATION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analysis.status != "completed":
        raise HTTPException(status_code=400, detail="Analysis must be completed")
    
    result = await negotiation_insights_generator.generate_insights(
        analysis_id,
        analysis.extracted_terms or {},
        analysis.compliance_checks or [],
    )
    
    # Save insights to database
    for insight in result["insights"]:
        ni = NegotiationInsight(
            id=str(uuid.uuid4()),
            analysis_id=analysis_id,
            clause_reference=insight.get("clause_reference", ""),
            clause_text=insight.get("clause_text", ""),
            negotiation_likelihood=insight.get("negotiation_likelihood", ""),
            suggested_redlines=insight.get("suggested_redlines", []),
            questions_for_agent=insight.get("questions_for_agent", []),
            risk_basis=insight.get("risk_basis", ""),
        )
        db.add(ni)
    
    db.commit()
    
    return result


# Monitoring endpoints
@app.post("/api/v1/analyses/{analysis_id}/monitoring/rules")
async def create_monitoring_rule(analysis_id: str, rule_config: dict):
    """Create a monitoring rule"""
    if not is_feature_enabled("MONITORING"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    rule_data = await monitoring_service.create_monitoring_rule(analysis_id, rule_config)
    
    rule = MonitoringRule(
        id=rule_data["id"],
        analysis_id=analysis_id,
        rule_type=rule_data["rule_type"],
        rule_name=rule_data["rule_name"],
        threshold_value=rule_data["threshold_value"],
        current_value=rule_data["current_value"],
        alert_threshold=rule_data["alert_threshold"],
        is_active=rule_data["is_active"],
    )
    
    db.add(rule)
    db.commit()
    
    return rule_data


@app.get("/api/v1/analyses/{analysis_id}/monitoring/alerts")
async def get_monitoring_alerts(analysis_id: str):
    """Get monitoring alerts for an analysis"""
    if not is_feature_enabled("MONITORING"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    rules = db.query(MonitoringRule).filter(
        MonitoringRule.analysis_id == analysis_id,
        MonitoringRule.is_active == True
    ).all()
    
    rules_data = [
        {
            "id": r.id,
            "rule_type": r.rule_type,
            "rule_name": r.rule_name,
            "threshold_value": r.threshold_value,
            "current_value": r.current_value,
            "alert_threshold": r.alert_threshold,
        }
        for r in rules
    ]
    
    alerts = await monitoring_service.check_rules(rules_data)
    
    return {"alerts": alerts, "rules": rules_data}


# Auction endpoints
@app.get("/api/v1/analyses/{analysis_id}/auctions")
async def get_auctions_for_analysis(analysis_id: str):
    """Get all auctions for an analysis"""
    if not is_feature_enabled("AUCTION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    auctions = db.query(Auction).filter(Auction.analysis_id == analysis_id).order_by(
        Auction.created_at.desc()
    ).all()
    
    return [
        {
            "id": a.id,
            "analysis_id": a.analysis_id,
            "loan_name": a.loan_name,
            "auction_type": a.auction_type,
            "lot_size": a.lot_size,
            "min_bid": a.min_bid,
            "bid_increment": a.bid_increment,
            "reserve_price": a.reserve_price,
            "start_time": a.start_time.isoformat(),
            "end_time": a.end_time.isoformat(),
            "status": a.status,
            "winning_bid_id": a.winning_bid_id,
            "created_by": a.created_by,
            "created_at": a.created_at.isoformat(),
        }
        for a in auctions
    ]


@app.post("/api/v1/auctions")
async def create_auction(auction_config: dict):
    """Create a new auction"""
    if not is_feature_enabled("AUCTION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    auction_data = await auction_service.create_auction(
        auction_config.get("analysis_id", ""),
        auction_config,
        auction_config.get("created_by", "demo_user"),
    )
    
    auction = Auction(
        id=auction_data["id"],
        analysis_id=auction_data["analysis_id"],
        loan_name=auction_data["loan_name"],
        auction_type=auction_data["auction_type"],
        lot_size=auction_data["lot_size"],
        min_bid=auction_data["min_bid"],
        bid_increment=auction_data["bid_increment"],
        reserve_price=auction_data["reserve_price"],
        start_time=datetime.fromisoformat(auction_data["start_time"]),
        end_time=datetime.fromisoformat(auction_data["end_time"]),
        status=auction_data["status"],
        created_by=auction_data["created_by"],
    )
    
    db.add(auction)
    db.commit()
    
    # Log audit event
    audit_event = AuditEvent(
        id=str(uuid.uuid4()),
        event_type="auction_created",
        entity_type="auction",
        entity_id=auction.id,
        user_id=auction.created_by,
        action="create",
        details={"auction_type": auction.auction_type, "loan_name": auction.loan_name},
    )
    db.add(audit_event)
    db.commit()
    
    return auction_data


@app.post("/api/v1/auctions/{auction_id}/bids")
async def place_bid(auction_id: str, bid_data: dict):
    """Place a bid on an auction - ultra-optimized for speed"""
    if not is_feature_enabled("AUCTION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = None
    try:
        # Validate bid amount first (before DB access)
        try:
            bid_amount = float(bid_data.get("bid_amount", 0.0))
        except (ValueError, TypeError) as e:
            print(f"Invalid bid amount: {bid_data.get('bid_amount')}, error: {e}")
            raise HTTPException(status_code=400, detail="Invalid bid amount")
        
        if bid_amount <= 0:
            raise HTTPException(status_code=400, detail="Bid amount must be greater than 0")
        
        db = next(get_db())
        
        # Get auction
        auction = db.query(Auction).filter(Auction.id == auction_id).first()
        if not auction:
            print(f"Auction not found: {auction_id}")
            raise HTTPException(status_code=404, detail="Auction not found")
        
        if auction.status == "closed":
            raise HTTPException(status_code=400, detail="Auction is closed")
        
        # Get highest bid with minimal query (use try/except for safety)
        try:
            highest_bid_obj = db.query(Bid.bid_amount).filter(
                Bid.auction_id == auction_id
            ).order_by(Bid.bid_amount.desc()).limit(1).scalar()
            highest_bid_amount = float(highest_bid_obj) if highest_bid_obj is not None else 0.0
        except Exception as e:
            print(f"Error querying highest bid: {e}")
            highest_bid_amount = 0.0
        
        # Quick validation
        min_bid = float(auction.min_bid) if auction.min_bid else 0.0
        bid_increment = float(auction.bid_increment) if auction.bid_increment else 0.01
        
        if bid_amount < min_bid:
            raise HTTPException(status_code=400, detail=f"Bid must be at least ${min_bid:,.2f}")
        
        if highest_bid_amount > 0:
            min_required = highest_bid_amount + bid_increment
            if bid_amount < min_required:
                raise HTTPException(status_code=400, detail=f"Bid must be at least ${min_required:,.2f}")
        
        # Quick time check
        now = datetime.utcnow()
        if auction.end_time and now > auction.end_time:
            raise HTTPException(status_code=400, detail="Auction has closed")
        
        # Update status if needed (combine with bid creation)
        if auction.status == "pending" and auction.start_time and now >= auction.start_time:
            auction.status = "active"
        
        # Create and commit bid in one transaction
        bid_id = str(uuid.uuid4())
        bid = Bid(
            id=bid_id,
            auction_id=auction_id,
            bidder_id=bid_data.get("bidder_id", ""),
            bidder_name=bid_data.get("bidder_name", ""),
            bid_amount=bid_amount,
            is_locked=False,
            timestamp=now,
        )
        
        db.add(bid)
        try:
            db.commit()
            print(f"Bid placed successfully: {bid_id} for auction {auction_id}, amount: {bid_amount}")
        except Exception as commit_error:
            print(f"Database commit error: {commit_error}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(commit_error)}")
        
        return {
            "id": bid_id,
            "auction_id": auction_id,
            "bidder_id": bid_data.get("bidder_id", ""),
            "bidder_name": bid_data.get("bidder_name", ""),
            "bid_amount": float(bid_amount),
            "is_locked": False,
            "timestamp": now.isoformat(),
            "is_winning": False,
        }
        
    except HTTPException:
        if db:
            try:
                db.rollback()
            except:
                pass
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error placing bid: {str(e)}")
        print(f"Traceback: {error_trace}")
        if db:
            try:
                db.rollback()
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to place bid: {str(e)}")
    finally:
        if db:
            try:
                db.close()
            except:
                pass


@app.get("/api/v1/auctions/{auction_id}")
async def get_auction(auction_id: str):
    """Get a single auction by ID with bid count and winner info - optimized"""
    if not is_feature_enabled("AUCTION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    try:
        auction = db.query(Auction).filter(Auction.id == auction_id).first()
        
        if not auction:
            raise HTTPException(status_code=404, detail="Auction not found")
        
        # Update status if needed
        now = datetime.utcnow()
        status_changed = False
        if auction.status == "pending" and now >= auction.start_time:
            auction.status = "active"
            status_changed = True
        elif auction.status == "active" and now >= auction.end_time:
            auction.status = "closed"
            status_changed = True
        
        if status_changed:
            db.commit()
        
        # Optimize: Get all bid info in one query using subquery
        from sqlalchemy import func
        
        # Get bid count and highest bid in one query
        bid_stats = db.query(
            func.count(Bid.id).label('bid_count'),
            func.max(Bid.bid_amount).label('max_bid')
        ).filter(Bid.auction_id == auction_id).first()
        
        bid_count = bid_stats.bid_count if bid_stats else 0
        
        # Get highest bid details only if there are bids
        highest_bid = None
        winning_bid = None
        
        if bid_count > 0:
            # Get highest bid in one query
            highest_bid_obj = db.query(Bid).filter(
                Bid.auction_id == auction_id
            ).order_by(Bid.bid_amount.desc()).first()
            
            if highest_bid_obj:
                if auction.status == "active":
                    highest_bid = {
                        "bidder_name": highest_bid_obj.bidder_name,
                        "bid_amount": float(highest_bid_obj.bid_amount),
                    }
                
                # If this is the winning bid, use it
                if auction.status == "closed" and auction.winning_bid_id == highest_bid_obj.id:
                    winning_bid = highest_bid_obj
                elif auction.status == "closed" and auction.winning_bid_id:
                    # Only query winning bid if it's different from highest
                    winning_bid = db.query(Bid).filter(Bid.id == auction.winning_bid_id).first()
        
        result = {
            "id": auction.id,
            "analysis_id": auction.analysis_id,
            "loan_name": auction.loan_name,
            "auction_type": auction.auction_type,
            "lot_size": auction.lot_size,
            "min_bid": auction.min_bid,
            "bid_increment": auction.bid_increment,
            "reserve_price": auction.reserve_price,
            "start_time": auction.start_time.isoformat(),
            "end_time": auction.end_time.isoformat(),
            "status": auction.status,
            "winning_bid_id": auction.winning_bid_id,
            "created_by": auction.created_by,
            "created_at": auction.created_at.isoformat(),
            "bid_count": bid_count,
        }
        
        # Add winner info if auction is closed
        if auction.status == "closed" and winning_bid:
            result["winner"] = {
                "bidder_name": winning_bid.bidder_name,
                "bid_amount": float(winning_bid.bid_amount),
                "timestamp": winning_bid.timestamp.isoformat(),
            }
        
        # Add current leader for active auctions
        if auction.status == "active" and highest_bid:
            result["current_leader"] = highest_bid
        
        return result
    finally:
        db.close()


@app.get("/api/v1/auctions/{auction_id}/leaderboard")
async def get_auction_leaderboard(auction_id: str):
    """Get leaderboard for an auction"""
    if not is_feature_enabled("AUCTION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    
    bids = db.query(Bid).filter(Bid.auction_id == auction_id).all()
    
    bids_data = [
        {
            "id": b.id,
            "bidder_name": b.bidder_name,
            "bid_amount": b.bid_amount,
            "timestamp": b.timestamp.isoformat(),
        }
        for b in bids
    ]
    
    auction_dict = {
        "id": auction.id,
        "auction_type": auction.auction_type,
    }
    
    leaderboard = await auction_service.get_auction_leaderboard(auction_dict, bids_data)
    
    return {"leaderboard": leaderboard}


@app.post("/api/v1/auctions/{auction_id}/close")
async def close_auction(auction_id: str):
    """Close an auction and determine winner"""
    if not is_feature_enabled("AUCTION"):
        raise HTTPException(status_code=403, detail="Feature not enabled")
    
    db = next(get_db())
    auction = db.query(Auction).filter(Auction.id == auction_id).first()
    
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    
    bids = db.query(Bid).filter(Bid.auction_id == auction_id).all()
    
    auction_dict = {
        "id": auction.id,
        "auction_type": auction.auction_type,
        "reserve_price": auction.reserve_price,
    }
    
    bids_data = [
        {
            "id": b.id,
            "bidder_name": b.bidder_name,
            "bid_amount": b.bid_amount,
            "timestamp": b.timestamp.isoformat(),
        }
        for b in bids
    ]
    
    result = await auction_service.close_auction(auction_dict, bids_data)
    
    # Update auction
    auction.status = "closed"
    if result.get("winning_bid_id"):
        auction.winning_bid_id = result["winning_bid_id"]
        # Mark winning bid
        winning_bid = db.query(Bid).filter(Bid.id == result["winning_bid_id"]).first()
        if winning_bid:
            winning_bid.is_winning = True
            # Add winner details to result
            result["winner"] = {
                "bidder_name": winning_bid.bidder_name,
                "bid_amount": float(winning_bid.bid_amount),
                "timestamp": winning_bid.timestamp.isoformat(),
            }
    
    result["total_bids"] = len(bids)
    db.commit()
    
    return result

