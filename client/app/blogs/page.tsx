import axios, { AxiosError, AxiosResponse } from "axios";

interface Blog {
  _id: string
  title: string
  image_url: string
}

const PageBlogs = async () => {

  const url = 'http://localhost:8000/api/v1/test/blogs/list';
  const result = await axios.get(url);

  const { data } = result;
  if (!data) {
    return <>Loading</>
  }

  let blogs = data as Blog[];
  
  return (
    <>
      <h1>My Blogs</h1>

      {blogs.map(item => (
        <div key={item._id}>
          <h2>{item.title}</h2>
          <img src={`http://localhost:8000/${item.image_url}?w=100`} alt="" />
        </div>
      ))}
    </>
  )
};


export default PageBlogs;