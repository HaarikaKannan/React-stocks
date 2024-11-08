import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './StockDataTable.css'; // Import the CSS file

const StockDataTable = () => {
    const [stockData, setStockData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = () => {
            axios.get("http://localhost:5000/api/stocks")
                .then(response => {
                    setStockData(response.data);
                    setLoading(false);
                })
                .catch(err => {
                    setError(err);
                    setLoading(false);
                });
        };

        fetchData();
        const intervalId = setInterval(fetchData, 1000);

        return () => clearInterval(intervalId);
    }, []);

    if (loading) return <p>Loading data...</p>;
    if (error) return <p>Error loading data: {error.message}</p>;

    return (
        <div>
            <h1>Stock Data</h1>
            <table>
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Symbol</th>
                        <th>Current LTP</th>
                        <th>5 Min Ago LTP</th>
                        <th>10 Min Ago LTP</th>
                        <th>5 Min % Change</th>
                        <th>10 Min % Change</th>
                    </tr>
                </thead>
                <tbody>
                    {stockData.map((entry, index) => (
                        <tr key={index}>
                            <td>{entry.timestamp}</td>
                            <td>{entry.symbol}</td>
                            <td>{entry.current_ltp !== 'NA' ? entry.current_ltp : 'NA'}</td>
                            <td>{entry.five_min_ago_ltp !== 'NA' ? entry.five_min_ago_ltp : 'NA'}</td>
                            <td>{entry.ten_min_ago_ltp !== 'NA' ? entry.ten_min_ago_ltp : 'NA'}</td>
                            <td>{entry.five_min_change !== 'NA' ? `${entry.five_min_change}%` : 'NA'}</td>
                            <td>{entry.ten_min_change !== 'NA' ? `${entry.ten_min_change}%` : 'NA'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default StockDataTable;
