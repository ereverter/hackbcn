import "dotenv/config";
import express, { Router } from "express";
import { router } from "./router.js";
import cors from "cors";

const PORT = process.env.PORT;
const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors());

// const storage = multer.diskStorage({
//   destination: (req, file, cb) => {
//     cb(null, ".public/videoUpload");
//   },
//   filename: (req, file, cb) => {
//     cb(null, Date.now() + "-" + file.originalname);
//   },
// });

app.use("/api", router);

app.listen(PORT, () => console.log(`Servidor in localhost:${PORT}`));
