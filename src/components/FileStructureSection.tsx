import { useState } from 'react';

interface FileNode {
  name: string;
  type: 'file' | 'dir';
  desc?: string;
  children?: FileNode[];
  badge?: string;
  badgeColor?: string;
}

const fileTree: FileNode[] = [
  {
    name: 'nexusbot/', type: 'dir', desc: 'Root project directory',
    children: [
      {
        name: 'bot/', type: 'dir', desc: 'Core bot package',
        children: [
          { name: '__init__.py', type: 'file', desc: 'Package init' },
          { name: 'main.py', type: 'file', desc: 'Entry point — bot startup & polling', badge: 'ENTRY', badgeColor: 'text-cyan-400' },
          { name: 'config.py', type: 'file', desc: 'Settings, env vars, constants', badge: 'CONFIG', badgeColor: 'text-yellow-400' },
          { name: 'database.py', type: 'file', desc: 'SQLite setup, migrations, helpers', badge: 'DB', badgeColor: 'text-green-400' },
          {
            name: 'handlers/', type: 'dir', desc: 'Command handlers',
            children: [
              { name: '__init__.py', type: 'file' },
              { name: 'start.py', type: 'file', desc: '/start /help commands' },
              { name: 'alpha.py', type: 'file', desc: '/alpha /trending /newprojects', badge: 'HOT', badgeColor: 'text-orange-400' },
              { name: 'jobs.py', type: 'file', desc: '/jobs /cmjobs /modjobs /nftjobs /tester' },
              { name: 'ai_chat.py', type: 'file', desc: '/ai command + conversation handler', badge: 'AI', badgeColor: 'text-purple-400' },
              { name: 'analysis.py', type: 'file', desc: '/checkproject /analyze commands' },
              { name: 'outreach.py', type: 'file', desc: '/outreach /raid /shill /network' },
              { name: 'organizer.py', type: 'file', desc: '/reminder /watchlist /save /notes' },
              { name: 'ecosystem.py', type: 'file', desc: '/solana /base /eth /memecoins /airdrops' },
              { name: 'settings.py', type: 'file', desc: '/settings /alerts configuration' },
            ],
          },
          {
            name: 'services/', type: 'dir', desc: 'Business logic & APIs',
            children: [
              { name: '__init__.py', type: 'file' },
              { name: 'ai_service.py', type: 'file', desc: 'Multi-model AI with fallback chain', badge: 'CORE', badgeColor: 'text-purple-400' },
              { name: 'dexscreener.py', type: 'file', desc: 'DexScreener API client' },
              { name: 'coingecko.py', type: 'file', desc: 'CoinGecko free API client' },
              { name: 'coinmarketcap.py', type: 'file', desc: 'CMC basic free API' },
              { name: 'jobs_scraper.py', type: 'file', desc: 'Web3 job boards scraper', badge: '🕷️', badgeColor: 'text-green-400' },
              { name: 'project_analyzer.py', type: 'file', desc: 'Scam/legit analysis engine' },
              { name: 'github_scraper.py', type: 'file', desc: 'GitHub trending crypto repos' },
              { name: 'reddit_scraper.py', type: 'file', desc: 'Reddit crypto community scanner' },
              { name: 'scheduler.py', type: 'file', desc: 'APScheduler jobs — alerts, scans', badge: 'CRON', badgeColor: 'text-orange-400' },
              { name: 'formatter.py', type: 'file', desc: 'Telegram message formatter (HTML/MD)' },
            ],
          },
          {
            name: 'keyboards/', type: 'dir', desc: 'Inline keyboard builders',
            children: [
              { name: '__init__.py', type: 'file' },
              { name: 'main_menu.py', type: 'file', desc: 'Main menu inline keyboard' },
              { name: 'alpha_kb.py', type: 'file', desc: 'Alpha section keyboards' },
              { name: 'jobs_kb.py', type: 'file', desc: 'Jobs section keyboards' },
              { name: 'analysis_kb.py', type: 'file', desc: 'Analysis result keyboards' },
            ],
          },
          {
            name: 'middleware/', type: 'dir', desc: 'Request middleware',
            children: [
              { name: '__init__.py', type: 'file' },
              { name: 'auth.py', type: 'file', desc: 'User whitelist/blacklist check' },
              { name: 'logging.py', type: 'file', desc: 'Request logging middleware' },
              { name: 'rate_limit.py', type: 'file', desc: 'Anti-spam rate limiter' },
            ],
          },
          {
            name: 'utils/', type: 'dir', desc: 'Shared utilities',
            children: [
              { name: '__init__.py', type: 'file' },
              { name: 'helpers.py', type: 'file', desc: 'Common helper functions' },
              { name: 'validators.py', type: 'file', desc: 'Input validation (address, URL)' },
              { name: 'cache.py', type: 'file', desc: 'In-memory caching layer' },
            ],
          },
        ],
      },
      { name: 'data/', type: 'dir', desc: 'SQLite database file storage', children: [{ name: 'nexusbot.db', type: 'file', desc: 'Main SQLite database', badge: 'DB', badgeColor: 'text-green-400' }, { name: '.gitkeep', type: 'file' }] },
      { name: 'logs/', type: 'dir', desc: 'Bot log files', children: [{ name: '.gitkeep', type: 'file' }] },
      { name: '.env', type: 'file', desc: 'Your secret API keys (never commit)', badge: '🔒 SECRET', badgeColor: 'text-red-400' },
      { name: '.env.example', type: 'file', desc: 'Template for environment variables', badge: '📋 COPY THIS', badgeColor: 'text-yellow-400' },
      { name: 'requirements.txt', type: 'file', desc: 'Python dependencies', badge: 'DEPS', badgeColor: 'text-cyan-400' },
      { name: 'Procfile', type: 'file', desc: 'Railway/Heroku process definition', badge: 'DEPLOY', badgeColor: 'text-orange-400' },
      { name: 'railway.json', type: 'file', desc: 'Railway deployment config', badge: 'RAILWAY', badgeColor: 'text-purple-400' },
      { name: 'README.md', type: 'file', desc: 'Setup and deployment guide' },
      { name: '.gitignore', type: 'file', desc: 'Git ignore rules' },
    ],
  },
];

