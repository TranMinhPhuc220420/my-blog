import axios, { AxiosError, AxiosResponse } from "axios";

interface Blog {
  title: string
  image_url: string
}

const PageBlogs = async () => {

  const url = 'http://localhost:8000/api/v1/test/blogs/6815b116edd2feb9cff179a7';
  const result = await axios.get(url);

  const { data } = result;
  if (!data) {
    return <>Loading</>
  }

  return (
    <>
      <h1>My Blogs</h1>

      {data.title}

      <img src={`http://localhost:8000/${data.image_url}?w=100`} alt="" />
    </>
  )
};


export default PageBlogs;