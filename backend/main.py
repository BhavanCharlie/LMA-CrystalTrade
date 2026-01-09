from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import uuid

from services.document_processor import DocumentProcessor
from services.ai_analyzer import AIAnalyzer
from services.due_diligence_engine import DueDiligenceEngine
from services.report_generator import ReportGenerator
from database import get_db, init_db
from models import Analysis, Document, Report

app = FastAPI(title="CrystalTrade API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Initialize services
document_processor = DocumentProcessor()
ai_analyzer = AIAnalyzer()
due_diligence_engine = DueDiligenceEngine()
report_generator = ReportGenerator()


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
    db = next(get_db())
    
    total = db.query(Analysis).count()
    completed = db.query(Analysis).filter(Analysis.status == "completed").count()
    in_progress = db.query(Analysis).filter(Analysis.status == "processing").count()
    
    high_risk = db.query(Analysis).filter(
        Analysis.status == "completed",
        Analysis.risk_score >= 70
    ).count()
    medium_risk = db.query(Analysis).filter(
        Analysis.status == "completed",
        Analysis.risk_score >= 40,
        Analysis.risk_score < 70
    ).count()
    low_risk = db.query(Analysis).filter(
        Analysis.status == "completed",
        Analysis.risk_score < 40
    ).count()
    
    recent_analyses = db.query(Analysis).order_by(
        Analysis.created_at.desc()
    ).limit(10).all()
    
    return {
        "total_analyses": total,
        "completed": completed,
        "in_progress": in_progress,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
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

