import React from 'react';
import StockDataTable from './StockDataTable';

function App() {
    return (
        <div className="App">
            <StockDataTable />
        </div>
    );
}

export default App;


{/*
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [stocks, setStocks] = useState([]);

  // API URL depending on the environment
  const API_URL = process.env.NODE_ENV === 'production' 
    ? 'https://your-production-backend.com/prices' 
    : 'http://127.0.0.1:5000/prices';

  // Fetch stock data from the Flask backend every second
  const fetchStockValues = () => {
    fetch(API_URL)
      .then(response => response.json())
      .then(data => {
        // Sort the stocks by percentage difference in descending order
        const sortedStocks = data.sort((a, b) => b.percentage_diff_5 - a.percentage_diff_5);
        setStocks(sortedStocks);
      })
      .catch(error => console.error('Error fetching stock data:', error));
  }

  useEffect(() => {
    // Fetch stock data every 400ms (roughly 4 times per second)
    const interval = setInterval(fetchStockValues, 400);

    // Clean up the interval on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1 className="title">Stock Prices Change Alert</h1>
      <table className="stock-table">
        <thead>
          <tr>
            <th className="header-cell">Stock Symbol</th>
            <th className="header-cell">CMP (₹)</th>
            <th className="header-cell">Price 5 Min Ago (₹)</th>
            <th className="header-cell">Price 10 Min Ago (₹)</th>
            <th className="header-cell">Percentage Diff 5 (%)</th>
            <th className="header-cell">Percentage Diff 10 (%)</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock, index) => (
            <tr
              key={index}
              className={`${
                stock.percentage_diff_5 > 5 ? 'highlight-row' : index % 2 === 0 ? 'even-row' : 'odd-row'
              }`}
            >
              <td>{stock.symbol.replace('.NS', '')}</td>
              <td>{stock.cmp ? stock.cmp.toFixed(2) : 'N/A'}</td>
              <td>{stock.price_5_min_ago && stock.price_5_min_ago !== 'N/A' ? stock.price_5_min_ago.toFixed(2) : 'N/A'}</td>
              <td>{stock.price_10_min_ago && stock.price_10_min_ago !== 'N/A' ? stock.price_10_min_ago.toFixed(2) : 'N/A'}</td>
              <td>{stock.percentage_diff_5 && stock.percentage_diff_5 !== 'N/A' ? stock.percentage_diff_5.toFixed(2) : 'N/A'}</td>
              <td>{stock.percentage_diff_10 && stock.percentage_diff_10 !== 'N/A' ? stock.percentage_diff_10.toFixed(2) : 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
*/
}