"""
Auction / Bidding Module
Manages English (ascending) and sealed-bid auctions
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class AuctionService:
    def __init__(self):
        pass

    async def create_auction(
        self, analysis_id: str, auction_config: Dict, created_by: str
    ) -> Dict[str, Any]:
        """Create a new auction"""
        auction_id = str(uuid.uuid4())
        
        # Parse times
        start_time = datetime.fromisoformat(auction_config.get("start_time", datetime.utcnow().isoformat()))
        duration_hours = auction_config.get("duration_hours", 24)
        end_time = start_time + timedelta(hours=duration_hours)
        
        return {
            "id": auction_id,
            "analysis_id": analysis_id,
            "loan_name": auction_config.get("loan_name", "Unnamed Loan"),
            "auction_type": auction_config.get("auction_type", "english"),
            "lot_size": float(auction_config.get("lot_size", 0.0)),
            "min_bid": float(auction_config.get("min_bid", 0.0)),
            "bid_increment": float(auction_config.get("bid_increment", 0.01)),
            "reserve_price": float(auction_config.get("reserve_price", 0.0)),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "status": "pending",
            "created_by": created_by,
            "created_at": datetime.utcnow().isoformat(),
        }

    async def place_bid(
        self, auction_id: str, bidder_id: str, bidder_name: str, bid_amount: float, auction: Dict, existing_bids: List[Dict] = None
    ) -> Dict[str, Any]:
        """Place a bid on an auction"""
        # Validate bid
        validation_result = self._validate_bid(auction, bid_amount, existing_bids or [])
        if not validation_result["valid"]:
            raise ValueError(validation_result["error"])
        
        bid_id = str(uuid.uuid4())
        
        return {
            "id": bid_id,
            "auction_id": auction_id,
            "bidder_id": bidder_id,
            "bidder_name": bidder_name,
            "bid_amount": bid_amount,
            "is_locked": False,
            "timestamp": datetime.utcnow().isoformat(),
            "is_winning": False,
        }

    async def close_auction(self, auction: Dict, bids: List[Dict]) -> Dict[str, Any]:
        """Close an auction and determine winner"""
        auction_type = auction.get("auction_type", "english")
        
        if auction_type == "english":
            return self._close_english_auction(auction, bids)
        elif auction_type == "sealed_bid":
            return self._close_sealed_bid_auction(auction, bids)
        else:
            raise ValueError(f"Unknown auction type: {auction_type}")

    def _close_english_auction(self, auction: Dict, bids: List[Dict]) -> Dict[str, Any]:
        """Close English (ascending) auction"""
        if not bids:
            return {
                "winning_bid_id": None,
                "winning_bidder": None,
                "winning_amount": None,
                "status": "no_bids",
            }
        
        # Highest bid wins
        winning_bid = max(bids, key=lambda b: b.get("bid_amount", 0.0))
        
        # Check reserve price
        reserve_price = auction.get("reserve_price", 0.0)
        if winning_bid.get("bid_amount", 0.0) < reserve_price:
            return {
                "winning_bid_id": None,
                "winning_bidder": None,
                "winning_amount": None,
                "status": "reserve_not_met",
            }
        
        return {
            "winning_bid_id": winning_bid.get("id"),
            "winning_bidder": winning_bid.get("bidder_name"),
            "winning_amount": winning_bid.get("bid_amount"),
            "status": "closed",
            "total_bids": len(bids),
        }

    def _close_sealed_bid_auction(self, auction: Dict, bids: List[Dict]) -> Dict[str, Any]:
        """Close sealed-bid auction"""
        if not bids:
            return {
                "winning_bid_id": None,
                "winning_bidder": None,
                "winning_amount": None,
                "status": "no_bids",
            }
        
        # Highest bid wins (same as English, but revealed at close)
        winning_bid = max(bids, key=lambda b: b.get("bid_amount", 0.0))
        
        # Check reserve price
        reserve_price = auction.get("reserve_price", 0.0)
        if winning_bid.get("bid_amount", 0.0) < reserve_price:
            return {
                "winning_bid_id": None,
                "winning_bidder": None,
                "winning_amount": None,
                "status": "reserve_not_met",
            }
        
        return {
            "winning_bid_id": winning_bid.get("id"),
            "winning_bidder": winning_bid.get("bidder_name"),
            "winning_amount": winning_bid.get("bid_amount"),
            "status": "closed",
            "total_bids": len(bids),
            "all_bids": [{"bidder": b.get("bidder_name"), "amount": b.get("bid_amount")} for b in bids],
        }

    def _validate_bid(self, auction: Dict, bid_amount: float, existing_bids: List[Dict] = None) -> Dict[str, Any]:
        """Validate a bid - optimized for speed"""
        if existing_bids is None:
            existing_bids = []
        
        # Check auction status - allow pending auctions to become active
        status = auction.get("status", "pending")
        if status == "closed":
            return {"valid": False, "error": "Auction is closed"}
        
        # Check timing - simplified to avoid timezone issues
        try:
            end_time_str = auction.get("end_time")
            if end_time_str:
                # Simple string comparison for ISO format (faster)
                if isinstance(end_time_str, str):
                    # Extract just the date/time part for comparison
                    end_time_clean = end_time_str.split('+')[0].split('Z')[0].split('.')[0]
                    now_clean = datetime.utcnow().isoformat().split('.')[0]
                    if now_clean > end_time_clean:
                        return {"valid": False, "error": "Auction has closed"}
        except Exception:
            # If time parsing fails, allow the bid (better UX than blocking)
            pass
        
        # Check minimum bid
        try:
            min_bid = float(auction.get("min_bid", 0.0))
            if bid_amount < min_bid:
                return {"valid": False, "error": f"Bid must be at least ${min_bid:,.2f}"}
        except (ValueError, TypeError):
            return {"valid": False, "error": "Invalid minimum bid configuration"}
        
        # Check bid increment against current highest bid
        try:
            bid_increment = float(auction.get("bid_increment", 0.01))
            if existing_bids:
                highest_bid = max((float(b.get("bid_amount", 0.0)) for b in existing_bids), default=0.0)
                if highest_bid > 0:
                    min_required_bid = highest_bid + bid_increment
                    if bid_amount < min_required_bid:
                        return {"valid": False, "error": f"Bid must be at least ${min_required_bid:,.2f} (current highest: ${highest_bid:,.2f} + increment: ${bid_increment:,.2f})"}
        except (ValueError, TypeError):
            # If increment check fails, just check minimum bid
            pass
        
        return {"valid": True}

    async def get_auction_leaderboard(self, auction: Dict, bids: List[Dict]) -> List[Dict]:
        """Get leaderboard for English auction"""
        if auction.get("auction_type") != "english":
            return []
        
        # Sort by bid amount descending
        sorted_bids = sorted(bids, key=lambda b: b.get("bid_amount", 0.0), reverse=True)
        
        return [
            {
                "rank": idx + 1,
                "bidder_name": bid.get("bidder_name"),
                "bid_amount": bid.get("bid_amount"),
                "timestamp": bid.get("timestamp"),
            }
            for idx, bid in enumerate(sorted_bids[:10])  # Top 10
        ]

