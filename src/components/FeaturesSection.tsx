import { useState } from 'react';

const featureCategories = [
  {
    id: 'discovery',
    icon: '🔍',
    title: 'Alpha Discovery Engine',
    color: 'cyan',
    description: 'Scrapes 10+ sources in real-time to surface new gems before they moon.',
    features: [
      { icon: '📡', text: 'DexScreener new pair scanner (every 5 mins)' },
      { icon: '🎯', text: 'Pump.fun launch tracker with AI scoring' },
      { icon: '📊', text: 'CoinGecko trending + gainers feed' },
      { icon: '🦁', text: 'CoinMarketCap new listings monitor' },
      { icon: '🐙', text: 'GitHub trending crypto repos' },
      { icon: '🔴', text: 'Reddit crypto community scanner' },
      { icon: '🌊', text: 'Solana, Base, Ethereum ecosystem filters' },
    ],
  },
  {
    id: 'jobs',
    icon: '💼',
    title: 'Web3 Job Hunter',
    color: 'purple',
    description: 'Automatically finds CM, Mod, NFT, and tester roles across platforms.',
    features: [
      { icon: '🎯', text: 'Community Manager job alerts (daily)' },
      { icon: '🛡️', text: 'Moderator role openings scanner' },
      { icon: '🎨', text: 'NFT artist & designer gig finder' },
      { icon: '🧪', text: 'Protocol tester opportunity tracker' },
      { icon: '📢', text: 'KOL / Influencer collab alerts' },
      { icon: '🌐', text: 'Remote-first Web3 role filter' },
      { icon: '✍️', text: 'AI-written custom application DMs' },
    ],
  },
  {
    id: 'ai',
    icon: '🤖',
    title: 'Multi-Model AI Brain',
    color: 'green',
    description: 'Falls back across 4 free AI APIs so you\'re never left without assistance.',
    features: [
      { icon: '⚡', text: 'Groq (primary) — blazing fast LLaMA 3' },
      { icon: '🌐', text: 'OpenRouter free models fallback' },
      { icon: '💎', text: 'Google Gemini free tier fallback' },
      { icon: '🐋', text: 'DeepSeek free API last resort' },
      { icon: '✍️', text: 'Raid message writer & shill generator' },
      { icon: '📬', text: 'KOL outreach DM composer' },
      { icon: '🔬', text: 'Project legitimacy analyzer' },
    ],
  },
  {
    id: 'alerts',
    icon: '🔔',
    title: 'Auto Alert System',
    color: 'yellow',
    description: 'Scheduled jobs push real-time alerts straight to your Telegram.',
    features: [
      { icon: '🐋', text: 'Whale wallet movement alerts' },
      { icon: '🔥', text: 'New meme coin launch notifications' },
      { icon: '📈', text: 'Trending project momentum alerts' },
      { icon: '🪂', text: 'Airdrop opportunity notifications' },
      { icon: '💼', text: 'Remote Web3 job postings push' },
      { icon: '⚠️', text: 'Scam project warnings' },
      { icon: '⏰', text: 'Custom reminder scheduler' },
    ],
  },
  {
    id: 'outreach',
    icon: '📬',
    title: 'Outreach & Community Tools',
    color: 'pink',
    description: 'Everything you need to run raids, grow communities, and network.',
    features: [
      { icon: '⚔️', text: 'Raid message templates + AI writer' },
      { icon: '🎙️', text: 'Shill content generator for Twitter/X' },
      { icon: '📊', text: 'Engagement strategy planner' },
      { icon: '🤝', text: 'Network contact manager (SQLite)' },
      { icon: '📋', text: 'Outreach history tracker' },
      { icon: '🔁', text: 'Follow-up reminder system' },
      { icon: '🏷️', text: 'Project tagging & watchlist' },
    ],
  },
  {
    id: 'analysis',
    icon: '🔬',
    title: 'Project Analyzer',
    color: 'orange',
    description: 'Paste any address, URL, or handle — get a full AI-powered audit.',
    features: [
      { icon: '🔗', text: 'Token contract address analyzer' },
      { icon: '🐦', text: 'Twitter/X fake engagement detector' },
      { icon: '📢', text: 'Telegram community health check' },
      { icon: '⚠️', text: 'Rug pull risk scoring (0-100)' },
      { icon: '📊', text: 'Market cap + liquidity analysis' },
      { icon: '🎨', text: 'Branding & website quality check' },
      { icon: '🤖', text: 'AI summary with go/no-go verdict' },
    ],
  },
];

