const techItems = [
  {
    category: '🤖 Bot Framework',
    color: 'cyan',
    items: [
      { name: 'Python 3.11+', badge: 'Runtime', detail: 'Async-ready, fast, free' },
      { name: 'aiogram 3.x', badge: 'Primary', detail: 'Best async Telegram library' },
      { name: 'APScheduler', badge: 'Scheduler', detail: 'Background job runner' },
      { name: 'python-dotenv', badge: 'Config', detail: 'Env variable management' },
    ],
  },
  {
    category: '🧠 AI APIs (Free Tier)',
    color: 'purple',
    items: [
      { name: 'Groq API', badge: 'Primary', detail: 'LLaMA 3 — 14,400 req/day free' },
      { name: 'OpenRouter', badge: 'Fallback 1', detail: 'Multiple free models' },
      { name: 'Google Gemini', badge: 'Fallback 2', detail: '60 req/min free tier' },
      { name: 'DeepSeek API', badge: 'Fallback 3', detail: 'Free generous limits' },
    ],
  },
  {
    category: '🌐 Data Sources (All Free)',
    color: 'green',
    items: [
      { name: 'DexScreener API', badge: 'Free', detail: 'New pairs + trending' },
      { name: 'CoinGecko API', badge: 'Free', detail: '30 calls/min free tier' },
      { name: 'CoinMarketCap', badge: 'Free', detail: 'Basic plan — free' },
      { name: 'GitHub API', badge: 'Free', detail: '60 req/hr unauthenticated' },
      { name: 'Reddit API', badge: 'Free', detail: 'PRAW library' },
      { name: 'BeautifulSoup', badge: 'Scraper', detail: 'Web scraping fallback' },
    ],
  },
  {
    category: '🗄️ Database & Storage',
    color: 'yellow',
    items: [
      { name: 'SQLite', badge: 'Primary DB', detail: 'Zero cost, file-based' },
      { name: 'aiosqlite', badge: 'Async', detail: 'Non-blocking DB ops' },
      { name: 'Local filesystem', badge: 'Storage', detail: 'Notes, logs, cache' },
    ],
  },
  {
    category: '🚀 Deployment (Free)',
    color: 'orange',
    items: [
      { name: 'Railway.app', badge: 'Host', detail: 'Free tier — 500hr/month' },
      { name: 'Procfile', badge: 'Process', detail: 'Simple worker definition' },
      { name: 'railway.json', badge: 'Config', detail: 'Auto-deploy on push' },
      { name: 'GitHub Actions', badge: 'CI/CD', detail: 'Auto-deploy pipeline' },
    ],
  },
  {
    category: '🛠️ Utilities',
    color: 'pink',
    items: [
      { name: 'requests', badge: 'HTTP', detail: 'API calls & scraping' },
      { name: 'aiohttp', badge: 'Async HTTP', detail: 'Non-blocking requests' },
      { name: 'BeautifulSoup4', badge: 'HTML Parse', detail: 'Web scraping' },
      { name: 'loguru', badge: 'Logging', detail: 'Beautiful log output' },
    ],
  },
];

const colorMap: Record<string, { border: string; title: string; badge: string }> = {
  cyan: { border: 'border-cyan-500/30', title: 'text-cyan-400', badge: 'bg-cyan-500/20 text-cyan-300' },
  purple: { border: 'border-purple-500/30', title: 'text-purple-400', badge: 'bg-purple-500/20 text-purple-300' },
  green: { border: 'border-green-500/30', title: 'text-green-400', badge: 'bg-green-500/20 text-green-300' },
  yellow: { border: 'border-yellow-500/30', title: 'text-yellow-400', badge: 'bg-yellow-500/20 text-yellow-300' },
  orange: { border: 'border-orange-500/30', title: 'text-orange-400', badge: 'bg-orange-500/20 text-orange-300' },
  pink: { border: 'border-pink-500/30', title: 'text-pink-400', badge: 'bg-pink-500/20 text-pink-300' },
};

