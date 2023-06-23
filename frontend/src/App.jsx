import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SignUpPage from './components/SignUpPage';
import LoginPage from './components/LoginPage';
import UserPage from './components/UserPage';

function App () {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<SignUpPage />} />
        <Route path='/login' element={<LoginPage />} />
        <Route path='/user' element={<UserPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
