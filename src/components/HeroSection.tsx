import { useState, useEffect } from 'react';

const glitchChars = '!@#$%^&*()_+-=[]{}|;:,.<>?/\\~`';

function GlitchText({ text }: { text: string }) {
  const [display, setDisplay] = useState(text);

  useEffect(() => {
    let iterations = 0;
    const maxIterations = text.length * 3;
    const interval = setInterval(() => {
      setDisplay(
        text
          .split('')
          .map((char, i) => {
            if (char === ' ') return ' ';
            if (i < iterations / 3) return char;
            return glitchChars[Math.floor(Math.random() * glitchChars.length)];
          })
          .join('')
      );
      iterations++;
      if (iterations > maxIterations) clearInterval(interval);
    }, 40);
    return () => clearInterval(interval);
  }, [text]);

  return <span>{display}</span>;
}

const stats = [
  { label: 'Commands', value: '30+' },
  { label: 'Free APIs', value: '8' },
  { label: 'AI Fallbacks', value: '4' },
  { label: 'Ecosystems', value: '3' },
];

const scrollingTags = [
  '🔥 DexScreener', '💊 Pump.fun', '🦎 CoinGecko', '🪄 Magic Eden',
  '🤖 Groq AI', '📡 Solana', '🔷 Base', '⟠ Ethereum',
  '💼 Web3 Jobs', '🎯 Alpha Hunting', '🚀 KOL Outreach', '🛡️ Scam Analysis',
  '📊 Token Analytics', '🐋 Whale Alerts', '💎 NFT Gigs', '🔔 Auto Alerts',
];

export default function HeroSection() {


  return (
    <section id="overview" className="relative pt-24 pb-20 px-4 overflow-hidden">
      {/* Animated background orbs */}
      <div className="absolute top-20 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-10 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      <div className="absolute top-40 right-1/3 w-64 h-64 bg-green-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s' }} />

      <div className="max-w-7xl mx-auto">
        {/* Badge */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-cyan-500/40 bg-cyan-500/10 text-cyan-400 text-sm">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <span>100% FREE STACK · RAILWAY READY · NO PAID APIS</span>
          </div>
        </div>

        {/* Main heading */}
        <div className="text-center mb-8">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black mb-4 leading-tight">
            <span className="text-white">NEXUS</span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">BOT</span>
          </h1>
          <div className="text-xl sm:text-2xl text-cyan-400 font-bold tracking-widest mb-2">
            <GlitchText text="WEB3 AI TELEGRAM ASSISTANT" />
          </div>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto mt-4 leading-relaxed">
            Your personal <span className="text-cyan-400">cyberpunk AI co-pilot</span> for crypto operations, Web3 job hunting,
            alpha discovery, community management & automated outreach — built entirely on{' '}
            <span className="text-green-400">FREE infrastructure</span>.
          </p>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-2xl mx-auto mb-12">
          {stats.map((stat) => (
            <div key={stat.label} className="border border-cyan-500/20 bg-gray-900/50 rounded-xl p-4 text-center hover:border-cyan-500/60 transition-all duration-300">
              <div className="text-3xl font-black text-cyan-400">{stat.value}</div>
              <div className="text-gray-400 text-xs mt-1 uppercase tracking-wider">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* CTA buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <a
            href="#setup"
            className="group px-8 py-4 bg-cyan-500 text-gray-950 rounded-xl font-black text-lg hover:bg-cyan-400 transition-all duration-300 hover:shadow-[0_0_40px_rgba(0,255,255,0.5)] flex items-center gap-2"
          >
            🚀 Deploy for Free
            <span className="group-hover:translate-x-1 transition-transform duration-200">→</span>
          </a>
          <a
            href="#commands"
            className="px-8 py-4 border border-cyan-500/40 text-cyan-400 rounded-xl font-bold text-lg hover:bg-cyan-500/10 transition-all duration-300"
          >
            📋 View Commands
          </a>
        </div>

        {/* Scrolling tags */}
        <div className="relative overflow-hidden py-4 border-y border-cyan-500/10">
          <div className="flex gap-4 whitespace-nowrap">
            {[...scrollingTags, ...scrollingTags].map((tag, i) => (
              <span
                key={i}
                className="inline-flex items-center gap-1 px-3 py-1 rounded-full border border-cyan-500/20 bg-gray-900/50 text-gray-400 text-sm hover:text-cyan-400 hover:border-cyan-500/50 transition-colors duration-200 cursor-default flex-shrink-0"
                style={{
                  animation: 'scroll-left 30s linear infinite',
                }}
              >
                {tag}
              </span>
            ))}
          </div>
        </div>

        {/* Terminal preview */}
        <div className="mt-16 max-w-4xl mx-auto">
          <div className="bg-gray-900 border border-cyan-500/30 rounded-2xl overflow-hidden shadow-[0_0_60px_rgba(0,255,255,0.1)]">
            {/* Terminal header */}
            <div className="flex items-center justify-between px-4 py-3 bg-gray-800/50 border-b border-cyan-500/20">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <div className="w-3 h-3 rounded-full bg-green-500" />
              </div>
              <span className="text-gray-500 text-xs">nexusbot · telegram · online</span>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                <span className="text-green-400 text-xs">LIVE</span>
              </div>
            </div>
            {/* Terminal body */}
            <div className="p-6 space-y-3 text-sm">
              <div className="flex gap-3">
                <span className="text-cyan-500">user@telegram:~$</span>
                <span className="text-white">/alpha</span>
              </div>
              <div className="pl-0 space-y-1 text-gray-300">
                <div><span className="text-cyan-400">⚡ NEXUSBOT ALPHA SCANNER</span></div>
                <div className="text-gray-500">─────────────────────────────</div>
                <div>🔥 <span className="text-yellow-400">$PEPE2</span> — <span className="text-green-400">+420%</span> · MC: $2.1M · Solana · 3h ago</div>
                <div>🚀 <span className="text-yellow-400">$DEGEN</span> — <span className="text-green-400">+89%</span> · MC: $890K · Base · 1h ago</div>
                <div>💎 <span className="text-yellow-400">$CHAD</span> — <span className="text-cyan-400">NEW</span> · MC: $45K · BSC · Just launched</div>
                <div className="text-gray-500">─────────────────────────────</div>
                <div className="text-purple-400">🤖 AI: High momentum on Solana. 3 whale wallets entered $PEPE2.</div>
              </div>
              <div className="flex gap-3 mt-2">
                <span className="text-cyan-500">user@telegram:~$</span>
                <span className="text-white">/cmjobs</span>
              </div>
              <div className="text-gray-300 space-y-1">
                <div><span className="text-green-400">✅ 12 CM roles</span> found on Crypto Twitter + Web3 job boards</div>
                <div className="text-gray-400 text-xs">Updated 5 mins ago · Apply now with AI-crafted DMs ✉️</div>
              </div>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-cyan-500">user@telegram:~$</span>
                <span className="text-white animate-pulse">█</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes scroll-left {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
      `}</style>
    </section>
  );
}
