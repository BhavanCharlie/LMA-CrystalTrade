from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from database import Base
from datetime import datetime


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True)
    loan_name = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    document_path = Column(String)
    document_type = Column(String)
    risk_score = Column(Integer)
    risk_breakdown = Column(JSON)
    compliance_checks = Column(JSON)
    extracted_terms = Column(JSON)
    recommendations = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    analysis_id = Column(String)
    file_path = Column(String)
    file_name = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True)
    analysis_id = Column(String)
    loan_name = Column(String)
    report_type = Column(String)  # executive, detailed, compliance
    file_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


