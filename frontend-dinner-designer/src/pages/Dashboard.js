import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

const food_list = [
];

const FridgeItemsDashboard = () => {
  const [fridgeItems, setFridgeItems] = useState([]);
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.removeItem('token'); // Remove token from sessionStorage
    navigate('/auth/login');
  }
  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = sessionStorage.getItem('token');  // Retrieve token from sessionStorage for JWT_requried endpoint

        const response = await fetch('http://127.0.0.1:5000/auth/dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.combined_item_list) {
            setFridgeItems(data.combined_item_list);
          } else {
            // Handle the case where combined_item_list is not in the response
            console.error('combined_item_list is missing in the response');
            setFridgeItems([]); // Reset or handle accordingly
          }
        } else {
          alert('Failed to fetch fridge items.');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to fetch fridge items.');
      }
    };
    fetchData();
  }, []);
  
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
      <div>
        <div>
          <Autocomplete
          disablePortal
          id="food_search"
          options={food_list}
          sx={{ width: 300 }}
          renderInput={(params) => <TextField {...params} label="Food" />}
          />
        </div>
          <Button onClick={() => handleLogout()}
          variant="contained" 
          color="primary"
          >Logout</Button>
      </div>
    </div>
  );
};

export default FridgeItemsDashboard;