const aiFallbackSteps = [
  { step: '1', name: 'Groq (LLaMA 3)', speed: 'Lightning fast', color: 'text-cyan-400', note: 'Primary — 14,400 req/day' },
  { step: '2', name: 'OpenRouter', speed: 'Fast', color: 'text-purple-400', note: 'Fallback — free models' },
  { step: '3', name: 'Google Gemini', speed: 'Medium', color: 'text-green-400', note: 'Fallback — 60 RPM free' },
  { step: '4', name: 'DeepSeek', speed: 'Good', color: 'text-yellow-400', note: 'Last resort — generous limits' },
];

export default function TechStackSection() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-green-500/40 bg-green-500/10 text-green-400 text-sm mb-6">
            🛠️ TECH STACK
          </div>
          <h2 className="text-4xl sm:text-5xl font-black text-white mb-4">
            100% Free{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-cyan-400">
              Infrastructure
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Carefully chosen tools that maximize capability while keeping costs at exactly $0.
          </p>
        </div>

        {/* AI Fallback Chain */}
        <div className="mb-16 border border-purple-500/30 bg-purple-500/5 rounded-2xl p-8">
          <h3 className="text-purple-400 font-black text-xl mb-6 text-center">🧠 AI Fallback Chain — Always Online</h3>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            {aiFallbackSteps.map((step, i) => (
              <div key={step.step} className="flex items-center gap-4">
                <div className="text-center">
                  <div className={`w-12 h-12 rounded-full border-2 border-current flex items-center justify-center mx-auto mb-2 ${step.color}`}>
                    <span className="font-black">{step.step}</span>
                  </div>
                  <div className={`font-bold text-sm ${step.color}`}>{step.name}</div>
                  <div className="text-gray-500 text-xs mt-1">{step.note}</div>
                </div>
                {i < aiFallbackSteps.length - 1 && (
                  <div className="text-gray-600 text-2xl hidden sm:block">→</div>
                )}
              </div>
            ))}
          </div>
          <p className="text-center text-gray-500 text-sm mt-6">
            If Groq fails → tries OpenRouter → if that fails → tries Gemini → DeepSeek as last resort
          </p>
        </div>

        {/* Tech grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {techItems.map((cat) => {
            const colors = colorMap[cat.color];
            return (
              <div key={cat.category} className={`border rounded-2xl p-6 ${colors.border} bg-gray-900/30`}>
                <h3 className={`font-black text-base mb-4 ${colors.title}`}>{cat.category}</h3>
                <div className="space-y-3">
                  {cat.items.map((item) => (
                    <div key={item.name} className="flex items-center justify-between gap-3">
                      <div className="min-w-0">
                        <div className="text-white text-sm font-semibold truncate">{item.name}</div>
                        <div className="text-gray-500 text-xs">{item.detail}</div>
                      </div>
                      <span className={`flex-shrink-0 px-2 py-0.5 rounded text-xs font-bold ${colors.badge}`}>
                        {item.badge}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Cost breakdown */}
        <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="border border-red-500/20 bg-red-500/5 rounded-2xl p-6 text-center">
            <div className="text-3xl mb-2">❌</div>
            <div className="text-red-400 font-black text-lg mb-2">What Others Pay</div>
            <div className="text-gray-400 text-sm space-y-1">
              <div>OpenAI GPT-4: $20+/mo</div>
              <div>AWS/Firebase: $15+/mo</div>
              <div>Redis Cloud: $7+/mo</div>
              <div>Paid hosting: $10+/mo</div>
              <div className="text-red-400 font-bold pt-2 border-t border-red-500/20">Total: $52+/mo</div>
            </div>
          </div>
          <div className="border border-gray-700/30 bg-gray-800/20 rounded-2xl p-6 text-center flex items-center justify-center">
            <div>
              <div className="text-4xl mb-2">⚡</div>
              <div className="text-gray-400 font-black text-lg">NEXUSBOT</div>
              <div className="text-gray-500 text-sm">replaces all of that</div>
            </div>
          </div>
          <div className="border border-green-500/30 bg-green-500/5 rounded-2xl p-6 text-center">
            <div className="text-3xl mb-2">✅</div>
            <div className="text-green-400 font-black text-lg mb-2">What You Pay</div>
            <div className="text-gray-400 text-sm space-y-1">
              <div>Groq API: FREE</div>
              <div>Railway tier: FREE</div>
              <div>SQLite: FREE</div>
              <div>All data APIs: FREE</div>
              <div className="text-green-400 font-black pt-2 text-xl border-t border-green-500/20">Total: $0.00</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
