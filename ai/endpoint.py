import json
import os
import time

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile

from .config import ANALYSIS_INTERVAL_SECONDS, NEGATIVE_EMOTIONS, POSITIVE_EMOTIONS
from .domain import TranscriptEvaluationRequest, TranscriptEvaluationResponse
from .evaluate import create_prompt, create_system_prompt, evaluate
from .get_transcript import (
    aggregate_emotions,
    calculate_average_emotions,
    fetch_job_predictions,
    filter_emotions,
    group_transcription,
    group_transcription_by_time,
    parse_response,
)
from .process_audio import start_inference_job
from .process_video import extract_audio, extract_frames

load_dotenv()

app = FastAPI()

HUMEAI_JOBS_ENDPOINT = "https://api.hume.ai/v0/batch/jobs"


def save_file(file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        buffer.write(file.file.read())
    return destination


@app.post("/process_video")
async def process_video(
    video_file: UploadFile = File(...), text_file: UploadFile = File(...)
):
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    video_path = os.path.join(temp_dir, video_file.filename)
    audio_path = os.path.join(
        temp_dir, f"{os.path.splitext(video_file.filename)[0]}.wav"
    )
    text_path = os.path.join(temp_dir, text_file.filename)

    try:
        # # Save the video and text files
        # save_file(video_file, video_path)
        # save_file(text_file, text_path)
        # print("Saved files")

        # # Extract audio and frames from the video
        # extract_audio(video_path, audio_path)
        # print("Extracted audio")
        # extract_frames(video_path, temp_dir, ANALYSIS_INTERVAL_SECONDS)
        # print("Extracted video")

        # # Start audio processing
        # job_id = start_inference_job(audio_path)
        # print("Job id,", job_id)

        # # Wait until audio processing is over
        # while check_job_status(job_id) != "COMPLETED":
        #     time.sleep(2)
        # print("Job id completed")

        # # Fetch and process predictions
        # response_json = fetch_job_predictions(
        #     "5b189d15-23a0-477a-9b84-70821a4f2792", os.getenv("HUMEAI_APIKEY")
        # )
        # api_response = parse_response(response_json)
        # print("Job has been fetched")

        # transcription_text = group_transcription(api_response)
        # grouped_transcription = group_transcription_by_time(
        #     api_response, ANALYSIS_INTERVAL_SECONDS
        # )
        # emotions_aggregated = aggregate_emotions(grouped_transcription)

        # detailed_transcription = []
        # for interval_start, texts_emotions in grouped_transcription.items():
        #     combined_text = " ".join(text for text, _ in texts_emotions)
        #     interval_emotions = emotions_aggregated[interval_start]
        #     detailed_transcription.append(
        #         (interval_start, combined_text, interval_emotions)
        #     )

        # print("Everything is aggregated")

        # # Read the original text for evaluation
        # with open(text_path, "r") as file:
        #     original_text = file.read()

        # feedback = evaluate(grouped_transcription, original_text)

        # print("Feedback done")

        # return {
        #     "original_text": original_text,
        #     "transcription": transcription_text,
        #     "grouped_transcription": filter_emotions(detailed_transcription),
        #     "emotions_summary": calculate_average_emotions(api_response),
        #     "evaluation": feedback,
        # }

        return {
            "original_text": "### Project Presentation: Mosquito Research - Saving Lives with Pantyhose and Paperclips\n\n---\n\n#### Slide 1: Introduction\n\n- **Title**: Mosquito Research: Saving Lives with Pantyhose and Paperclips\n- **Presenter**: Emily Johnston\n- **Affiliation**: School of Pharmacy and Medical Sciences\n\n---\n\n#### Slide 2: The Global Threat of Mosquitoes\n\n- **Key Point**: The deadliest animal on the planet is not a large predator but the small mosquito.\n- **Statistics**: Mosquitoes transmit diseases like malaria and dengue fever, killing over a million people annually.\n- **Relevance to Australia**: In Australia, the Ross River Virus is the most common mosquito-borne disease.\n\n---\n\n#### Slide 3: Research Motivation\n\n- **Central Question**: Why do certain areas in Australia have higher rates of mosquito-borne diseases?\n- **Objective**: Understand environmental factors that contribute to disease transmission to prevent human infections.\n\n---\n\n#### Slide 4: Innovative Methodology\n\n- **Traditional Challenges**: Testing mosquitoes for viruses has historically been difficult.\n- **New Technique**: Utilized virus-preserving cards coated with honey to attract mosquitoes, allowing for easier detection of viruses.\n- **Field Implementation**: Adapted this technique for broad-scale use, developing new traps and setting them at over 100 field sites across South Australia.\n\n---\n\n#### Slide 5: Fieldwork and Data Collection\n\n- **Traps and Data**: \n  - Over 20,000 mosquitoes captured and tested.\n  - Identified three types of viruses: Ross River, Barmer Forest, and Stratford Virus (new to South Australia).\n- **Environmental Analysis**: Collected data on human housing density, mammal biodiversity, and green space ratios to link virus hotspots.\n\n---\n\n#### Slide 6: Results and Impact\n\n- **Findings**: \n  - The new method is the most sensitive for detecting infected mosquitoes.\n  - Uncovered environmental factors contributing to virus prevalence.\n- **Public Health Applications**: \n  - Interest from health officials in Victoria, Queensland, and Western Australia.\n  - Potential for broader implementation in surveillance programs.\n\n---\n\n#### Slide 7: Cost-Effective Innovation\n\n- **Budget Constraints**: Developed traps using recycled materials like milk cartons, pantyhose, and paperclips.\n- **Cost Efficiency**: Each trap costs less than a dollar and can be reused for an entire season.\n- **Global Relevance**: This low-budget method is particularly important for economically impoverished countries facing high mosquito-borne disease risks.\n\n---\n\n#### Slide 8: Broader Implications\n\n- **Global Health Impact**: \n  - India example: 33 million dengue cases annually, with many living on less than a dollar a day.\n  - The new method can help any country, regardless of resources, to detect and control mosquito populations.\n- **Future Directions**: Expand this method to more regions, refine environmental analyses, and collaborate with global health organizations.\n\n---\n\n#### Slide 9: Conclusion\n\n- **Summary**: \n  - Successfully developed and implemented a cost-effective, sensitive method for mosquito virus detection.\n  - Findings have the potential to transform mosquito surveillance and control worldwide.\n- **Acknowledgments**: Thank you for your attention. Questions are welcome.\n\n---\n\n#### Slide 10: Questions and Discussion\n\n- **Q&A Session**: Open the floor for questions from the audience to discuss methodologies, findings, and future research directions.",
            "transcription": "Our third finalist is Emily Johnston from the school of pharmacy and medical sciences. Her presentation title is Mosquito research, saving lives with panty hose and paper clips. I came to Australia to study the deadliest animal in the world. Now there may be some Australian audience members thinking, ruth, Science has finally recognize recognized the importance of the drop bears, but I'm not studying drop bears because around the world, by transmitting diseases like malaria and Dengue fever. Mosquitoes kill more than a million people every year, making them the deadliest animal in the plant Now in Australia, the most common mosquito borne disease is Ross River virus, and it occurs at high rates in some areas, but not others. My question is why, what is it about certain areas that make some breed disease. If we can understand the environmental factors that contribute to disease transmission then we can alter the environment or target our control efforts to prevent human infections. But to answer that question, I had to find out where the infected mosquitoes were in South Australia. And traditionally, testing mosquitoes for virus has always been difficult. So I used a new technique. It takes these cards, which are embedded with virus, preserving chemicals and coats them in honey. Mosquitoes will come to feed on the honey, and in the process spit virus onto the card where it can later be detected, Now no one had ever used this technique in a broad scale virus survey before. So I had to adapt it. I developed new traps and set them at over a hundred field sites across South Australia. And I captured over twenty thousand hungry mosquitoes and let them feed on the card for a week before testing the cards for a virus. Now, you may not think that these traps look very impressive. But science doesn't have to be beautiful. It has to be effective, and these traps are proving to be our most sensitive method of detecting infected mosquitoes. I found three types of infection. Ross river virus, bar forest virus, and stratford for virus, which has never before been found in South Australia. I now have the virus data I need to conduct my analysis, and I'm collecting publicly available data about the environment surrounding my traps. Like the density of human housing, the biodiversity of mammals and the ratio of green space to buildings to see if any of those environmental factors can link these virus hotspots spots that I've shown here. But the most exciting part of my research so far has been the success of this method. Public health officials in Victoria, Queensland and Western Australia have been in contact with us about implementing this technique for their surveillance next year. And I developed these traps in a tight budget. I used recycled milk cartons, panty holes and paper clips to make the traps. Each trap costs less than a dollar and can be reused for the whole season. That was important to me because the majority of mosquito borne disease risk happens an economically impoverished countries. In India, for example, where about a quarter of the population lives on a dollar a day, there are thirty three million cases of dengue in infection every year. With my low budget virus available and spatial analysis method. I can help any country regardless of resources, find out where their deadliest animals occur, why they're there and how we can stop them from infecting humans. Thanks.",
            "grouped_transcription": [
                [
                    0,
                    "Our third finalist is Emily Johnston from the school of pharmacy and medical sciences. Her presentation title is Mosquito research, saving lives with panty hose and paper clips. I came to Australia to study the deadliest animal in the world. Now there may be some Australian audience members thinking, ruth, Science has finally recognize recognized the importance of the drop bears, but I'm not studying drop bears because around the world, by transmitting diseases like malaria and Dengue fever. Mosquitoes kill more than a million people every year, making them the deadliest animal in the plant Now in Australia, the most common mosquito borne disease is Ross River virus, and it occurs at high rates in some areas, but not others. My question is why, what is it about certain areas that make some breed disease. If we can understand the environmental",
                    {
                        "Admiration": 0.31,
                        "Anxiety": 0.28,
                        "Boredom": 0.19,
                        "Calmness": 0.53,
                        "Confusion": 0.39,
                        "Disappointment": 0.34,
                        "Doubt": 0.22,
                        "Excitement": 0.94,
                        "Interest": 1,
                        "Joy": 0.54,
                    },
                ],
                [
                    60,
                    "factors that contribute to disease transmission then we can alter the environment or target our control efforts to prevent human infections. But to answer that question, I had to find out where the infected mosquitoes were in South Australia. And traditionally, testing mosquitoes for virus has always been difficult. So I used a new technique. It takes these cards, which are embedded with virus, preserving chemicals and coats them in honey. Mosquitoes will come to feed on the honey, and in the process spit virus onto the card where it can later be detected, Now no one had ever used this technique in a broad scale virus survey before. So I had to adapt it. I developed new traps and set them at over a hundred field sites across South Australia. And I captured over twenty thousand hungry mosquitoes and let them feed on the card for a week before testing the cards for a virus. Now, you may not think that these traps look very impressive. But science doesn't have to be beautiful. It has to be effective, and these traps are proving to be our most sensitive method of detecting infected mosquitoes. I found three types of infection. Ross river virus, bar forest virus, and",
                    {
                        "Admiration": 0.17,
                        "Anxiety": 0.25,
                        "Boredom": 0.21,
                        "Calmness": 0.61,
                        "Confusion": 0.22,
                        "Disappointment": 0.37,
                        "Doubt": 0.2,
                        "Excitement": 0.5,
                        "Interest": 0.91,
                        "Joy": 0.23,
                    },
                ],
                [
                    120,
                    "stratford for virus, which has never before been found in South Australia. I now have the virus data I need to conduct my analysis, and I'm collecting publicly available data about the environment surrounding my traps. Like the density of human housing, the biodiversity of mammals and the ratio of green space to buildings to see if any of those environmental factors can link these virus hotspots spots that I've shown here. But the most exciting part of my research so far has been the success of this method. Public health officials in Victoria, Queensland and Western Australia have been in contact with us about implementing this technique for their surveillance next year. And I developed these traps in a tight budget. I used recycled milk cartons, panty holes and paper clips to make the traps. Each trap costs less than a dollar and can be reused for the whole season. That was important to me because the majority of mosquito borne disease risk happens an economically impoverished countries. In India, for example, where about a quarter of the population lives on a dollar a day, there are thirty three million cases of dengue in infection every year. With my low budget",
                    {
                        "Admiration": 0.22,
                        "Anxiety": 0.23,
                        "Boredom": 0.2,
                        "Calmness": 0.53,
                        "Confusion": 0.21,
                        "Disappointment": 0.31,
                        "Doubt": 0.17,
                        "Excitement": 0.62,
                        "Interest": 0.96,
                        "Joy": 0.26,
                    },
                ],
                [
                    180,
                    "virus available and spatial analysis method. I can help any country regardless of resources, find out where their deadliest animals occur, why they're there and how we can stop them from infecting humans. Thanks.",
                    {
                        "Admiration": 0.17,
                        "Anxiety": 0.22,
                        "Boredom": 0.19,
                        "Calmness": 0.73,
                        "Confusion": 0.24,
                        "Disappointment": 0.3,
                        "Doubt": 0.19,
                        "Excitement": 0.3,
                        "Interest": 0.94,
                        "Joy": 0.17,
                    },
                ],
            ],
            "emotions_summary": {
                "Admiration": 0.23,
                "Anxiety": 0.26,
                "Boredom": 0.21,
                "Calmness": 0.61,
                "Confusion": 0.28,
                "Disappointment": 0.36,
                "Doubt": 0.21,
                "Excitement": 0.68,
                "Interest": 1,
                "Joy": 0.33,
            },
            "evaluation": '{\n    "errors": [\n        "At timestamp 0:00 - Forgot to mention the affiliation of Emily Johnston (School of Pharmacy and Medical Sciences).",\n        "At timestamp 0:05 - The transcript mentions \'deadliest animal in the world\', deviating from \'deadliest animal on the planet\' as stated in the ground truth.",\n        "At timestamp 0:20 - The speaker did not explicitly mention the \'Key Point\' listed in Slide 2 of the ground truth.",\n        "At timestamp 0:25 - Missed emphasizing \'Statistics\' about mosquito-borne diseases killing over a million people annually.",\n        "At timestamp 3:18 - The focus on economic implications in India deviates slightly from Slide 7 where it is supposed to relate back to low-budget traps.",\n        "Overall, the section from 0:50 to 1:10 could be more aligned with the \'Fieldwork and Data Collection\' slide focusing on the specifics."\n    ],\n    "recommendations": [\n        "Include mentioning the affiliation of the presenter at the beginning to match Slide 1\'s ground truth content.",\n        "Emphasize \'Key Point\' from Slide 2 about mosquitoes being the deadliest animal on the planet.",\n        "Incorporate specific statistics about the annual death toll due to mosquito-borne diseases to strengthen the point.",\n        "Re-align the economic implications discussion in India to tie back to the cost-effectiveness of the traps as highlighted in Slide 7.",\n        "In the section from 0:50 to 1:10, ensure that all key points from the \'Fieldwork and Data Collection\' slide are mentioned, particularly highlighting the environmental analysis and its significance."\n    ]\n}',
        }

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error decoding JSON: {e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


def check_job_status(job_id: str) -> str:
    url = f"{HUMEAI_JOBS_ENDPOINT}/{job_id}"
    headers = {"X-Hume-Api-Key": os.getenv("HUMEAI_APIKEY")}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    job_status = response.json().get("state").get("status")
    return job_status


if __name__ == "__main__":
    print("bro")
    print(check_job_status("88dcf947-7467-4ced-b29f-c84b2e96d4c8"))
