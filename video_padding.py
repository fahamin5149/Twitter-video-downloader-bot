import cv2
import numpy as np
import os
from PIL import Image

def deleting_temps():
    # Delete temporary frames and video files
    if os.path.exists("frame"):
        for file in os.listdir("frame"):
            os.remove(os.path.join("frame", file))
        os.rmdir("frame")
    # Delete output_frames directory if it exists
    if os.path.exists("output_frames"):
        for file in os.listdir("output_frames"):
            os.remove(os.path.join("output_frames", file))
        os.rmdir("output_frames")
    if os.path.exists("op.avi"):
        os.remove("op.avi")

def calc_fps(ip_file):
    cap = cv2.VideoCapture(ip_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    no_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return fps, no_of_frames

def ext_frames(vid):
    cap = cv2.VideoCapture(vid)
    suc, frame = cap.read()
    frameid = 0
    os.makedirs("frame", exist_ok=True)
    while suc:
        cv2.imwrite(f"frame/{frameid}.jpg", frame)
        suc, frame = cap.read()
        frameid += 1

def create_black_background(first_frame_shape, height=1920):
    # Create a black image with width of the first frame and height of 1920
    width = first_frame_shape[1]
    black_image = np.zeros((height, width, 3), dtype=np.uint8)
    return black_image

def overlay_video_on_image(video_frames, black_bg, output_height=1920):
    os.makedirs("output_frames", exist_ok=True)
    video_height, video_width = video_frames[0].shape[:2]
    bg_height, bg_width = black_bg.shape[:2]

    # Calculate position to center the video
    x_offset = (bg_width - video_width) // 2
    y_offset = (bg_height - video_height) // 2

    for idx, frame in enumerate(video_frames):
        bg_copy = black_bg.copy()
        bg_copy[y_offset:y_offset + video_height, x_offset:x_offset + video_width] = frame
        cv2.imwrite(f"output_frames/{idx}.jpg", bg_copy)

def con2video(fps, width, height):
    frame_dir = 'output_frames'
    video_name = 'op.avi'

    images = [img for img in os.listdir(frame_dir) if img.endswith(".jpg")]
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    for image in sorted(images, key=lambda x: int(x.split('.')[0])):
        video.write(cv2.imread(os.path.join(frame_dir, image)))

    cv2.destroyAllWindows()
    video.release()

def cvn2mp4():
    # Convert op.avi to MP4 (video only)
    os.system("ffmpeg -y -i op.avi -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 out/result.mp4")

def add_audio_to_mp4(input_video, input_audio, output_video):
    # Add audio to the final MP4 using ffmpeg
    os.system(f"ffmpeg -y -i {input_video} -i {input_audio} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 -shortest {output_video}")


def padding_with_black(inp_file_name):
    """
    Pads the input video with black background and overwrites the original file.
    Args:
        inp_file_name (str): Path to the input video file (e.g., 'downloads/input.mp4')
    """
    output_folder = os.path.dirname(inp_file_name)
    if output_folder == "":
        output_folder = "."
    temp_audio_path = os.path.join(output_folder, "temp_audio.aac")
    temp_result_path = os.path.join(output_folder, "result.mp4")
    temp_final_path = os.path.join(output_folder, "final_with_audio.mp4")

    try:
        # Calculate FPS and extract frames
        fps, no_of_frames = calc_fps(inp_file_name)
        ext_frames(inp_file_name)

        # Read the first frame to determine video dimensions
        first_frame = cv2.imread("frame/0.jpg")
        black_bg = create_black_background(first_frame.shape)

        # Load all video frames
        video_frames = [cv2.imread(f"frame/{i}.jpg") for i in range(no_of_frames)]

        # Overlay video frames on the black background
        overlay_video_on_image(video_frames, black_bg)

        # Convert frames to video
        con2video(fps, black_bg.shape[1], black_bg.shape[0])

        # Convert AVI to MP4 (video only)
        os.makedirs(output_folder, exist_ok=True)
        os.system(f"ffmpeg -y -i op.avi -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 {temp_result_path}")

        # Extract audio from the original video
        os.system(f"ffmpeg -y -i {inp_file_name} -vn -acodec aac {temp_audio_path}")

        # Add audio to the final MP4
        add_audio_to_mp4(temp_result_path, temp_audio_path, temp_final_path)

        # Overwrite the original file with the padded video
        os.replace(temp_final_path, inp_file_name)

        print(f"Video with black padding saved and overwritten: {inp_file_name}")

    except Exception as e:
        print(f"Something went wrong: {e}")
        print("Check your inputs or contact support.")

    finally:
        # Clean up temporary files
        deleting_temps()
        # Optionally, remove the temporary audio and result files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(temp_result_path):
            os.remove(temp_result_path)
        if os.path.exists(temp_final_path):
            os.remove(temp_final_path)