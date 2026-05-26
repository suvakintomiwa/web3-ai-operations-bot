import { useState } from 'react';

const commandGroups = [
  {
    group: '🚀 Core',
    color: 'cyan',
    commands: [
      { cmd: '/start', desc: 'Initialize bot, setup profile, show dashboard', example: '/start' },
      { cmd: '/help', desc: 'Full command reference with inline buttons', example: '/help' },
      { cmd: '/ai [prompt]', desc: 'Chat with multi-model AI (Groq → OpenRouter → Gemini → DeepSeek)', example: '/ai write a KOL outreach for @vitalik' },
      { cmd: '/settings', desc: 'Configure alerts, AI model, timezone, preferences', example: '/settings' },
      { cmd: '/alerts', desc: 'Manage your push alert subscriptions', example: '/alerts' },
    ],
  },
  {
    group: '🔍 Alpha & Discovery',
    color: 'yellow',
    commands: [
      { cmd: '/alpha', desc: 'Top trending tokens from DexScreener + CoinGecko with AI scores', example: '/alpha' },
      { cmd: '/newprojects', desc: 'Freshly launched projects in last 24h across all chains', example: '/newprojects' },
      { cmd: '/trending', desc: 'What\'s pumping right now — aggregated from 5 sources', example: '/trending' },
      { cmd: '/memecoins', desc: 'New meme coin launches with pump potential score', example: '/memecoins' },
      { cmd: '/airdrops', desc: 'Active airdrop opportunities with eligibility guide', example: '/airdrops' },
      { cmd: '/solana', desc: 'Solana ecosystem new projects & trending tokens', example: '/solana' },
      { cmd: '/base', desc: 'Base chain projects, dApps, and new launches', example: '/base' },
      { cmd: '/eth', desc: 'Ethereum ecosystem analysis and opportunities', example: '/eth' },
    ],
  },
  {
    group: '💼 Job Hunting',
    color: 'green',
    commands: [
      { cmd: '/jobs', desc: 'All remote Web3 job listings aggregated from boards', example: '/jobs' },
      { cmd: '/cmjobs', desc: 'Community Manager roles across Telegram/Discord/Twitter', example: '/cmjobs' },
      { cmd: '/modjobs', desc: 'Moderator openings in active crypto communities', example: '/modjobs' },
      { cmd: '/nftjobs', desc: 'NFT art gigs, collab requests, and artist roles', example: '/nftjobs' },
      { cmd: '/tester', desc: 'Protocol testing & bug bounty opportunities', example: '/tester' },
    ],
  },
  {
    group: '🔬 Project Analysis',
    color: 'purple',
    commands: [
      { cmd: '/checkproject [input]', desc: 'Paste token address / URL / Twitter — get full AI audit', example: '/checkproject 0x1234...abcd' },
      { cmd: '/analyze [input]', desc: 'Deep analysis: legitimacy, community, scam risk (0-100)', example: '/analyze https://pump.fun/token/...' },
    ],
  },
  {
    group: '📬 Outreach & Content',
    color: 'pink',
    commands: [
      { cmd: '/outreach [project]', desc: 'AI writes a tailored KOL outreach DM for any project', example: '/outreach @SomeNFTProject - pitch my CM services' },
      { cmd: '/raid [project]', desc: 'Generate raid messages, Twitter engagement scripts', example: '/raid PepeCoin - big launch tomorrow' },
      { cmd: '/shill [project]', desc: 'Create Twitter/X shill threads and Telegram promos', example: '/shill $DEGEN on Base chain' },
      { cmd: '/network', desc: 'View and manage your outreach contact database', example: '/network' },
    ],
  },
  {
    group: '🗂️ Personal Organizer',
    color: 'orange',
    commands: [
      { cmd: '/reminder [time] [msg]', desc: 'Set custom reminders with natural language time', example: '/reminder 2h check alpha channel' },
      { cmd: '/watchlist', desc: 'View projects you\'re tracking with price/news updates', example: '/watchlist' },
      { cmd: '/save [text]', desc: 'Save any text, link, or note to your database', example: '/save https://new-alpha-project.xyz' },
      { cmd: '/notes', desc: 'View all saved notes with search and tags', example: '/notes' },
    ],
  },
];

const colorBorderMap: Record<string, string> = {
  cyan: 'border-cyan-500/40 bg-cyan-500/5',
  yellow: 'border-yellow-500/40 bg-yellow-500/5',
  green: 'border-green-500/40 bg-green-500/5',
  purple: 'border-purple-500/40 bg-purple-500/5',
  pink: 'border-pink-500/40 bg-pink-500/5',
  orange: 'border-orange-500/40 bg-orange-500/5',
};

