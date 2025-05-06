'use client';

import { FormEvent } from "react";

const PageLogin = () => {
  
  const login = async (event: FormEvent) => {
    event.preventDefault();
    event.stopPropagation();

    let formData = new FormData();

    fetch('/api/login', {
      method: 'POST',
      body: formData,
    })
      .then(async res => {
        let data = await res.json();
        if (data) {
          // Check redirect in params url
          const url = new URL(window.location.href);
          const redirect = url.searchParams.get('redirect');
          if (redirect) {
            window.location.href = redirect;
          }
        }
      })
      .then(data => console.log(data))
  };
  const getMe = async (event: FormEvent) => {
    event.preventDefault();
    event.stopPropagation();

    fetch('/api/me', {
    })
      .then(res => res.json())
      .then(data => console.log(data))
  };


  return (
    <div className="flex bg-sky-500/100">
      <h1 className="text-red-500 ">Login Page</h1>
      <p>Chào mừng đến với trang quản trị!</p>

      <button onClick={login}>Login</button>

      <button onClick={getMe}>Get Me</button>
    </div>
  );
}

export default PageLogin;