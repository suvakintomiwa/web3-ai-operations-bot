export default function Footer() {
  return (
    <footer className="border-t border-cyan-500/10 bg-gray-950/50 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-cyan-500 rounded-lg flex items-center justify-center text-gray-950 font-black text-sm">
                W3
              </div>
              <span className="text-cyan-400 font-black text-xl">NEXUS<span className="text-white">BOT</span></span>
            </div>
            <p className="text-gray-500 text-sm leading-relaxed">
              Your personal Web3 AI Telegram assistant. Built for solo operators. Powered by free tools.
            </p>
            <div className="mt-4 flex items-center gap-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              <span className="text-green-400 text-xs">All systems free</span>
            </div>
          </div>

          {/* Quick links */}
          <div>
            <h4 className="text-white font-black mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-gray-500">
              {[
                { label: '📋 Commands Reference', href: '#commands' },
                { label: '🛠️ Tech Stack', href: '#features' },
                { label: '🚀 Setup Guide', href: '#setup' },
                { label: '🚂 Railway Deploy', href: '#deploy' },
                { label: '🤖 Get Bot Token', href: 'https://t.me/BotFather' },
                { label: '⚡ Get Groq Key', href: 'https://console.groq.com' },
              ].map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    className="hover:text-cyan-400 transition-colors duration-200"
                    target={link.href.startsWith('http') ? '_blank' : undefined}
                    rel={link.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Free API keys */}
          <div>
            <h4 className="text-white font-black mb-4">Free API Keys</h4>
            <ul className="space-y-2 text-sm text-gray-500">
              {[
                { label: '⚡ Groq (LLaMA 3)', href: 'https://console.groq.com', badge: 'FREE', color: 'text-cyan-400' },
                { label: '🌐 OpenRouter', href: 'https://openrouter.ai', badge: 'FREE', color: 'text-purple-400' },
                { label: '💎 Google Gemini', href: 'https://aistudio.google.com', badge: 'FREE', color: 'text-green-400' },
                { label: '🐋 DeepSeek', href: 'https://platform.deepseek.com', badge: 'FREE', color: 'text-yellow-400' },
                { label: '📊 CoinMarketCap', href: 'https://coinmarketcap.com/api/', badge: 'FREE', color: 'text-orange-400' },
                { label: '📡 DexScreener', href: 'https://docs.dexscreener.com', badge: 'NO KEY', color: 'text-pink-400' },
              ].map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors duration-200 flex items-center gap-2"
                  >
                    {link.label}
                    <span className={`text-xs font-bold ${link.color}`}>[{link.badge}]</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Stack badges */}
        <div className="border-t border-gray-800 pt-8 mb-8">
          <div className="flex flex-wrap gap-2 justify-center">
            {[
              'Python 3.11', 'aiogram 3.x', 'APScheduler', 'SQLite', 'aiosqlite',
              'Groq API', 'OpenRouter', 'Gemini', 'DeepSeek',
              'DexScreener', 'CoinGecko', 'BeautifulSoup4', 'Railway',
            ].map((tech) => (
              <span key={tech} className="px-3 py-1 rounded-full border border-gray-700 text-gray-500 text-xs hover:border-cyan-500/30 hover:text-gray-400 transition-colors duration-200">
                {tech}
              </span>
            ))}
          </div>
        </div>

        {/* Bottom bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-gray-600 text-xs">
          <div>
            Built for Web3 operators · Community Managers · Alpha Hunters · Zero budget required
          </div>
          <div className="flex items-center gap-4">
            <span>🐍 Python</span>
            <span>·</span>
            <span>🚂 Railway</span>
            <span>·</span>
            <span>💸 $0/month</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
