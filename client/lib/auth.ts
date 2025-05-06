import axios from 'axios';
import { cookies } from 'next/headers';

export const login = async (username: string, password: string): Promise<any> => {
  try {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const response = await axios.post('http://localhost:8000/api/v1/test/login', formData);
    return response;
  } catch (error) {
    console.error("Failed to login:", error);
    throw error;
  }
}

export const getMe = (): Promise<any|null> => {
  return new Promise(async (resolve, reject) => {
    try {
      const withCredentials = true;
      const url = 'http://localhost:8000/api/v1/test/me';
      let my = await cookies();
  
      const accessToken = my.get('access_token')?.value;
  
      axios.get(url, { 
        headers: { Authorization: `Bearer ${accessToken}` }, 
        withCredentials 
      })
      .then(response => {
        resolve(response.data);
      })
      .catch(error => {
        resolve(null);
      })
      .finally(() => console.log("finally"));
  
  
    } catch (error) {
      console.error("Failed to fetch user information:", error);
      throw error;
    }
  })
};

