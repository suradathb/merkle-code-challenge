import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SymbolCard from './components/SymbolCard';
import './App.css';

function App() {
  const [symbols, setSymbols] = useState([]);
  const [showOpenOnly, setShowOpenOnly] = useState(false);

  useEffect(() => {
    axios.get('https://api.blockchain.com/v3/exchange/symbols')
      .then(response => {
        const data = response.data;
        const formattedSymbols = Object.keys(data).map(key => ({
          id: key,
          ...data[key]
        }));
        setSymbols(formattedSymbols);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const toggleOpenOnly = () => {
    setShowOpenOnly(!showOpenOnly);
  };

  const sortSymbols = () => {
    const sortedSymbols = [...symbols].sort((a, b) => a.id.toString().localeCompare(b.id.toString()));
    setSymbols(sortedSymbols);
  };

  const shuffleSymbols = () => {
    const shuffledSymbols = [...symbols].sort(() => Math.random() - 0.5);
    setSymbols(shuffledSymbols);
  };

  const filteredSymbols = showOpenOnly ? symbols.filter(symbol => symbol.status === 'open') : symbols;

  return (
    <div className="App">
      <h1>Blockchain Symbols</h1>
      <div className="buttons">
        <button onClick={toggleOpenOnly}>
          {showOpenOnly ? 'Show All' : 'Show Open Only'}
        </button>
        <button onClick={sortSymbols}>Sort Alphabetically</button>
        <button onClick={shuffleSymbols}>Shuffle</button>
      </div>
      <div className="symbols-container">
        {filteredSymbols.map(symbol => (
          <SymbolCard key={symbol.id} symbol={symbol} />
        ))}
      </div>
    </div>
  );
}

export default App;
