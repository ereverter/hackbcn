import express from "express";

export const router = express.router();

router.post("/uploadVideo", upload.single("video"), async (req, res) => {
  const video = req.file;
  const response = await fetch("processVideo", {});
  const response1 = await fetch("transcriveAudio");
  const respons2 = await fetch("comperTo");
  const respons3 = await fetch("analizeEmotion");
  const respons4 = await fetch("analizeBodyLL");
  res.send();
});
