import React, { useState } from 'react';
import { ArrowLeft, ArrowRight, ChevronDown, Upload } from 'lucide-react';

const NewsCard = ({ source, time, title, effect, stockName, stockPrice, priceChange, percentChange, sentiment }) => (
  <div className="w-80 p-3 bg-white rounded-2xl border border-gray-200 flex-col gap-3 flex">
    <div className="h-40 rounded-lg flex justify-center items-center">
      <img className="w-80 h-48 rounded-lg object-cover" src="/api/placeholder/320/192" alt="News thumbnail" />
    </div>
    <div className="flex-col gap-1 flex">
      <div className="justify-between items-center flex">
        <div className="text-gray-600 text-sm font-medium">{source}</div>
        <div className="text-gray-400 text-xs font-medium">{time}</div>
      </div>
      <div className="text-gray-900 text-xl font-semibold">{title}</div>
    </div>
    <div className="pt-3 pb-1 border-t border-gray-200 flex-col gap-2.5 flex">
      <div className="h-5">
        <div className={`px-2 py-1 ${sentiment === 'negative' ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'} rounded-full inline-flex`}>
          <div className="text-xs font-medium">{effect}% {sentiment === 'negative' ? 'Negative' : 'Positive'} Effect</div>
        </div>
      </div>
      <div className="flex-col gap-1 flex">
        <div className="text-sm">Your Stock: <span className="font-bold">{stockName}</span></div>
        <div className="flex items-center gap-1">
          <div className="text-sm font-medium">${stockPrice}</div>
          <div className={`text-xs ${priceChange < 0 ? 'text-red-600' : 'text-green-600'}`}>
            {priceChange > 0 ? '+' : ''}{priceChange} ({percentChange}%) <span className="text-gray-600">today</span>
          </div>
        </div>
      </div>
      <div className="h-3 bg-gradient-to-r from-green-600 via-gray-600 to-red-600 rounded-full relative">
        <div className="w-0.5 h-4 bg-white absolute" style={{ left: '50%' }} />
        <div className="w-4 h-4 bg-white rounded-full border-2 border-gray-200 absolute top-1/2 -translate-y-1/2" style={{ left: `${50 + effect}%` }} />
      </div>
    </div>
  </div>
);

const UploadModal = ({ onClose }) => (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div className="w-96 px-11 py-8 bg-white rounded-3xl flex-col gap-5">
      <div className="text-2xl font-semibold">Upload Documents to get started</div>
      <div className="h-px bg-gray-300" />
      <div className="flex-col gap-8">
        <div className="border-2 border-dashed border-gray-200 rounded-2xl p-8 text-center">
          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <div className="text-gray-600 text-xl font-semibold">
            Upload .pdf, .doc, .docx, .txt files
          </div>
        </div>
        <div className="flex justify-end gap-2">
          <button 
            onClick={onClose}
            className="px-4 py-3 bg-gray-100 rounded-xl text-sm font-semibold"
          >
            Cancel
          </button>
          <button className="px-4 py-3 bg-blue-600 text-white rounded-xl text-sm font-semibold flex items-center gap-2">
            Save & Continue
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
);

const App = () => {
  const [showUploadModal, setShowUploadModal] = useState(false);
  
  const newsData = [
    {
      source: "Yahoo News",
      time: "1d ago",
      title: "Chipotle faces lawsuit over portion sizes controversy",
      effect: 45,
      sentiment: "negative",
      stockName: "Chipotle (CMG)",
      stockPrice: "2455.23",
      priceChange: -345.65,
      percentChange: -15.2
    },
    {
      source: "Wall Street Journal",
      time: "22h ago",
      title: "Nvidia Tops List of Favored S&P 500 Stocks",
      effect: 12,
      sentiment: "positive",
      stockName: "Nvidia (NVDA)",
      stockPrice: "23412.67",
      priceChange: -250.65,
      percentChange: -1.2
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="w-full px-9 py-3.5 bg-white border-b border-gray-200 flex justify-between items-center">
        <div className="text-blue-600 text-xl font-semibold">TradeTrends</div>
        <button
          onClick={() => setShowUploadModal(true)}
          className="pl-2 pr-3 py-2 bg-gray-100 rounded-xl border border-gray-200 flex items-center gap-2.5"
        >
          <span className="text-gray-900 text-sm font-semibold">Upload Documents</span>
          <Upload className="w-5 h-5" />
        </button>
      </header>

      <main className="container mx-auto px-10 py-8">
        <section>
          <h2 className="text-2xl font-semibold mb-6">Briefing</h2>
          <div className="flex gap-5 overflow-x-auto pb-4">
            {newsData.map((news, index) => (
              <NewsCard key={index} {...news} />
            ))}
          </div>
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-semibold mb-6">Your Investments</h2>
          <div className="bg-white rounded-2xl border border-gray-200 p-4">
            <div className="flex justify-between items-center mb-4">
              <div className="text-xl">
                Stock: <span className="font-semibold">Chipotle Mexican Grill </span>
                <span className="text-gray-600">(CMG)</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-gray-600">today:</span>
                <span className="font-medium">$ 2455.23</span>
                <div className="bg-red-600 text-white px-3 py-2 rounded-full">
                  -$ 345.65 (-15.2%)
                </div>
              </div>
            </div>
            
            <div className="flex justify-between items-center mb-4">
              <div className="flex gap-2">
                <button className="px-2 py-1 bg-gray-100 rounded-full border text-sm">
                  Time Period: <span className="font-bold">Past Week</span>
                  <ChevronDown className="w-3.5 h-3.5 inline ml-1" />
                </button>
                <button className="px-2 py-1 bg-gray-100 rounded-full border text-sm">
                  Sort By: <span className="font-bold">New</span>
                  <ChevronDown className="w-3.5 h-3.5 inline ml-1" />
                </button>
                <button className="px-2 py-1 bg-gray-100 rounded-full border text-sm">
                  Positioning: <span className="font-bold">Negative</span>
                  <ChevronDown className="w-3.5 h-3.5 inline ml-1" />
                </button>
              </div>
              <div className="flex gap-2">
                <button className="p-2 bg-gray-100 rounded-full border">
                  <ArrowLeft className="w-4 h-4" />
                </button>
                <button className="p-2 bg-gray-100 rounded-full border">
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="flex gap-2 overflow-x-auto">
              {newsData.slice(0, 5).map((news, index) => (
                <div key={index} className="min-w-[280px] p-3 bg-white rounded-xl border border-gray-200">
                  <div className="mb-3">
                    <div className={`px-2 py-1 ${news.sentiment === 'negative' ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'} rounded-full inline-flex`}>
                      <div className="text-xs font-medium">{news.effect}% {news.sentiment === 'negative' ? 'Negative' : 'Positive'} Effect</div>
                    </div>
                  </div>
                  <div className="mb-4">
                    <h3 className="text-xl font-semibold mb-2">{news.title}</h3>
                    <div className="flex justify-between items-center">
                      <div className="text-gray-600 text-sm font-medium">{news.source}</div>
                      <div className="text-gray-400 text-xs font-medium">{news.time}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      {showUploadModal && <UploadModal onClose={() => setShowUploadModal(false)} />}
    </div>
  );
};

export default App;