import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import SignUpPage from './components/SignUpPage';
import LoginPage from './components/LoginPage';
import UserPage from './components/UserPage';
import { ChakraProvider } from '@chakra-ui/react'

function App () {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<SignUpPage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/user' element={<UserPage />} />
        </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
