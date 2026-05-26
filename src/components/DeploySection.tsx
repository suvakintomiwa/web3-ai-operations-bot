import { useState } from 'react';

const railwaySteps = [
  {
    icon: '🔗',
    title: 'Connect GitHub',
    desc: 'Push your NexusBot code to a GitHub repository (can be private). Railway pulls directly from GitHub.',
    code: `git init
git add .
git commit -m "🚀 Initial NexusBot deploy"
git remote add origin https://github.com/YOUR_USERNAME/nexusbot.git
git push -u origin main`,
  },
  {
    icon: '🚂',
    title: 'Create Railway Project',
    desc: 'Go to railway.app → New Project → Deploy from GitHub repo → Select nexusbot.',
    code: `# Or use Railway CLI:
npm install -g @railway/cli
railway login
railway init
railway link`,
  },
  {
    icon: '🔒',
    title: 'Set Environment Variables',
    desc: 'In Railway dashboard → Variables tab → Add all your .env variables one by one.',
    code: `# Key variables to add in Railway UI:
BOT_TOKEN         = your_telegram_bot_token
GROQ_API_KEY      = gsk_your_groq_key
OPENROUTER_API_KEY = sk-or-your_key
GEMINI_API_KEY    = your_gemini_key
DEEPSEEK_API_KEY  = your_deepseek_key
CMC_API_KEY       = your_cmc_key
ADMIN_USER_ID     = your_telegram_id
DB_PATH           = data/nexusbot.db`,
  },
  {
    icon: '⚙️',
    title: 'Verify Procfile & railway.json',
    desc: 'These files tell Railway how to run your bot. They\'re already included in the project.',
    code: `# Procfile (already in project):
worker: python -m bot.main

# railway.json (already in project):
{
  "build": { "builder": "NIXPACKS" },
  "deploy": {
    "startCommand": "python -m bot.main",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}`,
  },
  {
    icon: '🚀',
    title: 'Deploy!',
    desc: 'Click Deploy in Railway or push to GitHub. Railway auto-detects Python and installs requirements.txt.',
    code: `# Railway auto-runs:
pip install -r requirements.txt
python -m bot.main

# Watch logs in Railway dashboard:
✅ Database initialized
✅ AI Service: Groq (primary) ready
✅ Scheduler: 5 jobs registered
🚀 NexusBot polling started!`,
  },
];

const procfileContent = `worker: python -m bot.main`;

const railwayJsonContent = `{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m bot.main",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": null
  }
}`;

const requirementsContent = `# ─── Telegram Bot ───────────────────
aiogram==3.4.1
aiohttp==3.9.3

# ─── Database ───────────────────────
aiosqlite==0.20.0

# ─── Scheduler ──────────────────────
APScheduler==3.10.4

# ─── AI APIs ────────────────────────
groq==0.4.2
openai==1.12.0
google-generativeai==0.4.1

# ─── HTTP / Scraping ────────────────
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
praw==7.7.1

# ─── Utilities ──────────────────────
python-dotenv==1.0.1
loguru==0.7.2
pytz==2024.1
aiofiles==23.2.1`;