const colorTextMap: Record<string, string> = {
  cyan: 'text-cyan-400',
  yellow: 'text-yellow-400',
  green: 'text-green-400',
  purple: 'text-purple-400',
  pink: 'text-pink-400',
  orange: 'text-orange-400',
};

const colorCmdBg: Record<string, string> = {
  cyan: 'bg-cyan-500/10 text-cyan-300 border-cyan-500/20',
  yellow: 'bg-yellow-500/10 text-yellow-300 border-yellow-500/20',
  green: 'bg-green-500/10 text-green-300 border-green-500/20',
  purple: 'bg-purple-500/10 text-purple-300 border-purple-500/20',
  pink: 'bg-pink-500/10 text-pink-300 border-pink-500/20',
  orange: 'bg-orange-500/10 text-orange-300 border-orange-500/20',
};

export default function CommandsSection() {
  const [search, setSearch] = useState('');
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);

  const handleCopy = (cmd: string) => {
    navigator.clipboard.writeText(cmd);
    setCopiedCmd(cmd);
    setTimeout(() => setCopiedCmd(null), 1500);
  };

  const filteredGroups = commandGroups.map((group) => ({
    ...group,
    commands: group.commands.filter(
      (c) =>
        c.cmd.toLowerCase().includes(search.toLowerCase()) ||
        c.desc.toLowerCase().includes(search.toLowerCase())
    ),
  })).filter((group) => group.commands.length > 0);

  const totalCommands = commandGroups.reduce((acc, g) => acc + g.commands.length, 0);

  return (
    <section id="commands" className="py-20 px-4 bg-gray-900/30">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-500/40 bg-cyan-500/10 text-cyan-400 text-sm mb-6">
            💻 COMMAND REFERENCE
          </div>
          <h2 className="text-4xl sm:text-5xl font-black text-white mb-4">
            {totalCommands}+ Bot Commands
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto mb-8">
            Every command built for the Web3 grind — click to copy any command.
          </p>

          {/* Search */}
          <div className="max-w-md mx-auto">
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">🔍</span>
              <input
                type="text"
                placeholder="Search commands..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors duration-200"
              />
            </div>
          </div>
        </div>

        {/* Command groups */}
        <div className="space-y-8">
          {filteredGroups.map((group) => (
            <div key={group.group} className={`border rounded-2xl overflow-hidden ${colorBorderMap[group.color]}`}>
              {/* Group header */}
              <div className={`px-6 py-4 border-b ${colorBorderMap[group.color]}`}>
                <h3 className={`font-black text-lg ${colorTextMap[group.color]}`}>{group.group}</h3>
              </div>

              {/* Commands list */}
              <div className="divide-y divide-gray-800/50">
                {group.commands.map((cmd) => (
                  <div
                    key={cmd.cmd}
                    className="px-6 py-4 hover:bg-gray-800/30 transition-all duration-200 group"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-start gap-3">
                      {/* Command name */}
                      <button
                        onClick={() => handleCopy(cmd.cmd)}
                        className={`flex-shrink-0 px-3 py-1.5 rounded-lg border font-mono text-sm font-bold cursor-copy hover:opacity-80 transition-opacity ${colorCmdBg[group.color]}`}
                        title="Click to copy"
                      >
                        {copiedCmd === cmd.cmd ? '✓ Copied!' : cmd.cmd}
                      </button>

                      {/* Description */}
                      <div className="flex-1 min-w-0">
                        <p className="text-gray-300 text-sm">{cmd.desc}</p>
                        <p className="text-gray-600 text-xs mt-1 font-mono">
                          Example: <span className="text-gray-500">{cmd.example}</span>
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* BotFather setup note */}
        <div className="mt-12 border border-yellow-500/30 bg-yellow-500/5 rounded-2xl p-6">
          <h4 className="text-yellow-400 font-black text-lg mb-3">📋 Register Commands with BotFather</h4>
          <p className="text-gray-400 text-sm mb-4">Paste this into BotFather after <code className="text-yellow-300">/setcommands</code>:</p>
          <div className="bg-gray-950 border border-yellow-500/20 rounded-xl p-4 font-mono text-xs text-gray-400 overflow-auto max-h-64">
            {commandGroups.flatMap(g => g.commands).map(c => (
              <div key={c.cmd} className="mb-1">
                <span className="text-yellow-300">{c.cmd.replace(/\[.*?\]/g, '').trim().replace('/', '')}</span>
                {' '}
                <span className="text-gray-500">- {c.desc.split('—')[0].split('(')[0].trim().substring(0, 60)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
