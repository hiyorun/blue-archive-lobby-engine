import os
import sys
import UnityPy
import concurrent.futures

def extractTextAsset(obj, dest):
    data = obj.read()
    with open(os.path.join(dest, data.name), "wb") as f:
        f.write(bytes(data.script))
    data.save()

def extractTexture2D(obj, dest):
    data = obj.read()
    exportfile = os.path.join(dest, os.path.splitext(data.name)[0] + ".png")
    img = data.image
    img.save(exportfile)

def process_file(file_path, destination_folder):
    unity = UnityPy.load(file_path)
    character_name = file_path.split("-")[3].split(".")[0]
    print(character_name)
    dest = os.path.join(destination_folder, character_name)
    os.makedirs(dest, exist_ok=True)

    for obj in unity.objects:
        if obj.type.name in ["Texture2D", "Sprite"]:
            data = obj.read()
            print(data.name)
            extractTexture2D(obj, dest)

        if obj.type.name == "TextAsset":
            data = obj.read()
            print(data.name)
            if ".atlas" in data.name or ".skel" in data.name:
                extractTextAsset(obj, dest)

def unpack_all_assets_concurrently(source_folder: str, destination_folder: str):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(source_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                executor.submit(process_file, file_path, destination_folder)

def main():
    if len(sys.argv) != 3:
        print("Usage:\n" + sys.argv[0], "/source/folder /destination/folder")
        sys.exit()
    unpack_all_assets_concurrently(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()