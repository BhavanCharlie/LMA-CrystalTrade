#!/usr/bin/env python3
"""
Clear all analyses and related data from the database
Keeps users intact
"""
from database import get_db, init_db
from models import (
    Analysis, Document, Report, TradeReadiness, TransferSimulation,
    LMADeviation, BuyerFit, NegotiationInsight, MonitoringRule, MonitoringAlert,
    Auction, Bid, EvidenceLog, AuditEvent, Deal
)
from sqlalchemy import delete

def clear_analyses():
    """Clear all analyses and related data, keeping users"""
    print("Clearing all analyses and related data...")
    
    # Initialize database
    init_db()
    
    db = next(get_db())
    
    try:
        # Count existing data
        analysis_count = db.query(Analysis).count()
        deal_count = db.query(Deal).count()
        auction_count = db.query(Auction).count()
        report_count = db.query(Report).count()
        
        print(f"\nCurrent data:")
        print(f"  Analyses: {analysis_count}")
        print(f"  Deals: {deal_count}")
        print(f"  Auctions: {auction_count}")
        print(f"  Reports: {report_count}")
        
        # Delete in order to respect foreign key constraints
        print("\nDeleting data...")
        
        # Delete bids first (references auctions)
        bids_deleted = db.execute(delete(Bid)).rowcount
        print(f"  ✓ Deleted {bids_deleted} bids")
        
        # Delete auctions (references analyses)
        auctions_deleted = db.execute(delete(Auction)).rowcount
        print(f"  ✓ Deleted {auctions_deleted} auctions")
        
        # Delete monitoring alerts (references analyses)
        alerts_deleted = db.execute(delete(MonitoringAlert)).rowcount
        print(f"  ✓ Deleted {alerts_deleted} monitoring alerts")
        
        # Delete monitoring rules (references analyses)
        rules_deleted = db.execute(delete(MonitoringRule)).rowcount
        print(f"  ✓ Deleted {rules_deleted} monitoring rules")
        
        # Delete negotiation insights (references analyses)
        insights_deleted = db.execute(delete(NegotiationInsight)).rowcount
        print(f"  ✓ Deleted {insights_deleted} negotiation insights")
        
        # Delete buyer fit (references analyses)
        buyer_fit_deleted = db.execute(delete(BuyerFit)).rowcount
        print(f"  ✓ Deleted {buyer_fit_deleted} buyer fit records")
        
        # Delete LMA deviations (references analyses)
        deviations_deleted = db.execute(delete(LMADeviation)).rowcount
        print(f"  ✓ Deleted {deviations_deleted} LMA deviations")
        
        # Delete transfer simulations (references analyses)
        transfers_deleted = db.execute(delete(TransferSimulation)).rowcount
        print(f"  ✓ Deleted {transfers_deleted} transfer simulations")
        
        # Delete trade readiness (references analyses)
        trade_readiness_deleted = db.execute(delete(TradeReadiness)).rowcount
        print(f"  ✓ Deleted {trade_readiness_deleted} trade readiness records")
        
        # Delete reports (references analyses)
        reports_deleted = db.execute(delete(Report)).rowcount
        print(f"  ✓ Deleted {reports_deleted} reports")
        
        # Delete documents (references analyses)
        documents_deleted = db.execute(delete(Document)).rowcount
        print(f"  ✓ Deleted {documents_deleted} documents")
        
        # Delete evidence logs (references analyses)
        evidence_logs_deleted = db.execute(delete(EvidenceLog)).rowcount
        print(f"  ✓ Deleted {evidence_logs_deleted} evidence logs")
        
        # Delete audit events (references analyses)
        audit_events_deleted = db.execute(delete(AuditEvent)).rowcount
        print(f"  ✓ Deleted {audit_events_deleted} audit events")
        
        # Delete analyses
        analyses_deleted = db.execute(delete(Analysis)).rowcount
        print(f"  ✓ Deleted {analyses_deleted} analyses")
        
        # Delete deals
        deals_deleted = db.execute(delete(Deal)).rowcount
        print(f"  ✓ Deleted {deals_deleted} deals")
        
        # Commit all deletions
        db.commit()
        
        print("\n✅ All analyses and related data cleared successfully!")
        print("\n📋 What was kept:")
        print("  ✓ Users (demo and admin accounts)")
        print("  ✓ Database structure")
        
        print("\n🚀 You can now:")
        print("  1. Upload new documents from the uploads folder")
        print("  2. Start fresh analyses")
        print("  3. Test with clean data")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error clearing data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    clear_analyses()
