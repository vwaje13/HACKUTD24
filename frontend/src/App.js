import React, { useState } from 'react';
import { ArrowLeft, ArrowRight, ChevronDown, Upload } from 'lucide-react';
import stockImage from './stock_image.jpg'


const jsonData = {
  "stocks": [
    {
      "symbol": "CMG",
      "price": 0.0,
      "change": {
        "value": 0.0,
        "percentage": 0.0
      },
      "news": [
        {
          "source": "MarketBeat",
          "title": "Chipotle Mexican Grill, Inc. (NYSE:CMG) Stock Position Lowered by Victory Capital Management Inc.",
          "time": "1 hour ago",
          "link": "https://www.marketbeat.com/instant-alerts/chipotle-mexican-grill-inc-nysecmg-stock-position-lowered-by-victory-capital-management-inc-2024-11-17/",
          "impact": {
            "percentage": 5,
            "effect": "Negative",
            "description": "Victory Capital Management Inc. lowering its stock position in Chipotle Mexican Grill, Inc. (CMG) may indicate a loss of investor confidence, potentially leading to a slight decrease in stock value."
          }
        },
        {
          "source": "Investor's Business Daily",
          "title": "Chipotle Mexican Grill Stock Gets A RS Rating Bump",
          "time": "1 day ago",
          "link": "https://www.investors.com/news/chipotle-mexican-grill-stock-gets-a-rs-rating-bump/",
          "impact": {
            "percentage": 20,
            "effect": "Positive",
            "description": "The Relative Strength (RS) rating bump indicates that Chipotle Mexican Grill (CMG) stock is outperforming a significant portion of the market, signaling increased investor confidence and potential for further growth."
          }
        },
        {
          "source": "Yahoo Finance",
          "title": "YUMC vs. CMG: Which Stock Is the Better Value Option?",
          "time": "2 days ago",
          "link": "https://finance.yahoo.com/news/yumc-vs-cmg-stock-better-164007973.html",
          "impact": {
            "percentage": 5,
            "effect": "Positive",
            "description": "The article compares CMG stock to YUMC, framing it as a value option, which may attract investors and increase stock price."
          }
        },
        {
          "source": "The Motley Fool",
          "title": "3 Must-Know Facts About Chipotle Before You Buy the Stock",
          "time": "1 day ago",
          "link": "https://www.fool.com/investing/2024/11/16/3-must-know-facts-chipotle-before-you-buy-stock/",
          "impact": {
            "percentage": 5,
            "effect": "Positive",
            "description": "The article highlights three key facts about Chipotle, likely increasing investor awareness and confidence in the stock, but the impact is minimal as it does not reveal significant new information."
          }
        },
        {
          "source": "Business Wire",
          "title": "CMG INVESTOR ALERT: Robbins Geller Rudman & Dowd LLP Announces that Chipotle Mexican Grill, Inc. Investors with Substantial Losses Have Opportunity to Lead Class Action Lawsuit",
          "time": "3 days ago",
          "link": "https://www.businesswire.com/news/home/20241113604406/en/CMG-INVESTOR-ALERT-Robbins-Geller-Rudman-Dowd-LLP-Announces-that-Chipotle-Mexican-Grill-Inc.-Investors-with-Substantial-Losses-Have-Opportunity-to-Lead-Class-Action-Lawsuit",
          "impact": {
            "percentage": -8,
            "effect": "Negative",
            "description": "The announcement of a potential class action lawsuit against Chipotle Mexican Grill, Inc. may lead to a decrease in investor confidence, potentially causing a slight decline in the stock price as investors become cautious about the company's future prospects."
          }
        }
      ]
    },
    {
      "symbol": "NVDA",
      "price": 0.0,
      "change": {
        "value": 0.0,
        "percentage": 0.0
      },
      "news": [
        {
          "source": "The Motley Fool",
          "title": "Should You Buy Nvidia Stock Before Nov. 20? Wall Street Has a Compelling Answer.",
          "time": "3 hours ago",
          "link": "https://www.fool.com/investing/2024/11/17/should-you-buy-nvidia-stock-before-nov-20-wall-str/",
          "impact": {
            "percentage": 8,
            "effect": "Positive",
            "description": "The article from The Motley Fool presents a positive outlook on Nvidia stock, suggesting that Wall Street has a compelling reason to buy the stock before Nov. 20. This implies that there is optimism about the company's performance, which could lead to an increase in stock price."
          }
        },
        {
          "source": "Yahoo",
          "title": "Nvidia Stock Could Soar Between 10% and 28%, According to Select Wall Street Analysts. Is the Stock a Buy Before Nov. 20?",
          "time": "1 day ago",
          "link": "https://www.yahoo.com/finance/news/nvidia-stock-could-soar-between-115000056.html",
          "impact": {
            "percentage": 19,
            "effect": "Positive",
            "description": "Select Wall Street analysts predict a potential 10% to 28% increase in Nvidia stock, indicating a positive outlook and potential buying opportunity before Nov. 20."
          }
        },
        {
          "source": "MarketWatch",
          "title": "Will Nvidia\u2019s earnings report signal a stock-market pullback?",
          "time": "1 day ago",
          "link": "https://www.marketwatch.com/story/will-nvidias-earnings-report-signal-a-stock-market-pullback-02cfcec5",
          "impact": {
            "percentage": 8,
            "effect": "Negative",
            "description": "The article suggests that Nvidia's earnings report may signal a stock-market pullback, implying a potential decline in NVDA stock value. This could lead to a modest negative impact on the stock price as investors may become cautious ahead of the earnings report."
          }
        },
        {
          "source": "Benzinga",
          "title": "Nvidia Reveals 3.6% Stake In Applied Digital, Stock Soars",
          "time": "1 day ago",
          "link": "https://www.benzinga.com/news/24/11/42016662/nvidia-reveals-3-6-stake-in-applied-digital-stock-soars",
          "impact": {
            "percentage": 8,
            "effect": "Positive",
            "description": "Nvidia's 3.6% stake in Applied Digital has led to a surge in NVDA stock, indicating investor confidence in the company's strategic investment decisions."
          }
        },
        {
          "source": "TheStreet",
          "title": "Nvidia results will rock markets",
          "time": "2 hours ago",
          "link": "https://www.thestreet.com/finance/nvidia-results-will-rock-markets",
          "impact": {
            "percentage": 80,
            "effect": "Positive",
            "description": "The article title 'Nvidia results will rock markets' from a reputable financial source, TheStreet, suggests that Nvidia's upcoming results are expected to have a significant and positive impact on the market, implying strong financial performance and potentially driving up the stock price."
          }
        }
      ]
    }
  ]
};

