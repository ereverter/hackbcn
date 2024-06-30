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
  const [uploaded, setUploaded] = useState(false);
  const [text, setText] = useState({
    userText: null,
    llmText: null
  })

  useEffect(() => {
    
    if (dataExample && dataExample.grouped_transcription) {
      setDatafetch(dataExample.grouped_transcription);
    }
  }, []);


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
    fetch("/uploadVideo", {
      method: "POST",
      body: formData,
    })
    .then(async (result) =>{     
      const data = await result.json();
      console.log(data)
      if (data && data.grouped_transcription) {
        setDatafetch(data.grouped_transcription);
        setUploaded(true);
      } else {
        console.error('Invalid data structure:', data);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };
  const processEmotionSums = (groupedTranscription) => {
    const emotions = [
      "Admiration", "Anxiety", "Boredom", "Calmness",
      "Confusion", "Disappointment", "Doubt", "Excitement",
      "Interest", "Joy"
    ];
    let emotionSums = emotions.map(emotion => ({
      emotion,
      sum: 0
    }));
    
    groupedTranscription.forEach(([, , emotionData]) => {
      emotions.forEach((emotion, idx) => {
        emotionSums[idx].sum += emotionData[emotion] || 0;
      });
    });

    return emotionSums.map(({ sum }) => sum);
  };

  let dataOBJ = {};
  if (dataFetch) {
    const emotionSums = processEmotionSums(dataFetch);
    dataOBJ = {
      labels: [
        "Admiration", "Anxiety", "Boredom", "Calmness",
        "Confusion", "Disappointment", "Doubt", "Excitement",
        "Interest", "Joy"
      ],
      datasets: [
        {
          label: "Emotion Scores",
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
              src="src/img/NervousFree-removebg-preview.png"
              alt="logo"
              className="w-36"
            />
          </a>
        </div>
      </header>
      <main className="container bg-slate-200 w-full p-20 content-center">
        <div className="text-center my-8">
          <h1 className="text-8xl font-bold text-gray-900">NervousFree</h1>
          <h2 className="text-2xl font-light text-gray-600 mt-4">
            You can get all you want
          </h2>
          <section className="w-full m-10 ">
            {!uploaded && (
              <form
                // action="http://localhost:4000/api/uploadVideo"
                method="post"
                // encType="multipart/form-data"
                className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
              >
              <div className="mb-4 grid grid-cols-1 px-40 content-around">
                <h1 className="text-2xl m-5">
                  Upload your video presentation
                </h1>
                <div className="flex flex-col justify-between items-center">
                  <input
                    type="file"
                    name="video"
                    id="video"
                    onChange={handleChange}
                    className="m-5"
                  />
                  <h1 className="text-2xl mt-5">Write your pro text</h1>
                  <textarea
                    // type="textarea"
                    name="text"
                    id="text"
                    value="Lorem ipsum dolor sit amet consectetur adipisicing elit. Nisi, quam sequi! Tempora atque, delectus officia totam deserunt accusantium, vero voluptates obcaecati quibusdam consequuntur debitis quas hic eaque unde libero esse rem reprehenderit fuga aspernatur ullam illum et, porro necessitatibus? Saepe suscipit tempore, placeat ipsa error accusantium quod consequatur blanditiis eum!"
                    onChange={handleChange}
                    className="w-[500px] y-[100px] my-5"
                  />
                </div>
                <button
                  className="bg-blue-500 w-[500px] hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  onClick={handleSubmit}
                >
                  send
                </button>
                </div>
              </form>
            )}
            {uploaded && (
              <div>
                <div className="flex justify-center">
                  <article className="max-w-sm m-3.5">
                    <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <span className="text-blue-400">Your</span> video
                      transcript
                    </h5>
                    <p className="font-normal text-justify py-3 text-gray-700 dark:text-gray-400">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      At qui nemo consequatur totam provident voluptatem soluta
                      labore deleniti dolor pariatur eaque maiores dolorem,
                      asperiores natus animi perspiciatis explicabo, fugit
                      laudantium ducimus rem sequi! Ipsum excepturi atque vero
                      quia, ab officiis sint corrupti aliquam dolorem eos
                      asperiores libero sed laudantium possimus explicabo
                      delectus veniam quisquam exercitationem similique dolorum
                      tenetur qui doloremque. Eligendi quidem aperiam
                      accusantium quae harum dolores dolorum cumque deleniti
                      excepturi, nobis assumenda unde deserunt facilis. Amet
                      reprehenderit ut dignissimos perferendis natus. Iure,
                      nostrum voluptate molestias odio dolores commodi ad porro
                      placeat aliquam id quos ab a aspernatur expedita iste?
                      Reprehenderit recusandae neque officia? Expedita, dolores
                      officiis suscipit nostrum eos porro assumenda cum sunt
                      earum quaerat deserunt dicta optio consequuntur est, sint
                      adipisci accusamus similique? Quas dignissimos ad esse
                      fugit aperiam sequi maiores. Omnis dolor accusantium iure,
                      exercitationem a mollitia illo vitae, neque ducimus
                      perferendis ut! Aperiam magnam nostrum ipsa laborum.
                      Voluptas facilis harum molestias consequatur in deleniti
                      recusandae assumenda optio delectus odio unde repellat ut,
                      cum, dolorem nisi sunt odit blanditiis voluptate? Eius
                      quasi excepturi quod facere? Commodi, similique? Minima
                      reiciendis quis adipisci, vitae fugit iste officiis
                      mollitia. Optio aperiam possimus neque, rerum hic
                      reiciendis! Cumque, nulla. Cupiditate, tempore!
                    </p>
                  </article>
                  <article className="max-w-sm m-5">
                    <h5 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                      <span className="text-red-500">LLM trancript</span>
                    </h5>
                    <p className="font-normal text-justify py-3 text-gray-700 dark:text-gray-400">
                      Lorem ipsum dolor sit amet consectetur adipisicing elit.
                      Porro, ullam, iure temporibus deleniti et sit iste quas
                      soluta cum eligendi molestiae facere officia sunt
                      accusamus quia repellendus labore voluptas tenetur? Ipsa,
                      facere aut. Vitae ipsum minima placeat dolorum error
                      obcaecati unde iusto ullam officiis nemo. Sed quisquam
                      voluptatibus facilis debitis laudantium exercitationem
                      omnis consequatur esse, neque laboriosam ducimus repellat,
                      odio quo id nisi quis repellendus nobis ut? Magnam in
                      delectus atque illo ex, vero rerum dolor officia tempora
                      consequatur quisquam ducimus, ratione sequi, iste dicta
                      asperiores quidem iure praesentium ab repudiandae vitae
                      ipsa corrupti? At molestiae, mollitia nihil suscipit
                      expedita fugiat sequi quo, minus vitae vel facilis
                      voluptatibus maiores quos commodi dolores quod! Ut vel
                      doloremque error beatae minus ipsum labore consequuntur
                      alias est amet voluptas maiores officia libero, adipisci
                      eligendi! Eveniet cupiditate maiores, magnam, recusandae
                      porro molestiae quia dolorem provident eligendi adipisci
                      dicta totam. Accusamus culpa, alias excepturi labore sint
                      nostrum aperiam dicta dolorum dolore provident blanditiis!
                      Dicta ducimus odit sunt tempora velit? Exercitationem
                      eligendi voluptatibus blanditiis itaque dolore accusamus
                      obcaecati? Repellat recusandae quam rem ratione et magnam
                      corporis autem quas nobis cum magni aspernatur, corrupti
                      dolore temporibus harum, consequuntur quasi sint, quidem
                      iusto dignissimos veniam eos itaque soluta!
                    </p>
                  </article>
                </div>
                <div>
                  <Radar data={dataOBJ} />
                </div>
              </div>
            )}
          </section>
        </div>
      </main>
    </>
  );
}

export default App;
