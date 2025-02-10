# **Prediction of Startup Success Based on Founders' Features**

This project aims to predict startup success by analyzing various features of startup founders, including job experience, education, connectivity, personality traits, and natural language data. Below is a detailed breakdown of the key features and methods used in this project:

Note: The Data is not uploaded on Github for ethical privacy reasons. For more detailed information feel free to have a look at the thesis PDF:https://drive.google.com/file/d/1KSs1wXHfSNwH5m1gqUWgfJZFeFjF9-lM/view?usp=sharing. This study is conducted in collaboration with **YunoAI**, a pioneering AI technology company dedicated to empowering stakeholders with actionable and timely data.

## **Features Analyzed**

### **1. Job Experience**
- **Creation of Company Success Scores**
- **Utilization of a Company Prestige Score**
- **VC (Venture Capital) Experience**
- **Consulting Experience**
- **Number of Job Experiences**

### **2. Education**
- **University Degree**
- **Utilization of a Company Prestige Score**
- **Creation of University Prestige Scores**

### **3. Connectivity on LinkedIn**
- **Number of LinkedIn Followers**

### **4. Extraction Numerical Features LinkedIn Post, Comments, Reactions**
### **5. Natural Language Processing**
Analysis of LinkedIn data (comments, posts, reactions, and profile descriptions) to create features using:
- **Unsupervised Clustering Models**
- **Sentiment Analysis Models**
- **Supervised Classification Algorithms** (with University Success as the prediction label)
### **6. Personality Prediction**
- **Publicly Available Tweets**:  
  Use tweets labeled with personality traits to train personality prediction models.
- **LinkedIn Profile Labeling**:  
  - Leverage Crunchbase to connect LinkedIn profiles with `X` profiles (formerly Twitter) shared by founders.
  - Predict personality traits of founders who share their `X` profiles on Crunchbase.
  - Use these predictions to label LinkedIn profiles with personality traits.
- **Personality Features for Startup Success Prediction**:  
  Labeled LinkedIn profiles enable personality prediction for founders, which serves as a feature in startup success prediction.
### **7. Final Model**
The final model is designed to:
- Predict startup success based on the aggregated founder features.
- Extract the **relative importance** of various founder features.
---
### **Key Features of This Repository**
- Data preprocessing and feature engineering scripts.
- Machine learning models for personality prediction and startup success prediction.
- Analysis of feature importance for founder traits contributing to startup success.

# **Data Collection Process**

The data pipeline is illustrated in the image below. This work was conducted in collaboration with the company YunoAI, which provided us with a dataset of startups. The dataset was enriched by joining and scraping additional data. 

The data scraping processes for Crunchbase, X (formerly Twitter), and LinkedIn can be found in the **0_Scraping** repository.

![image](https://github.com/user-attachments/assets/e2e6bd7f-ea92-48a1-8bad-afcd20a74d61)

# **X Personality Prediction**
Personality prediction for the Twitter data can be found in the repository **1_Labeling_Twitter_Data_With_Personality_With_Best_Model**.

# **Results**
Through this project, I identified significant potential in leveraging LinkedIn comments, posts, and reactions as predictive features for startup success. I also found that a founder’s VC experience was one of the strongest indicators of founder success and explored the power of company and university success and failure scores as features, measuring the percentage of alumni who become successful founders.

# **Feature Creation and Final Model**
Feature extraction, prediction, and the final model can be found in the **2_Predicting_Founders_Success** repository.

---

# License
This project is licensed under the **MIT License**. You are free to use, modify, and distribute this work for personal, academic, or commercial purposes, provided that proper attribution is given.

For full license details, see the LICENSE file.