const colorMap: Record<string, string> = {
  cyan: 'border-cyan-500/30 hover:border-cyan-500/60 bg-cyan-500/5',
  purple: 'border-purple-500/30 hover:border-purple-500/60 bg-purple-500/5',
  green: 'border-green-500/30 hover:border-green-500/60 bg-green-500/5',
  yellow: 'border-yellow-500/30 hover:border-yellow-500/60 bg-yellow-500/5',
  pink: 'border-pink-500/30 hover:border-pink-500/60 bg-pink-500/5',
  orange: 'border-orange-500/30 hover:border-orange-500/60 bg-orange-500/5',
};

const textColorMap: Record<string, string> = {
  cyan: 'text-cyan-400',
  purple: 'text-purple-400',
  green: 'text-green-400',
  yellow: 'text-yellow-400',
  pink: 'text-pink-400',
  orange: 'text-orange-400',
};

export default function FeaturesSection() {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <section id="features" className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-purple-500/40 bg-purple-500/10 text-purple-400 text-sm mb-6">
            🤖 FEATURE ARSENAL
          </div>
          <h2 className="text-4xl sm:text-5xl font-black text-white mb-4">
            Built for the{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">
              Solo Web3 Operator
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Every feature is hand-crafted for community managers, alpha hunters, and crypto freelancers — with zero monthly cost.
          </p>
        </div>

        {/* Feature cards grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featureCategories.map((cat) => (
            <div
              key={cat.id}
              className={`border rounded-2xl p-6 transition-all duration-300 cursor-pointer ${colorMap[cat.color]}`}
              onClick={() => setExpanded(expanded === cat.id ? null : cat.id)}
            >
              {/* Card header */}
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="text-3xl mb-2">{cat.icon}</div>
                  <h3 className={`text-lg font-black ${textColorMap[cat.color]}`}>{cat.title}</h3>
                </div>
                <span className="text-gray-500 text-xl">{expanded === cat.id ? '▼' : '▶'}</span>
              </div>

              <p className="text-gray-400 text-sm mb-4">{cat.description}</p>

              {/* Feature list */}
              <div className={`space-y-2 overflow-hidden transition-all duration-300 ${expanded === cat.id ? 'max-h-96' : 'max-h-20'}`}>
                {cat.features.map((feature, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm">
                    <span className="flex-shrink-0">{feature.icon}</span>
                    <span className="text-gray-300">{feature.text}</span>
                  </div>
                ))}
              </div>

              {!expanded !== (expanded === cat.id) && cat.features.length > 3 && (
                <div className={`text-xs mt-2 ${textColorMap[cat.color]}`}>
                  {expanded === cat.id ? 'Click to collapse' : `+${cat.features.length - 3} more features`}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Bottom banner */}
        <div className="mt-16 border border-green-500/30 bg-green-500/5 rounded-2xl p-8 text-center">
          <div className="text-4xl mb-4">💸</div>
          <h3 className="text-2xl font-black text-green-400 mb-2">Total Monthly Cost: $0.00</h3>
          <p className="text-gray-400 max-w-xl mx-auto">
            Railway free tier · Groq free API · OpenRouter free models · Gemini free tier · SQLite · DexScreener free API · CoinGecko free tier
          </p>
        </div>
      </div>
    </section>
  );
}
