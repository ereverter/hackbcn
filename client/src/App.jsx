import { useState, useEffect } from "react";
import "./App.css";
import dataExample from "./exampleJsonData/response.json";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { Radar } from "react-chartjs-2";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

function App() {
  const [form, setForm] = useState({ video: "", text: "" });
  const [dataFetch, setDatafetch] = useState();
  const [evaluation, setEvaluation] = useState();
  const [uploaded, setUploaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState({
    userText: null,
    llmText: null,
  });

  const handleChange = (e) => {
    console.log(e);
    setForm({
      ...form,
      [e.target.name]:
        e.target.name == "video" ? e.target.files[0] : e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("video", form.video);
    formData.append("text", form.text);
    console.log(formData);
    setLoading(true);
    fetch("/uploadVideo", {
      method: "POST",
      body: formData,
    })
      .then(async (result) => {
        const data = await result.json();
        //setDatafetch(data.grouped_transcription[2].emotions_sumary)
        setDatafetch(data);
        const ev = JSON.parse(data.evaluation);
        console.log("erer", ev);
        setEvaluation(ev);
        console.log(data.grouped_transcription);
        // setDatafetch(data.grouped_transcription);
        setUploaded(true);
        setText({ userText: data.original_text, llmText: data.transcription });
        setDatafetch(data.emotions_summary);

        setLoading(false);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };
  const processEmotionSums = (emotions_summary) => {
    const emotions = [
      "Admiration",
      "Anxiety",
      "Boredom",
      "Calmness",
      "Confusion",
      "Disappointment",
      "Doubt",
      "Excitement",
      "Interest",
      "Joy",
    ];
    let emotionSums = emotions.map((emotion) => ({
      emotion,
      sum: emotions_summary[emotion] || 0,
    }));

    return emotionSums.map(({ sum }) => sum);
  };

  let dataOBJ = {};
  if (dataFetch) {
    const emotionSums = processEmotionSums(dataFetch);
    dataOBJ = {
      labels: [
        "Admiration",
        "Anxiety",
        "Boredom",
        "Calmness",
        "Confusion",
        "Disappointment",
        "Doubt",
        "Excitement",
        "Interest",
        "Joy",
      ],
      datasets: [
        {
          label: "Emotion Scores Stastics",
          data: emotionSums,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    };
  }

  return (
    <>
      <header className="flex border-b py-4 px-4 sm:px-10 bg-white font-[sans-serif] min-h-[70px] tracking-wide relative z-50">
        <div className="flex flex-wrap items-center gap-5 w-full">
          <a href="#">
            <img
              src="src/img/Pitch-removebg-preview.png"
              alt="logo"
              className="w-36"
            />
          </a>
        </div>
      </header>
      <main className="container bg-slate-200 w-full p-20 content-center">
        <div className="text-center my-8">
          <h1 className="text-8xl font-bold text-gray-900">Pitch AI</h1>
          <h2 className="text-2xl font-light text-gray-600 mt-4">
            Rehearse with Multimodal-based Feedback
          </h2>
          <section className="w-full m-10 ">
            {!uploaded && (
              <form
                // action="http://localhost:4000/api/uploadVideo"
                method="post"
                // encType="multipart/form-data"
                className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
              >
                {/* <div className="mb-4 grid grid-cols-1 px-40 content-around"> */}
                <h1 className="text-2xl m-5">Upload your video presentation</h1>
                <div className="flex flex-col justify-between items-center">
                  <input
                    type="file"
                    name="video"
                    id="video"
                    onChange={handleChange}
                    className="m-5"
                  />
                  <h1 className="text-2xl mt-5">Write your reference speech</h1>
                  <textarea
                    name="text"
                    id="text"
                    style={{ height: "100px" }}
                    placeholder="Write your speech "
                    onChange={handleChange}
                    className="w-[500px] y-[100px] my-5 p-2"
                    prefix="Your speech"
                  />
                </div>
                <button
                  className="bg-blue-500 w-[500px] hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  onClick={handleSubmit}
                >
                  Send
                </button>
                {/* </div> */}
              </form>
            )}
            {loading && (
              <div
                className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
                role="status"
              >
                <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
                  Loading...
                </span>
              </div>
            )}
            {uploaded && (
              <div>
                <div className="flex justify-center">
                  <article className="max-w-sm m-3.5">
                    <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <span className="text-blue-400">Reference</span> text
                    </h5>
                    <p className="font-normal text-justify py-3 text-gray-700 dark:text-gray-400">
                      {text.userText}
                    </p>
                  </article>
                  <article className="max-w-sm m-5">
                    <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <span className="text-red-500">Transcript</span>
                    </h5>
                    <p className="font-normal text-justify py-3 text-gray-700 dark:text-gray-400">
                      {text.llmText}
                    </p>
                  </article>
                </div>
                <div className="w-[600px] mx-auto">
                  <Radar data={dataOBJ} />
                </div>
              </div>
            )}
          </section>
          {evaluation != undefined && (
            <h1 className="text-5xl font-bold">Feedback</h1>
          )}
          <div className="flex justify-center text-left">
            {evaluation != undefined && (
              <div className="m-8 border p-10 rounded-md bg-red-100">
                <h1 className="text-2xl font-bold text-center mb-5">Errors</h1>
                <ul className="w-[300px]">
                  {evaluation.errors.map((item) => {
                    return <li className="list-disc">{item}</li>;
                  })}
                </ul>
              </div>
            )}
            {evaluation != undefined && (
              <div className="m-8 border p-10 rounded-md bg-green-100">
                <h1 className="text-2xl font-bold text-center mb-5">
                  Recommendations
                </h1>
                <ul className="w-[300px]">
                  {evaluation.recommendations.map((item) => {
                    return <li className="list-disc">{item}</li>;
                  })}
                </ul>
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  );
}

export default App;
