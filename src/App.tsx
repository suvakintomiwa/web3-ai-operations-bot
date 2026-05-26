import { useState } from 'react';
import HeroSection from './components/HeroSection';
import FeaturesSection from './components/FeaturesSection';
import CommandsSection from './components/CommandsSection';
import TechStackSection from './components/TechStackSection';
import SetupSection from './components/SetupSection';
import DeploySection from './components/DeploySection';
import FileStructureSection from './components/FileStructureSection';
import Footer from './components/Footer';
import Navigation from './components/Navigation';

function App() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-gray-950 text-white font-mono overflow-x-hidden">
      {/* Cyberpunk grid background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,170,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,170,0.03)_1px,transparent_1px)] bg-[size:50px_50px]" />
        <div className="absolute inset-0 bg-gradient-to-br from-gray-950 via-gray-950/95 to-cyan-950/20" />
      </div>

      <div className="relative z-10">
        <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
        <HeroSection />
        <FeaturesSection />
        <CommandsSection />
        <TechStackSection />
        <FileStructureSection />
        <SetupSection />
        <DeploySection />
        <Footer />
      </div>
    </div>
  );
}

export default App;
