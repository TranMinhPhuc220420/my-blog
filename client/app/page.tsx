"use client"

import { useRef, useEffect, useState, FormEvent } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";

const PageLogin = () => {
  const usernameRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  const usernameRegisterRef = useRef<HTMLInputElement>(null);
  const passwordRegisterRef = useRef<HTMLInputElement>(null);

  const [me, setMe] = useState<object|null>(null);

  const processLoginSuccess = (payload: AxiosResponse) => {
    const { data } = payload;
    if (!data) return;

    const { token_type, access_token } = data;
    console.log(token_type, access_token);

    // Save access_token to localstorage
    localStorage.setItem("access_token", access_token);

    getMe();
  };
  const processLoginError = (error: AxiosError) => {
    const { code, response } = error;
    
    if (response) {
      const { status } = response;
      console.log(status, code);
    }
  };
  const handlerSubmit = async (event: FormEvent) => {
    event.preventDefault();
    event.stopPropagation();

    const username = usernameRef.current?.value;
    const password = passwordRef.current?.value;

    const formData = new FormData();
    formData.append("username", username || "");
    formData.append("password", password || "");

    // axios.post("http://localhost:8000/api/v1/test/login", formData)
    // .then(processLoginSuccess)
    // .catch(processLoginError)
    // .finally(() => console.log("finally"));

    let withCredentials = true;

    await axios.post("http://localhost:8000/api/v1/test/login", formData, { withCredentials })
      .then(processLoginSuccess)
      .catch(processLoginError)
      .finally(() => console.log("finally"));
  };

  const handlerSubmitRegister = async (event: FormEvent) => {
    event.preventDefault();
    event.stopPropagation();

    const username = usernameRegisterRef.current?.value;
    const password = passwordRegisterRef.current?.value;

    const formData = new FormData();
    formData.append("username", username || "");
    formData.append("password", password || "");

    await axios.post("http://localhost:8000/api/v1/test/register", formData)
      .then(res => {
        console.log(res);
      })
      .catch(error => {

      })
      .finally(() => console.log("finally"));
  }

  const refreshAccessToken = async () => {
    let withCredentials = true;
    
    let url = 'http://localhost:8000/api/v1/test/refresh-token';
    
    const response = await axios.post(url, null, { withCredentials });
    localStorage.setItem("access_token", response.data.access_token);

    getMe();
  };

  const processGetMeError = (error: AxiosError) => {
    const { code, response } = error;
    
    if (response) {
      const { status, data } = response;
      
      if (status === 401) {
        refreshAccessToken();
      }
    }
  };

  const handlerLogout = () => {
    const url = 'http://localhost:8000/api/v1/test/logout';
    let accessToken = localStorage.getItem("access_token");
    let withCredentials = true;
    
    axios.post(url, null, { headers: { Authorization: `Bearer ${accessToken}` }, withCredentials })
      .then((response) => {
        localStorage.removeItem("access_token");
        console.log(response);

        // Reload page
        window.location.reload();
      })
      .catch(async (error) => {
        console.log(error);
        if (error.response.status === 401) {
          await refreshAccessToken();

          handlerLogout();
        }
      })
      .finally(() => console.log("finally"));
  };

  const getMe = async () => {
    let withCredentials = true;
    
    let url = 'http://localhost:8000/api/v1/test/me';
    let accessToken = localStorage.getItem("access_token");

    await axios.get(url, { headers: { Authorization: `Bearer ${accessToken}` }, withCredentials })
      .then((response) => {
        setMe(response.data);
      })
      .catch(processGetMeError)
      .finally(() => console.log("finally"));
  };
  useEffect(() => {
    getMe();
  }, []);

  return (
    <div className="flex h-screen w-screen flex-grow flex-col justify-center items-center">
      <h1>PageLogin</h1>

      <div className="shadow-md p-2">
        <form className="flex flex-col max-w-[300px]" action="/login" method="post" onSubmit={handlerSubmit}>
          <input type="text" className="border rounded-md border-gray-300 py-1 px-2" name="username" id="username" ref={usernameRef} />
          <input type="password" className="border rounded-md border-gray-300 py-1 px-2" name="password" id="password" ref={passwordRef} />

          <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Login</button>
        </form>
      </div>

      <hr />

      {/* Logout button */}
      <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" onClick={handlerLogout}>Logout</button>

      {me && <pre>{JSON.stringify(me, null, 2)}</pre>}

      <div className="shadow-md p-2">
        <form className="flex flex-col max-w-[300px]" action="/register" method="post" onSubmit={handlerSubmitRegister}>
          <input type="text" className="border rounded-md border-gray-300 py-1 px-2" name="username" id="username" ref={usernameRegisterRef} />
          <input type="password" className="border rounded-md border-gray-300 py-1 px-2" name="password" id="password" ref={passwordRegisterRef} />

          <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Register</button>
        </form>
      </div>

    </div>
  )
};


export default PageLogin;