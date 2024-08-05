import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Dialog from '@mui/material/Dialog';
import { DialogActions, DialogContent } from '@mui/material';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';



const FridgeItemsDashboard = () => {
  const navigate = useNavigate();

  // Use the response from backend to update the fridge items
  const [fridgeItems, setFridgeItems] = useState([]);
  // Food data for the Autocomplete component
  const [foodList, setFoodList] = useState([]);
  // Selected food item from the Autocomplete component
  const [selectedFood, setSelectedFood] = useState(null);
  // Food items returned from the search
  const [foodItems, setFoodItems] = useState(null);
  // Dialog open state
  const [dialogOpen, setDialogOpen] = useState(false);
  // Food items to add to the fridge
  const [addFood, setAddFood] = useState({
    food_id: foodItems ? foodItems[0].id : '', 
    quantity: 1,
    best_before: '',
    weight: 100,
  });
  const [token, setToken] = useState(sessionStorage.getItem('token'));

  const handleLogout = () => {
    sessionStorage.removeItem('token'); // Remove token from sessionStorage
    alert('Logout successful!'); 
    navigate('/auth/login');
  }

  const isAuthenticated = useCallback(() => {
    const auth = token !== null;
    if (!auth) {
      navigate('/auth/login');
    }
  }, [token, navigate]);

  const handleSearchFood = async () => {
    if (selectedFood) {
      try {
        const response = await fetch('http://127.0.0.1:5000/search_food', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'query': selectedFood.name,
          },});
        
        if (response.ok) {
          const data = await response.json();
          if (data.food_items && data.food_items.length > 0) {
            setFoodItems(data.food_items);
          } else {
            console.error('food_items is missing in the response');
            alert('No such food found.');
            setFoodItems(null); 
          }
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to search food.');
      }
    }
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
  }

  const handleAddFood = async () => {
    try {

      const response = await fetch('http://127.0.0.1:5000/add_food', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(addFood),
      });
      
      if (response.ok) {
        alert('Food added successfully.');
        fetchUserFridgeItems();
        setDialogOpen(false);
        setAddFood({
          food_id: foodItems ? foodItems[0].id : '', 
          quantity: 1,
          best_before: '',
          weight: 100,
        });
      } else {
        alert('Failed to add food.');
      }
    } catch (error) {
      console.error('Add Food Error:', error);
      alert('Failed to add food.');
    } 
  };

  const handleInputChange = (event) => {
    const { id, value } = event.target;
    setAddFood((prevState) => ({
      ...prevState,
      [id]: value
    }));
  };

  const fetchFoodList = useCallback(async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_food_list', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.food_list) {
          setFoodList(data.food_list);
        } else {
          // Handle the case where food_list is not in the response
          console.error('food_list is missing in the response');
          setFoodList([]); 
        }
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to fetch food list.');
    }
  }, []);

  const fetchUserFridgeItems = useCallback(async () => {
    try {
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
  }, [token]);

  useEffect(() => {
    isAuthenticated();
    fetchFoodList();
    fetchUserFridgeItems();
  }, [isAuthenticated, fetchFoodList, fetchUserFridgeItems]);
  
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
          options={foodList}
          getOptionLabel={(option) => option.name}
          sx={{ width: 500 }}
          renderInput={(params) => <TextField {...params} label="Food" />}
          onChange={(event, value) => setSelectedFood(value)}
          />
          <Button onClick={() => handleSearchFood()}
          variant="contained"
          color="primary"
          >Search</Button>
        </div>
        <div>
          <Dialog 
            open={foodItems !== null && dialogOpen} 
            onClose={handleCloseDialog}
            PaperProps={{
            component: 'form',
            onSubmit: handleAddFood,
            }}
          >
            <DialogTitle>Add Food to the Fridge</DialogTitle>
            <DialogContent>
              <DialogContentText>
                {foodItems ? foodItems[0].description : ''}
              </DialogContentText>

              <TextField
                autoFocus
                margin="dense"
                id="quantity"
                label="Quantity"
                type="number"
                fullWidth
                value={addFood.quantity}
                onChange={handleInputChange}
              />
              <TextField
                margin="dense"
                id="best_before"
                label="Best Before"
                type="date"
                fullWidth
                InputLabelProps={{
                  shrink: true,
                }}
                value={addFood.best_before}
                onChange={handleInputChange}
              />
              <TextField
                margin="dense"
                id="weight"
                label="Weight"
                type="number"
                fullWidth
                value={addFood.weight}
                onChange={handleInputChange}
              />
              
            </DialogContent>
            <DialogActions>
                <Button onClick={handleCloseDialog} color="primary">
                  Cancel
                </Button>
                <Button type="submit" color="primary">
                  Add
                </Button>
              </DialogActions>

          </Dialog>
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