import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import {
  Editable,
  EditableInput,
  EditablePreview,
  VStack,
  Heading,
  Text,
  Flex,
  HStack,
  Button,
  ButtonGroup,
  FormControl,
  useToast
} from '@chakra-ui/react';
import { fetchBackend } from '../fetch';
import jwt_decode from 'jwt-decode';

const UserPage = () => {
  const navigate = useNavigate();
  const [jwt] = useState(window.localStorage.getItem('jwt'));
  const [user, setUser] = useState(null);
  const [password, setPassword] = useState('');
  const [birthday, setBirthday] = useState('');
  const [errMessage, setErrMessage] = useState('')
  const [username, setUsername] = useState('');
  const toast = useToast()

  const fetchUser = async () => {
    try {
      const decoded = jwt_decode(jwt);
      const { username } = decoded;
      const res = await fetchBackend(`/user/${username}`);
      if (res.status === 200) {
        setUser(res);
        setUsername(res.username);
        setPassword(res.password);
        setBirthday(res.birthday);
      } else {
        console.error(res);
        navigate('/login');
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  useEffect(() => {
    if (!jwt) {
      navigate('/login');
    }
  }, [jwt]);

  const save = async() => {
    const res=await fetchBackend(`/user/${username}`,'PUT',{
      password:password,
      birthday:birthday
    });
    if(res.status!==200){
      console.error(res);
      setErrMessage(res.detail);
    }else{
      setErrMessage('');
      toast({
        title: 'Saved.',
        description: "We've saved your changes",
        status: 'success',
        duration: 9000,
        isClosable: true,
      })
    }
   }

  const logOut = () => {
    window.localStorage.clear();
    navigate('/login');
   }

  if (!user) {
    return <Text>Loading...</Text>;
  }

  return (
    <VStack minH='100vh' bgColor='orange.50'>
      <Heading>Your data</Heading>
      <Flex direction='column' gap={4}>
        <Text>{`username: ${user?.username}`}</Text>
        <HStack>
          <Text as='u'>password: </Text>
          <Editable value={password} onChange={(nextValue)=>setPassword(nextValue)}>
            <EditablePreview />
            <EditableInput />
          </Editable>
        </HStack>
        <HStack>
          <Text as='u'>birthday: </Text>
          <Editable value={birthday} onChange={(nextValue)=>setBirthday(nextValue)}>
            <EditablePreview />
            <EditableInput />
          </Editable>
        </HStack>

        <Text>{`created_time: ${user?.created_time}`}</Text>
        <Text>{`last_login: ${user?.last_login}`}</Text>
        <Text color={'red.500'}>{errMessage}</Text>
      </Flex>
      <ButtonGroup>
      <Button colorScheme='blue' onClick={save}>Save</Button>
      <Button colorScheme='gray' onClick={logOut}>Log out</Button>
      </ButtonGroup>
    </VStack>
  );
};

export default UserPage;
