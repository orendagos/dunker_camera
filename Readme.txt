git remote add origin git@github.com:orendagos/od2.git
git branch -M main
git push -u origin main

raspistill -o image-small.jpg -w 640 -h 480

python3 camera.py
