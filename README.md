# dense-cap
![dense cap](https://github.com/jcjohnson/densecap/raw/master/imgs/resultsfig.png)

To clone this project use this command
```git
    git clone --recurse-submodules https://github.com/semantic-search/dense-cap.git
```

```
docker run -it --env-file .env ghcr.io/semantic-search/densecap_gpu:consumer
```

# Usage:

1. Pull the image

```
docker pull jainal09/densecap_gpu:latest
```

2.  Fork the repo - https://github.com/qassemoquab/stnbhwd

3. Head to https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/ and find your gpu `sm` version.

4. Open the `CMakeLists.txt` file in edit mode in the forked repo of `stnbhwd`.

5. Edit line no. 55

```
LIST(APPEND CUDA_NVCC_FLAGS "-arch=sm_20")
```

to your sm version.

For Example for my nvidia tesla k80 gpu sm version is `sm_37`.

```
LIST(APPEND CUDA_NVCC_FLAGS "-arch=sm_37")

```

Commit and push the code.

6. Open the file `stnbhwd-scm-1.rockspec` in edit mode in forked repo of `stnbhwd`.

7. Change the source - url to the url of the forked repository.

For example:

```json
source = {
   url = "git://github.com/qassemoquab/stnbhwd.git",
}
```

to

```json
source = {
   url = "git://github.com/jainal09/stnbhwd.git",
}
```

10. In Github click on raw button in file `stnbhwd-scm-1.rockspec` and copy the raw url

11. Run the image and access the shell by:

```
docker run --gpus all -it -p 7000:7000 jainal09/densecap_gpu:latest
```

12. run the following command:

```
luarocks install [********the raw url of stnbhwd-scm-1.rockspec of your forked repo ********]
```

## Inference and testing the build

1. Download an image

```
wget https://raw.githubusercontent.com/jcjohnson/densecap/master/imgs/elephant.jpg
```
2. Run the model on this image

```
th run_model.lua -input_image elephant.jpg
```

3. If the above step ran successful without any error than you can find caption results at `densecap/vis/data/results.json`

Also you can run:

```
cd vis
python -m SimpleHTTPServer 7000
```
And head to `localhost:7000` in browser to view the results.

# Bonus Rest Api Server

I have also added a rest api server for inference on the pre trained model!

1. Start the server
 
```
uvicorn main:app --reload --host 0.0.0.0 --port 7000
```
2. Head to `localhost:7000/docs` to upload an image and fetch its captions. (Only works on single image files)

3. Curl Command

```
curl -X POST "http://localhost:7000/uploadfile/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@img1.jpg;type=image/jpeg"
```
