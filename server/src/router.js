import express from "express";
import multer from "multer";

export const router = express.Router();
// const upload = multer({ dest: "./public/uploads/video" });

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, ".public/videoUpload");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

const uploadVideo = multer({ storage: storage });

// router.post("/uploadVideo", async (req, res) => {
router.post("/uploadVideo", uploadVideo.single("video"), async (req, res) => {
  console.log("hola");
  const video = req.file.mimetype;
  console.log("file", video);

  const response = await fetch("processVideo", {});
  const dataVideo = await response.json();

  const response1 = await fetch("transcriveAudio");
  const dataTansf = await response.json();

  const respons2 = await fetch("comperTo");
  const dataCompare = await response.json();

  const respons3 = await fetch("analizeEmotion");
  const dataEmotion = await response.json();

  const respons4 = await fetch("analizeBodyLL");
  const dataBody = await response.json();

  res.send({
    video: dataVideo,
    transcrif: dataTansf,
    compare: dataCompare,
    emotion: dataEmotion,
    bodyLL: dataBody,
  });
});
