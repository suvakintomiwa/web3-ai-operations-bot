import { useState } from 'react';

interface Step {
  num: string;
  title: string;
  desc: string;
  code?: string;
  links?: { label: string; url: string }[];
  note?: string;
}

const setupSteps: Step[] = [
  {
    num: '01',
    title: 'Get Your Free API Keys',
    desc: 'Register for free accounts and grab your API tokens. All of these are completely free.',
    links: [
      { label: '🤖 Telegram BotFather', url: 'https://t.me/BotFather' },
      { label: '⚡ Groq Console (Free)', url: 'https://console.groq.com' },
      { label: '🌐 OpenRouter (Free)', url: 'https://openrouter.ai' },
      { label: '💎 Google AI Studio (Gemini)', url: 'https://aistudio.google.com' },
      { label: '🐋 DeepSeek API', url: 'https://platform.deepseek.com' },
      { label: '📊 CoinMarketCap API', url: 'https://coinmarketcap.com/api/' },
    ],
    note: 'DexScreener and CoinGecko APIs need NO key — they\'re fully open!',
  },
  {
    num: '02',
    title: 'Clone the Repository',
    desc: 'Download the project and set up your Python environment.',
    code: `git clone https://github.com/yourusername/nexusbot.git
cd nexusbot

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\\Scripts\\activate  # Windows

# Install all dependencies
pip install -r requirements.txt`,
  },
  {
    num: '03',
    title: 'Configure Environment Variables',
    desc: 'Copy the example env file and fill in your API keys.',
    code: `cp .env.example .env
nano .env  # or use any text editor

# Fill these in:
BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_key
GEMINI_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_key
CMC_API_KEY=your_coinmarketcap_free_key
ADMIN_USER_ID=your_telegram_user_id`,
  },
  {
    num: '04',
    title: 'Initialize the Database',
    desc: 'Run the database setup to create all SQLite tables.',
    code: `# Initialize the database
python -c "import asyncio; from bot.database import init_db; asyncio.run(init_db())"

# Verify it worked
ls -la data/
# You should see: nexusbot.db`,
  },
  {
    num: '05',
    title: 'Test Run Locally',
    desc: 'Start the bot locally to verify everything works before deploying.',
    code: `# Start the bot
python -m bot.main

# You should see:
# ✅ Database initialized
# ✅ AI Service loaded (Groq primary)
# ✅ Scheduler started
# 🚀 NexusBot is online!
# 
# Now open Telegram and send /start to your bot!`,
  },
  {
    num: '06',
    title: 'Register BotFather Commands',
    desc: 'Set your bot\'s command list in Telegram for auto-complete.',
    code: `# Go to @BotFather on Telegram
# Send: /setcommands
# Select your bot
# Then paste this list:

start - Initialize bot and show dashboard
help - Full command reference
ai - Chat with AI assistant
alpha - Top trending crypto tokens
newprojects - Fresh project launches
trending - What is pumping right now
jobs - All Web3 job listings
cmjobs - Community Manager roles
modjobs - Moderator openings
nftjobs - NFT artist gigs
tester - Protocol testing opportunities
checkproject - Analyze any project
outreach - AI-written KOL DMs
raid - Generate raid messages
shill - Create shill content
reminder - Set a reminder
watchlist - View tracked projects
save - Save a note or link
notes - View all your notes
settings - Configure bot settings
alerts - Manage push alerts`,
  },
];

const envContent = `# ====================================
# NEXUSBOT — Environment Configuration
# ====================================

# ─── TELEGRAM ───────────────────────
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_USER_ID=your_telegram_numeric_id

# ─── AI APIs (FREE TIERS) ───────────
GROQ_API_KEY=gsk_your_groq_key_here
OPENROUTER_API_KEY=sk-or-your_openrouter_key
GEMINI_API_KEY=your_google_gemini_key
DEEPSEEK_API_KEY=your_deepseek_key

# ─── CRYPTO DATA APIs ───────────────
CMC_API_KEY=your_coinmarketcap_free_key
# DexScreener = NO KEY NEEDED
# CoinGecko = NO KEY NEEDED (free tier)

# ─── DATABASE ───────────────────────
DB_PATH=data/nexusbot.db

# ─── BOT SETTINGS ───────────────────
LOG_LEVEL=INFO
TIMEZONE=UTC
ALERT_INTERVAL_MINUTES=30
MAX_RESULTS=10
BOT_NAME=NexusBot`;

