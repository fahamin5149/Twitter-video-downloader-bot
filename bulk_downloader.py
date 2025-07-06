import subprocess
import sys
from google_drive import upload_videos_to_drive


def bulk_download_twitter_videos(urls):
    """
    Calls the twitter_downloader.py script for each URL in a list.

    Args:
        urls (list): A list of Twitter video URLs to download.
    """
    if not urls:
        print("The URL list is empty. Please add URLs to the 'urls_to_download' list in the script.")
        return

    print(f"Found {len(urls)} videos to download.")

    for i, url in enumerate(urls):
        print(f"\n--- Downloading video {i+1} of {len(urls)} ---")
        print(f"URL: {url}")
        try:
            # We call the original script 'twitter_downloader.py' as a subprocess.
            # We pass the python interpreter path, the script name, and the URL.
            # This is equivalent to running 'python twitter_downloader.py <URL>' in your terminal.
            subprocess.run([sys.executable, "twitter_downloader.py", url], check=True)
            print(f"--- Finished video {i+1} ---")
        except FileNotFoundError:
            print("\nError: 'twitter_downloader.py' not found.")
            print("Please make sure this bulk downloader script is in the same directory as 'twitter_downloader.py'.")
            break # Stop the script if the downloader is not found
        except subprocess.CalledProcessError as e:
            # This error occurs if the subprocess returns a non-zero exit code (i.e., it failed).
            print(f"An error occurred while trying to download the video from {url}.")
            print(f"Error details: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # --- Instructions ---
    # 1. Save this script as 'bulk_downloader.py' in the SAME directory
    #    as your 'twitter_downloader.py' script.
    # 2. Add the Twitter video URLs you want to download into the list below.
    # 3. Run this script from your terminal: python bulk_downloader.py

    urls_to_download = [
"https://x.com/wushtini/status/1941418899377094924",
"https://x.com/lfcmarkk/status/1941436966903701973",
"https://x.com/mateo91218_/status/1941558863653933275",
"https://x.com/BarcaSpaces/status/1941498990824128641",
"https://x.com/SibiLFC/status/1941478132713930890"
    ]

    bulk_download_twitter_videos(urls_to_download)
        
    #politics
    #football
    local_path = r"C:\Users\user\Downloads\videos"
    folder_name = "politics"
    