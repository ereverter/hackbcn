import express from "express";
import multer from "multer";

export const router = express.Router();
const upload = multer({ dest: "./public/uploads/video" });

router.post("/uploadVideo", upload.single("video"), async (req, res) => {
  const video = req.file;

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
