'use client';

export default function TikTokShopBudgetToolsPage() {
  // Your ToolSuite Affiliate Links
  const TOOLSUITE_VIP_LINK = "https://whop.com/toolsuite/buy-vip?a=aptdiocese";
  const TOOLSUITE_365_LINK = "https://whop.com/toolsuite/365-days-access-e9?a=aptdiocese";

  // Retained Navigation Links from Main Site
  const OPUSCLIP_LINK = "https://opus.pro/?via=waylon";
  const WRITING_JOBS_BANNER_LINK = "https://2b8aauomsgsvvl2acqagzdx4tu.hop.clickbank.net?tid=homepage_top_bar";

  return (
    <div className="min-h-screen flex flex-col justify-between bg-slate-950 text-slate-100 font-sans">
      
      {/* 1. Sticky Top Announcement Bar */}
      <div className="bg-gradient-to-r from-indigo-900 via-purple-900 to-slate-900 border-b border-indigo-500/30 py-2.5 px-4 text-center text-xs text-slate-200">
        <div className="max-w-6xl mx-auto flex items-center justify-center gap-2 flex-wrap">
          <span className="bg-amber-500 text-slate-950 font-black px-2 py-0.5 rounded text-[10px] uppercase">Hiring</span>
          <span>Earn $25–$50/Hr reviewing social media apps & organizing video clips from home.</span>
          <a 
            href={WRITING_JOBS_BANNER_LINK} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="font-bold text-amber-400 hover:underline underline-offset-2 ml-1"
          >
            Apply Now →
          </a>
        </div>
      </div>

      {/* Navigation Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <a href="/" className="text-xl font-extrabold text-indigo-400">
            Socials<span className="text-white">Fetcher</span>
          </a>
          <nav className="hidden md:flex items-center space-x-6 text-sm text-slate-400 font-medium">
            <a href="/" className="hover:text-indigo-400 transition">Video Downloader</a>
            <a href="/tiktok/download/no-watermark" className="hover:text-indigo-400 transition">TikTok</a>
            <a href="/instagram/reels/downloader" className="hover:text-indigo-400 transition">Instagram</a>
            <a href={OPUSCLIP_LINK} target="_blank" rel="noopener noreferrer" className="text-purple-400 font-bold hover:text-purple-300 transition flex items-center gap-1">
              ✨ OpusClip AI
            </a>
            <a 
              href={TOOLSUITE_VIP_LINK} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-3 py-1.5 rounded-lg text-xs transition"
            >
              Get ToolSuite ⚡
            </a>
          </nav>
        </div>
      </header>

      {/* Main Article Container */}
      <main className="flex-grow max-w-3xl mx-auto px-4 py-12 text-left">
        
        {/* Breadcrumb / Tag */}
        <div className="flex items-center gap-2 mb-4 text-xs font-semibold">
          <span className="bg-indigo-950 border border-indigo-700/60 text-indigo-400 px-2.5 py-0.5 rounded-full uppercase tracking-wider">
            TikTok Shop Blueprint
          </span>
          <span className="text-slate-500">• 6 min read</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-3xl sm:text-4xl sm:leading-tight font-extrabold mb-4 tracking-tight text-white">
          The Essential TikTok Shop Software Stack on a Budget (Under $30/Month)
        </h1>

        <p className="text-slate-400 text-base sm:text-lg mb-8 leading-relaxed">
          Launching a TikTok Shop dropshipping store or affiliate account requires more than just guessing what is viral. Here is the exact budget-friendly tech stack to find winning items, scrape competitor creatives, and scale profitably.
        </p>

        {/* Quick Answer Summary Box */}
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 mb-8">
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            <strong className="text-indigo-400 font-semibold">Key Takeaway:</strong> Subscribing to PiPiADS ($155/mo), Kalodata ($60/mo), Canva Pro ($15/mo), and ChatGPT Plus ($20/mo) separately costs over $250 each month. With <a href={TOOLSUITE_VIP_LINK} target="_blank" rel="noopener noreferrer" className="text-indigo-400 underline font-bold">ToolSuite on Whop</a>, you get full, 1-click access to every single one of these tools under one unified dashboard for less than $30/month.
          </p>
        </div>

        {/* Section 1: The Essential Stack */}
        <section className="mb-10 space-y-4">
          <h2 className="text-xl sm:text-2xl font-bold text-white">
            The 4 Tools Every TikTok Shop Creator Actually Needs
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            To generate consistent sales on TikTok Shop, top creators follow a 4-step loop that requires four specific types of software:
          </p>

          <div className="space-y-4 my-4">
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <h3 className="font-bold text-white text-base mb-1">1. Product & GMV Analytics (Kalodata)</h3>
              <p className="text-xs sm:text-sm text-slate-400">
                You cannot pick products by instinct. You need Kalodata to see real-time GMV, top-selling SKUs, and which affiliate creators are driving the volume.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <h3 className="font-bold text-white text-base mb-1">2. Competitor Ad Spying (PiPiADS)</h3>
              <p className="text-xs sm:text-sm text-slate-400">
                PiPiADS shows you the exact video ads currently running, the number of impressions, target audiences, and high-converting landing pages.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <h3 className="font-bold text-white text-base mb-1">3. Hook & UGC Scriptwriting (ChatGPT Plus)</h3>
              <p className="text-xs sm:text-sm text-slate-400">
                Writing fresh video hooks and 30-second scripts daily requires advanced reasoning models to capture scroll-stopping attention in the first 3 seconds.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <h3 className="font-bold text-white text-base mb-1">4. Fast Visual Editing & Covers (Canva Pro)</h3>
              <p className="text-xs sm:text-sm text-slate-400">
                1-click background removal, vertical video frames, and bold hook stickers create professional video cover art and product display images.
              </p>
            </div>
          </div>
        </section>

        {/* Section 2: Budget Breakdown */}
        <section className="mb-10 space-y-4">
          <h2 className="text-xl sm:text-2xl font-bold text-white">
            Cost Breakdown: Individual Subscriptions vs. ToolSuite
          </h2>
          <div className="overflow-x-auto rounded-xl border border-slate-800 my-4">
            <table className="w-full text-xs sm:text-sm text-slate-300">
              <thead className="bg-slate-900 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4 text-left">Tool Required</th>
                  <th className="py-3 px-4 text-left">Standalone Price</th>
                  <th className="py-3 px-4 text-left">Inside ToolSuite</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 bg-slate-900/40">
                <tr>
                  <td className="py-3 px-4 font-semibold text-white">PiPiADS VIP</td>
                  <td className="py-3 px-4 text-red-400 font-bold">$155/mo</td>
                  <td className="py-3 px-4 text-emerald-400 font-bold">Included</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-semibold text-white">Kalodata Standard</td>
                  <td className="py-3 px-4 text-red-400 font-bold">$60/mo</td>
                  <td className="py-3 px-4 text-emerald-400 font-bold">Included</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-semibold text-white">ChatGPT Plus</td>
                  <td className="py-3 px-4 text-red-400 font-bold">$20/mo</td>
                  <td className="py-3 px-4 text-emerald-400 font-bold">Included</td>
                </tr>
                <tr>
                  <td className="py-3 px-4 font-semibold text-white">Canva Pro</td>
                  <td className="py-3 px-4 text-red-400 font-bold">$15/mo</td>
                  <td className="py-3 px-4 text-emerald-400 font-bold">Included</td>
                </tr>
                <tr className="bg-indigo-950/40 font-bold border-t-2 border-indigo-500/40">
                  <td className="py-3 px-4 text-indigo-400">Total Monthly Investment</td>
                  <td className="py-3 px-4 text-red-400 font-extrabold">$250+/month</td>
                  <td className="py-3 px-4 text-emerald-400 font-extrabold">Under $30/month</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Section 3: High Converting CTA Card */}
        <div className="p-6 rounded-2xl bg-gradient-to-br from-indigo-950 via-slate-900 to-slate-900 border border-indigo-500/40 my-8 shadow-xl">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-indigo-400 bg-indigo-950 border border-indigo-800 px-2.5 py-0.5 rounded-full uppercase">
              Beginner Stack Solution
            </span>
            <span className="text-xs text-slate-400">Full 50+ Tool Access</span>
          </div>
          <h3 className="text-lg font-bold text-white mb-2">
            Get the Entire TikTok Shop Stack for Under $30
          </h3>
          <p className="text-xs sm:text-sm text-slate-300 mb-5 leading-relaxed">
            Stop letting expensive SaaS bills stop you before you start. Access PiPiADS, Kalodata, Canva Pro, and ChatGPT Plus with 1-click auto-login on Whop.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <a
              href={TOOLSUITE_VIP_LINK}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 text-center py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs sm:text-sm transition"
            >
              Get Monthly VIP Access →
            </a>
            <a
              href={TOOLSUITE_365_LINK}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 text-center py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-400 border border-amber-500/30 font-bold text-xs sm:text-sm transition"
            >
              Get 365-Day Access (Save More) ⚡
            </a>
          </div>
        </div>

        {/* Section 4: Practical Workflow */}
        <section className="mb-10 space-y-4">
          <h2 className="text-xl sm:text-2xl font-bold text-white">
            How to Use This Stack to Launch in 24 Hours
          </h2>
          <ol className="space-y-3 text-sm text-slate-300 list-decimal pl-5 leading-relaxed">
            <li>
              <strong>Find the Winner:</strong> Open <em>Kalodata</em> inside your ToolSuite browser and filter for products doing over $5,000 GMV/day with high creator commissions.
            </li>
            <li>
              <strong>Analyze the Angles:</strong> Switch to <em>PiPiADS</em> and inspect the top 3 video ads scaling that exact product right now.
            </li>
            <li>
              <strong>Write the Script:</strong> Use <em>ChatGPT Plus</em> to generate 5 variations of the winning hook tailored for your target audience.
            </li>
            <li>
              <strong>Create Assets:</strong> Open <em>Canva Pro</em> to design clean thumbnail overlays and download high-contrast badges for your video.
            </li>
          </ol>
        </section>

        {/* Final CTA Box */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center">
          <h3 className="text-lg font-bold text-white mb-2">Build Your TikTok Shop Business Today</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto mb-4">
            Protect your capital for ad spend and product samples by keeping your software costs lean.
          </p>
          <div className="flex justify-center gap-4 flex-wrap">
            <a 
              href={TOOLSUITE_VIP_LINK} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 font-bold text-xs sm:text-sm text-white transition"
            >
              Get Monthly VIP Access
            </a>
            <a 
              href={TOOLSUITE_365_LINK} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 font-bold text-xs sm:text-sm text-slate-950 transition"
            >
              Get 365-Day All-Access Pass
            </a>
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        <p>© 2026 SocialsFetcher.com — Free Online Media Utility.</p>
      </footer>
    </div>
  );
}
