import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [file, setFile] = useState();

  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("video", file);
    console.log(formData);
    fetch("/uploadVideo", {
      method: "POST",
      body: formData,
    }).then((result) => console.log(result));
  };

  return (
    <>
     <header class='flex border-b py-4 px-4 sm:px-10 bg-white font-[sans-serif] min-h-[70px] tracking-wide relative z-50'>
    <div class='flex flex-wrap items-center gap-5 w-full'>
      <a href="javascript:void(0)"><img src="src/img/NervousFree-removebg-preview.png" alt="logo" class='w-36' />
      </a>
  </div>
  </header>
        <main className="container">
      <div className="text-center my-8">
        <h1 className="text-4xl font-bold text-gray-900">
          NervousFree
        </h1>
        <h2 className="text-2xl font-light text-gray-600 mt-4">
          You can get all you want
        </h2>
        <section>
      <form
        // action="http://localhost:4000/api/uploadVideo"
        method="post"
        // encType="multipart/form-data"
      >
        <input type="file" name="video" id="video" onChange={handleChange} />
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          onClick={handleSubmit}
        >
          send
        </button>
      </form>
      </section>
      </div>
      </main>
    </>
  );
}

export default App;
     
      
