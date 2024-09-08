# 🪧 About Spectia

Spectia is a Streamlit program specifically made for monitoring Linux server resources (GPU, CPU, SSD, MEM) for AI/ML developers. You don't need frontend, backend, or anything else — just a Python Virtual Environment. Monitor the usage of the server & take care of it before running the new AI/ML training process!

![spectia](https://github.com/user-attachments/assets/3f64614f-55a0-493c-8c2f-0ff3b2194876)

# ✅ How to use

First, make new Python Environment with Anaconda and install requirements:
```bash
conda create -n spectia python=3.10
conda activate spectia
pip install -r requirements.txt
```

You can run the program with:
```bash
streamlit run app.py
```

To run as backgrond process:
```bash
nohup streamlit run app.py &
```
