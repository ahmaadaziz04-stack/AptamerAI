import os
import shutil

# Move index.html to correct location
src = r"C:\Users\HC\AptamerAI\frontend\index.html"
dst_folder = r"C:\Users\HC\AptamerAI\backend\templates"

os.makedirs(dst_folder, exist_ok=True)
shutil.copy(src, dst_folder)
print("Done! File moved successfully!")