function FileNodeRow({ node, depth = 0 }: { node: FileNode; depth?: number }) {
  const [open, setOpen] = useState(depth < 2);
  const isDir = node.type === 'dir';
  const hasChildren = isDir && node.children && node.children.length > 0;

  return (
    <div>
      <div
        className={`flex items-center gap-2 py-1 px-2 rounded hover:bg-gray-800/50 transition-colors duration-100 cursor-pointer group ${depth === 0 ? 'font-bold' : ''}`}
        style={{ paddingLeft: `${8 + depth * 20}px` }}
        onClick={() => hasChildren && setOpen(!open)}
      >
        {/* Tree lines */}
        {depth > 0 && (
          <span className="text-gray-700 flex-shrink-0 text-xs">
            {hasChildren ? (open ? '▼' : '▶') : '·'}
          </span>
        )}

        {/* Icon */}
        <span className="flex-shrink-0 text-sm">
          {isDir ? (open ? '📂' : '📁') : getFileIcon(node.name)}
        </span>

        {/* Name */}
        <span className={`text-sm font-mono ${isDir ? 'text-cyan-400' : 'text-gray-300'}`}>
          {node.name}
        </span>

        {/* Badge */}
        {node.badge && (
          <span className={`text-xs font-bold ${node.badgeColor} opacity-80`}>
            [{node.badge}]
          </span>
        )}

        {/* Description */}
        {node.desc && (
          <span className="text-gray-600 text-xs hidden sm:block truncate">
            — {node.desc}
          </span>
        )}
      </div>

      {/* Children */}
      {hasChildren && open && (
        <div>
          {node.children!.map((child) => (
            <FileNodeRow key={child.name} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

function getFileIcon(name: string): string {
  if (name.endsWith('.py')) return '🐍';
  if (name.endsWith('.txt')) return '📄';
  if (name.endsWith('.md')) return '📝';
  if (name.endsWith('.json')) return '📋';
  if (name.endsWith('.env') || name.includes('.env')) return '🔒';
  if (name === 'Procfile') return '⚙️';
  if (name.endsWith('.db')) return '🗄️';
  if (name.endsWith('.gitignore') || name === '.gitkeep') return '🚫';
  return '📄';
}

export default function FileStructureSection() {
  return (
    <section className="py-20 px-4 bg-gray-900/20">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-orange-500/40 bg-orange-500/10 text-orange-400 text-sm mb-6">
            📁 PROJECT STRUCTURE
          </div>
          <h2 className="text-4xl font-black text-white mb-4">
            Complete File Architecture
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Production-ready modular structure — scalable to SaaS with zero refactoring needed.
          </p>
        </div>

        {/* File tree */}
        <div className="bg-gray-950 border border-cyan-500/20 rounded-2xl overflow-hidden shadow-[0_0_60px_rgba(0,255,255,0.05)]">
          {/* Terminal header */}
          <div className="flex items-center gap-2 px-4 py-3 bg-gray-900 border-b border-cyan-500/20">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span className="text-gray-500 text-xs ml-2 font-mono">nexusbot — project tree</span>
          </div>

          {/* Tree content */}
          <div className="p-4 font-mono text-sm overflow-auto">
            {fileTree.map((node) => (
              <FileNodeRow key={node.name} node={node} depth={0} />
            ))}
          </div>
        </div>

        {/* Key files explanation */}
        <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 gap-6">
          {[
            {
              file: 'bot/main.py',
              color: 'border-cyan-500/30 text-cyan-400',
              desc: 'Entry point. Initializes bot, registers all handlers, starts APScheduler, and begins polling.',
            },
            {
              file: 'bot/services/ai_service.py',
              color: 'border-purple-500/30 text-purple-400',
              desc: 'The brain. Tries Groq → OpenRouter → Gemini → DeepSeek in sequence with exponential backoff.',
            },
            {
              file: 'bot/services/scheduler.py',
              color: 'border-orange-500/30 text-orange-400',
              desc: 'APScheduler runs background jobs: alpha scans every 5min, job alerts daily, whale monitoring.',
            },
            {
              file: 'bot/database.py',
              color: 'border-green-500/30 text-green-400',
              desc: 'SQLite setup with aiosqlite. Tables: users, notes, reminders, watchlist, outreach, conversations.',
            },
          ].map((item) => (
            <div key={item.file} className={`border rounded-xl p-5 ${item.color.split(' ')[0]} bg-gray-900/30`}>
              <div className={`font-mono text-sm font-bold mb-2 ${item.color.split(' ')[1]}`}>
                📄 {item.file}
              </div>
              <p className="text-gray-400 text-sm">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
