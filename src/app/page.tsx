import RentForm from '@/components/RentForm';

export default function Home() {
    return (
        <main className="min-h-screen bg-[#0a0a0a] text-white overflow-hidden relative selection:bg-emerald-500/30">

            {/* Background Gradients */}
            <div className="fixed inset-0 z-0 pointer-events-none">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-emerald-500/10 rounded-full blur-[120px]"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-600/10 rounded-full blur-[120px]"></div>
            </div>

            <div className="relative z-10 container mx-auto px-4 py-12 md:py-24 flex flex-col items-center">
                {/* Header */}
                <div className="text-center mb-12 space-y-4">
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 mb-4">
                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                        <span className="text-xs font-medium text-emerald-400 tracking-wide uppercase">AI Powered Real Estate</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-white to-gray-400">
                        Dubai Rent Predictor
                    </h1>
                    <p className="text-lg text-gray-400 max-w-2xl mx-auto">
                        Make smarter property decisions with our advanced machine learning evaluation engine.
                    </p>
                </div>

                {/* Main Interface */}
                <RentForm />

                {/* Footer */}
                <footer className="mt-24 text-center text-gray-600 text-sm">
                    <p>© 2025 Dubai PropTech AI. Built for Vercel.</p>
                </footer>
            </div>
        </main>
    );
}
