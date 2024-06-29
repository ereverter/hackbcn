import express from "express";
import multer from "multer";
import fs from "node:fs";
import fetch from "node-fetch";
import FormData from "form-data";

export const router = express.Router();
// const uploadVideo = multer({ dest: "./public/uploads" });

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    // console.log(req);
    cb(null, "./public/uploads");
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const uploadVideo = multer({ storage: storage });

// router.post("/uploadVideo", async (req, res) => {
router.post("/uploadVideo", uploadVideo.single("video"), async (req, res) => {
  console.log("videoData", req.file);
  const file = req.file;
  // const video = req.files.mimetype;
  // const data = req.body.file;
  // console.log("file", video, data);
  const formData = new FormData();
  // formData.append("file", req.file.path);
  formData.append("file", fs.createReadStream(file.path), file.originalname);
  try {
    const responseVideo = await fetch("http://localhost:8000/process_video", {
      method: "POST",
      body: formData,
      // headers: formData.getHeaders(),
    });
    const dataVideo = await responseVideo.json();
    console.log(dataVideo);
    const job_id = "782b9a58-b09b-4d9b-9ead-952b7a2d85a6";
    const agg_time = "30";
    const responsePredict = await fetch(
      `http://localhost:8000/fetch_predictions/${job_id}/${agg_time}`
    );
    const dataTansf = await responsePredict.json();
    console.log(dataTansf.grouped_transcription);
    const response = dataTansf.grouped_transcription;
    res.send({ data: response });
  } catch (err) {
    console.log(err);
  }

  // const dataTansf = await response.json();

  // const respons2 = await fetch("comperTo");
  // const dataCompare = await response.json();

  // const respons3 = await fetch("analizeEmotion");
  // const dataEmotion = await response.json();

  // const respons4 = await fetch("analizeBodyLL");
  // const dataBody = await response.json();

  res.send({
    //   video: dataVideo,
    //   transcrif: dataTansf,
    //   compare: dataCompare,
    //   emotion: dataEmotion,
    //   bodyLL: dataBody,
  });
});
