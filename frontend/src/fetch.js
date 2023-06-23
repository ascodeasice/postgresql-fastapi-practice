const fetchBackend = (path, method = 'GET', body = null) => {
  const jwt=window.localStorage.getItem('jwt');
  const headers = {
    'Content-Type': 'application/json',
    Authorization: jwt
  };

  return fetch(`${import.meta.env.VITE_BACKEND_HOST}${path}`, {
    headers,
    method,
    mode: 'cors',
    body: body ? JSON.stringify(body) : null
  }).then(async (res) => {
    const json = await res.json();
    json.status = res.status;
    return json;
  });
};

export { fetchBackend };