export default function DeploySection() {
  const [activeStep, setActiveStep] = useState(0);
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <section className="py-20 px-4 bg-gray-900/20">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-orange-500/40 bg-orange-500/10 text-orange-400 text-sm mb-6">
            🚂 RAILWAY DEPLOYMENT
          </div>
          <h2 className="text-4xl sm:text-5xl font-black text-white mb-4">
            Free Hosting on{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-pink-400">
              Railway
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Railway's free tier gives you 500 hours/month — more than enough for a personal Telegram bot running 24/7.
          </p>
        </div>

        {/* Railway free tier info */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-12">
          {[
            { icon: '⏱️', label: '500 hrs/month', desc: 'Free execution time' },
            { icon: '💾', label: '1GB RAM', desc: 'More than enough for bot' },
            { icon: '🔄', label: 'Auto-restart', desc: 'On failure restart' },
          ].map((item) => (
            <div key={item.label} className="border border-orange-500/20 bg-orange-500/5 rounded-xl p-5 text-center">
              <div className="text-3xl mb-2">{item.icon}</div>
              <div className="text-orange-400 font-black text-lg">{item.label}</div>
              <div className="text-gray-400 text-sm">{item.desc}</div>
            </div>
          ))}
        </div>

        {/* Railway steps */}
        <div className="mb-12">
          <div className="flex overflow-x-auto gap-2 mb-6 pb-2">
            {railwaySteps.map((step, i) => (
              <button
                key={i}
                onClick={() => setActiveStep(i)}
                className={`flex-shrink-0 px-4 py-2 rounded-lg text-sm font-bold transition-all duration-200 flex items-center gap-2 ${
                  activeStep === i
                    ? 'bg-orange-500 text-white'
                    : 'border border-gray-700 text-gray-400 hover:border-orange-500/50 hover:text-orange-400'
                }`}
              >
                <span>{step.icon}</span>
                <span className="hidden sm:inline">{step.title}</span>
                <span className="sm:hidden">{i + 1}</span>
              </button>
            ))}
          </div>

          <div className="border border-orange-500/20 bg-gray-900/50 rounded-2xl overflow-hidden">
            <div className="p-6 border-b border-gray-800">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-3xl">{railwaySteps[activeStep].icon}</span>
                <h3 className="text-xl font-black text-white">{railwaySteps[activeStep].title}</h3>
              </div>
              <p className="text-gray-400 text-sm">{railwaySteps[activeStep].desc}</p>
            </div>

            <div className="p-6">
              <div className="relative">
                <div className="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-xl">
                  <span className="text-gray-500 text-xs font-mono">
                    {activeStep === 2 ? 'Railway Variables' : activeStep === 3 ? 'Config Files' : 'bash'}
                  </span>
                  <button
                    onClick={() => handleCopy(railwaySteps[activeStep].code, `railway-${activeStep}`)}
                    className="text-xs text-gray-400 hover:text-orange-400 transition-colors"
                  >
                    {copied === `railway-${activeStep}` ? '✓ Copied!' : '📋 Copy'}
                  </button>
                </div>
                <pre className="bg-gray-950 border border-gray-800 rounded-b-xl p-4 text-sm text-gray-300 overflow-auto font-mono whitespace-pre-wrap">
                  {railwaySteps[activeStep].code}
                </pre>
              </div>
            </div>

            <div className="p-4 border-t border-gray-800 flex justify-between">
              <button
                onClick={() => setActiveStep(Math.max(0, activeStep - 1))}
                disabled={activeStep === 0}
                className="px-4 py-2 border border-gray-700 text-gray-400 rounded-lg text-sm disabled:opacity-30 hover:border-orange-500/50 hover:text-orange-400 transition-all disabled:cursor-not-allowed"
              >
                ← Back
              </button>
              <button
                onClick={() => setActiveStep(Math.min(railwaySteps.length - 1, activeStep + 1))}
                disabled={activeStep === railwaySteps.length - 1}
                className="px-4 py-2 bg-orange-500 text-white rounded-lg text-sm font-bold disabled:opacity-30 hover:bg-orange-400 transition-all disabled:cursor-not-allowed"
              >
                Next →
              </button>
            </div>
          </div>
        </div>

        {/* Key files */}
        <div className="space-y-4">
          <h3 className="text-xl font-black text-white mb-6">📄 Deployment Files Content</h3>

          {/* Procfile */}
          <div>
            <div className="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-xl">
              <span className="text-gray-400 text-sm font-mono font-bold">Procfile</span>
              <button
                onClick={() => handleCopy(procfileContent, 'procfile')}
                className="text-xs text-gray-400 hover:text-cyan-400 transition-colors"
              >
                {copied === 'procfile' ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
            <pre className="bg-gray-950 border border-gray-800 rounded-b-xl p-4 text-sm text-green-300 font-mono">
              {procfileContent}
            </pre>
          </div>

          {/* railway.json */}
          <div>
            <div className="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-xl">
              <span className="text-gray-400 text-sm font-mono font-bold">railway.json</span>
              <button
                onClick={() => handleCopy(railwayJsonContent, 'railway-json')}
                className="text-xs text-gray-400 hover:text-cyan-400 transition-colors"
              >
                {copied === 'railway-json' ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
            <pre className="bg-gray-950 border border-gray-800 rounded-b-xl p-4 text-sm text-purple-300 font-mono">
              {railwayJsonContent}
            </pre>
          </div>

          {/* requirements.txt */}
          <div>
            <div className="flex items-center justify-between px-4 py-2 bg-gray-800 rounded-t-xl">
              <span className="text-gray-400 text-sm font-mono font-bold">requirements.txt</span>
              <button
                onClick={() => handleCopy(requirementsContent, 'requirements')}
                className="text-xs text-gray-400 hover:text-cyan-400 transition-colors"
              >
                {copied === 'requirements' ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
            <pre className="bg-gray-950 border border-gray-800 rounded-b-xl p-4 text-sm text-cyan-300 font-mono">
              {requirementsContent}
            </pre>
          </div>
        </div>

        {/* Railway link */}
        <div className="mt-12 text-center border border-orange-500/30 bg-orange-500/5 rounded-2xl p-8">
          <div className="text-4xl mb-4">🚂</div>
          <h3 className="text-2xl font-black text-orange-400 mb-2">Ready to Deploy?</h3>
          <p className="text-gray-400 mb-6">Create your free Railway account and get your bot live in minutes.</p>
          <a
            href="https://railway.app"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-4 bg-orange-500 text-white rounded-xl font-black text-lg hover:bg-orange-400 transition-all duration-300 hover:shadow-[0_0_30px_rgba(249,115,22,0.4)]"
          >
            🚀 Open Railway.app →
          </a>
        </div>
      </div>
    </section>
  );
}
