# CAT-A-THON-Project
This Project is done for the CAT-A-THON 2021 Finale. <br>
What are we doing ----> Searching various models in the internet and trying them one by one and takes which ever suits us...

Reality ----> We have no idea what we are doing!!!


## Usage Instructions
1. Clone the repo
2. Install dependencies
    ```
    pip install pandas scikit-learn openpyxl fastapi uvicorn[standard] aiofiles
    ```
3. Start the server:
    ```
    uvicorn server:app --reload
    ```
    (Wait for few minutes till the server is started and you get an info "Application startup complete")
4. Browse to http://127.0.0.1:8000/public/index.html
