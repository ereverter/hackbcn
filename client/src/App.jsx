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
    </>
  );
}

export default App;
