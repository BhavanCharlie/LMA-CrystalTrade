import { useState, useEffect } from 'react'
import { Gavel, Clock, DollarSign, Users, Trophy, Plus, Send } from 'lucide-react'
import { api } from '../services/api'
import toast from 'react-hot-toast'

interface AuctionRoomProps {
  analysisId: string
  loanName: string
}

interface Auction {
  id: string
  analysis_id: string
  loan_name: string
  auction_type: 'english' | 'sealed_bid'
  lot_size: number
  min_bid: number
  bid_increment: number
  reserve_price: number
  start_time: string
  end_time: string
  status: 'pending' | 'active' | 'closed'
  winning_bid_id?: string
  created_by: string
  bid_count?: number
  current_leader?: {
    bidder_name: string
    bid_amount: number
  }
  winner?: {
    bidder_name: string
    bid_amount: number
    timestamp: string
  }
}

export default function AuctionRoom({ analysisId, loanName }: AuctionRoomProps) {
  const [auctions, setAuctions] = useState<Auction[]>([])
  const [selectedAuction, setSelectedAuction] = useState<Auction | null>(null)
  const [leaderboard, setLeaderboard] = useState<any[]>([])
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [timeRemaining, setTimeRemaining] = useState<string>('')
  
  // Create auction form state
  const [auctionForm, setAuctionForm] = useState({
    auction_type: 'english' as 'english' | 'sealed_bid',
    lot_size: '',
    min_bid: '',
    bid_increment: '',
    reserve_price: '',
    duration_hours: '24',
  })
  
  // Bid form state
  const [bidForm, setBidForm] = useState({
    bidder_name: 'Demo Institution',
    bid_amount: '',
  })

  useEffect(() => {
    fetchAuctions()
  }, [analysisId])

  // Countdown timer effect
  useEffect(() => {
    if (!selectedAuction || selectedAuction.status === 'closed') {
      setTimeRemaining('')
      return
    }

    const updateTimer = () => {
      const now = new Date().getTime()
      const end = new Date(selectedAuction.end_time).getTime()
      const diff = end - now

      if (diff <= 0) {
        setTimeRemaining('Auction Ended')
        loadAuctionDetails(selectedAuction.id)
        return
      }

      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((diff % (1000 * 60)) / 1000)

      if (days > 0) {
        setTimeRemaining(`${days}d ${hours}h ${minutes}m ${seconds}s`)
      } else if (hours > 0) {
        setTimeRemaining(`${hours}h ${minutes}m ${seconds}s`)
      } else if (minutes > 0) {
        setTimeRemaining(`${minutes}m ${seconds}s`)
      } else {
        setTimeRemaining(`${seconds}s`)
      }
    }

    updateTimer()
    const interval = setInterval(updateTimer, 1000)

    return () => clearInterval(interval)
  }, [selectedAuction])

  useEffect(() => {
    if (selectedAuction) {
      loadAuctionDetails(selectedAuction.id)
      if (selectedAuction.status === 'active') {
        // Increase polling interval to 5 seconds to reduce load
        const interval = setInterval(() => {
          loadAuctionDetails(selectedAuction.id)
        }, 5000) // Changed from 2000ms to 5000ms
        return () => clearInterval(interval)
      }
    }
  }, [selectedAuction])

  const loadAuctionDetails = async (auctionId: string) => {
    try {
      const [auctionData, leaderboardData] = await Promise.allSettled([
        api.getAuction(auctionId),
        api.getAuctionLeaderboard(auctionId),
      ])
      
      if (auctionData.status === 'fulfilled') {
        setSelectedAuction(auctionData.value as Auction)
      }
      
      if (leaderboardData.status === 'fulfilled') {
        setLeaderboard(leaderboardData.value.leaderboard || [])
      }
    } catch (error) {
      console.error('Failed to load auction details:', error)
    }
  }

  const createAuction = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const startTime = new Date()
      
      const auctionConfig = {
        analysis_id: analysisId,
        loan_name: loanName,
        auction_type: auctionForm.auction_type,
        lot_size: parseFloat(auctionForm.lot_size),
        min_bid: parseFloat(auctionForm.min_bid),
        bid_increment: parseFloat(auctionForm.bid_increment),
        reserve_price: parseFloat(auctionForm.reserve_price),
        start_time: startTime.toISOString(),
        duration_hours: parseInt(auctionForm.duration_hours),
        created_by: 'demo_user',
      }
      
      const newAuction = await api.createAuction(auctionConfig)
      toast.success('Auction created successfully!')
      setShowCreateForm(false)
      setAuctionForm({
        auction_type: 'english',
        lot_size: '',
        min_bid: '',
        bid_increment: '',
        reserve_price: '',
        duration_hours: '24',
      })
      // Reload auctions
      await fetchAuctions()
      if (newAuction) {
        setSelectedAuction(newAuction as any)
      }
    } catch (error: any) {
      toast.error(`Failed to create auction: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const placeBid = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedAuction) return
    
    // Validate bid amount
    const bidAmount = parseFloat(bidForm.bid_amount)
    if (isNaN(bidAmount) || bidAmount <= 0) {
      toast.error('Please enter a valid bid amount')
      return
    }
    
    if (bidAmount < selectedAuction.min_bid) {
      toast.error(`Bid must be at least $${selectedAuction.min_bid.toLocaleString()}`)
      return
    }
    
    // Check if bid meets increment requirement
    if (leaderboard.length > 0) {
      const highestBid = leaderboard[0].bid_amount
      const minRequiredBid = highestBid + selectedAuction.bid_increment
      if (bidAmount < minRequiredBid) {
        toast.error(`Bid must be at least $${minRequiredBid.toLocaleString()} (current highest: $${highestBid.toLocaleString()} + increment: $${selectedAuction.bid_increment.toLocaleString()})`)
        return
      }
    }
    
    setLoading(true)
    try {
      const bidData = {
        bidder_id: 'demo_bidder_' + Date.now(),
        bidder_name: bidForm.bidder_name || 'Demo Institution',
        bid_amount: bidAmount,
      }
      
      console.log('Placing bid:', { auctionId: selectedAuction.id, bidData })
      
      // Place bid with timeout handling
      const bidPromise = api.placeBid(selectedAuction.id, bidData)
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout - please try again')), 15000)
      )
      
      const result = await Promise.race([bidPromise, timeoutPromise])
      
      console.log('Bid placed successfully:', result)
      toast.success('Bid placed successfully!')
      setBidForm({ ...bidForm, bid_amount: '' })
      
      // Refresh auction details immediately
      await Promise.all([
        loadAuctionDetails(selectedAuction.id),
        fetchAuctions()
      ])
    } catch (error: any) {
      console.error('Bid placement error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        fullError: error
      })
      
      let errorMessage = 'Failed to place bid'
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.message) {
        errorMessage = error.message
      }
      
      if (errorMessage.includes('timeout') || errorMessage.includes('exceeded')) {
        toast.error('Bid placement timed out. Please check your connection and try again.')
      } else if (error.response?.status === 404) {
        toast.error('Auction not found. Please refresh and try again.')
      } else if (error.response?.status === 400) {
        toast.error(errorMessage)
      } else {
        toast.error(`Error: ${errorMessage}`)
      }
    } finally {
      setLoading(false)
    }
  }

  const closeAuction = async () => {
    if (!selectedAuction) return
    
    setLoading(true)
    try {
      const result = await api.closeAuction(selectedAuction.id)
      toast.success(`Auction closed! Winner: ${result.winner?.bidder_name || result.winning_bidder || 'No winner'}`)
      await loadAuctionDetails(selectedAuction.id)
      await fetchAuctions()
    } catch (error: any) {
      toast.error(`Failed to close auction: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const fetchAuctions = async () => {
    try {
      const auctionsData = await api.getAuctionsForAnalysis(analysisId)
      setAuctions(auctionsData)
      
      // Update selected auction if it exists in the list
      if (selectedAuction) {
        const updated = auctionsData.find((a: Auction) => a.id === selectedAuction.id)
        if (updated) {
          setSelectedAuction(updated)
        }
      } else if (auctionsData.length > 0) {
        // Auto-select first auction if none selected
        setSelectedAuction(auctionsData[0])
      }
    } catch (error) {
      console.error('Failed to fetch auctions:', error)
    }
  }

  useEffect(() => {
    fetchAuctions()
  }, [analysisId])

  const formatTime = (timeString: string) => {
    return new Date(timeString).toLocaleString()
  }

  return (
    <div className="space-y-6 fade-in">
      <div className="flex items-center justify-between glass-panel rounded-2xl p-6">
        <div className="flex items-center">
          <div className="p-3 rounded-xl bg-gradient-to-br from-orange-100 to-orange-200 mr-4">
            <Gavel className="w-6 h-6 text-orange-600" />
          </div>
          <h3 className="text-2xl font-bold gradient-text">Auction Room</h3>
        </div>
        <button
          onClick={() => setShowCreateForm(!showCreateForm)}
          className="btn-gradient flex items-center space-x-2 px-6 py-3 text-white rounded-xl font-semibold shadow-lg"
        >
          <Plus className="h-5 w-5" />
          <span>{showCreateForm ? 'Cancel' : 'Create Auction'}</span>
        </button>
      </div>

      {showCreateForm && (
        <div className="glass-panel rounded-2xl p-8 fade-in">
          <div className="flex items-center mb-6">
            <div className="p-3 rounded-xl bg-gradient-to-br from-primary-100 to-primary-200 mr-4">
              <Plus className="w-6 h-6 text-primary-600" />
            </div>
            <h4 className="text-xl font-bold gradient-text">Create New Auction</h4>
          </div>
          <form onSubmit={createAuction} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Auction Type
                </label>
                <select
                  value={auctionForm.auction_type}
                  onChange={(e) => setAuctionForm({ ...auctionForm, auction_type: e.target.value as any })}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  required
                >
                  <option value="english">English (Ascending)</option>
                  <option value="sealed_bid">Sealed Bid</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Duration (hours)
                </label>
                <input
                  type="number"
                  value={auctionForm.duration_hours}
                  onChange={(e) => setAuctionForm({ ...auctionForm, duration_hours: e.target.value })}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  min="1"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Lot Size ($)
                </label>
                <input
                  type="number"
                  value={auctionForm.lot_size}
                  onChange={(e) => setAuctionForm({ ...auctionForm, lot_size: e.target.value })}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  step="0.01"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Minimum Bid ($)
                </label>
                <input
                  type="number"
                  value={auctionForm.min_bid}
                  onChange={(e) => setAuctionForm({ ...auctionForm, min_bid: e.target.value })}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  step="0.01"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Bid Increment ($)
                </label>
                <input
                  type="number"
                  value={auctionForm.bid_increment}
                  onChange={(e) => setAuctionForm({ ...auctionForm, bid_increment: e.target.value })}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  step="0.01"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Reserve Price ($)
                </label>
                <input
                  type="number"
                  value={auctionForm.reserve_price}
                  onChange={(e) => setAuctionForm({ ...auctionForm, reserve_price: e.target.value })}
                  className="w-full border border-gray-300 rounded-md px-3 py-2"
                  step="0.01"
                  required
                />
              </div>
            </div>
            
            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 btn-gradient text-white px-6 py-4 rounded-xl font-bold text-lg disabled:bg-gray-400 disabled:cursor-not-allowed shadow-lg"
              >
                {loading ? 'Creating Auction...' : 'Create Auction'}
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="px-6 py-4 bg-gray-200 text-gray-700 rounded-xl hover:bg-gray-300 font-semibold transition-all"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {selectedAuction && (
        <div className="glass-panel rounded-2xl p-8 fade-in">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h4 className="text-2xl font-bold gradient-text mb-2">{selectedAuction.loan_name}</h4>
              <div className="flex items-center space-x-3">
                <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                  selectedAuction.status === 'active' ? 'bg-green-100 text-green-800' :
                  selectedAuction.status === 'closed' ? 'bg-gray-100 text-gray-800' :
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {selectedAuction.status.toUpperCase()}
                </span>
                <span className="text-sm text-gray-600 capitalize font-medium">
                  {selectedAuction.auction_type} Auction
                </span>
              </div>
            </div>
            {selectedAuction.status === 'active' && (
              <button
                onClick={closeAuction}
                disabled={loading}
                className="px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 disabled:bg-gray-400 font-bold shadow-lg transition-all"
              >
                Close Auction
              </button>
            )}
          </div>

          {/* Countdown Timer and Key Stats */}
          {selectedAuction.status === 'active' && (
            <div className="mb-8 p-6 bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 border-2 border-blue-200 rounded-2xl shadow-lg">
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div className="flex items-center space-x-6">
                  <div className="flex items-center space-x-3 glass-strong rounded-xl p-4">
                    <div className="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-blue-600">
                      <Clock className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide">Time Remaining</div>
                      <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                        {timeRemaining || 'Calculating...'}
                      </div>
                    </div>
                  </div>
                  <div className="h-16 w-px bg-gradient-to-b from-blue-300 to-indigo-300"></div>
                  <div className="flex items-center space-x-3 glass-strong rounded-xl p-4">
                    <div className="p-2 rounded-lg bg-gradient-to-br from-indigo-500 to-indigo-600">
                      <Users className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide">Total Bids</div>
                      <div className="text-3xl font-bold text-indigo-700">{selectedAuction.bid_count || 0}</div>
                    </div>
                  </div>
                </div>
                {selectedAuction.current_leader && (
                  <div className="flex items-center space-x-3 bg-gradient-to-r from-yellow-100 to-yellow-200 px-6 py-4 rounded-xl border-2 border-yellow-400 shadow-lg">
                    <div className="p-2 rounded-lg bg-gradient-to-br from-yellow-500 to-yellow-600">
                      <Trophy className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-gray-600 uppercase tracking-wide">Current Leader</div>
                      <div className="text-xl font-bold text-yellow-900">
                        {selectedAuction.current_leader.bidder_name}
                      </div>
                      <div className="text-lg font-bold text-yellow-700">
                        ${selectedAuction.current_leader.bid_amount.toLocaleString()}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Winner Display for Closed Auctions */}
          {selectedAuction.status === 'closed' && selectedAuction.winner && (
            <div className="mb-8 p-8 bg-gradient-to-r from-green-50 via-emerald-50 to-teal-50 border-2 border-green-400 rounded-2xl shadow-xl">
              <div className="flex items-center space-x-6">
                <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-4 shadow-lg">
                  <Trophy className="h-10 w-10 text-white" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-bold text-green-800 mb-2 uppercase tracking-wide">🎉 Auction Winner</div>
                  <div className="text-3xl font-bold text-green-900 mb-2">
                    {selectedAuction.winner.bidder_name}
                  </div>
                  <div className="text-xl text-green-700 mb-3">
                    Winning Bid: <span className="font-bold">${selectedAuction.winner.bid_amount.toLocaleString()}</span>
                  </div>
                  <div className="text-sm text-green-600 font-medium">
                    Won on {formatTime(selectedAuction.winner.timestamp)} • Total Bids: {selectedAuction.bid_count || 0}
                  </div>
                </div>
              </div>
            </div>
          )}

          {selectedAuction.status === 'closed' && !selectedAuction.winner && (
            <div className="mb-8 p-6 glass-strong rounded-2xl border-2 border-gray-300">
              <div className="text-center">
                <div className="bg-gray-200 rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <Trophy className="h-8 w-8 text-gray-400" />
                </div>
                <div className="font-bold text-gray-900 text-lg mb-2">No Winner</div>
                <div className="text-sm text-gray-600">Auction closed with {selectedAuction.bid_count || 0} bid(s). Reserve price not met.</div>
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div className="glass-strong rounded-xl p-4 text-center border-l-4 border-primary-500">
              <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Lot Size</div>
              <div className="text-2xl font-bold text-gray-900">${selectedAuction.lot_size.toLocaleString()}</div>
            </div>
            <div className="glass-strong rounded-xl p-4 text-center border-l-4 border-blue-500">
              <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Min Bid</div>
              <div className="text-2xl font-bold text-gray-900">${selectedAuction.min_bid.toLocaleString()}</div>
            </div>
            <div className="glass-strong rounded-xl p-4 text-center border-l-4 border-purple-500">
              <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Ends At</div>
              <div className="text-sm font-bold text-gray-900">{formatTime(selectedAuction.end_time)}</div>
            </div>
            <div className="glass-strong rounded-xl p-4 text-center border-l-4 border-green-500">
              <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Reserve</div>
              <div className="text-2xl font-bold text-gray-900">${selectedAuction.reserve_price.toLocaleString()}</div>
            </div>
          </div>

              {(selectedAuction.status === 'active' || selectedAuction.status === 'pending') && (
                <>
                  {selectedAuction.auction_type === 'english' && (
                    <div className="mb-8 glass-panel rounded-2xl p-6">
                      <div className="flex items-center justify-between mb-6">
                        <div className="flex items-center">
                          <div className="p-2 rounded-lg bg-gradient-to-br from-yellow-100 to-yellow-200 mr-3">
                            <Trophy className="h-5 w-5 text-yellow-600" />
                          </div>
                          <h5 className="text-lg font-bold text-gray-900">Leaderboard</h5>
                        </div>
                        <span className="px-4 py-2 rounded-xl bg-primary-100 text-primary-800 text-sm font-bold">
                          {leaderboard.length} {leaderboard.length === 1 ? 'bid' : 'bids'}
                        </span>
                      </div>
                      {leaderboard.length > 0 ? (
                        <div className="space-y-3">
                          {leaderboard.map((entry, idx) => (
                            <div key={idx} className={`flex items-center justify-between glass-strong rounded-xl p-4 transition-all ${
                              idx === 0 ? 'border-2 border-yellow-400 bg-gradient-to-r from-yellow-50 to-yellow-100 shadow-lg scale-105' : 'border border-gray-200'
                            }`}>
                              <div className="flex items-center space-x-4">
                                <div className={`w-12 h-12 rounded-xl flex items-center justify-center font-bold text-lg shadow-lg ${
                                  idx === 0 ? 'bg-gradient-to-br from-yellow-400 to-yellow-500 text-yellow-900' : 'bg-gradient-to-br from-gray-200 to-gray-300 text-gray-700'
                                }`}>
                                  {entry.rank}
                                </div>
                                <div>
                                  <div className={`font-bold text-base ${idx === 0 ? 'text-yellow-900' : 'text-gray-900'}`}>
                                    {entry.bidder_name}
                                    {idx === 0 && <span className="ml-2 text-xs bg-yellow-400 text-yellow-900 px-2 py-1 rounded-lg font-bold">LEADING</span>}
                                  </div>
                                  <div className="text-xs text-gray-500 font-medium mt-1">{formatTime(entry.timestamp)}</div>
                                </div>
                              </div>
                              <div className={`text-2xl font-bold ${idx === 0 ? 'text-yellow-700' : 'text-primary-600'}`}>
                                ${entry.bid_amount.toLocaleString()}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-center py-12 glass-strong rounded-xl">
                          <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                          <div className="font-bold text-gray-700 mb-2">No bids yet</div>
                          <div className="text-sm text-gray-600">Be the first to bid!</div>
                        </div>
                      )}
                    </div>
                  )}

              <form onSubmit={placeBid} className="glass-panel rounded-2xl p-6">
                <div className="flex items-center mb-6">
                  <div className="p-2 rounded-lg bg-gradient-to-br from-primary-100 to-primary-200 mr-3">
                    <DollarSign className="h-5 w-5 text-primary-600" />
                  </div>
                  <h5 className="text-lg font-bold text-gray-900">Place Bid</h5>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Bidder Name</label>
                    <input
                      type="text"
                      value={bidForm.bidder_name}
                      onChange={(e) => setBidForm({ ...bidForm, bidder_name: e.target.value })}
                      className="w-full glass-strong border border-gray-300 rounded-xl px-4 py-3 font-medium focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">Bid Amount ($)</label>
                    <input
                      type="number"
                      value={bidForm.bid_amount}
                      onChange={(e) => setBidForm({ ...bidForm, bid_amount: e.target.value })}
                      className="w-full glass-strong border border-gray-300 rounded-xl px-4 py-3 font-medium focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
                      step={selectedAuction.bid_increment || 0.01}
                      min={leaderboard.length > 0 
                        ? leaderboard[0].bid_amount + (selectedAuction.bid_increment || 0.01)
                        : selectedAuction.min_bid}
                      placeholder={leaderboard.length > 0 
                        ? `Min: $${(leaderboard[0].bid_amount + (selectedAuction.bid_increment || 0.01)).toLocaleString()}`
                        : `Min: $${selectedAuction.min_bid.toLocaleString()}`}
                      required
                    />
                    {leaderboard.length > 0 ? (
                      <div className="text-xs text-gray-600 mt-2 font-medium bg-blue-50 rounded-lg p-2">
                        Current highest: <span className="font-bold">${leaderboard[0].bid_amount.toLocaleString()}</span> | 
                        Min next bid: <span className="font-bold text-primary-600">${(leaderboard[0].bid_amount + (selectedAuction.bid_increment || 0.01)).toLocaleString()}</span>
                      </div>
                    ) : (
                      <div className="text-xs text-gray-600 mt-2 font-medium bg-blue-50 rounded-lg p-2">
                        Minimum bid: <span className="font-bold">${selectedAuction.min_bid.toLocaleString()}</span> | 
                        Increment: <span className="font-bold">${(selectedAuction.bid_increment || 0.01).toLocaleString()}</span>
                      </div>
                    )}
                  </div>
                </div>
                <button
                  type="submit"
                  disabled={loading || (selectedAuction.status !== 'active' && selectedAuction.status !== 'pending')}
                  className="mt-6 w-full btn-gradient text-white px-6 py-4 rounded-xl font-bold text-lg disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center space-x-2 shadow-lg"
                >
                  <Send className="h-5 w-5" />
                  <span>{loading ? 'Placing Bid...' : 'Place Bid'}</span>
                </button>
              </form>
            </>
          )}

        </div>
      )}

      {auctions.length > 0 && !selectedAuction && !showCreateForm && (
        <div className="glass-panel rounded-2xl p-8 fade-in">
          <h4 className="text-xl font-bold gradient-text mb-6">Existing Auctions</h4>
          <div className="space-y-4">
            {auctions.map((auction, idx) => (
              <div
                key={auction.id}
                onClick={() => setSelectedAuction(auction)}
                className="glass-strong rounded-xl p-6 cursor-pointer card-hover fade-in border-l-4 border-primary-500"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="font-bold text-lg text-gray-900">{auction.loan_name}</div>
                      <span className={`px-3 py-1 rounded-lg text-xs font-bold ${
                        auction.status === 'active' ? 'bg-green-100 text-green-800' :
                        auction.status === 'closed' ? 'bg-gray-100 text-gray-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {auction.status.toUpperCase()}
                      </span>
                    </div>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span className="capitalize font-medium">{auction.auction_type}</span>
                      <span>•</span>
                      <span className="font-bold text-gray-900">Lot: ${auction.lot_size.toLocaleString()}</span>
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-1">Ends</div>
                    <div className="text-sm font-bold text-gray-900">{formatTime(auction.end_time)}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {auctions.length === 0 && !selectedAuction && !showCreateForm && (
        <div className="glass-panel rounded-2xl p-12 text-center fade-in">
          <div className="bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl p-6 w-20 h-20 mx-auto mb-6 flex items-center justify-center">
            <Gavel className="h-10 w-10 text-gray-400" />
          </div>
          <h4 className="text-xl font-bold text-gray-900 mb-2">No Auctions</h4>
          <p className="text-sm text-gray-600 font-medium mb-6">Create your first auction to get started</p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="btn-gradient px-6 py-3 rounded-xl font-bold text-white shadow-lg"
          >
            Create First Auction
          </button>
        </div>
      )}
    </div>
  )
}

