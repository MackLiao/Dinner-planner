import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FridgeItemsDashboard = () => {
  const [fridgeItems, setFridgeItems] = useState([]);

  // error to fix: axios.get('/search_user_fridge')
  useEffect(() => {
    axios.get('/search_user_fridge')
      .then(response => {
        setFridgeItems(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the fridge items:', error);
      });
  }, []); // The empty array ensures this effect runs only once after the initial render

  return (
    <div>
      <h1>Fridge Items</h1>
      {fridgeItems.length > 0 ? (
        <ul>
          {fridgeItems.map(item => (
            <li key={item.id}>{item.name} - Quantity: {item.quantity}</li>
          ))}
        </ul>
      ) : (
        <p>No items in the fridge.</p>
      )}
    </div>
  );
};

export default FridgeItemsDashboard;