export default function SetupSection() {
  const [activeStep, setActiveStep] = useState(0);
  const [showEnv, setShowEnv] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <section id="setup" className="py-20 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-yellow-500/40 bg-yellow-500/10 text-yellow-400 text-sm mb-6">
            🚀 SETUP GUIDE
          </div>
          <h2 className="text-4xl sm:text-5xl font-black text-white mb-4">
            Deploy in{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-400">
              6 Steps
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            No DevOps experience needed. If you can copy-paste, you can deploy NexusBot.
          </p>
        </div>

        {/* Step navigation */}
        <div className="flex overflow-x-auto gap-2 mb-8 pb-2">
          {setupSteps.map((step, i) => (
            <button
              key={i}
              onClick={() => setActiveStep(i)}
              className={`flex-shrink-0 px-4 py-2 rounded-lg text-sm font-bold transition-all duration-200 ${
                activeStep === i
                  ? 'bg-cyan-500 text-gray-950'
                  : 'border border-gray-700 text-gray-400 hover:border-cyan-500/50 hover:text-cyan-400'
              }`}
            >
              {step.num}
            </button>
          ))}
        </div>

        {/* Active step */}
        <div className="border border-cyan-500/30 bg-gray-900/50 rounded-2xl overflow-hidden">
          <div className="p-6 border-b border-cyan-500/20">
            <div className="flex items-center gap-4">
              <span className="text-4xl font-black text-cyan-400">{setupSteps[activeStep].num}</span>
              <div>
                <h3 className="text-xl font-black text-white">{setupSteps[activeStep].title}</h3>
                <p className="text-gray-400 text-sm mt-1">{setupSteps[activeStep].desc}</p>
              </div>
            </div>
          </div>

          <div className="p-6">
            {/* Links */}
            {setupSteps[activeStep].links && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
                {setupSteps[activeStep].links!.map((link) => (
                  <a
                    key={link.url}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 px-4 py-3 border border-gray-700 rounded-xl text-gray-300 hover:border-cyan-500/50 hover:text-cyan-400 hover:bg-cyan-500/5 transition-all duration-200 text-sm"
                  >
                    {link.label}
                    <span className="ml-auto text-gray-600">→</span>
                  </a>
                ))}
              </div>
            )}

            {/* Note */}
            {setupSteps[activeStep].note && (
              <div className="mb-6 flex items-start gap-3 p-4 bg-green-500/10 border border-green-500/30 rounded-xl">
                <span className="text-green-400 flex-shrink-0">✅</span>
                <p className="text-green-300 text-sm">{setupSteps[activeStep].note}</p>
              </div>
            )}

            {/* Code block */}
            {setupSteps[activeStep].code && (
              <div className="relative">
                <div className="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-xl">
                  <span className="text-gray-500 text-xs font-mono">bash</span>
                  <button
                    onClick={() => handleCopy(setupSteps[activeStep].code!, `step-${activeStep}`)}
                    className="text-xs text-gray-400 hover:text-cyan-400 transition-colors"
                  >
                    {copied === `step-${activeStep}` ? '✓ Copied!' : '📋 Copy'}
                  </button>
                </div>
                <pre className="bg-gray-950 border border-gray-800 rounded-b-xl p-4 text-sm text-gray-300 overflow-auto font-mono whitespace-pre-wrap">
                  {setupSteps[activeStep].code}
                </pre>
              </div>
            )}
          </div>

          {/* Step navigation */}
          <div className="p-6 border-t border-gray-800 flex justify-between">
            <button
              onClick={() => setActiveStep(Math.max(0, activeStep - 1))}
              disabled={activeStep === 0}
              className="px-4 py-2 border border-gray-700 text-gray-400 rounded-lg text-sm disabled:opacity-30 hover:border-cyan-500/50 hover:text-cyan-400 transition-all disabled:cursor-not-allowed"
            >
              ← Previous
            </button>
            <span className="text-gray-600 text-sm self-center">
              {activeStep + 1} / {setupSteps.length}
            </span>
            <button
              onClick={() => setActiveStep(Math.min(setupSteps.length - 1, activeStep + 1))}
              disabled={activeStep === setupSteps.length - 1}
              className="px-4 py-2 bg-cyan-500 text-gray-950 rounded-lg text-sm font-bold disabled:opacity-30 hover:bg-cyan-400 transition-all disabled:cursor-not-allowed"
            >
              Next →
            </button>
          </div>
        </div>

        {/* .env.example */}
        <div className="mt-12">
          <button
            onClick={() => setShowEnv(!showEnv)}
            className="w-full flex items-center justify-between px-6 py-4 border border-yellow-500/30 bg-yellow-500/5 rounded-xl hover:bg-yellow-500/10 transition-all duration-200"
          >
            <span className="text-yellow-400 font-black">📄 View .env.example File</span>
            <span className="text-gray-500">{showEnv ? '▼' : '▶'}</span>
          </button>

          {showEnv && (
            <div className="mt-2 relative">
              <div className="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-xl">
                <span className="text-gray-500 text-xs font-mono">.env.example</span>
                <button
                  onClick={() => handleCopy(envContent, 'env')}
                  className="text-xs text-gray-400 hover:text-cyan-400 transition-colors"
                >
                  {copied === 'env' ? '✓ Copied!' : '📋 Copy'}
                </button>
              </div>
              <pre className="bg-gray-950 border border-gray-800 rounded-b-xl p-4 text-sm text-gray-300 overflow-auto font-mono">
                {envContent}
              </pre>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
