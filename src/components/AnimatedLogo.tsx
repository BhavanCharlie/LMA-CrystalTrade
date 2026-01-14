import './AnimatedLogo.css'

interface AnimatedLogoProps {
  size?: 'sm' | 'md' | 'lg'
  showText?: boolean
  className?: string
}

export default function AnimatedLogo({ 
  size = 'md', 
  showText = true,
  className = '' 
}: AnimatedLogoProps) {

  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
  }

  const textSizeClasses = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl',
  }

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <div className={`relative ${sizeClasses[size]}`}>
        {/* Outer crystal ring */}
        <svg
          className="absolute inset-0 w-full h-full"
          viewBox="0 0 64 64"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Animated crystal facets */}
          <g className="crystal-facets">
            <path
              d="M32 8 L40 20 L32 32 L24 20 Z"
              fill="url(#crystalGradient1)"
              className="crystal-facet-1"
            />
            <path
              d="M32 32 L40 44 L32 56 L24 44 Z"
              fill="url(#crystalGradient2)"
              className="crystal-facet-2"
            />
            <path
              d="M32 8 L40 20 L48 16 L40 4 Z"
              fill="url(#crystalGradient3)"
              className="crystal-facet-3"
            />
            <path
              d="M16 16 L24 20 L32 8 L24 4 Z"
              fill="url(#crystalGradient4)"
              className="crystal-facet-4"
            />
            <path
              d="M48 48 L40 44 L32 56 L40 60 Z"
              fill="url(#crystalGradient5)"
              className="crystal-facet-5"
            />
            <path
              d="M16 48 L24 44 L32 56 L24 60 Z"
              fill="url(#crystalGradient6)"
              className="crystal-facet-6"
            />
            
            {/* Center hexagon representing transparency */}
            <path
              d="M32 20 L38 26 L38 32 L32 38 L26 32 L26 26 Z"
              fill="url(#centerGradient)"
              className="center-hexagon"
            />
            
            {/* Trading arrows */}
            <path
              d="M20 32 L28 32 M28 28 L28 32 L24 36"
              stroke="url(#arrowGradient)"
              strokeWidth="2"
              strokeLinecap="round"
              className="arrow-left"
            />
            <path
              d="M44 32 L36 32 M36 28 L36 32 L40 36"
              stroke="url(#arrowGradient)"
              strokeWidth="2"
              strokeLinecap="round"
              className="arrow-right"
            />

            {/* Gradients */}
            <defs>
              <linearGradient id="crystalGradient1" x1="32" y1="8" x2="32" y2="32">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.9" />
                <stop offset="100%" stopColor="#38bdf8" stopOpacity="0.6" />
              </linearGradient>
              <linearGradient id="crystalGradient2" x1="32" y1="32" x2="32" y2="56">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.6" />
                <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0.9" />
              </linearGradient>
              <linearGradient id="crystalGradient3" x1="32" y1="8" x2="48" y2="16">
                <stop offset="0%" stopColor="#7dd3fc" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0.5" />
              </linearGradient>
              <linearGradient id="crystalGradient4" x1="16" y1="16" x2="32" y2="8">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.5" />
                <stop offset="100%" stopColor="#7dd3fc" stopOpacity="0.8" />
              </linearGradient>
              <linearGradient id="crystalGradient5" x1="48" y1="48" x2="32" y2="56">
                <stop offset="0%" stopColor="#7dd3fc" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0.5" />
              </linearGradient>
              <linearGradient id="crystalGradient6" x1="16" y1="48" x2="32" y2="56">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.5" />
                <stop offset="100%" stopColor="#7dd3fc" stopOpacity="0.8" />
              </linearGradient>
              <linearGradient id="centerGradient" x1="26" y1="20" x2="38" y2="38">
                <stop offset="0%" stopColor="#ffffff" stopOpacity="0.9" />
                <stop offset="50%" stopColor="#e0f2fe" stopOpacity="0.7" />
                <stop offset="100%" stopColor="#ffffff" stopOpacity="0.9" />
              </linearGradient>
              <linearGradient id="arrowGradient" x1="20" y1="32" x2="44" y2="32">
                <stop offset="0%" stopColor="#10b981" />
                <stop offset="50%" stopColor="#0ea5e9" />
                <stop offset="100%" stopColor="#10b981" />
              </linearGradient>
            </defs>
          </g>
        </svg>

        {/* Shimmer effect */}
        <div className="absolute inset-0 shimmer-overlay" />
      </div>

      {showText && (
        <div className={`font-bold ${textSizeClasses[size]} bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent`}>
          CrystalTrade
        </div>
      )}

    </div>
  )
}

