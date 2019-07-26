# importing google_images_download module
from google_images_download import google_images_download

# creating object
response = google_images_download.googleimagesdownload()

search_queries = [
<<<<<<< Updated upstream
    'yosemite',
    'india traffic',
    'cereal brand logo'
=======
    'car keys'
>>>>>>> Stashed changes
]


def downloadimages(query):
    # keywords is the search query
    # format is the image file format
    # limit is the number of images to be downloaded
    # print urs is to print the image file url
    # size is the image size which can
    # be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio
    # of images to download. ("tall, square, wide, panoramic")
    arguments = {
        "keywords": query,
        "format": "jpg",
        "limit": 200,
        "print_urls": True,
        "size": "large",
        "aspect_ratio": "wide",
        "chromedriver": "/usr/local/bin/chromedriver",
        "output_directory": "/Users/adhamelarabawy/Documents/GitHub/Yolo_mark/x64/Release/data/scraped/",
        # "no_directory": True,
        "no_numbering": True
    }
    try:
        response.download(arguments)

    # Handling File NotFound Error
    except FileNotFoundError:
        print("FILE NOT FOUND ERROR")
        arguments = {
            "keywords": query,
            "format": "jpg",
            "limit": 200,
            "print_urls": True,
            "size": "large",
            "chromedriver": "/usr/local/bin/chromedriver",
            "output_directory": "/Users/adhamelarabawy/Documents/GitHub/Yolo_mark/x64/Release/data/scraped/",
            # "no_directory": True,
            "no_numbering": True
        }

        # Providing arguments for the searched query
        try:
            # Downloading the photos based
            # on the given arguments
            response.download(arguments)
        except:
            pass


# Driver Code
for query in search_queries:
    downloadimages(query)
    print()
