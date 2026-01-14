from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, Float, Boolean, ForeignKey, Index
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
    
    # Add indexes for frequently queried columns
    __table_args__ = (
        Index('idx_analysis_status', 'status'),
        Index('idx_analysis_created_at', 'created_at'),
        Index('idx_analysis_status_risk', 'status', 'risk_score'),
    )


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


# Loan Markets feature models

class TradeReadiness(Base):
    __tablename__ = "trade_readiness"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    score = Column(Integer)  # 0-100
    label = Column(String)  # Green, Amber, Red
    breakdown = Column(JSON)  # Detailed breakdown by category
    confidence = Column(Float)  # 0.0-1.0
    evidence_links = Column(JSON)  # Links to evidence
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class TransferSimulation(Base):
    __tablename__ = "transfer_simulations"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    pathway_type = Column(String)  # assignment, participation
    required_consents = Column(JSON)  # List of consent requirements
    estimated_timeline_days = Column(Integer)
    blockers = Column(JSON)  # List of blockers
    recommended_actions = Column(JSON)  # List of actions
    playbook = Column(Text)  # Text playbook
    created_at = Column(DateTime, default=datetime.utcnow)


class LMADeviation(Base):
    __tablename__ = "lma_deviations"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    document_id = Column(String)
    clause_text = Column(Text)
    clause_type = Column(String)  # transfer, covenant, payment, etc.
    deviation_severity = Column(String)  # high, medium, low
    market_impact = Column(Text)  # Impact description
    baseline_template = Column(Text)  # Expected LMA-standard text
    confidence = Column(Float)
    page_reference = Column(String)
    section_reference = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class BuyerFit(Base):
    __tablename__ = "buyer_fits"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    buyer_type = Column(String)  # CLO, Bank, DistressedFund, etc.
    fit_score = Column(Integer)  # 0-100
    indicators = Column(JSON)  # List of fit indicators
    reasoning = Column(Text)  # Why this buyer type fits
    diligence_summary = Column(Text)  # Buyer-specific summary
    created_at = Column(DateTime, default=datetime.utcnow)


class NegotiationInsight(Base):
    __tablename__ = "negotiation_insights"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    clause_reference = Column(String)
    clause_text = Column(Text)
    negotiation_likelihood = Column(String)  # high, medium, low
    suggested_redlines = Column(JSON)  # List of suggested changes
    questions_for_agent = Column(JSON)  # Questions to ask
    risk_basis = Column(Text)  # Why this is likely to be negotiated
    created_at = Column(DateTime, default=datetime.utcnow)


class MonitoringRule(Base):
    __tablename__ = "monitoring_rules"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    rule_type = Column(String)  # covenant, date, obligation
    rule_name = Column(String)
    threshold_value = Column(Float)
    current_value = Column(Float)
    alert_threshold = Column(Float)  # When to alert (e.g., 0.9 = 90% of threshold)
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
class MonitoringAlert(Base):
    __tablename__ = "monitoring_alerts"

    id = Column(String, primary_key=True)
    rule_id = Column(String, ForeignKey("monitoring_rules.id"))
    analysis_id = Column(String, ForeignKey("analyses.id"))
    alert_type = Column(String)  # warning, critical
    message = Column(Text)
    threshold_breach_percentage = Column(Float)
    is_acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Auction(Base):
    __tablename__ = "auctions"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    loan_name = Column(String)
    auction_type = Column(String)  # english, sealed_bid
    lot_size = Column(Float)  # Position size
    min_bid = Column(Float)
    bid_increment = Column(Float)
    reserve_price = Column(Float)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String, default="pending")  # pending, active, closed
    winning_bid_id = Column(String, nullable=True)
    created_by = Column(String)  # User/institution ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Add indexes for frequently queried columns
    __table_args__ = (
        Index('idx_auction_analysis_id', 'analysis_id'),
        Index('idx_auction_status', 'status'),
        Index('idx_auction_end_time', 'end_time'),
    )


class Bid(Base):
    __tablename__ = "bids"

    id = Column(String, primary_key=True)
    auction_id = Column(String, ForeignKey("auctions.id"))
    bidder_id = Column(String)  # Institution/user ID
    bidder_name = Column(String)
    bid_amount = Column(Float)
    is_locked = Column(Boolean, default=False)  # Prevent modification
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_winning = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Add indexes for frequently queried columns
    __table_args__ = (
        Index('idx_bid_auction_id', 'auction_id'),
        Index('idx_bid_auction_amount', 'auction_id', 'bid_amount'),
        Index('idx_bid_timestamp', 'timestamp'),
    )


class EvidenceLog(Base):
    __tablename__ = "evidence_logs"

    id = Column(String, primary_key=True)
    analysis_id = Column(String, ForeignKey("analyses.id"))
    document_id = Column(String)
    document_name = Column(String)
    page_number = Column(Integer, nullable=True)
    section = Column(String, nullable=True)
    extraction_text = Column(Text)
    extraction_confidence = Column(Float)
    feature_type = Column(String)  # trade_readiness, deviation, etc.
    feature_id = Column(String)  # ID of the related feature record
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String, primary_key=True)
    event_type = Column(String)  # auction_created, bid_placed, analysis_completed, etc.
    entity_type = Column(String)  # auction, bid, analysis, etc.
    entity_id = Column(String)
    user_id = Column(String, nullable=True)
    action = Column(String)  # create, update, delete, etc.
    details = Column(JSON)  # Additional event details
    timestamp = Column(DateTime, default=datetime.utcnow)


class Deal(Base):
    __tablename__ = "deals"

    id = Column(String, primary_key=True)
    deal_name = Column(String)
    borrower_name = Column(String)
    deal_type = Column(String)  # term_loan, revolver, etc.
    principal_amount = Column(Float)
    currency = Column(String, default="USD")
    status = Column(String, default="active")  # active, closed, archived
    analysis_ids = Column(JSON)  # List of related analysis IDs
    deal_metadata = Column(JSON)  # Additional deal metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)



class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Add indexes for faster lookups
    __table_args__ = (
        Index('idx_user_username', 'username'),
        Index('idx_user_email', 'email'),
    )