import cv2

import os
import sys


def process_video(input_path, output_dir):

    if not os.path.isfile(input_path):
        print("\nError: Input video does not exist.")
        return

    video = cv2.VideoCapture(input_path)

    if not video.isOpened():
        print("\nError: Unable to open video.")
        return

    try:

        fps = video.get(cv2.CAP_PROP_FPS)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if fps <= 0:
            fps = 25

        os.makedirs(output_dir, exist_ok=True)

        # Directory for extracted frames
        frames_dir = os.path.join(
            output_dir,
            "frames"
        )

        os.makedirs(
            frames_dir,
            exist_ok=True
        )

        # Resize dimensions
        new_width = width // 2
        new_height = height // 2

        # Video writer
        output_video = os.path.join(
            output_dir,
            "processed_video.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        writer = cv2.VideoWriter(
            output_video,
            fourcc,
            fps,
            (new_width, new_height),
            True
        )

        if not writer.isOpened():
            print("\nError: Unable to create output video.")
            return

        frame_number = 0
        extracted_count = 0

        # Extract one frame every second
        frame_interval = max(
            int(fps),
            1
        )

        while True:

            success, frame = video.read()

            if not success:
                break

            frame_number += 1

            # Resize frame
            resized = cv2.resize(
                frame,
                (new_width, new_height)
            )

            # Convert to grayscale
            gray = cv2.cvtColor(
                resized,
                cv2.COLOR_BGR2GRAY
            )

            # Convert grayscale back to BGR
            # so it can be written into a video.
            processed_frame = cv2.cvtColor(
                gray,
                cv2.COLOR_GRAY2BGR
            )

            writer.write(processed_frame)

            # Extract one frame per second
            if frame_number % frame_interval == 0:

                frame_name = os.path.join(
                    frames_dir,
                    f"frame_{extracted_count + 1:03d}.jpg"
                )

                cv2.imwrite(
                    frame_name,
                    processed_frame
                )

                extracted_count += 1

        video.release()
        writer.release()

        print("\n" + "=" * 44)
        print("       VIDEO PROCESSING COMPLETED")
        print("=" * 44)

        print(
            f"\nFrames processed : {frame_number}"
        )

        print(
            f"Frames extracted: {extracted_count}"
        )

        print(
            f"\nProcessed video:"
        )

        print(
            f" {output_video}"
        )

        print(
            "\nExtracted frames:"
        )

        print(
            f" {frames_dir}"
        )

    except Exception as error:

        print("\nError while processing video.")
        print(f"Details: {error}")

        video.release()


def main():

    if len(sys.argv) != 2:

        print("\nUsage:")
        print(
            "python video_processing.py "
            "<video_path>"
        )

        return

    input_path = sys.argv[1]

    output_dir = os.path.join(
        os.path.dirname(
            os.path.dirname(input_path)
        ),
        "output"
    )

    process_video(
        input_path,
        output_dir
    )


if __name__ == "__main__":
    main()