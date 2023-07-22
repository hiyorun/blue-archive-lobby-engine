import os
import sys
import UnityPy

def extractTextAsset(obj, dest):
    data = obj.read()
    with open( dest + "/" + data.name, "wb") as f:
        f.write(bytes(data.script))
    # edit asset
    # fp = os.path.join(replace_dir, data.name)
    # with open(fp, "rb") as f:
    #     data.script = f.read()
    data.save()

def extractTexture2D(obj,dest):
    data = obj.read()

    # create destination path

    # make sure that the extension is correct
    # you probably only want to do so with images/textures
    exportfile = dest + "/" + data.name
    exportfile, ext = os.path.splitext(exportfile)
    exportfile = exportfile + ".png"

    img = data.image
    img.save(exportfile)

def unpack_all_assets(source_folder : str, destination_folder : str):
    # iterate over all files in source folder
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            # generate file_path
            file_path = os.path.join(root, file_name)
            # load that file via UnityPy.load
            env = UnityPy.load(file_path)

            character_name = ''.join(file_name.split("spinecharacters-")[1].split("-")[0] if "spinecharacters" in file_name else file_name.split("spinelobbies-")[1].split("-")[0])

            dest = os.path.join(destination_folder + "/" + character_name)
            if not os.path.exists(dest):
                os.makedirs(dest)

            # iterate over internal objects
            for obj in env.objects:
                # process specific object types
                if obj.type.name in ["Texture2D", "Sprite"]:
                    # parse the object data
                    extractTexture2D(obj,dest)

                if obj.type.name == "TextAsset":
                    data = obj.read()
                    if ".atlas" in data.name or ".skel" in data.name:
                        print(data.name)
                        extractTextAsset(obj, dest)

def main():
    if len(sys.argv) <= 2:
        print("Usage:\n" + sys.argv[0],"/source/folder /destination/folder")
        sys.exit()
    unpack_all_assets(sys.argv[1],sys.argv[2])

main()