const NewsCard = ({ source, time, title, description, effect, sentiment, stockName, stockPrice, priceChange, percentChange }) => (
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
        <div className={`px-2 py-1 ${sentiment === 'Negative' ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'} rounded-full inline-flex`}>
          <div className="text-xs font-medium">{effect}% {sentiment} Effect</div>
        </div>
      </div>
      <div className="flex-col gap-1 flex">
        <div className="text-sm">Your Stock: <span className="font-bold">{stockName}</span></div>
        <div className="flex items-center gap-1">
          <div className="text-sm font-medium">${stockPrice.toFixed(2)}</div>
          <div className={`text-xs ${priceChange < 0 ? 'text-red-600' : 'text-green-600'}`}>
            {priceChange > 0 ? '+' : ''}{priceChange.toFixed(2)} ({percentChange.toFixed(2)}%) <span className="text-gray-600">today</span>
          </div>
        </div>
      </div>
      <div className="h-3 bg-gradient-to-r from-green-600 via-gray-600 to-red-600 rounded-full relative">
        {/* Central marker */}
        <div className="w-0.5 h-4 bg-white absolute" style={{ left: '50%' }} />

        {/* Effect marker */}
        <div
          className="w-4 h-4 bg-white rounded-full border-2 border-gray-200 absolute top-1/2 -translate-y-1/2"
          style={{
            left: sentiment === 'Positive'
              ? `${45 - (effect / 2)}%` // Positive moves right
              : `${50 + (Math.abs(effect) / 2)}%`, // Negative moves left
          }}
        />
      </div>
      <div className="text-gray-600 text-sm font-medium">{description}</div>

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
          <div className="text-gray-600 text-xl font-semibold">Upload .pdf, .doc, .docx, .txt files</div>
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

  // Flatten and sort all news articles by impact percentage
  const sortedNews = jsonData.stocks
    .flatMap(stock => stock.news.map(news => ({ ...news, stock })))
    .sort((a, b) => b.impact.percentage - a.impact.percentage);

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
            {sortedNews.map((news, index) => (
              <NewsCard
                key={index}
                source={news.source}
                time={news.time}
                title={news.title}
                description={news.impact.description}
                effect={news.impact.percentage}
                sentiment={news.impact.effect}
                stockName={news.stock.symbol}
                stockPrice={news.stock.price}
                priceChange={news.stock.change.value}
                percentChange={news.stock.change.percentage}
              />
            ))}
          </div>
        </section>
      
        <section className="mt-12">
          <h2 className="text-2xl font-semibold mb-6">Your Investments</h2>
          <div className="bg-white rounded-2xl border border-gray-200 p-4">
            {jsonData.stocks.map((stock, stockIndex) => {
              // Sort the news array for this stock by percentage effect in descending order
              const sortedNews = [...stock.news].sort((a, b) => b.impact.percentage - a.impact.percentage);

              return (
                <div key={stockIndex} className="mb-8">
                  <div className="flex justify-between items-center mb-4">
                    <div className="text-xl">
                      Stock: <span className="font-semibold">{stock.symbol}</span>
                      <span className="text-gray-600"> ({stock.symbol})</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-600">today:</span>
                      <span className="font-medium">${stock.price.toFixed(2)}</span>
                      <div
                        className={`px-3 py-2 rounded-full text-white ${
                          stock.change.value < 0 ? 'bg-red-600' : 'bg-green-600'
                        }`}
                      >
                        {stock.change.value > 0 ? '+' : ''}
                        ${stock.change.value.toFixed(2)} ({stock.change.percentage.toFixed(2)}%)
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center mb-4">
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
                    {sortedNews.map((news, newsIndex) => (
                      <div
                        key={`${stock.symbol}-${newsIndex}`}
                        className="min-w-[280px] p-3 bg-white rounded-xl border border-gray-200"
                      >
                        <div className="mb-3">
                          <div
                            className={`px-2 py-1 ${
                              news.impact.effect === 'Negative'
                                ? 'bg-red-50 text-red-600'
                                : 'bg-green-50 text-green-600'
                            } rounded-full inline-flex`}
                          >
                            <div className="text-xs font-medium">
                              {news.impact.percentage}% {news.impact.effect} Effect
                            </div>
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
              );
            })}
          </div>
        </section>


      </main>

      {showUploadModal && <UploadModal onClose={() => setShowUploadModal(false)} />}
    </div>
  );
};

export default App;
