import React, { useState } from 'react';
import {Button, FormControl,  FormErrorMessage,  FormLabel, HStack, Heading, Input,  Text, VStack,Link} from '@chakra-ui/react'
import { fetchBackend } from '../fetch';
import { useNavigate } from 'react-router';
import {Link as ReactRouterLink} from 'react-router-dom'

const SignUpPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errMessage ,setErrMessage] = useState('');
  const navigate=useNavigate();

  const submit = async(e) => {
    e.preventDefault();
    const res=await fetchBackend('/sign-up','POST',{
      username:username,
      password:password
    });

    if(res.status===200){
      navigate('/login');
    }else{
      console.error(res);
      setErrMessage(res.detail)
    }
  }

  return (
    <VStack bgColor={'orange.50'} minH={'100vh'}>
      <form onSubmit={(e)=>submit(e)}>
      <VStack w={'40vw'}>
      <Heading>Sign Up</Heading>
      <FormControl isRequired>
      <FormLabel htmlFor='username'>Username</FormLabel>
      <Input id='username' variant={'filled'} value={username} onChange={(event)=>setUsername(event.target.value)}/>
      </FormControl>
      <FormControl isRequired>
      <FormLabel htmlFor='password'>Password</FormLabel>
      <Input id='password' variant={'filled'} value={password} onChange={(event)=>setPassword(event.target.value)}/>
      </FormControl>
      <Text color={'red.500'}>
        {errMessage}
      </Text>
      <Button colorScheme='blue' type='submit'>Submit</Button>
      </VStack>
    </form>
    <HStack>
    <Text>Already has account?</Text>
    <Link to='/login' color='blue.400' as={ReactRouterLink}>Login</Link>
    </HStack>
   </VStack>
    );
};

export default SignUpPage;
